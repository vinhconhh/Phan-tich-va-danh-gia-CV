"""
classifier.py  –  Tối ưu cho 50+ CV
Thay đổi chính:
  1. Cache embedding của category descriptions (tính 1 lần duy nhất).
  2. classify_cv_batch(): embed toàn bộ CV 1 lần với embed_batch().
  3. classify_cv() giữ nguyên API nhưng gọi lại classify_cv_batch().
"""

import re
import numpy as np
import streamlit as st
from sklearn.metrics.pairwise import cosine_similarity

from services.embedding import embed_batch

# ─── Taxonomy ────────────────────────────────────────────────────────────────

CATEGORIES = {
    "Web Development":        "frontend backend fullstack javascript react nodejs html css typescript flask django express nextjs bootstrap tailwind",
    "Mobile Development":     "ios android react-native flutter swift kotlin objective-c dart jetpack-compose",
    "Data Engineering":       "data-pipeline sql spark hadoop etl warehouse airflow kafka dbt redshift snowflake bigquery databricks hive",
    "Data Science & AI":      "machine-learning deep-learning ai-engineer cnn rnn transformers nlp computer-vision tensorflow pytorch sagemaker azure-ml tensorrt onnx opencv scikit-learn pandas numpy",
    "Cybersecurity":          "pentest security ethical-hacking firewall cryptography network-security soc malware-analysis owasp siem vulnerability penetration-tester",
    "Cloud & DevOps":         "kubernetes jenkins terraform ansible cicd infrastructure-as-code monitoring logging bash-scripting automation aws azure google-cloud docker ec2",
    "Game Development":       "unity unreal-engine csharp game-design graphics-programming directx opengl shader cplusplus",
    "Embedded Systems / IoT": "c firmware microcontroller hardware raspberry-pi arduino embedded-linux rtos assembly fpga arm",
    "Software Testing / QA":  "automation-testing manual-testing selenium cypress quality-assurance unit-test jmeter postman appium",
    "IT Support & Networking":"helpdesk system-admin cisco network-protocol windows-server virtualization vlan active-directory routing dns dhcp",
}

CONCEPT_TO_CATEGORY = {
    "python":             ["Data Science & AI", "Web Development", "Data Engineering", "Cloud & DevOps"],
    "javascript":         ["Web Development", "Mobile Development", "Software Testing / QA"],
    "typescript":         ["Web Development", "Mobile Development"],
    "java":               ["Web Development", "Mobile Development", "Data Engineering", "Software Testing / QA"],
    "csharp":             ["Game Development", "Web Development"],
    "cplusplus":          ["Game Development", "Embedded Systems / IoT"],
    "c":                  ["Embedded Systems / IoT"],
    "php":                ["Web Development"],
    "go":                 ["Cloud & DevOps", "Web Development", "Data Engineering"],
    "rust":               ["Web Development", "Embedded Systems / IoT", "Data Engineering"],
    "swift":              ["Mobile Development"],
    "kotlin":             ["Mobile Development"],
    "sql":                ["Data Engineering", "Data Science & AI", "Web Development"],
    "machine-learning":   ["Data Science & AI"],
    "deep-learning":      ["Data Science & AI"],
    "cnn":                ["Data Science & AI"],
    "rnn":                ["Data Science & AI"],
    "transformers":       ["Data Science & AI"],
    "nlp":                ["Data Science & AI"],
    "tensorflow":         ["Data Science & AI"],
    "pytorch":            ["Data Science & AI"],
    "sagemaker":          ["Data Science & AI"],
    "azure-ml":           ["Data Science & AI"],
    "tensorrt":           ["Data Science & AI"],
    "onnx":               ["Data Science & AI"],
    "opencv":             ["Data Science & AI"],
    "pandas":             ["Data Science & AI", "Data Engineering"],
    "scikit-learn":       ["Data Science & AI"],
    "tableau":            ["Data Science & AI"],
    "power-bi":           ["Data Science & AI"],
    "spark":              ["Data Engineering"],
    "hadoop":             ["Data Engineering"],
    "kafka":              ["Data Engineering"],
    "airflow":            ["Data Engineering"],
    "dbt":                ["Data Engineering"],
    "snowflake":          ["Data Engineering"],
    "redshift":           ["Data Engineering"],
    "nosql":              ["Data Engineering", "Web Development"],
    "mongodb":            ["Web Development", "Data Engineering"],
    "postgresql":         ["Web Development", "Data Engineering"],
    "docker":             ["Cloud & DevOps", "Data Science & AI", "Web Development"],
    "kubernetes":         ["Cloud & DevOps"],
    "aws":                ["Cloud & DevOps"],
    "azure":              ["Cloud & DevOps"],
    "google-cloud":       ["Cloud & DevOps"],
    "terraform":          ["Cloud & DevOps"],
    "jenkins":            ["Cloud & DevOps"],
    "ansible":            ["Cloud & DevOps"],
    "linux":              ["Cloud & DevOps", "Embedded Systems / IoT", "IT Support & Networking"],
    "git":                ["Web Development", "Mobile Development", "Data Engineering", "Cloud & DevOps"],
    "wireshark":          ["Cybersecurity", "IT Support & Networking"],
    "metasploit":         ["Cybersecurity"],
    "nmap":               ["Cybersecurity"],
    "firewall":           ["Cybersecurity", "IT Support & Networking"],
    "owasp":              ["Cybersecurity"],
    "penetration-tester": ["Cybersecurity"],
    "selenium":           ["Software Testing / QA"],
    "cypress":            ["Software Testing / QA"],
    "postman":            ["Software Testing / QA", "Web Development"],
    "jmeter":             ["Software Testing / QA"],
    "unity":              ["Game Development"],
    "unreal-engine":      ["Game Development"],
    "arduino":            ["Embedded Systems / IoT"],
    "raspberry-pi":       ["Embedded Systems / IoT"],
    "active-directory":   ["IT Support & Networking"],
    "cisco":              ["IT Support & Networking"],
}

