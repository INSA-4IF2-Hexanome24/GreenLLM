import os
import csv
import json
import traceback
import pandas as pd
from llmrouter.utils import load_csv, load_jsonl, jsonl_to_csv, load_pt


def load_json_file(path: str):
    """Load JSON file with proper file handle management."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_routing_jsonl_compact(path: str):
    """Load only routing-critical columns from JSONL to reduce memory pressure."""
    model_names = []
    performances = []
    embedding_ids = []

    with open(path, "r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            if line_no % 5000 == 0:
                print(f"[DATA-DEBUG] Parsed {line_no} routing rows...", flush=True)
            try:
                obj = json.loads(line)
            except Exception as exc:
                print(
                    f"[DATA-DEBUG] Invalid JSON at line {line_no} in {path}: {exc}",
                    flush=True,
                )
                raise

            model_names.append(obj.get("model_name"))
            performances.append(obj.get("performance"))
            embedding_ids.append(obj.get("embedding_id"))

    total_rows = len(model_names)
    print(f"[DATA-DEBUG] Creating compact routing dataframe with rows={total_rows}", flush=True)
    df = pd.DataFrame(
        {
            "model_name": model_names,
            "performance": performances,
            "embedding_id": embedding_ids,
        }
    )
    print(f"[DATA-DEBUG] Compact routing dataframe shape={df.shape}", flush=True)
    return df


def load_routing_table(path: str):
    """Load routing data from CSV or JSONL depending on extension."""
    lower = path.lower()
    if lower.endswith(".csv"):
        print(f"[DATA-DEBUG] Loading routing data as compact CSV (stream+agg): {path}", flush=True)
        # Aggregate maximium performance per (embedding_id, model_name) while streaming
        perf_map: dict = {}  # embedding_id -> { model_name: max_perf }

        with open(path, "r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for line_no, row in enumerate(reader, start=2):
                if line_no % 5000 == 0:
                    print(f"[DATA-DEBUG] Streamed {line_no} CSV rows...", flush=True)
                try:
                    emb_raw = row.get("embedding_id")
                    if emb_raw is None:
                        continue
                    emb = int(emb_raw)
                    m = row.get("model_name")
                    perf_raw = row.get("performance")
                    perf = float(perf_raw) if perf_raw not in (None, "") else None
                except Exception:
                    # skip malformed rows but warn
                    print(f"[DATA-DEBUG] malformed CSV row at {line_no}", flush=True)
                    continue

                if perf is None:
                    continue

                model_dict = perf_map.setdefault(emb, {})
                prev = model_dict.get(m)
                if (prev is None) or (perf > prev):
                    model_dict[m] = perf

        # Build compact DataFrame from aggregated map (much smaller than full table)
        rows = []
        for emb, mdict in perf_map.items():
            for mname, p in mdict.items():
                rows.append({"embedding_id": emb, "model_name": mname, "performance": p})

        print(f"[DATA-DEBUG] Aggregated routing rows={len(rows)} (unique embedding-model pairs)", flush=True)
        if not rows:
            print("[DATA-DEBUG] No routing rows found after aggregation", flush=True)
            return None

        # Return the compact aggregated structure (perf_map + rows).
        # Higher-level code (DataLoader.load_data) will attach lightweight
        # mappings to the router object to avoid building large DataFrames.
        return {"perf_map": perf_map, "rows": rows}
    if lower.endswith(".jsonl"):
        print(f"[DATA-DEBUG] Loading routing data as compact JSONL: {path}", flush=True)
        return load_routing_jsonl_compact(path)

    print(f"[DATA-DEBUG] Unsupported routing file extension for {path}", flush=True)
    return None


class DataLoader:
    """
    DataLoaderCore
    --------------
    Handles all file-loading logic used by MetaRouter.
    """

    def __init__(self, project_root: str):
        self.project_root = project_root

    def to_abs(self, path_str: str) -> str:
        """Convert relative path (in YAML) to absolute path based on project root."""
        if os.path.isabs(path_str):
            return path_str
        return os.path.join(self.project_root, path_str)

    def load_data(self, config, obj_ref):
        """Attach loaded data fields directly onto the given object (obj_ref)."""
        data_path = config.get("data_path", {})
        print("[DATA-DEBUG] Starting load_data", flush=True)

        def safe_load(path_key, loader_fn, desc):
            if path_key in data_path:
                abs_path = self.to_abs(data_path[path_key])
                print(f"[DATA-DEBUG] Loading {desc} from {abs_path}", flush=True)
                if os.path.exists(abs_path):
                    try:
                        value = loader_fn(abs_path)
                        print(
                            f"[DATA-DEBUG] Loaded {desc} (is_none={value is None})",
                            flush=True,
                        )
                        return value
                    except Exception:
                        print(f"[DATA-DEBUG] Exception while loading {desc}", flush=True)
                        traceback.print_exc()
                        raise
                else:
                    print(f"[Warning] Missing {desc}: {abs_path}", flush=True)
            else:
                print(f"[DATA-DEBUG] Skipping {desc} (not in config)", flush=True)
            return None

        # Query data
        obj_ref.query_data_train = safe_load("query_data_train", load_jsonl, "query_data_train")
        obj_ref.query_data_test = safe_load("query_data_test", load_jsonl, "query_data_test")

        # Routing data (load BEFORE embeddings to reduce peak memory)
        routing_train_val = safe_load("routing_data_train", load_routing_table, "routing_data_train")
        obj_ref.routing_data_test = safe_load("routing_data_test", load_routing_table, "routing_data_test")

        # If we received the compact aggregated structure, attach lightweight
        # mappings to the object to be used by routers/trainers without
        # constructing large pandas DataFrames.
        if isinstance(routing_train_val, dict) and "perf_map" in routing_train_val:
            obj_ref.routing_perf_map = routing_train_val["perf_map"]
            obj_ref.routing_aggregated_rows = routing_train_val.get("rows", [])
            # Keep a marker to indicate that routing_data_train is not a DataFrame
            obj_ref.routing_data_train = None
        else:
            obj_ref.routing_data_train = routing_train_val

        # Embeddings (loaded after routing table)
        obj_ref.query_embedding_data = safe_load("query_embedding_data", load_pt, "query_embedding_data")

        # LLM info
        obj_ref.llm_data = safe_load("llm_data", load_json_file, "llm_data")
        obj_ref.llm_embedding_data = safe_load("llm_embedding_data", load_json_file, "llm_embedding_data")

        # If embeddings are present and we have an aggregated perf_map, compute
        # the lightweight lists required by GreenKNNRouter to avoid heavy DataFrames.
        try:
            if getattr(obj_ref, "routing_perf_map", None) and getattr(obj_ref, "query_embedding_data", None):
                perf_map = obj_ref.routing_perf_map
                # Build routing_best ordering (sort by embedding_id for determinism)
                embedding_ids = sorted(perf_map.keys())
                best_models = []
                idx_to_embedding = []
                for emb in embedding_ids:
                    md = perf_map[emb]
                    # choose best model by max performance
                    best_model = max(md.items(), key=lambda kv: kv[1])[0]
                    best_models.append(best_model)
                    idx_to_embedding.append(int(emb))

                # Attach small structures expected by the router
                # query_embedding_data is assumed to be indexable by embedding id
                obj_ref.query_embedding_list = [obj_ref.query_embedding_data[i].numpy() for i in idx_to_embedding if i < len(obj_ref.query_embedding_data)]
                obj_ref.model_name_list = best_models[: len(obj_ref.query_embedding_list) ]
                obj_ref._perf_lookup = {int(e): {k: float(v) for k, v in md.items()} for e, md in perf_map.items()}
                import numpy as _np
                obj_ref._idx_to_embedding_id_arr = _np.array(idx_to_embedding, dtype=_np.int64)
                print(f"[DATA-DEBUG] Attached lightweight routing structures: embeddings={len(obj_ref.query_embedding_list)}, models={len(obj_ref.model_name_list)}", flush=True)
        except Exception:
            print("[DATA-DEBUG] Failed to attach lightweight routing structures", flush=True)
            traceback.print_exc()

        print("[DATA-DEBUG] load_data completed", flush=True)
