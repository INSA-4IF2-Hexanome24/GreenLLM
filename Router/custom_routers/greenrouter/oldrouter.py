"""
GreenKNNRouter
--------------
Routeur hybride combinant :
  1. KNN   → trouver les K voisins les plus proches dans l'historique
  2. Threshold → estimer la difficulté de la requête
  3. Score CO₂ → pénaliser les modèles selon leur empreinte carbone
  4. Web Search → si difficulté > web_search_threshold, recherche web directe

Score d'utilité final :
    utility(m) = w_perf · perf(m) - w_co2 · co2_impact(m)

Flux :
    Query
      │
      ▼
  Embedding (Longformer)
      │
      ▼
  Estimation difficulté (MLP)
      │
      ├── difficulty > web_search_threshold ET use_web_search=true
      │         │
      │         ▼
      │   Recherche Web (DuckDuckGo)
      │         │
      │         ▼
      │   TF-IDF → filtrer les snippets les plus pertinents
      │         │
      │         ├── résultat trouvé → retourner réponse + source URL
      │         └── rien trouvé    → fallback petit LLM
      │
      └── difficulty <= web_search_threshold
                │
                ▼
          KNN + Score CO₂ → utility → meilleur LLM
"""

from typing import Any, Dict, List, Optional, Tuple
import os
import copy
import json
import re

import numpy as np
import torch
import torch.nn as nn
import requests

from sklearn.neighbors import KNeighborsClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from llmrouter.models.meta_router import MetaRouter
from llmrouter.utils import (
    load_model,
    get_longformer_embedding,
    call_api,
    generate_task_query,
    calculate_task_performance,
)


# ---------------------------------------------------------------------------
# Module d'estimation de difficulté
# ---------------------------------------------------------------------------

