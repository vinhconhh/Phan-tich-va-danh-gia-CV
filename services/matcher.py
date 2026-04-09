import numpy as np
from services.embedding import embed_batch

_SIM_MIN = 0.60
_SIM_MAX = 0.95

_CATEGORY_PENALTY = 25.0


def _rescale(raw: float) -> float:
    return float(np.clip((raw - _SIM_MIN) / (_SIM_MAX - _SIM_MIN), 0, 1)) * 100


def rank_multiple_cvs(
    cv_texts: dict,
    jd_text: str,
    classify_results: dict = None,
    jd_category: str = None,
) -> list:
    names = list(cv_texts.keys())
    texts = list(cv_texts.values()) + [jd_text]

    vecs    = embed_batch(texts)
    cv_vecs = vecs[:-1]
    jd_vec  = vecs[-1]

    raw_scores = cv_vecs @ jd_vec    # cosine sim thô

    results = []
    for name, raw in zip(names, raw_scores):
        score = _rescale(float(raw))

        if classify_results and jd_category:
            cv_category = classify_results.get(name, {}).get("category", "")
            if cv_category and cv_category != jd_category:
                score = max(0.0, score - _CATEGORY_PENALTY)

        results.append((name, round(score, 2)))

    return sorted(results, key=lambda x: x[1], reverse=True)


def match_cv_jd_sbert(cv_text: str, jd_text: str) -> float:
    vecs = embed_batch([cv_text, jd_text])
    raw  = float(vecs[0] @ vecs[1])
    return round(_rescale(raw), 2)