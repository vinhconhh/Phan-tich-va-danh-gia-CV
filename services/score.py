def score_cv(text, info):
    breakdown = {
        "skills": {
            "weight": 30,
            "score": 1 if info["skills"] else 0
        },
        "experience": {
            "weight": 35,
            "score": 1 if len(info["experience"]) > 0 else 0
        },
        "education": {
            "weight": 15,
            "score": min(len(info["education"]) / 2, 1)
        },
        "formatting": {
            "weight": 10,
            "score": 1 if len(text) > 500 else 0.5
        },
        "keywords": {
            "weight": 10,
            "score": 1 if "python" in text.lower() else 0.5
        }
    }

    total_score = sum(v["score"] * v["weight"] for v in breakdown.values())

    return {
        "total_score": round(total_score),
        "breakdown": breakdown
    }