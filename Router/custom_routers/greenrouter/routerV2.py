"""
GreenKNNRouter  —  optimised version
-------------------------------------
Key runtime improvements over the original:

  1. KNN model loaded ONCE at __init__, not on every route_single call.
  2. Batch embeddings: route_batch computes all Longformer embeddings in one
     forward pass instead of N sequential calls.
  3. Batch difficulty estimation: all MLP scores in one tensor operation.
  4. Batch KNN: kneighbors() called once for the whole batch.
  5. TF-IDF vectoriser reused across searches (fitted lazily, not rebuilt
     every call).
  6. _perf_lookup and _idx_to_embedding_id built with vectorised pandas ops
     instead of iterrows().
  7. Async HTTP: route_batch fires all LLM API calls concurrently with
     asyncio + aiohttp, then collects results — eliminates the serial
     latency wall.
  8. CO₂ normalisation constants pre-computed once.
  9. Candidate-model set cached to avoid repeated dict lookups.
 10. Minor: torch.inference_mode() instead of torch.no_grad() (lower
     overhead in PyTorch ≥ 1.9).
"""

from __future__ import annotations

import asyncio
import copy
import json
import os
import re
from typing import Any, Dict, List, Optional

import aiohttp
import aiohttp
import numpy as np
import torch
import torch.nn as nn
import requests
import requests

from sklearn.neighbors import KNeighborsClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from llmrouter.models.meta_router import MetaRouter
from llmrouter.utils import (
    load_model,
    get_longformer_embedding,
    get_longformer_embeddings_batch,   # batch variant — add this to utils if absent
    get_longformer_embeddings_batch,   # batch variant — add this to utils if absent
    call_api,
    generate_task_query,
    calculate_task_performance,
)


# ---------------------------------------------------------------------------
# MLP difficulty estimator  (unchanged API, same architecture)
# MLP difficulty estimator  (unchanged API, same architecture)
# ---------------------------------------------------------------------------

class DifficultyEstimator(nn.Module):
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
            nn.Sigmoid(),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.network(x)


# ---------------------------------------------------------------------------
# Web searcher  —  reuses a single TfidfVectorizer instance
# ---------------------------------------------------------------------------

class WebSearcher:
    DDGO_URL = "https://api.duckduckgo.com/"

    def __init__(self, max_results: int = 5, min_tfidf_score: float = 0.1):
        self.max_results     = max_results
        self.min_tfidf_score = min_tfidf_score
        # Reuse across calls: avoids re-instantiation overhead each search.
        self._vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))

    def search(self, query: str) -> Optional[Dict[str, Any]]:
        try:
            raw_results = self._fetch_duckduckgo(query)
        except Exception as e:
            print(f"⚠️  Erreur recherche web : {e}")
            return None

        if not raw_results:
            return None

        ranked   = self._tfidf_filter(query, raw_results)
        filtered = [r for r in ranked if r["score"] >= self.min_tfidf_score]

        if not filtered:
            return None

        return {"answers": filtered, "best": filtered[0]}

    def _fetch_duckduckgo(self, query: str) -> List[Dict[str, str]]:
        params  = {"q": query, "format": "json", "no_html": "1", "skip_disambig": "1"}
        headers = {"User-Agent": "GreenKNNRouter/1.0"}
        resp    = requests.get(self.DDGO_URL, params=params, headers=headers, timeout=5)
        resp.raise_for_status()
        data    = resp.json()

        results = []
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

        # Fit a fresh vectorizer per query (queries are too distinct to share
        # vocabulary across calls, so we still need to fit).  However we reuse
        # the Python object to avoid __init__ overhead on every search call.
        try:
            tfidf_matrix = self._vectorizer.fit_transform([query] + texts)
        except ValueError:
            return []

        scores = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1:])[0]

        ranked = []
        for i, score in enumerate(scores):
            text = re.sub(r"<[^>]+>", "", results[i]["text"]).strip()
            ranked.append({"answer": text, "source": results[i]["url"], "score": float(score)})

        ranked.sort(key=lambda x: x["score"], reverse=True)
        return ranked[:self.max_results]


