def score_cv(text, info):
    breakdown = {
        "skills": {
            "score": 30 if info["skills"] else 5,
            "weight": 30   # %
        },
        "experience": {
            "score": 35 if len(text) > 800 else 15,
            "weight": 35
        },
        "education": {
            "score": 15 if "đại học" in text.lower() else 5,
            "weight": 15
        },
        "formatting": {
            "score": 10,
            "weight": 10
        },
        "keywords": {
            "score": 10 if len(info["skills"]) >= 3 else 5,
            "weight": 10
        }
    }

    total_score = sum(v["score"] for v in breakdown.values())

    return {
        "total_score": total_score,
        "breakdown": breakdown
    }
