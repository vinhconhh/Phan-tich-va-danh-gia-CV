from services.embedding import embed_text
from sklearn.metrics.pairwise import cosine_similarity

def match_cv_jd_sbert(cv_text, jd_text):
    cv_vec = embed_text(cv_text)
    jd_vec = embed_text(jd_text)
    score = cosine_similarity([cv_vec], [jd_vec])[0][0]
    score = float(score)
    score = max(0, min(score, 1))
    return round(score * 100, 2)

def rank_multiple_cvs(cv_texts, jd_text):
    jd_vec = embed_text(jd_text)
    results = []

    for name, cv_text in cv_texts.items():
        cv_vec = embed_text(cv_text)
        score = cosine_similarity([cv_vec], [jd_vec])[0][0]
        score = float(score)
        score = max(0, min(score, 1))
        results.append((name, round(score * 100, 2)))

    return sorted(results, key=lambda x: x[1], reverse=True)