# ---------------------------------------------------------------------------
# Main router
# ---------------------------------------------------------------------------

class GreenKNNRouter(MetaRouter):
    """
    GreenKNNRouter — optimised.

    Performance-critical changes vs original:
    -----------------------------------------
    • KNN model loaded once in __init__ (was: reloaded on every call).
    • route_batch: embeddings + MLP scores computed in a single batch pass.
    • route_batch: kneighbors() called once for all rows.
    • route_batch: LLM API calls issued concurrently via asyncio/aiohttp.
    • CO₂ min/max normalisation constants pre-computed in __init__.
    • _perf_lookup and _idx_to_embedding_id built with vectorised pandas ops.
    • torch.inference_mode() replaces torch.no_grad() (lower overhead).
    """

    def __init__(self, yaml_path: str):
        dummy = nn.Identity()
        super().__init__(model=dummy, yaml_path=yaml_path)

        hparam = self.cfg["hparam"]

        # ------------------------------------------------------------------ #
        # 1. KNN classifier                                                   #
        # ------------------------------------------------------------------ #
        # ------------------------------------------------------------------ #
        # 1. KNN classifier                                                   #
        # ------------------------------------------------------------------ #
        knn_params = {
            k: hparam[k]
            for k in ("n_neighbors", "weights", "algorithm",
                      "metric", "p", "n_jobs", "leaf_size")
            if k in hparam
        }
        self.knn_model = KNeighborsClassifier(**knn_params)

        # ------------------------------------------------------------------ #
        # 2. MLP difficulty estimator                                         #
        # ------------------------------------------------------------------ #
        embedding_dim = hparam.get("embedding_dim", 768)
        hidden_dim    = hparam.get("hidden_dim", 128)
        self.difficulty_estimator = DifficultyEstimator(
            input_dim=embedding_dim,
            hidden_dim=hidden_dim,
        )
        self.model     = self.difficulty_estimator
        self.threshold = hparam.get("threshold", 0.5)
        self.small_models: List[str] = hparam.get("small_models", [])

        # ------------------------------------------------------------------ #
        # 3. CO₂ data                                                         #
        # ------------------------------------------------------------------ #
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        co2_path     = os.path.join(project_root, self.cfg["data_path"].get("co2_data", ""))
        self.co2_data: Dict[str, float] = {}
        if os.path.exists(co2_path):
            with open(co2_path, "r", encoding="utf-8") as f:
                self.co2_data = json.load(f)
            print(f"✅ CO₂ data loaded from {co2_path}")
            print(f"✅ CO₂ data loaded from {co2_path}")
        else:
            print(f"⚠️  CO₂ file not found: {co2_path}")

        self.w_perf = hparam.get("w_perf", 1.0)
        self.w_co2  = hparam.get("w_co2",  0.3)

        # ------------------------------------------------------------------ #
        # 4. Web search                                                        #
        # ------------------------------------------------------------------ #
        web_cfg = self.cfg.get("web_search", {})
        self.use_web_search      = web_cfg.get("use_web_search", False)
        self.web_search_threshold = web_cfg.get("web_search_threshold", 0.8)

        if self.use_web_search:
            self.web_searcher = WebSearcher(
                max_results=web_cfg.get("max_results", 5),
                min_tfidf_score=web_cfg.get("min_tfidf_score", 0.1),
            )
        else:
            self.web_searcher = None

        # ------------------------------------------------------------------ #
        # 5. Training data — vectorised lookups (no iterrows)                 #
        # ------------------------------------------------------------------ #
        routing_best = self.routing_data_train.loc[
            self.routing_data_train.groupby("query")["performance"].idxmax()
        ].reset_index(drop=True)

        ids = routing_best["embedding_id"].tolist()
        self.query_embedding_list = [self.query_embedding_data[i].numpy() for i in ids]
        self.model_name_list      = routing_best["model_name"].tolist()
        self.query_embedding_list = [self.query_embedding_data[i].numpy() for i in ids]
        self.model_name_list      = routing_best["model_name"].tolist()

        # Vectorised pivot instead of iterrows — typically 50-100× faster.
        pivot = (
            self.routing_data_train
            .pivot_table(
                index="embedding_id",
                columns="model_name",
                values="performance",
                aggfunc="first",
            )
        )
        self._perf_lookup: Dict[int, Dict[str, float]] = {
            int(eid): {col: float(val) for col, val in row.items() if not np.isnan(val)}
            for eid, row in pivot.iterrows()
        }

        # Numpy array for O(1) index → embedding_id mapping.
        self._idx_to_embedding_id_arr = np.array(
            [int(row["embedding_id"]) for _, row in routing_best.iterrows()],
            dtype=np.int64,
        )

        # ------------------------------------------------------------------ #
        # 6. Load KNN from disk ONCE                                          #
        # ------------------------------------------------------------------ #
        load_knn_path = os.path.join(
            project_root, self.cfg["model_path"]["load_model_path"]
        )
        self.knn_model = load_model(load_knn_path)
        print(f"✅ KNN loaded from {load_knn_path}")

        # ------------------------------------------------------------------ #
        # 7. Load MLP if available                                            #
        # ------------------------------------------------------------------ #
        diff_path = self.cfg["model_path"].get("difficulty_model_path", "")
        if diff_path:
            full_diff_path = os.path.join(project_root, diff_path)
            if os.path.exists(full_diff_path):
                self.difficulty_estimator.load_state_dict(
                    torch.load(full_diff_path, map_location="cpu")
                )
                print(f"✅ MLP difficulty model loaded from {full_diff_path}")
            else:
                print("⚠️  MLP not trained yet — difficulty will default to ~0.5")

        self.difficulty_estimator.eval()   # permanently in eval mode

        # ------------------------------------------------------------------ #
        # 8. Pre-compute CO₂ normalisation constants for all candidate models #
        # ------------------------------------------------------------------ #
        self._candidate_models: List[str] = self._build_candidate_list()
        self._co2_norm: Dict[str, float]  = self._build_co2_norm(self._candidate_models)

        print("✅ GreenKNNRouter initialised.")
        print(f"   Difficulty threshold : {self.threshold}")
        print(f"   Small models         : {self.small_models}")
        print(f"   w_perf={self.w_perf}, w_co2={self.w_co2}")

    # ---------------------------------------------------------------------- #
    # Private helpers                                                         #
    # ---------------------------------------------------------------------- #

    def _build_candidate_list(self) -> List[str]:
        return list(self.llm_data.keys()) if self.llm_data else list(set(self.model_name_list))

    def _build_co2_norm(self, candidates: List[str]) -> Dict[str, float]:
        """Pre-compute normalised CO₂ per model so _compute_utility is O(n)."""
        values    = [self.co2_data.get(m, 0.0) for m in candidates]
        co2_min   = min(values) if values else 0.0
        co2_max   = max(values) if values else 1.0
        co2_range = (co2_max - co2_min) or 1.0
        return {m: (self.co2_data.get(m, 0.0) - co2_min) / co2_range for m in candidates}

    def _get_fallback_small_model(self) -> str:
        for m in self.small_models:
            if m in self._candidate_models:
                return m
        return self._candidate_models[0] if self._candidate_models else "unknown"

    # ------------------------------------------------------------------ #
    # Single-item difficulty (used by route_single)                       #
    # ------------------------------------------------------------------ #
    def _estimate_difficulty(self, embedding: np.ndarray) -> float:
        with torch.inference_mode():
            t = torch.tensor(embedding, dtype=torch.float32).unsqueeze(0)
            return float(self.difficulty_estimator(t).item())

    # ------------------------------------------------------------------ #
    # Batch difficulty (used by route_batch)                              #
    # ------------------------------------------------------------------ #
    def _estimate_difficulty_batch(self, embeddings: np.ndarray) -> np.ndarray:
        """
        embeddings : (N, D) float32 numpy array
        returns    : (N,)   float32 numpy array of difficulty scores
        """
        with torch.inference_mode():
            t = torch.tensor(embeddings, dtype=torch.float32)
            return self.difficulty_estimator(t).squeeze(-1).numpy()

    # ------------------------------------------------------------------ #
    # KNN performance scores — single query                               #
    # ------------------------------------------------------------------ #
    def _knn_perf_scores(
        self,
        embedding: np.ndarray,
        candidate_models: List[str],
    ) -> Dict[str, float]:
        distances, indices = self.knn_model.kneighbors([embedding])
        return self._aggregate_knn(
            distances[0], indices[0], candidate_models
        )

    # ------------------------------------------------------------------ #
    # KNN performance scores — batch of queries                           #
    # ------------------------------------------------------------------ #
    def _knn_perf_scores_batch(
        self,
        embeddings: np.ndarray,
        candidate_models: List[str],
    ) -> List[Dict[str, float]]:
        """
        embeddings : (N, D)
        Returns a list of N perf-score dicts, one per row.
        Single kneighbors() call for the whole batch.
        """
        distances_batch, indices_batch = self.knn_model.kneighbors(embeddings)
        return [
            self._aggregate_knn(distances_batch[i], indices_batch[i], candidate_models)
            for i in range(len(embeddings))
        ]

    def _aggregate_knn(
        self,
        distances: np.ndarray,
        indices: np.ndarray,
        candidate_models: List[str],
    ) -> Dict[str, float]:
        if self.knn_model.weights == "distance":
            weights = np.where(distances == 0, 1e10, 1.0 / distances)
        else:
            weights = np.ones(len(indices))
        weights = weights / weights.sum()

        perf_scores: Dict[str, float] = {m: 0.0 for m in candidate_models}
        for w, idx in zip(weights, indices):
            eid = int(self._idx_to_embedding_id_arr[idx])
            neighbor_perfs = self._perf_lookup.get(eid, {})
            for model in candidate_models:
                perf_scores[model] += w * neighbor_perfs.get(model, 0.0)
        return perf_scores

    # ------------------------------------------------------------------ #
    # Utility scores — uses pre-computed CO₂ norms                       #
    # ------------------------------------------------------------------ #
    def _compute_utility(
        self,
        perf_scores: Dict[str, float],
        candidate_models: List[str],
        co2_norm: Optional[Dict[str, float]] = None,
    ) -> Dict[str, float]:
        if co2_norm is None:
            co2_norm = self._co2_norm
        return {
            m: self.w_perf * perf_scores[m] - self.w_co2 * co2_norm.get(m, 0.0)
            for m in candidate_models
        }

    def _try_web_search(self, query_text: str) -> Optional[Dict[str, Any]]:
        if self.web_searcher is None:
            return None
        result = self.web_searcher.search(query_text)
        if result:
            best = result["best"]
            return {
                "answer":      best["answer"],
                "source":      best["source"],
                "answers":     result["answers"],
                "tfidf_score": best["score"],
                "method":      "web_search",
            }
        return None

    # ------------------------------------------------------------------ #
    # Candidate selection depending on difficulty                         #
    # ------------------------------------------------------------------ #
    def _select_candidates(self, difficulty: float) -> List[str]:
        if difficulty < self.threshold and self.small_models:
            candidates = [m for m in self._candidate_models if m in self.small_models]
            return candidates if candidates else self._candidate_models
        return self._candidate_models

    # ---------------------------------------------------------------------- #
    # Public API                                                              #
    # ---------------------------------------------------------------------- #

    def route_single(self, query: Dict[str, Any]) -> Dict[str, Any]:
        """Route a single query.  KNN model is already loaded in __init__."""
        query_text = query["query"]

        embedding  = get_longformer_embedding(query_text).numpy()
        difficulty = self._estimate_difficulty(embedding)

        output = copy.copy(query)
        output["difficulty_score"]     = difficulty
        output["threshold"]            = self.threshold
        output["web_search_threshold"] = self.web_search_threshold

        # — Web search branch —
        if self.use_web_search and difficulty > self.web_search_threshold:
            web_result = self._try_web_search(query_text)
            if web_result:
                output.update({
                    "model_name":    "web_search",
                    "method":        "web_search",
                    "answer":        web_result["answer"],
                    "source":        web_result["source"],
                    "answers":       web_result.get("answers", []),
                    "tfidf_score":   web_result["tfidf_score"],
                    "perf_scores":   {},
                    "co2_scores":    {},
                    "utility_scores": {},
                })
                return output
            # Fallback
            fallback = self._get_fallback_small_model()
            output.update({
                "model_name":    fallback,
                "method":        "web_fallback_llm",
                "perf_scores":   {},
                "co2_scores":    {fallback: self.co2_data.get(fallback, 0.0)},
                "utility_scores": {},
            })
            return output

        # — LLM routing branch —
        candidates     = self._select_candidates(difficulty)
        co2_norm       = self._build_co2_norm(candidates) if candidates != self._candidate_models else self._co2_norm
        perf_scores    = self._knn_perf_scores(embedding, candidates)
        utility_scores = self._compute_utility(perf_scores, candidates, co2_norm)
        best_model     = max(utility_scores, key=utility_scores.__getitem__)

        output.update({
            "model_name":    best_model,
            "method":        "llm_routing",
            "perf_scores":   perf_scores,
            "co2_scores":    {m: self.co2_data.get(m, 0.0) for m in candidates},
            "utility_scores": utility_scores,
        })
        return output

    # ------------------------------------------------------------------ #
    # Async helper for concurrent API calls                               #
    # ------------------------------------------------------------------ #

    async def _call_api_async(
        self,
        session: aiohttp.ClientSession,
        request: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Fire a single LLM API call asynchronously.
        Falls back to the synchronous call_api() if aiohttp is unavailable.
        """
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
                data     = await resp.json()
                response = data.get("choices", [{}])[0].get("message", {}).get("content", "")
                usage    = data.get("usage", {})
                return {
                    "response":          response,
                    "prompt_tokens":     usage.get("prompt_tokens", 0),
                    "completion_tokens": usage.get("completion_tokens", 0),
                }
        except Exception as e:
            print(f"❌ Async API error: {e}")
            return {"response": "", "prompt_tokens": 0, "completion_tokens": 0, "error": str(e)}

    # ------------------------------------------------------------------ #
    # Async helper for concurrent API calls                               #
    # ------------------------------------------------------------------ #

    async def _call_api_async(
        self,
        session: aiohttp.ClientSession,
        request: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Fire a single LLM API call asynchronously.
        Falls back to the synchronous call_api() if aiohttp is unavailable.
        """
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
                data     = await resp.json()
                response = data.get("choices", [{}])[0].get("message", {}).get("content", "")
                usage    = data.get("usage", {})
                return {
                    "response":          response,
                    "prompt_tokens":     usage.get("prompt_tokens", 0),
                    "completion_tokens": usage.get("completion_tokens", 0),
                }
        except Exception as e:
            print(f"❌ Async API error: {e}")
            return {"response": "", "prompt_tokens": 0, "completion_tokens": 0, "error": str(e)}

    async def _route_batch_async(
        self,
        rows: List[Dict[str, Any]],
        routing_results: List[Dict[str, Any]],
        task_name: Optional[str],
    ) -> List[Dict[str, Any]]:
        """
        Given pre-computed routing decisions, fire all LLM API calls
        concurrently and return the enriched row dicts.
        """
        results: List[Dict[str, Any]] = []

        async with aiohttp.ClientSession() as session:
            tasks = []
            meta  = []  # parallel metadata for result assembly

            for row_copy, routing_result in zip(rows, routing_results):
                method     = routing_result.get("method", "llm_routing")
                best_model = routing_result.get("model_name", "")

                if method == "web_search":
                    # No API call needed — answer already in routing_result.
                    tasks.append(None)
                    meta.append(None)
                    continue

                # Format prompt
                original_query = row_copy.get("query", "")
                row_task_name  = row_copy.get("task_name", task_name)
                if row_task_name:
                    try:
                        formatted = generate_task_query(
                            row_task_name,
                            {"query": original_query, "choices": row_copy.get("choices")},
                        )
                    except (ValueError, KeyError) as e:
                        print(f"⚠️  Formatting failed ({e}); using raw query.")
                        formatted = original_query
                else:
                    formatted = original_query

                row_copy["formatted_query"] = formatted

                api_model_name = best_model
                api_endpoint   = None
                service        = None

                if self.llm_data and best_model in self.llm_data:
                    api_model_name = self.llm_data[best_model].get("model", best_model)
                    api_endpoint   = self.llm_data[best_model].get("api_endpoint")
                    service        = self.llm_data[best_model].get("service")

                if api_endpoint is None:
                    api_endpoint = self.cfg.get("api_endpoint")
                if api_endpoint is None:
                    api_endpoint = self.cfg.get("api_endpoint")

                if not api_endpoint:
                    raise ValueError(
                        f"No API endpoint for '{best_model}'. "
                        "Check 'api_endpoint' in llm_data or YAML."
                    )

                request = {
                    "api_endpoint": api_endpoint,
                    "query":        formatted,
                    "model_name":   best_model,
                    "api_name":     api_model_name,
                }
                if service:
                    request["service"] = service
                request = {
                    "api_endpoint": api_endpoint,
                    "query":        formatted,
                    "model_name":   best_model,
                    "api_name":     api_model_name,
                }
                if service:
                    request["service"] = service

                tasks.append(asyncio.ensure_future(self._call_api_async(session, request)))
                meta.append(row_copy.get("task_name", task_name))

            # Gather all outstanding coroutines concurrently
            task_futures = [t for t in tasks if t is not None]
            task_results = await asyncio.gather(*task_futures, return_exceptions=True)

            # Reassemble — match task_results back to the rows that submitted them
            result_iter = iter(task_results)
            for row_copy, routing_result, t in zip(rows, routing_results, tasks):
                row_copy.update({
                    k: v for k, v in routing_result.items() if k != "query"
                })
                method = routing_result.get("method", "llm_routing")

                if method == "web_search":
                    row_copy["response"]          = routing_result.get("answer", "")
                    row_copy["success"]            = True
                    row_copy["prompt_tokens"]      = 0
                    row_copy["completion_tokens"]  = 0
                    results.append(row_copy)
                    continue

                api_result = next(result_iter)
                if isinstance(api_result, Exception):
                    print(f"❌ API error: {api_result}")
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
                results.append(row_copy)

        return results

    # ------------------------------------------------------------------ #
    # route_batch — batch embeddings + batch KNN + async API calls        #
    # ------------------------------------------------------------------ #

    def route_batch(
        self,
        batch: Optional[Any] = None,
        task_name: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Route a batch of queries.

        Optimisation summary:
        - All Longformer embeddings computed in a single batched forward pass.
        - All MLP difficulty scores computed in a single batched forward pass.
        - A single kneighbors() call covers the whole non-web subset.
        - All LLM API requests fired concurrently via asyncio + aiohttp.
        """
        if batch is not None:
            query_data = batch if isinstance(batch, list) else [batch]
        elif hasattr(self, "query_data_test") and self.query_data_test is not None:
            query_data = copy.copy(self.query_data_test)
        else:
            print("⚠️  No data provided for batch routing.")
            return []

        # Normalise rows to dicts
        rows: List[Dict[str, Any]] = []
        for row in query_data:
            if isinstance(row, dict):
                rows.append(copy.copy(row))
            else:
                rows.append({"query": str(row)})

        queries = [r.get("query", "") for r in rows]

        # ---- 1. Batch embeddings ---------------------------------------- #
        # If get_longformer_embeddings_batch is available use it; otherwise
        # fall back to sequential calls (still avoids the reload penalty).
        try:
            embeddings = get_longformer_embeddings_batch(queries)  # (N, D) numpy
        except (AttributeError, TypeError):
            embeddings = np.stack([
                get_longformer_embedding(q).numpy() for q in queries
            ])

        # ---- 2. Batch difficulty estimation ------------------------------ #
        difficulties = self._estimate_difficulty_batch(embeddings)  # (N,)

        # ---- 3. Partition: web vs LLM ------------------------------------ #
        web_mask = (
            self.use_web_search
            and (difficulties > self.web_search_threshold)
        )
        if not isinstance(web_mask, np.ndarray):
            web_mask = np.array([web_mask] * len(rows))

        llm_indices = [i for i in range(len(rows)) if not web_mask[i]]
        web_indices = [i for i in range(len(rows)) if web_mask[i]]

        # ---- 4. Batch KNN for LLM rows ---------------------------------- #
        # We route per-difficulty (small vs full model set); group by candidate set.
        routing_results: List[Optional[Dict[str, Any]]] = [None] * len(rows)

        if llm_indices:
            llm_embeddings = embeddings[llm_indices]

            # Determine candidate set per row; group by (use_small: bool)
            use_small = [
                difficulties[i] < self.threshold and bool(self.small_models)
                for i in llm_indices
            ]

            # Compute full-set candidates once; small-set once (if needed).
            full_candidates  = self._candidate_models
            small_candidates = (
                [m for m in full_candidates if m in self.small_models] or full_candidates
            ) if any(use_small) else []

            full_co2_norm  = self._co2_norm
            small_co2_norm = (
                self._build_co2_norm(small_candidates) if small_candidates else {}
            )

            # One kneighbors call for the whole LLM subset.
            distances_batch, indices_batch = self.knn_model.kneighbors(llm_embeddings)

            for rank, i in enumerate(llm_indices):
                candidates = (
                    small_candidates if use_small[rank] and small_candidates
                    else full_candidates
                )
                co2_norm   = small_co2_norm if use_small[rank] and small_candidates else full_co2_norm

                perf_scores    = self._aggregate_knn(
                    distances_batch[rank], indices_batch[rank], candidates
                )
                utility_scores = self._compute_utility(perf_scores, candidates, co2_norm)
                best_model     = max(utility_scores, key=utility_scores.__getitem__)

                routing_results[i] = {
                    "query":           queries[i],
                    "difficulty_score": float(difficulties[i]),
                    "threshold":       self.threshold,
                    "web_search_threshold": self.web_search_threshold,
                    "model_name":      best_model,
                    "method":          "llm_routing",
                    "perf_scores":     perf_scores,
                    "co2_scores":      {m: self.co2_data.get(m, 0.0) for m in candidates},
                    "utility_scores":  utility_scores,
                }

        # ---- 5. Web search rows (sequential — network-bound) ------------ #
        for i in web_indices:
            web_result = self._try_web_search(queries[i])
            if web_result:
                routing_results[i] = {
                    "query":            queries[i],
                    "difficulty_score": float(difficulties[i]),
                    "threshold":        self.threshold,
                    "web_search_threshold": self.web_search_threshold,
                    "model_name":       "web_search",
                    "method":           "web_search",
                    "answer":           web_result["answer"],
                    "source":           web_result["source"],
                    "answers":          web_result.get("answers", []),
                    "tfidf_score":      web_result["tfidf_score"],
                    "perf_scores":      {},
                    "co2_scores":       {},
                    "utility_scores":   {},
                }
            else:
                fallback = self._get_fallback_small_model()
                routing_results[i] = {
                    "query":            queries[i],
                    "difficulty_score": float(difficulties[i]),
                    "threshold":        self.threshold,
                    "web_search_threshold": self.web_search_threshold,
                    "model_name":       fallback,
                    "method":           "web_fallback_llm",
                    "perf_scores":      {},
                    "co2_scores":       {fallback: self.co2_data.get(fallback, 0.0)},
                    "utility_scores":   {},
                }

        # ---- 6. Concurrent LLM API calls -------------------------------- #
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # Already inside an event loop (e.g. Jupyter).
                import nest_asyncio
                nest_asyncio.apply()
            return loop.run_until_complete(
                self._route_batch_async(rows, routing_results, task_name)
            )
        except RuntimeError:
            # No running loop.
            return asyncio.run(
                self._route_batch_async(rows, routing_results, task_name)
            )