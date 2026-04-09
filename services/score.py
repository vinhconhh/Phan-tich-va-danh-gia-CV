# SAU
import re
from services.infor_extractor import SKILL_DB

_FALLBACK_KEYWORDS = ["python", "sql", "ai", "data", "developer"]


def _extract_jd_keywords(jd_text: str) -> list:
    if not jd_text:
        return _FALLBACK_KEYWORDS
    t = jd_text.lower()
    found = [s for s in SKILL_DB if s in t]
    return found if found else _FALLBACK_KEYWORDS


def score_cv(text, info, jd_text: str = ""):
    skill_score = min(len(info["skills"]) / 5, 1)
    exp_score   = min(len(info["experience"]) / 3, 1)
    edu_score   = min(len(info["education"]) / 2, 1)

    length_score = 1 if 500 < len(text) < 3000 else 0.5

    jd_keywords  = _extract_jd_keywords(jd_text)
    keyword_score = sum(
        1 for k in jd_keywords if k in text.lower()
    ) / max(len(jd_keywords), 1)

    total = (
        skill_score   * 30 +
        exp_score     * 30 +
        edu_score     * 15 +
        length_score  * 10 +
        keyword_score * 15
    )

    return {
        "total_score": round(total),
        "breakdown": {
            "skills":     skill_score,
            "experience": exp_score,
            "education":  edu_score,
            "length":     length_score,
            "keywords":   keyword_score,
        }
    }