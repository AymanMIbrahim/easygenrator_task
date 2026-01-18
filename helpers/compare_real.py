import json
import random
import numpy as np
from sentence_transformers import SentenceTransformer

semantic_model = SentenceTransformer(
    "all-MiniLM-L6-v2",
    device="cpu"
)

def load_real_reviews(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def random_sample(samples, k):
    return random.sample(samples, min(k, len(samples)))

def nearest_real_similarity(synthetic_texts, real_texts):
    syn_embs = semantic_model.encode(
        synthetic_texts, normalize_embeddings=True
    )
    real_embs = semantic_model.encode(
        real_texts, normalize_embeddings=True
    )

    sims = np.dot(syn_embs, real_embs.T)  # (N_syn, N_real)
    max_sims = np.max(sims, axis=1)

    return {
        "avg": float(np.mean(max_sims)),
        "median": float(np.median(max_sims)),
        "std": float(np.std(max_sims))
    }

def length_stats(texts):
    lengths = [len(t.split()) for t in texts]
    return {
        "avg": round(np.mean(lengths), 2),
        "std": round(np.std(lengths), 2)
    }

def compare_synthetic_with_real(
    real_reviews,
    synthetic_samples,
    sample_size=50
):
    sampled = random_sample(
        [s for s in synthetic_samples if s.get("accepted")],
        sample_size
    )

    syn_texts = [s["text"] for s in sampled]

    return {
        "sample_size": len(sampled),
        "semantic": nearest_real_similarity(syn_texts, real_reviews),
        "length": length_stats(syn_texts)
    }
