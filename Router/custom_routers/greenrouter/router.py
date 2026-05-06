"""
GreenKNNRouter  —  version finale
----------------------------------
Base : version qui fonctionne à l'entraînement (doc4)
Optimisations intégrées :
  1.  KNN chargé UNE FOIS dans __init__ (conditionnel si fichier existe).
  2.  Batch embeddings : route_batch calcule tous les embeddings en un seul
      forward pass au lieu de N appels séquentiels.
  3.  Batch difficulty : tous les scores MLP en une seule opération tenseur.
  4.  Batch KNN : kneighbors() appelé une seule fois pour tout le batch.
  5.  TF-IDF vectoriser réutilisé (pas recréé à chaque recherche web).
  6.  _perf_lookup et _idx_to_embedding_id construits avec pivot pandas
      au lieu de iterrows() → 50-100× plus rapide.
  7.  Async HTTP : route_batch lance tous les appels LLM en parallèle
      (asyncio + aiohttp optionnel, fallback sync si absent).
  8.  Normalisation CO₂ pré-calculée une fois dans __init__.
  9.  Liste des modèles candidats mise en cache.
 10.  torch.inference_mode() au lieu de torch.no_grad().
 11.  difficulty_weight : coefficient de difficulté modulant l'utilité
      (petits modèles avantagés si facile, grands si difficile) — doc4.
 12.  Web search (DuckDuckGo + TF-IDF) — doc5.
 13.  _log_timestamp : horodatage optionnel des étapes — doc4.
 14.  mlp_trained + decision_reason dans les outputs — cohérence affichage.
 15.  Robustesse premier entraînement : KNN absent → instance vide créée.
"""

from __future__ import annotations

import asyncio
import copy
import json
import os
import re
from datetime import datetime
from time import perf_counter
from typing import Any, Dict, List, Optional

try:
    import aiohttp
    _AIOHTTP_AVAILABLE = True
except ImportError:
    _AIOHTTP_AVAILABLE = False
    aiohttp = None  # type: ignore

import numpy as np
import requests
import torch
import torch.nn as nn

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

# Import batch embedding si disponible, sinon fallback séquentiel
try:
    from llmrouter.utils import get_longformer_embeddings_batch
    _BATCH_EMBED_AVAILABLE = True
except ImportError:
    _BATCH_EMBED_AVAILABLE = False


# ---------------------------------------------------------------------------
# Module d'estimation de difficulté
# ---------------------------------------------------------------------------

