import numpy as np
import torch

def get_longformer_embeddings_batch(queries, model, tokenizer, device="cpu"):
    inputs = tokenizer(
        queries,
        padding=True,
        truncation=True,
        return_tensors="pt"
    ).to(device)

    with torch.no_grad():
        outputs = model(**inputs)
        embeddings = outputs.last_hidden_state[:, 0, :]  # CLS token

    return embeddings.cpu().numpy()