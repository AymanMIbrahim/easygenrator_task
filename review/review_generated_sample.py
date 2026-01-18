import re
from sentence_transformers import SentenceTransformer
import numpy as np
import json
semantic_model = SentenceTransformer("all-MiniLM-L6-v2",device="cpu")
with open("./config/config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

DOMAIN_ANCHOR = config["DOMAIN_ANCHOR"]
domain_anchor_emb = semantic_model.encode(
    DOMAIN_ANCHOR, normalize_embeddings=True
)

FORBIDDEN_ANCHOR = config["FORBIDDEN_ANCHOR"]
forbidden_anchor_emb = semantic_model.encode(
    FORBIDDEN_ANCHOR, normalize_embeddings=True
)


class Review:
    def __init__(self):
        pass

    def word_count(self,text: str) -> int:
        return len(re.findall(r"\b\w+\b", text))

    def length_score(self,text, min_words, max_words):
        wc = self.word_count(text)
        if min_words <= wc <= max_words:
            return 1.0
        if wc < min_words:
            return wc / max(1, min_words)
        return max_words / max(1, wc)

    def domain_score_semantic(self,text, threshold=0.3):
        text_emb = semantic_model.encode(text, normalize_embeddings=True)
        sims = np.dot(domain_anchor_emb, text_emb)
        max_sim = float(np.max(sims))

        if max_sim < 0.3:
            return 0.2
        elif max_sim < 0.45:
            return 0.6
        elif max_sim < 0.6:
            return 0.8
        else:
            return 1.0

    def forbidden_score_semantic(self,text):
        text_emb = semantic_model.encode(text, normalize_embeddings=True)
        sim = np.max(np.dot(forbidden_anchor_emb,text_emb))
        return float(sim)

    def diversity_score(self,max_similarity):
        if max_similarity < 0.5:
            return 1.0
        if max_similarity < 0.7:
            return 0.7
        if max_similarity < 0.8:
            return 0.4
        return 0.1

    def max_semantic_similarity(self,current_text, previous_texts):
        if not previous_texts:
            return 0.0

        current_emb = semantic_model.encode(current_text, normalize_embeddings=True)
        prev_embs = semantic_model.encode(previous_texts, normalize_embeddings=True)

        sims = np.dot(prev_embs, current_emb)
        return float(np.max(sims))

    def compute_quality(self,sample, cfg, previous_texts):
        text = sample["text"]
        rating = sample["rating"]

        min_w = cfg["review_rules"]["min_words"]
        max_w = cfg["review_rules"]["max_words"]

        # Scores
        ls = self.length_score(text, min_w, max_w)

        max_sim = self.max_semantic_similarity(text, previous_texts)
        ds = self.diversity_score(max_sim)

        dom = self.domain_score_semantic(text)

        rating_score = 1.0 if rating >= 4 else (0.8 if rating == 3 else 0.7)

        forbidden_sim = self.forbidden_score_semantic(text)
        penalty = 0.5 if forbidden_sim > 0.6 else 1.0

        quality = (0.20 * ls +0.35 * ds +0.25 * dom +0.20 * rating_score) * penalty

        return round(quality, 3), {
            "length": ls,
            "semantic_similarity": round(max_sim, 3),
            "diversity": ds,
            "domain_semantic": round(dom, 3),
            "rating": rating_score,
            "forbidden_semantic": round(forbidden_sim, 3),
            "penalty": penalty
        }

    def accept_or_reject(self,sample, cfg,previous_texts):
        threshold = cfg["quality"]["min_quality_score"]
        score, parts = self.compute_quality(sample, cfg,previous_texts)

        sample["quality_score"] = score
        sample["quality_parts"] = parts
        sample["accepted"] = score >= threshold
        return sample