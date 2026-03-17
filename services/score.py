def score_cv(text, info):
    skill_score = min(len(info["skills"]) / 5, 1)
    exp_score = min(len(info["experience"]) / 3, 1)
    edu_score = min(len(info["education"]) / 2, 1)

    length_score = 1 if 500 < len(text) < 3000 else 0.5

    keyword_score = sum([
        1 for k in ["python","sql","ai","data","developer"]
        if k in text.lower()
    ]) / 5

    total = (
        skill_score * 30 +
        exp_score * 30 +
        edu_score * 15 +
        length_score * 10 +
        keyword_score * 15
    )

    return {
        "total_score": round(total),
        "breakdown": {
            "skills": skill_score,
            "experience": exp_score,
            "education": edu_score,
            "length": length_score,
            "keywords": keyword_score
        }
    }