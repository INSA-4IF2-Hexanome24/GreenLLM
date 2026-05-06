from typing import Any, Dict, List, Optional
import traceback
import pandas as pd
import torch
import json
import os


def load_csv(path: str) -> Optional[pd.DataFrame]:
    """
    Load a CSV file and return a pandas DataFrame.
    """
    if not os.path.exists(path):
        return None
    try:
        df = pd.read_csv(path)
        return df
    except Exception:
        return None


def load_jsonl(path: str) -> Optional[List[Dict[str, Any]]]:
    """
    Load a JSONL (JSON Lines) file and return a list of dictionaries.
    """
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = [json.loads(line) for line in f]
        return data
    except Exception:
        return None


def jsonl_to_csv(jsonl_path: str, csv_path: Optional[str] = None) -> Optional[pd.DataFrame]:
    """
    Convert a JSONL file to CSV and return the DataFrame.
    If `csv_path` is not provided, the CSV will be saved in the same directory as the JSONL.
    """
    if not os.path.exists(jsonl_path):
        print(f"[UTILS-DEBUG] jsonl_to_csv missing path: {jsonl_path}", flush=True)
        return None

    try:
        print(f"[UTILS-DEBUG] jsonl_to_csv reading: {jsonl_path}", flush=True)
        # Use pandas JSONL reader directly to avoid building a huge intermediate
        # Python list of dicts, which can spike memory usage.
        df = pd.read_json(jsonl_path, lines=True)
        print(f"[UTILS-DEBUG] jsonl_to_csv dataframe shape={df.shape}", flush=True)

        if csv_path is None:
            csv_path = os.path.splitext(jsonl_path)[0] + ".csv"

        print(f"[UTILS-DEBUG] jsonl_to_csv writing csv: {csv_path}", flush=True)
        df.to_csv(csv_path, index=False, encoding="utf-8")
        print("[UTILS-DEBUG] jsonl_to_csv done", flush=True)
        return df
    except Exception:
        print("[UTILS-DEBUG] jsonl_to_csv failed with traceback:", flush=True)
        traceback.print_exc()
        return None


def load_pt(path: str) -> Optional[Any]:
    """
    Load a PyTorch .pt file (can be a Tensor or a Dict).
    """
    if not os.path.exists(path):
        return None
    try:
        data = torch.load(path, map_location="cpu")
        return data
    except Exception:
        return None
