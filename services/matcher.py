from services.embedding import embed_batch
from sklearn.metrics.pairwise import cosine_similarity

def rank_multiple_cvs(cv_texts: dict, jd_text: str):
    """FIX: encode JD + tất cả CV trong 1 lần batch thay vì gọi từng cái"""
    names = list(cv_texts.keys())
    texts = list(cv_texts.values()) + [jd_text]

    vecs = embed_batch(texts)
    cv_vecs = vecs[:-1]
    jd_vec = vecs[-1].reshape(1, -1)

    scores = cosine_similarity(cv_vecs, jd_vec).flatten()
    results = [
        (name, round(float(max(0, min(s, 1))) * 100, 2))
        for name, s in zip(names, scores)
    ]
    return sorted(results, key=lambda x: x[1], reverse=True)


def match_cv_jd_sbert(cv_text: str, jd_text: str):
    vecs = embed_batch([cv_text, jd_text])
    score = cosine_similarity([vecs[0]], [vecs[1]])[0][0]
    return round(float(max(0, min(score, 1))) * 100, 2)