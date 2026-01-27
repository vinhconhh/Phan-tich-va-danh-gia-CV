# services/classifier.py
from services.embedding import embed_text
from sklearn.metrics.pairwise import cosine_similarity

# taxonomy mô tả ngành
CATEGORIES = {
    "IT / Software": "software developer programming backend frontend",
    "Data / AI": "data science machine learning ai",
    "DevOps": "devops docker kubernetes ci cd aws linux system",
    "Marketing": "seo digital marketing",
    "Finance": "accounting finance audit",
    "Education": "teacher lecturer training",
    "Healthcare": "nurse doctor medical"
}

# mapping concept → ngành
CONCEPT_TO_CATEGORY = {
    "python": ["IT / Software", "Data / AI"],
    "java": ["IT / Software"],
    "docker": ["IT / Software", "DevOps"],
    "sql": ["IT / Software", "Data / AI"],
    "seo": ["Marketing"],
    "accounting": ["Finance"],
    "teacher": ["Education"],
    "nurse": ["Healthcare"]
}

def extract_concepts(cv_text):
    text = cv_text.lower()
    concepts = []
    for k in CONCEPT_TO_CATEGORY.keys():
        if k in text:
            concepts.append(k)
    return concepts

def infer_candidate_categories(concepts):
    cats = set()
    for c in concepts:
        for cat in CONCEPT_TO_CATEGORY.get(c, []):
            cats.add(cat)
    return list(cats)

def classify_cv(cv_text):
    concepts = extract_concepts(cv_text)
    candidate_cats = infer_candidate_categories(concepts)

    if not candidate_cats:
        return {
            "category": "Other",
            "confidence": 0,
            "concepts": [],
            "all_scores": {}
        }

    cv_vec = embed_text(cv_text)
    scores = {}

    for cat in candidate_cats:
        if cat not in CATEGORIES:
            continue   # chống crash
        desc = CATEGORIES[cat]
        cat_vec = embed_text(desc)
        sim = cosine_similarity([cv_vec], [cat_vec])[0][0]
        scores[cat] = float(sim)

    if not scores:
        return {
            "category": "Other",
            "confidence": 0,
            "concepts": concepts,
            "all_scores": {}
        }

    best_cat = max(scores, key=scores.get)

    return {
        "concepts": concepts,
        "category": best_cat,
        "confidence": round(scores[best_cat] * 100),
        "all_scores": scores
    }

