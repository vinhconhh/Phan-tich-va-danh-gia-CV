"""
matcher.py  –  Tối ưu với normalized embeddings
Vì embedding.py đã normalize_embeddings=True, cosine similarity = dot product.
Dùng np.dot thay vì sklearn.cosine_similarity → nhanh hơn ~3x.
"""

import numpy as np
from services.embedding import embed_batch


def rank_multiple_cvs(cv_texts: dict, jd_text: str) -> list:
    names = list(cv_texts.keys())
    texts = list(cv_texts.values()) + [jd_text]

    vecs    = embed_batch(texts)          # đã normalized
    cv_vecs = vecs[:-1]                   # (N, dim)
    jd_vec  = vecs[-1]                    # (dim,)

    # Với normalized vectors: cosine_sim = dot product
    scores = cv_vecs @ jd_vec             # (N,)

    results = [
        (name, round(float(np.clip(s, 0, 1)) * 100, 2))
        for name, s in zip(names, scores)
    ]
    return sorted(results, key=lambda x: x[1], reverse=True)


def match_cv_jd_sbert(cv_text: str, jd_text: str) -> float:
    vecs  = embed_batch([cv_text, jd_text])
    score = float(np.clip(vecs[0] @ vecs[1], 0, 1))
    return round(score * 100, 2)