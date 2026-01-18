import json
import numpy as np
from statistics import mean, median, stdev

def load_samples(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return list(data.values())

def safe_mean(values):
    return round(mean(values), 3) if values else 0.0

def safe_median(values):
    return round(median(values), 3) if values else 0.0

def safe_std(values):
    return round(stdev(values), 3) if len(values) > 1 else 0.0

def compute_metrics(samples, quality_threshold=0.6):
    accepted = [s for s in samples if s.get("accepted")]

    return {
        "total_samples": len(samples),
        "accepted_samples": len(accepted),
        "acceptance_rate": round(len(accepted) / len(samples), 3),

        "avg_gen_time_ms": safe_mean([s["gen_time_ms"] for s in accepted]),
        "median_gen_time_ms": safe_median([s["gen_time_ms"] for s in accepted]),
        "avg_attempts": safe_mean([s["attempt"] + 1 for s in accepted]),

        "avg_quality": safe_mean([s["quality_score"] for s in accepted]),
        "median_quality": safe_median([s["quality_score"] for s in accepted]),
        "quality_std": safe_std([s["quality_score"] for s in accepted]),
        "pct_quality_above_threshold": round(
            sum(1 for s in accepted if s["quality_score"] >= quality_threshold)
            / len(accepted),
            3
        ),

        "avg_semantic_similarity": safe_mean(
            [s["quality_parts"]["semantic_similarity"] for s in accepted]
        ),
        "near_duplicate_rate": round(
            sum(
                1 for s in accepted
                if s["quality_parts"]["semantic_similarity"] >= 0.85
            ) / len(accepted),
            3
        ),
        "avg_diversity": safe_mean(
            [s["quality_parts"]["diversity"] for s in accepted]
        ),

        "avg_domain_score": safe_mean(
            [s["quality_parts"]["domain_semantic"] for s in accepted]
        ),
        "avg_forbidden_score": safe_mean(
            [s["quality_parts"]["forbidden_semantic"] for s in accepted]
        )
    }