class DifficultyEstimator(nn.Module):
    """
    Réseau de neurones léger MLP qui estime la difficulté d'une requête.
    Entrée  : embedding de la requête  [batch_size, input_dim]
    Sortie  : score de difficulté      [batch_size, 1]  ∈ [0, 1]
    """

    def __init__(self, input_dim: int, hidden_dim: int = 128):
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(),
            nn.Linear(hidden_dim // 2, 1),
            nn.Sigmoid(),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.network(x)

# ---------------------------------------------------------------------------
# Module de recherche web
# ---------------------------------------------------------------------------

class WebSearcher:
    DDGO_URL = "https://api.duckduckgo.com/"

    def __init__(self, max_results: int = 5, min_tfidf_score: float = 0.1):
        self.max_results     = max_results
        self.min_tfidf_score = min_tfidf_score

    def search(self, query: str) -> Optional[Dict[str, Any]]:
        try:
            raw_results = self._fetch_duckduckgo(query)
        except Exception as e:
            print(f"⚠️  Erreur recherche web : {e}")
            return None

        if not raw_results:
            return None

        ranked = self._tfidf_filter(query, raw_results)

        # filtrage par seuil
        filtered = [r for r in ranked if r["score"] >= self.min_tfidf_score]

        if not filtered:
            return None

        return {
            "answers": filtered,
            "best": filtered[0],
        }

    def _fetch_duckduckgo(self, query: str) -> List[Dict[str, str]]:
        params = {
            "q":      query,
            "format": "json",
            "no_html": "1",
            "skip_disambig": "1",
        }
        headers = {"User-Agent": "GreenKNNRouter/1.0"}

        resp = requests.get(
            self.DDGO_URL,
            params=params,
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        data = resp.json()

        results = []

        if data.get("AbstractText"):
            results.append({
                "text": data["AbstractText"],
                "url":  data.get("AbstractURL", ""),
            })

        if data.get("Answer"):
            results.append({
                "text": str(data["Answer"]),
                "url":  data.get("AbstractURL", ""),
            })

        for topic in data.get("RelatedTopics", [])[:self.max_results]:
            if isinstance(topic, dict) and topic.get("Text"):
                results.append({
                    "text": topic["Text"],
                    "url":  topic.get("FirstURL", ""),
                })
            elif isinstance(topic, dict) and topic.get("Topics"):
                for sub in topic["Topics"]:
                    if sub.get("Text"):
                        results.append({
                            "text": sub["Text"],
                            "url":  sub.get("FirstURL", ""),
                        })

        return results[:self.max_results]

    # Retourne TOP-K au lieu d’un seul
    def _tfidf_filter(
        self,
        query: str,
        results: List[Dict[str, str]],
    ) -> List[Dict[str, Any]]:
        if not results:
            return []

        texts = [r["text"] for r in results]

        vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        try:
            tfidf_matrix = vectorizer.fit_transform([query] + texts)
        except ValueError:
            return []

        query_vec   = tfidf_matrix[0]
        snippet_vec = tfidf_matrix[1:]
        scores      = cosine_similarity(query_vec, snippet_vec)[0]

        ranked = []
        for i, score in enumerate(scores):
            text = re.sub(r"<[^>]+>", "", results[i]["text"]).strip()
            ranked.append({
                "answer": text,
                "source": results[i]["url"],
                "score": float(score),
            })

        ranked.sort(key=lambda x: x["score"], reverse=True)

        return ranked[:self.max_results]
# ---------------------------------------------------------------------------
# Routeur principal
# ---------------------------------------------------------------------------

class GreenKNNRouter(MetaRouter):
    """
    GreenKNNRouter
    --------------
    Combine quatre mécanismes de routage :

    (1) Web Search  : si difficulty > web_search_threshold ET use_web_search=true
                      → recherche web directe (DuckDuckGo + TF-)
                      → zéro coût LLM, zéro CO₂ de calcul
                      → fallback petit LLM si rien trouvé

    (2) KNN         : pour chaque requête, retrouve les K requêtes historiques
                      les plus similaires et calcule la performance par modèle.

    (3) Threshold   : si difficulty < threshold → petits modèles seulement
                      si difficulty >= threshold → tous les modèles

    (4) CO₂         : utility(m) = w_perf · perf(m) - w_co2 · co2(m)
    """

    def __init__(self, yaml_path: str):
        dummy = nn.Identity()
        super().__init__(model=dummy, yaml_path=yaml_path)

        hparam = self.cfg["hparam"]

        # ------------------------------------------------------------------
        # (1) Classifieur KNN
        # ------------------------------------------------------------------
        knn_params = {
            k: hparam[k]
            for k in ("n_neighbors", "weights", "algorithm",
                      "metric", "p", "n_jobs", "leaf_size")
            if k in hparam
        }
        self.knn_model = KNeighborsClassifier(**knn_params)

        # ------------------------------------------------------------------
        # (2) MLP d'estimation de difficulté
        # ------------------------------------------------------------------
        embedding_dim = hparam.get("embedding_dim", 768)
        hidden_dim    = hparam.get("hidden_dim", 128)
        self.difficulty_estimator = DifficultyEstimator(
            input_dim=embedding_dim,
            hidden_dim=hidden_dim,
        )
        self.model = self.difficulty_estimator

        self.threshold    = hparam.get("threshold", 0.5)
        self.small_models = hparam.get("small_models", [])

        # ------------------------------------------------------------------
        # (3) Données CO₂ statiques
        # ------------------------------------------------------------------
        project_root = os.path.dirname(
            os.path.dirname(os.path.dirname(__file__))
        )
        co2_path = os.path.join(
            project_root,
            self.cfg["data_path"].get("co2_data", ""),
        )
        self.co2_data: Dict[str, float] = {}
        if os.path.exists(co2_path):
            with open(co2_path, "r", encoding="utf-8") as f:
                self.co2_data = json.load(f)
            print(f"✅ Données CO₂ chargées depuis {co2_path}")
        else:
            print(f"⚠️  Fichier CO₂ introuvable : {co2_path}")

        self.w_perf = hparam.get("w_perf", 1.0)
        self.w_co2  = hparam.get("w_co2",  0.3)

        # ------------------------------------------------------------------
        # (4) Configuration de la recherche web
        # ------------------------------------------------------------------
        web_cfg = self.cfg.get("web_search", {})

        # use_web_search : active/désactive la recherche web
        self.use_web_search = web_cfg.get("use_web_search", False)

        # web_search_threshold : si difficulty > ce seuil → recherche web
        # Par défaut 0.15 : seulement les requêtes très simples
        self.web_search_threshold = web_cfg.get("web_search_threshold", 0.15)

        if self.use_web_search:
            self.web_searcher = WebSearcher(
                max_results=web_cfg.get("max_results", 5),
                min_tfidf_score=web_cfg.get("min_tfidf_score", 0.1),
            )
            print(f"✅ Recherche web activée")
            print(f"   Seuil web       : difficulty > {self.web_search_threshold}")
            print(f"   Score TF-IDF min: {web_cfg.get('min_tfidf_score', 0.1)}")
        else:
            self.web_searcher = None
            print("ℹ️  Recherche web désactivée (use_web_search: false dans YAML)")

        # ------------------------------------------------------------------
        # (5) Préparation des données d'entraînement pour le KNN
        # ------------------------------------------------------------------
        routing_best = self.routing_data_train.loc[
            self.routing_data_train.groupby("query")["performance"].idxmax()
        ].reset_index(drop=True)

        ids = routing_best["embedding_id"].tolist()
        self.query_embedding_list = [
            self.query_embedding_data[i].numpy() for i in ids
        ]
        self.model_name_list = routing_best["model_name"].tolist()

        self._perf_lookup: Dict[int, Dict[str, float]] = {}
        for _, row in self.routing_data_train.iterrows():
            eid = int(row["embedding_id"])
            if eid not in self._perf_lookup:
                self._perf_lookup[eid] = {}
            self._perf_lookup[eid][row["model_name"]] = float(row["performance"])

        self._idx_to_embedding_id = {
            i: int(row["embedding_id"])
            for i, (_, row) in enumerate(routing_best.iterrows())
        }

        # ------------------------------------------------------------------
        # (6) Chargement du MLP si déjà entraîné
        # ------------------------------------------------------------------
        diff_path = self.cfg["model_path"].get("difficulty_model_path", "")
        if diff_path:
            full_diff_path = os.path.join(project_root, diff_path)
            if os.path.exists(full_diff_path):
                self.difficulty_estimator.load_state_dict(
                    torch.load(full_diff_path, map_location="cpu")
                )
                print(f"✅ MLP de difficulté chargé depuis {full_diff_path}")
            else:
                print(f"⚠️  MLP non entraîné encore → difficulté sera ~0.5")
                print(f"   Lance d'abord : llmrouter train --router greenrouter")

        print("✅ GreenKNNRouter initialisé.")
        print(f"   Seuil de difficulté : {self.threshold}")
        print(f"   Petits modèles      : {self.small_models}")
        print(f"   w_perf={self.w_perf}, w_co2={self.w_co2}")

    # ------------------------------------------------------------------
    # Méthodes internes
    # ------------------------------------------------------------------

    def _get_candidate_models(self) -> List[str]:
        return list(self.llm_data.keys()) if self.llm_data else self.model_name_list

    def _get_fallback_small_model(self) -> str:
        """
        Retourne le premier petit modèle disponible pour le fallback web.
        Si small_models est vide, retourne le premier modèle candidat.
        """
        all_models = self._get_candidate_models()
        for m in self.small_models:
            if m in all_models:
                return m
        return all_models[0] if all_models else "unknown"

    def _estimate_difficulty(self, embedding: np.ndarray) -> float:
        self.difficulty_estimator.eval()
        with torch.no_grad():
            t = torch.tensor(embedding, dtype=torch.float32).unsqueeze(0)
            score = self.difficulty_estimator(t)
        return float(score.item())

    def _knn_perf_scores(
        self,
        embedding: np.ndarray,
        candidate_models: List[str],
    ) -> Dict[str, float]:
        distances, indices = self.knn_model.kneighbors(
            [embedding], n_neighbors=self.knn_model.n_neighbors
        )
        neighbor_indices   = indices[0]
        neighbor_distances = distances[0]

        if self.knn_model.weights == "distance":
            weights = np.where(
                neighbor_distances == 0,
                1e10,
                1.0 / neighbor_distances,
            )
        else:
            weights = np.ones(len(neighbor_indices))
        weights = weights / weights.sum()

        perf_scores: Dict[str, float] = {m: 0.0 for m in candidate_models}
        for w, idx in zip(weights, neighbor_indices):
            embedding_id = self._get_embedding_id_from_index(idx)
            if embedding_id is None:
                continue
            neighbor_perfs = self._perf_lookup.get(embedding_id, {})
            for model in candidate_models:
                perf_scores[model] += w * neighbor_perfs.get(model, 0.0)

        return perf_scores

    def _get_embedding_id_from_index(self, idx: int) -> Optional[int]:
        if hasattr(self, "_idx_to_embedding_id"):
            return self._idx_to_embedding_id.get(idx)
        return None

    def _compute_utility(
        self,
        perf_scores: Dict[str, float],
        candidate_models: List[str],
    ) -> Dict[str, float]:
        co2_raw = {m: self.co2_data.get(m, 0.0) for m in candidate_models}
        co2_values = list(co2_raw.values())
        co2_min   = min(co2_values) if co2_values else 0.0
        co2_max   = max(co2_values) if co2_values else 1.0
        co2_range = co2_max - co2_min if co2_max != co2_min else 1.0

        utility: Dict[str, float] = {}
        for m in candidate_models:
            co2_norm  = (co2_raw[m] - co2_min) / co2_range
            utility[m] = self.w_perf * perf_scores[m] - self.w_co2 * co2_norm
        return utility

    def _try_web_search(self, query_text: str) -> Optional[Dict[str, Any]]:
        if self.web_searcher is None:
            return None

        print(f"🌐 Recherche web pour : '{query_text[:60]}...'")
        result = self.web_searcher.search(query_text)

        if result:
            best = result["best"]

            print(f"   ✅ {len(result['answers'])} résultats trouvés")
            print(f"   📎 Best source : {best['source']}")

            return {
                "answer": best["answer"],
                "source": best["source"],
                "answers": result["answers"], 
                "tfidf_score": best["score"],
                "method": "web_search",
            }

        print("   ⚠️  Aucun résultat pertinent → fallback LLM")
        return None

    # ------------------------------------------------------------------
    # Interface publique
    # ------------------------------------------------------------------

    def route_single(self, query: Dict[str, Any]) -> Dict[str, Any]:
        """
        Route une seule requête.

        Flux de décision :
          1. Embedding + estimation de difficulté
          2. Si difficulty > web_search_threshold ET use_web_search=true
               → recherche web
               → si résultat : retourne directement (pas de LLM)
               → si pas de résultat : fallback petit LLM
          3. Sinon : KNN + CO₂ → meilleur LLM

        Returns:
            dict avec :
              - model_name       : LLM sélectionné (ou "web_search")
              - difficulty_score : score MLP [0,1]
              - method           : "web_search" | "llm_routing"
              - answer           : réponse web (si web_search)
              - source           : URL source (si web_search)
              - perf_scores      : scores KNN par modèle
              - co2_scores       : empreinte CO₂ par modèle
              - utility_scores   : scores d'utilité par modèle
        """
        # Chargement du KNN entraîné
        project_root = os.path.dirname(
            os.path.dirname(os.path.dirname(__file__))
        )
        load_knn_path = os.path.join(
            project_root, self.cfg["model_path"]["load_model_path"]
        )
        self.knn_model = load_model(load_knn_path)

        query_text = query["query"]

        # (1) Embedding + difficulté
        embedding  = get_longformer_embedding(query_text).numpy()
        difficulty = self._estimate_difficulty(embedding)

        output = copy.copy(query)
        output["difficulty_score"] = difficulty
        output["threshold"]        = self.threshold
        output["web_search_threshold"] = self.web_search_threshold

        # (2) Court-circuit web si requête très simple
        if self.use_web_search and difficulty > self.web_search_threshold:
            print(f"💡 Difficulté {difficulty:.3f} > seuil web {self.web_search_threshold}"
                  f" → tentative recherche web")

            web_result = self._try_web_search(query_text)

            if web_result:
                output["model_name"]  = "web_search"
                output["method"]      = "web_search"
                output["answer"]      = web_result["answer"]
                output["source"]      = web_result["source"]
                output["answers"]     = web_result.get("answers", [])  
                output["tfidf_score"] = web_result["tfidf_score"]
                output["perf_scores"] = {}
                output["co2_scores"]  = {}
                output["utility_scores"] = {}
                return output
            else:
                # Fallback : forcer un petit LLM
                fallback = self._get_fallback_small_model()
                print(f"   → Fallback LLM : {fallback}")
                output["model_name"] = fallback
                output["method"]     = "web_fallback_llm"
                output["perf_scores"]    = {}
                output["co2_scores"]     = {fallback: self.co2_data.get(fallback, 0.0)}
                output["utility_scores"] = {}
                return output

        # (3) Routing LLM normal (KNN + CO₂)
        all_models = self._get_candidate_models()
        if difficulty < self.threshold and self.small_models:
            candidates = [m for m in all_models if m in self.small_models]
            if not candidates:
                candidates = all_models
        else:
            candidates = all_models

        perf_scores    = self._knn_perf_scores(embedding, candidates)
        utility_scores = self._compute_utility(perf_scores, candidates)
        best_model     = max(utility_scores, key=utility_scores.__getitem__)

        output["model_name"]     = best_model
        output["method"]         = "llm_routing"
        output["perf_scores"]    = perf_scores
        output["co2_scores"]     = {m: self.co2_data.get(m, 0.0) for m in candidates}
        output["utility_scores"] = utility_scores
        return output

    def route_batch(
        self,
        batch: Optional[Any] = None,
        task_name: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Route un lot de requêtes avec la même logique que route_single,
        puis appelle les APIs pour les requêtes routées vers un LLM.
        Les requêtes résolues par recherche web ne font pas d'appel API.
        """
        project_root = os.path.dirname(
            os.path.dirname(os.path.dirname(__file__))
        )
        load_knn_path = os.path.join(
            project_root, self.cfg["model_path"]["load_model_path"]
        )
        self.knn_model = load_model(load_knn_path)

        if batch is not None:
            query_data = batch if isinstance(batch, list) else [batch]
        elif hasattr(self, "query_data_test") and self.query_data_test is not None:
            query_data = copy.copy(self.query_data_test)
        else:
            print("⚠️  Aucune donnée fournie pour le routage par lot.")
            return []

        results = []
        for row in query_data:
            if isinstance(row, dict):
                row_copy       = copy.copy(row)
                original_query = row_copy.get("query", "")
                row_task_name  = row_copy.get("task_name", task_name)
            else:
                row_copy       = {"query": str(row)}
                original_query = str(row)
                row_task_name  = task_name

            # Routing (inclut la logique web)
            routing_result = self.route_single({"query": original_query})
            row_copy.update({
                k: v for k, v in routing_result.items()
                if k != "query"
            })

            method     = routing_result.get("method", "llm_routing")
            best_model = routing_result.get("model_name", "")

            # Si réponse web directe → pas d'appel API
            if method == "web_search":
                row_copy["response"] = routing_result.get("answer", "")
                row_copy["success"]  = True
                row_copy["prompt_tokens"]     = 0
                row_copy["completion_tokens"] = 0
                results.append(row_copy)
                continue

            # Formatage du prompt pour les LLMs
            if row_task_name:
                try:
                    formatted = generate_task_query(
                        row_task_name,
                        {"query": original_query, "choices": row_copy.get("choices")},
                    )
                    row_copy["formatted_query"]  = formatted
                    query_text_for_execution     = formatted
                except (ValueError, KeyError) as e:
                    print(f"⚠️  Formatage échoué ({e}). Requête originale utilisée.")
                    query_text_for_execution = original_query
            else:
                query_text_for_execution = original_query

            # Appel API LLM
            api_model_name = best_model
            api_endpoint   = None
            service        = None

            if self.llm_data and best_model in self.llm_data:
                api_model_name = self.llm_data[best_model].get("model", best_model)
                api_endpoint   = self.llm_data[best_model].get(
                    "api_endpoint", self.cfg.get("api_endpoint")
                )
                service = self.llm_data[best_model].get("service")

            if api_endpoint is None:
                api_endpoint = self.cfg.get("api_endpoint")

            if not api_endpoint:
                raise ValueError(
                    f"Endpoint API introuvable pour '{best_model}'. "
                    "Vérifiez 'api_endpoint' dans llm_data ou dans le YAML."
                )

            request = {
                "api_endpoint": api_endpoint,
                "query":        query_text_for_execution,
                "model_name":   best_model,
                "api_name":     api_model_name,
            }
            if service:
                request["service"] = service

            try:
                result            = call_api(request, max_tokens=1024, temperature=0.7)
                response          = result.get("response", "")
                prompt_tokens     = result.get("prompt_tokens", 0)
                completion_tokens = result.get("completion_tokens", 0)
                success           = "error" not in result
            except Exception as e:
                print(f"❌ Erreur API : {e}")
                response, prompt_tokens, completion_tokens, success = "", 0, 0, False

            row_copy["response"]          = response
            row_copy["prompt_tokens"]     = prompt_tokens
            row_copy["completion_tokens"] = completion_tokens
            row_copy["input_token"]       = prompt_tokens
            row_copy["output_token"]      = completion_tokens
            row_copy["success"]           = success

            ground_truth = (
                row_copy.get("ground_truth")
                or row_copy.get("gt")
                or row_copy.get("answer")
            )
            if ground_truth:
                tp = calculate_task_performance(
                    prediction=response,
                    ground_truth=ground_truth,
                    task_name=row_task_name,
                    metric=row_copy.get("metric"),
                )
                if tp is not None:
                    row_copy["task_performance"] = tp

            results.append(row_copy)

        return results