_CAT_NAMES  = list(CATEGORIES.keys())
_CAT_DESCS  = list(CATEGORIES.values())


# ─── Cache category embeddings (tính 1 lần, dùng mãi mãi) ───────────────────

@st.cache_resource(show_spinner=False)
def _get_cat_vecs() -> np.ndarray:
    """Embed category descriptions 1 lần, cache vĩnh viễn."""
    return embed_batch(_CAT_DESCS)   # shape: (num_cats, embed_dim)


# ─── Helpers ─────────────────────────────────────────────────────────────────

def extract_concepts(cv_text: str) -> list:
    text = cv_text.lower()
    return [k for k in CONCEPT_TO_CATEGORY
            if re.search(r'\b' + re.escape(k) + r'\b', text)]


def _infer_candidate_indices(concepts: list) -> list:
    """Trả về index trong _CAT_NAMES thay vì tên string."""
    cats = set()
    for c in concepts:
        for cat in CONCEPT_TO_CATEGORY.get(c, []):
            if cat in _CAT_NAMES:
                cats.add(_CAT_NAMES.index(cat))
    return list(cats)


# ─── Batch classify (API mới, dùng trong app.py) ─────────────────────────────

def classify_cv_batch(cv_texts: list) -> list:
    """
    Classify nhiều CV cùng lúc.
    Trả về list[dict] theo đúng thứ tự đầu vào.

    Ưu điểm:
      - embed_batch() 1 lần cho toàn bộ CV
      - category embeddings được cache sẵn
      - cosine_similarity tính trên numpy arrays → nhanh
    """
    if not cv_texts:
        return []

    cat_vecs = _get_cat_vecs()               # (num_cats, dim)
    cv_vecs  = embed_batch(cv_texts)         # (num_cvs, dim)  – 1 lần duy nhất

    # Ma trận similarity: (num_cvs, num_cats)
    all_sims = cosine_similarity(cv_vecs, cat_vecs)

    results = []
    for i, cv_text in enumerate(cv_texts):
        concepts       = extract_concepts(cv_text)
        cand_indices   = _infer_candidate_indices(concepts)

        if not cand_indices:
            results.append({"category": "Other", "confidence": 0,
                            "concepts": [], "all_scores": {}})
            continue

        # Chỉ xét các category ứng viên
        row    = all_sims[i]                 # (num_cats,)
        scores = {_CAT_NAMES[j]: float(row[j]) for j in cand_indices}
        best   = max(scores, key=scores.get)

        results.append({
            "concepts":   concepts,
            "category":   best,
            "confidence": round(scores[best] * 100),
            "all_scores": scores,
        })

    return results


# ─── Single-CV wrapper (giữ nguyên API cũ) ───────────────────────────────────

def classify_cv(cv_text: str) -> dict:
    return classify_cv_batch([cv_text])[0]