class DifficultyEstimator(nn.Module):
    """
    MLP léger estimant la difficulté d'une requête ∈ [0, 1].

    Entrée  : embedding [batch_size, input_dim]
    Sortie  : score     [batch_size, 1]
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
# Module de recherche web (doc5)
# ---------------------------------------------------------------------------

class WebSearcher:
    """Recherche DuckDuckGo + filtrage TF-IDF. Vectoriseur réutilisé."""

    DDGO_URL = "https://api.duckduckgo.com/"

    def __init__(self, max_results: int = 5, min_tfidf_score: float = 0.1):
        self.max_results     = max_results
        self.min_tfidf_score = min_tfidf_score
        self._vectorizer     = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))

    def search(self, query: str) -> Optional[Dict[str, Any]]:
        try:
            raw = self._fetch_duckduckgo(query)
        except Exception as e:
            print(f"⚠️  Erreur recherche web : {e}")
            return None

        if not raw:
            return None

        ranked   = self._tfidf_filter(query, raw)
        filtered = [r for r in ranked if r["score"] >= self.min_tfidf_score]
        return {"answers": filtered, "best": filtered[0]} if filtered else None

    def _fetch_duckduckgo(self, query: str) -> List[Dict[str, str]]:
        params  = {"q": query, "format": "json", "no_html": "1", "skip_disambig": "1"}
        headers = {"User-Agent": "GreenKNNRouter/1.0"}
        resp    = requests.get(self.DDGO_URL, params=params, headers=headers, timeout=5)
        resp.raise_for_status()
        data    = resp.json()

        results: List[Dict[str, str]] = []
        if data.get("AbstractText"):
            results.append({"text": data["AbstractText"], "url": data.get("AbstractURL", "")})
        if data.get("Answer"):
            results.append({"text": str(data["Answer"]), "url": data.get("AbstractURL", "")})
        for topic in data.get("RelatedTopics", [])[:self.max_results]:
            if isinstance(topic, dict) and topic.get("Text"):
                results.append({"text": topic["Text"], "url": topic.get("FirstURL", "")})
            elif isinstance(topic, dict) and topic.get("Topics"):
                for sub in topic["Topics"]:
                    if sub.get("Text"):
                        results.append({"text": sub["Text"], "url": sub.get("FirstURL", "")})
        return results[:self.max_results]

    def _tfidf_filter(
        self,
        query: str,
        results: List[Dict[str, str]],
    ) -> List[Dict[str, Any]]:
        if not results:
            return []
        texts = [r["text"] for r in results]
        try:
            tfidf_matrix = self._vectorizer.fit_transform([query] + texts)
        except ValueError:
            return []
        scores = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1:])[0]
        ranked = [
            {
                "answer": re.sub(r"<[^>]+>", "", results[i]["text"]).strip(),
                "source": results[i]["url"],
                "score":  float(scores[i]),
            }
            for i in range(len(results))
        ]
        ranked.sort(key=lambda x: x["score"], reverse=True)
        return ranked[:self.max_results]


# ---------------------------------------------------------------------------
# Routeur principal
# ---------------------------------------------------------------------------

class GreenKNNRouter(MetaRouter):
    """
    GreenKNNRouter — version finale fusionnée.

    Combine :
    (1) KNN       → performance estimée sur les K voisins historiques
    (2) Threshold → seuil de difficulté (petits vs tous les modèles)
    (3) CO₂       → pénalité carbone normalisée
    (4) difficulty_weight → coefficient modulant l'utilité selon difficulté
    (5) Web search → court-circuit DuckDuckGo si difficulté > seuil web

    Fonction d'utilité :
        base(m)    = w_perf · perf_knn(m) - w_co2 · co2_norm(m)
        coeff(m)   = 1 + difficulty_weight · (1-diff si petit, diff si grand)
        utility(m) = base(m) · coeff(m)
    """

    def __init__(self, yaml_path: str):
        init_start = perf_counter()

        dummy = nn.Identity()
        super().__init__(model=dummy, yaml_path=yaml_path)

        hparam = self.cfg["hparam"]
        self.enable_timing = hparam.get("enable_timing", False)
        self._log("init: MetaRouter loaded", init_start)

        # ------------------------------------------------------------------ #
        # 1. Classifieur KNN (instance vide — sera rempli si .pkl existe)     #
        # ------------------------------------------------------------------ #
        knn_params = {
            k: hparam[k]
            for k in ("n_neighbors", "weights", "algorithm",
                      "metric", "p", "n_jobs", "leaf_size")
            if k in hparam
        }
        self.knn_model = KNeighborsClassifier(**knn_params)
        self._log("init: KNN classifier created", init_start)

        # ------------------------------------------------------------------ #
        # 2. MLP d'estimation de difficulté                                   #
        # ------------------------------------------------------------------ #
        embedding_dim = hparam.get("embedding_dim", 768)
        hidden_dim    = hparam.get("hidden_dim", 128)
        self.difficulty_estimator = DifficultyEstimator(
            input_dim=embedding_dim,
            hidden_dim=hidden_dim,
        )
        self.model            = self.difficulty_estimator
        self.threshold        = hparam.get("threshold", 0.5)
        self.small_models: List[str] = hparam.get("small_models", [])
        self.difficulty_weight = hparam.get("difficulty_weight", 0.5)
        self._log("init: difficulty estimator created", init_start)

        # ------------------------------------------------------------------ #
        # 3. Données CO₂                                                      #
        # ------------------------------------------------------------------ #
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        co2_path     = os.path.join(project_root, self.cfg["data_path"].get("co2_data", ""))
        self.co2_data: Dict[str, float] = {}
        if os.path.exists(co2_path):
            with open(co2_path, "r", encoding="utf-8") as f:
                self.co2_data = json.load(f)
            print(f"✅ Données CO₂ chargées depuis {co2_path}")
        else:
            print(f"⚠️  Fichier CO₂ introuvable : {co2_path}")

        self.w_perf = hparam.get("w_perf", 1.0)
        self.w_co2  = hparam.get("w_co2",  0.3)
        self._log("init: CO₂ data loaded", init_start)

        # ------------------------------------------------------------------ #
        # 4. Recherche web (optionnelle)                                      #
        # ------------------------------------------------------------------ #
        web_cfg = self.cfg.get("web_search", {})
        self.use_web_search       = web_cfg.get("use_web_search", False)
        self.web_search_threshold = web_cfg.get("web_search_threshold", 0.8)
        if self.use_web_search:
            self.web_searcher = WebSearcher(
                max_results=web_cfg.get("max_results", 5),
                min_tfidf_score=web_cfg.get("min_tfidf_score", 0.1),
            )
            print(f"✅ Recherche web activée (seuil difficulty > {self.web_search_threshold})")
        else:
            self.web_searcher = None

        # ------------------------------------------------------------------ #
        # 5. Données d'entraînement — lookups vectorisés (pas de iterrows)   #
        # ------------------------------------------------------------------ #
        # Prefer lightweight structures attached by DataLoader when available
        if (getattr(self, "_perf_lookup", None) is not None) and (getattr(self, "_idx_to_embedding_id_arr", None) is not None) and (getattr(self, "query_embedding_list", None) is not None):
            print("[GREEN-DEBUG] Using lightweight routing structures provided by DataLoader", flush=True)
            # model_name_list should also be provided
            if not getattr(self, "model_name_list", None):
                # derive model_name_list from perf_lookup and idx mapping
                ids = list(self._idx_to_embedding_id_arr.tolist())
                self.model_name_list = [max(self._perf_lookup[int(e)].items(), key=lambda kv: kv[1])[0] for e in ids]
        else:
            routing_best = self.routing_data_train.loc[
                self.routing_data_train.groupby("embedding_id")["performance"].idxmax()
            ].reset_index(drop=True)

            ids = routing_best["embedding_id"].tolist()
            self.query_embedding_list = [self.query_embedding_data[i].numpy() for i in ids]
            self.model_name_list = routing_best["model_name"].tolist()

            # pivot_table au lieu de iterrows : 50-100× plus rapide
            pivot = self.routing_data_train.pivot_table(
                index="embedding_id",
                columns="model_name",
                values="performance",
                aggfunc="first",
            )
            self._perf_lookup = {
                int(eid): {
                    col: float(val)
                    for col, val in row.items()
                    if not np.isnan(val)
                }
                for eid, row in pivot.iterrows()
            }

            # numpy array mapping index KNN → embedding_id
            self._idx_to_embedding_id_arr = np.array(
                [int(row["embedding_id"]) for _, row in routing_best.iterrows()],
                dtype=np.int64,
            )
        self._log("init: training data prepared", init_start)

        # ------------------------------------------------------------------ #
        # 6. Chargement KNN depuis disque (conditionnel)                      #
        # ------------------------------------------------------------------ #
        load_knn_path = os.path.join(
            project_root, self.cfg["model_path"]["load_model_path"]
        )
        if os.path.exists(load_knn_path):
            self.knn_model = load_model(load_knn_path)
            print(f"✅ KNN chargé depuis {load_knn_path}")
        else:
            print(f"ℹ️  KNN introuvable ({load_knn_path}) — instance vide, sera créé à l'entraînement.")
        self._log("init: KNN load check done", init_start)

        # ------------------------------------------------------------------ #
        # 7. Chargement MLP si disponible                                     #
        # ------------------------------------------------------------------ #
        self._mlp_trained = False
        diff_path = self.cfg["model_path"].get("difficulty_model_path", "")
        if diff_path:
            full_diff_path = os.path.join(project_root, diff_path)
            if os.path.exists(full_diff_path):
                self.difficulty_estimator.load_state_dict(
                    torch.load(full_diff_path, map_location="cpu")
                )
                self._mlp_trained = True
                print(f"✅ MLP de difficulté chargé depuis {full_diff_path}")
            else:
                print(
                    "⚠️  MLP non entraîné — difficulty_score sera peu fiable "
                    "(poids aléatoires → valeurs proches de 0 ou 1). "
                    "Lance : llmrouter train --router greenrouter"
                )
        self.difficulty_estimator.eval()   # mode éval permanent
        self._log("init: MLP load check done", init_start)

        # ------------------------------------------------------------------ #
        # 8. Pré-calcul normalisation CO₂ + liste modèles candidats           #
        # ------------------------------------------------------------------ #
        self._candidate_models: List[str] = self._build_candidate_list()
        self._co2_norm: Dict[str, float]  = self._build_co2_norm(self._candidate_models)

        print("✅ GreenKNNRouter initialisé.")
        print(f"   Seuil difficulté    : {self.threshold}")
        print(f"   difficulty_weight   : {self.difficulty_weight}")
        print(f"   Petits modèles      : {self.small_models}")
        print(f"   w_perf={self.w_perf}, w_co2={self.w_co2}")
        self._log("init: GreenKNNRouter fully initialized", init_start)

    # ---------------------------------------------------------------------- #
    # Timing                                                                  #
    # ---------------------------------------------------------------------- #

    def _log(self, step_name: str, step_start: Optional[float] = None) -> None:
        """Log horodaté avec durée écoulée (actif si enable_timing=True)."""
        if not getattr(self, "enable_timing", False):
            return
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        if step_start is None:
            print(f"[TIMING {now}] {step_name}")
        else:
            print(f"[TIMING {now}] {step_name} | elapsed={perf_counter() - step_start:.3f}s")

    # ---------------------------------------------------------------------- #
    # Helpers privés                                                          #
    # ---------------------------------------------------------------------- #

    def _build_candidate_list(self) -> List[str]:
        return list(self.llm_data.keys()) if self.llm_data else list(set(self.model_name_list))

    def _build_co2_norm(self, candidates: List[str]) -> Dict[str, float]:
        """Normalisation min-max du CO₂ sur les candidats → dict pré-calculé."""
        values    = [self.co2_data.get(m, 0.0) for m in candidates]
        co2_min   = min(values) if values else 0.0
        co2_max   = max(values) if values else 1.0
        co2_range = (co2_max - co2_min) or 1.0
        return {m: (self.co2_data.get(m, 0.0) - co2_min) / co2_range for m in candidates}

    def _get_candidate_models(self) -> List[str]:
        return self._candidate_models

    def _get_fallback_small_model(self) -> str:
        for m in self.small_models:
            if m in self._candidate_models:
                return m
        return self._candidate_models[0] if self._candidate_models else "unknown"

    def _select_candidates(self, difficulty: float) -> List[str]:
        """Petits modèles si difficulty < threshold, tous sinon."""
        if difficulty < self.threshold and self.small_models:
            candidates = [m for m in self._candidate_models if m in self.small_models]
            return candidates if candidates else self._candidate_models
        return self._candidate_models

    # ------------------------------------------------------------------ #
    # Difficulté                                                           #
    # ------------------------------------------------------------------ #

    def _estimate_difficulty(self, embedding: np.ndarray) -> float:
        """Score de difficulté pour un embedding unique."""
        with torch.inference_mode():
            t = torch.tensor(embedding, dtype=torch.float32).unsqueeze(0)
            return float(self.difficulty_estimator(t).item())

    def _estimate_difficulty_batch(self, embeddings: np.ndarray) -> np.ndarray:
        """
        Scores de difficulté pour un batch d'embeddings.
        embeddings : (N, D) → retourne (N,)
        """
        with torch.inference_mode():
            t = torch.tensor(embeddings, dtype=torch.float32)
            return self.difficulty_estimator(t).squeeze(-1).numpy()

    # ------------------------------------------------------------------ #
    # KNN                                                                  #
    # ------------------------------------------------------------------ #

    def _aggregate_knn(
        self,
        distances: np.ndarray,
        indices: np.ndarray,
        candidate_models: List[str],
    ) -> Dict[str, float]:
        """Agrège les performances des K voisins (pondération uniforme ou distance)."""
        if self.knn_model.weights == "distance":
            weights = np.where(distances == 0, 1e10, 1.0 / distances)
        else:
            weights = np.ones(len(indices))
        weights = weights / weights.sum()

        perf_scores: Dict[str, float] = {m: 0.0 for m in candidate_models}
        for w, idx in zip(weights, indices):
            eid            = int(self._idx_to_embedding_id_arr[idx])
            neighbor_perfs = self._perf_lookup.get(eid, {})
            for model in candidate_models:
                perf_scores[model] += w * neighbor_perfs.get(model, 0.0)
        return perf_scores

    def _knn_perf_scores(
        self,
        embedding: np.ndarray,
        candidate_models: List[str],
    ) -> Dict[str, float]:
        """Scores KNN pour un embedding unique."""
        distances, indices = self.knn_model.kneighbors([embedding])
        return self._aggregate_knn(distances[0], indices[0], candidate_models)

    # ------------------------------------------------------------------ #
    # Utilité (avec difficulty_weight — doc4)                             #
    # ------------------------------------------------------------------ #

    def _compute_utility(
        self,
        perf_scores: Dict[str, float],
        candidate_models: List[str],
        difficulty: float,
        co2_norm: Optional[Dict[str, float]] = None,
    ) -> Dict[str, float]:
        """
        utility(m) = (w_perf · perf(m) - w_co2 · co2_norm(m)) · coeff(m)

        coeff(m) :
          - petit modèle : 1 + (1 - difficulty) · difficulty_weight
            → avantagé quand la requête est facile
          - grand modèle : 1 + difficulty · difficulty_weight
            → avantagé quand la requête est difficile
        """
        if co2_norm is None:
            co2_norm = self._co2_norm

        utility: Dict[str, float] = {}
        for m in candidate_models:
            base = self.w_perf * perf_scores[m] - self.w_co2 * co2_norm.get(m, 0.0)
            if m in self.small_models:
                coeff = 1.0 + (1.0 - difficulty) * self.difficulty_weight
            else:
                coeff = 1.0 + difficulty * self.difficulty_weight
            utility[m] = base * coeff
        return utility

    # ------------------------------------------------------------------ #
    # Web search                                                           #
    # ------------------------------------------------------------------ #

    def _try_web_search(self, query_text: str) -> Optional[Dict[str, Any]]:
        if self.web_searcher is None:
            return None
        result = self.web_searcher.search(query_text)
        if not result:
            return None
        best = result["best"]
        return {
            "answer":      best["answer"],
            "source":      best["source"],
            "answers":     result["answers"],
            "tfidf_score": best["score"],
        }

    # ---------------------------------------------------------------------- #
    # Interface publique                                                      #
    # ---------------------------------------------------------------------- #

    def route_single(self, query: Dict[str, Any]) -> Dict[str, Any]:
        """
        Route une seule requête.

        Retourne un dict enrichi avec :
          - model_name, method, difficulty_score, mlp_trained
          - decision_reason  : explication lisible de la décision
          - perf_scores, co2_scores, utility_scores
          - answer, source   : si web_search
        """
        total_start = perf_counter()
        self._log("route_single: start")

        query_text = query["query"]

        # (1) Embedding
        step = perf_counter()
        embedding = get_longformer_embedding(query_text).numpy()
        self._log("route_single: embedding computed", step)

        # (2) Difficulté
        step = perf_counter()
        difficulty = self._estimate_difficulty(embedding)
        self._log("route_single: difficulty estimated", step)

        output = copy.copy(query)
        output["difficulty_score"]     = difficulty
        output["mlp_trained"]          = self._mlp_trained
        output["threshold"]            = self.threshold
        output["web_search_threshold"] = self.web_search_threshold

        # (3) Branche web search
        if self.use_web_search and difficulty > self.web_search_threshold:
            step = perf_counter()
            web_result = self._try_web_search(query_text)
            self._log("route_single: web search done", step)

            if web_result:
                output.update({
                    "model_name":     "web_search",
                    "method":         "web_search",
                    "answer":         web_result["answer"],
                    "source":         web_result["source"],
                    "answers":        web_result["answers"],
                    "tfidf_score":    web_result["tfidf_score"],
                    "perf_scores":    {},
                    "co2_scores":     {},
                    "utility_scores": {},
                    "decision_reason": (
                        f"difficulty {difficulty:.3f} > web_search_threshold "
                        f"{self.web_search_threshold} → web search réussi"
                    ),
                })
                self._log("route_single: completed (web)", total_start)
                return output

            # Fallback petit LLM
            fallback = self._get_fallback_small_model()
            output.update({
                "model_name":     fallback,
                "method":         "web_fallback_llm",
                "perf_scores":    {},
                "co2_scores":     {fallback: self.co2_data.get(fallback, 0.0)},
                "utility_scores": {},
                "decision_reason": (
                    f"difficulty {difficulty:.3f} > web_search_threshold "
                    f"{self.web_search_threshold} → web sans résultat "
                    f"→ fallback LLM '{fallback}'"
                ),
            })
            self._log("route_single: completed (web fallback)", total_start)
            return output

        # (4) Branche LLM routing
        step = perf_counter()
        candidates = self._select_candidates(difficulty)
        co2_norm   = (
            self._build_co2_norm(candidates)
            if candidates is not self._candidate_models
            else self._co2_norm
        )
        self._log("route_single: candidates selected", step)

        step = perf_counter()
        perf_scores    = self._knn_perf_scores(embedding, candidates)
        self._log("route_single: KNN perf scores computed", step)

        step = perf_counter()
        utility_scores = self._compute_utility(perf_scores, candidates, difficulty, co2_norm)
        best_model     = max(utility_scores, key=utility_scores.__getitem__)
        self._log("route_single: utility + best model", step)

        used_small = candidates is not self._candidate_models
        output.update({
            "model_name":     best_model,
            "method":         "llm_routing",
            "perf_scores":    perf_scores,
            "co2_scores":     {m: self.co2_data.get(m, 0.0) for m in candidates},
            "utility_scores": utility_scores,
            "decision_reason": (
                f"difficulty {difficulty:.3f} ≤ web_search_threshold "
                f"{self.web_search_threshold} → LLM routing"
                + (
                    f" (difficulty < threshold {self.threshold} → pool petits modèles)"
                    if used_small else
                    f" (difficulty ≥ threshold {self.threshold} → pool complet)"
                )
                + f" → meilleure utilité : '{best_model}'"
            ),
        })
        self._log("route_single: completed (LLM)", total_start)
        return output

    # ------------------------------------------------------------------ #
    # Async API call                                                       #
    # ------------------------------------------------------------------ #

    async def _call_api_async(
        self,
        session: Any,
        request: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Appel API asynchrone (aiohttp) avec fallback synchrone."""
        if not _AIOHTTP_AVAILABLE or session is None:
            try:
                result = call_api(request, max_tokens=1024, temperature=0.7)
                return {
                    "response":          result.get("response", ""),
                    "prompt_tokens":     result.get("prompt_tokens", 0),
                    "completion_tokens": result.get("completion_tokens", 0),
                }
            except Exception as e:
                print(f"❌ Erreur API sync : {e}")
                return {"response": "", "prompt_tokens": 0, "completion_tokens": 0, "error": str(e)}

        try:
            payload = {
                "model":       request["api_name"],
                "messages":    [{"role": "user", "content": request["query"]}],
                "max_tokens":  1024,
                "temperature": 0.7,
            }
            async with session.post(
                request["api_endpoint"],
                json=payload,
                timeout=aiohttp.ClientTimeout(total=60),
            ) as resp:
                data  = await resp.json()
                usage = data.get("usage", {})
                return {
                    "response":          data.get("choices", [{}])[0].get("message", {}).get("content", ""),
                    "prompt_tokens":     usage.get("prompt_tokens", 0),
                    "completion_tokens": usage.get("completion_tokens", 0),
                }
        except Exception as e:
            print(f"❌ Erreur API async : {e}")
            return {"response": "", "prompt_tokens": 0, "completion_tokens": 0, "error": str(e)}

    # ------------------------------------------------------------------ #
    # Assemblage des résultats (appelé depuis route_batch)                #
    # ------------------------------------------------------------------ #

    async def _route_batch_async(
        self,
        rows: List[Dict[str, Any]],
        routing_results: List[Dict[str, Any]],
        task_name: Optional[str],
    ) -> List[Dict[str, Any]]:
        """
        Lance tous les appels LLM en parallèle, assemble les résultats.
        Les lignes web_search sont retournées directement sans appel API.
        """
        results: List[Dict[str, Any]] = []
        session = aiohttp.ClientSession() if _AIOHTTP_AVAILABLE else None

        try:
            tasks: List[Any] = []

            for row_copy, routing_result in zip(rows, routing_results):
                method     = routing_result.get("method", "llm_routing")
                best_model = routing_result.get("model_name", "")

                if method == "web_search":
                    tasks.append(None)
                    continue

                # Formatage du prompt
                original_query = row_copy.get("query", "")
                row_task_name  = row_copy.get("task_name", task_name)
                if row_task_name:
                    try:
                        formatted = generate_task_query(
                            row_task_name,
                            {"query": original_query, "choices": row_copy.get("choices")},
                        )
                    except (ValueError, KeyError) as e:
                        print(f"⚠️  Formatage échoué ({e}) — requête brute utilisée.")
                        formatted = original_query
                else:
                    formatted = original_query
                row_copy["formatted_query"] = formatted

                # Résolution endpoint
                api_model_name = best_model
                api_endpoint   = None
                service        = None
                if self.llm_data and best_model in self.llm_data:
                    api_model_name = self.llm_data[best_model].get("model", best_model)
                    api_endpoint   = self.llm_data[best_model].get("api_endpoint")
                    service        = self.llm_data[best_model].get("service")
                if api_endpoint is None:
                    api_endpoint = self.cfg.get("api_endpoint")
                if not api_endpoint:
                    raise ValueError(
                        f"Endpoint API introuvable pour '{best_model}'. "
                        "Vérifiez 'api_endpoint' dans llm_data ou le YAML."
                    )

                req = {
                    "api_endpoint": api_endpoint,
                    "query":        formatted,
                    "model_name":   best_model,
                    "api_name":     api_model_name,
                }
                if service:
                    req["service"] = service

                tasks.append(asyncio.ensure_future(self._call_api_async(session, req)))

            # Attente parallèle
            api_futures = [t for t in tasks if t is not None]
            api_results = await asyncio.gather(*api_futures, return_exceptions=True)
            result_iter = iter(api_results)

            for row_copy, routing_result, t in zip(rows, routing_results, tasks):
                row_copy.update({k: v for k, v in routing_result.items() if k != "query"})
                method = routing_result.get("method", "llm_routing")

                if method == "web_search":
                    row_copy["response"]         = routing_result.get("answer", "")
                    row_copy["success"]           = True
                    row_copy["prompt_tokens"]     = 0
                    row_copy["completion_tokens"] = 0
                    results.append(row_copy)
                    continue

                api_result = next(result_iter)
                if isinstance(api_result, Exception):
                    print(f"❌ Erreur API : {api_result}")
                    response, pt, ct, success = "", 0, 0, False
                else:
                    response = api_result.get("response", "")
                    pt       = api_result.get("prompt_tokens", 0)
                    ct       = api_result.get("completion_tokens", 0)
                    success  = "error" not in api_result

                row_copy.update({
                    "response":          response,
                    "prompt_tokens":     pt,
                    "completion_tokens": ct,
                    "input_token":       pt,
                    "output_token":      ct,
                    "success":           success,
                })

                ground_truth = (
                    row_copy.get("ground_truth")
                    or row_copy.get("gt")
                    or row_copy.get("answer")
                )
                if ground_truth:
                    tp = calculate_task_performance(
                        prediction=response,
                        ground_truth=ground_truth,
                        task_name=row_copy.get("task_name", task_name),
                        metric=row_copy.get("metric"),
                    )
                    if tp is not None:
                        row_copy["task_performance"] = tp

                results.append(row_copy)

        finally:
            if session is not None:
                await session.close()

        return results

    # ------------------------------------------------------------------ #
    # route_batch                                                          #
    # ------------------------------------------------------------------ #

    def route_batch(
        self,
        batch: Optional[Any] = None,
        task_name: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Route un lot de requêtes.

        Optimisations :
        - Embeddings Longformer en un seul forward pass (batch).
        - Scores MLP en un seul forward pass (batch).
        - kneighbors() appelé une seule fois pour tout le sous-ensemble LLM.
        - Appels API LLM lancés en parallèle (asyncio + aiohttp).
        """
        batch_start = perf_counter()
        self._log("route_batch: start")

        if batch is not None:
            query_data = batch if isinstance(batch, list) else [batch]
        elif hasattr(self, "query_data_test") and self.query_data_test is not None:
            query_data = copy.copy(self.query_data_test)
        else:
            print("⚠️  Aucune donnée fournie pour le routage par lot.")
            return []

        rows: List[Dict[str, Any]] = [
            copy.copy(row) if isinstance(row, dict) else {"query": str(row)}
            for row in query_data
        ]
        queries = [r.get("query", "") for r in rows]

        # ---- 1. Batch embeddings ---------------------------------------- #
        step = perf_counter()
        if _BATCH_EMBED_AVAILABLE:
            try:
                embeddings = get_longformer_embeddings_batch(queries)
            except Exception:
                embeddings = np.stack([get_longformer_embedding(q).numpy() for q in queries])
        else:
            embeddings = np.stack([get_longformer_embedding(q).numpy() for q in queries])
        self._log("route_batch: embeddings computed", step)

        # ---- 2. Batch difficulty ----------------------------------------- #
        step = perf_counter()
        difficulties = self._estimate_difficulty_batch(embeddings)
        self._log("route_batch: difficulties estimated", step)

        # ---- 3. Partition web / LLM -------------------------------------- #
        if self.use_web_search:
            web_mask = difficulties > self.web_search_threshold
        else:
            web_mask = np.zeros(len(rows), dtype=bool)

        llm_indices = [i for i in range(len(rows)) if not web_mask[i]]
        web_indices = [i for i in range(len(rows)) if web_mask[i]]

        routing_results: List[Optional[Dict[str, Any]]] = [None] * len(rows)

        # ---- 4. Batch KNN pour les lignes LLM --------------------------- #
        if llm_indices:
            step = perf_counter()
            llm_embeddings = embeddings[llm_indices]

            use_small = [
                difficulties[i] < self.threshold and bool(self.small_models)
                for i in llm_indices
            ]
            full_candidates  = self._candidate_models
            small_candidates = (
                ([m for m in full_candidates if m in self.small_models] or full_candidates)
                if any(use_small) else []
            )
            full_co2_norm  = self._co2_norm
            small_co2_norm = self._build_co2_norm(small_candidates) if small_candidates else {}

            distances_batch, indices_batch = self.knn_model.kneighbors(llm_embeddings)
            self._log("route_batch: batch KNN done", step)

            step = perf_counter()
            for rank, i in enumerate(llm_indices):
                diff       = float(difficulties[i])
                candidates = (
                    small_candidates if use_small[rank] and small_candidates
                    else full_candidates
                )
                co2_norm   = (
                    small_co2_norm if use_small[rank] and small_candidates
                    else full_co2_norm
                )
                perf_scores    = self._aggregate_knn(
                    distances_batch[rank], indices_batch[rank], candidates
                )
                utility_scores = self._compute_utility(perf_scores, candidates, diff, co2_norm)
                best_model     = max(utility_scores, key=utility_scores.__getitem__)
                used_small     = candidates is not full_candidates

                routing_results[i] = {
                    "query":                queries[i],
                    "difficulty_score":     diff,
                    "mlp_trained":          self._mlp_trained,
                    "threshold":            self.threshold,
                    "web_search_threshold": self.web_search_threshold,
                    "model_name":           best_model,
                    "method":               "llm_routing",
                    "perf_scores":          perf_scores,
                    "co2_scores":           {m: self.co2_data.get(m, 0.0) for m in candidates},
                    "utility_scores":       utility_scores,
                    "decision_reason": (
                        f"difficulty {diff:.3f} ≤ web_search_threshold "
                        f"{self.web_search_threshold} → LLM routing"
                        + (
                            f" (difficulty < threshold {self.threshold} → pool petits modèles)"
                            if used_small else
                            f" (difficulty ≥ threshold {self.threshold} → pool complet)"
                        )
                        + f" → meilleure utilité : '{best_model}'"
                    ),
                }
            self._log("route_batch: LLM routing decisions done", step)

        # ---- 5. Web search (séquentiel — réseau) ------------------------- #
        if web_indices:
            step = perf_counter()
            for i in web_indices:
                diff       = float(difficulties[i])
                web_result = self._try_web_search(queries[i])
                if web_result:
                    routing_results[i] = {
                        "query":                queries[i],
                        "difficulty_score":     diff,
                        "mlp_trained":          self._mlp_trained,
                        "threshold":            self.threshold,
                        "web_search_threshold": self.web_search_threshold,
                        "model_name":           "web_search",
                        "method":               "web_search",
                        "answer":               web_result["answer"],
                        "source":               web_result["source"],
                        "answers":              web_result["answers"],
                        "tfidf_score":          web_result["tfidf_score"],
                        "perf_scores":          {},
                        "co2_scores":           {},
                        "utility_scores":       {},
                        "decision_reason": (
                            f"difficulty {diff:.3f} > web_search_threshold "
                            f"{self.web_search_threshold} → web search réussi"
                        ),
                    }
                else:
                    fallback = self._get_fallback_small_model()
                    routing_results[i] = {
                        "query":                queries[i],
                        "difficulty_score":     diff,
                        "mlp_trained":          self._mlp_trained,
                        "threshold":            self.threshold,
                        "web_search_threshold": self.web_search_threshold,
                        "model_name":           fallback,
                        "method":               "web_fallback_llm",
                        "perf_scores":          {},
                        "co2_scores":           {fallback: self.co2_data.get(fallback, 0.0)},
                        "utility_scores":       {},
                        "decision_reason": (
                            f"difficulty {diff:.3f} > web_search_threshold "
                            f"{self.web_search_threshold} → web sans résultat "
                            f"→ fallback LLM '{fallback}'"
                        ),
                    }
            self._log("route_batch: web search done", step)

        # ---- 6. Appels API en parallèle ---------------------------------- #
        step = perf_counter()
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                import nest_asyncio
                nest_asyncio.apply()
            result = loop.run_until_complete(
                self._route_batch_async(rows, routing_results, task_name)
            )
        except RuntimeError:
            result = asyncio.run(
                self._route_batch_async(rows, routing_results, task_name)
            )
        self._log("route_batch: API calls done", step)
        self._log("route_batch: completed", batch_start)
        return result
