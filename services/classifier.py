import re
from services.embedding import embed_text
from sklearn.metrics.pairwise import cosine_similarity

# taxonomy mô tả ngành
CATEGORIES = {
    "Web Development": "frontend backend fullstack javascript react nodejs html css typescript flask django express nextjs bootstrap tailwind",
    "Mobile Development": "ios android react-native flutter swift kotlin objective-c dart jetpack-compose",
    "Data Engineering": "data-pipeline sql spark hadoop etl warehouse airflow kafka dbt redshift snowflake bigquery databricks hive",
    "Data Science & AI": "machine-learning deep-learning ai-engineer cnn rnn transformers nlp computer-vision tensorflow pytorch sagemaker azure-ml tensorrt onnx opencv scikit-learn pandas numpy",
    "Cybersecurity": "pentest security ethical-hacking firewall cryptography network-security soc malware-analysis owasp siem vulnerability penetration-tester",
    "Cloud & DevOps": "kubernetes jenkins terraform ansible cicd infrastructure-as-code monitoring logging bash-scripting automation aws azure google-cloud docker ec2",
    "Game Development": "unity unreal-engine csharp game-design graphics-programming directx opengl shader cplusplus",
    "Embedded Systems / IoT": "c firmware microcontroller hardware raspberry-pi arduino embedded-linux rtos assembly fpga arm",
    "Software Testing / QA": "automation-testing manual-testing selenium cypress quality-assurance unit-test jmeter postman appium",
    "IT Support & Networking": "helpdesk system-admin cisco network-protocol windows-server virtualization vlan active-directory routing dns dhcp"
}

# mapping concept → ngành
CONCEPT_TO_CATEGORY = {
    # --- Ngôn ngữ lập trình (Programming Languages) ---
    "python": ["Data Science & AI", "Web Development", "Data Engineering", "Cloud & DevOps"],
    "javascript": ["Web Development", "Mobile Development", "Software Testing / QA"],
    "typescript": ["Web Development", "Mobile Development"],
    "java": ["Web Development", "Mobile Development", "Data Engineering", "Software Testing / QA"],
    "csharp": ["Game Development", "Web Development"],
    "cplusplus": ["Game Development", "Embedded Systems / IoT"],
    "c": ["Embedded Systems / IoT"],
    "php": ["Web Development"],
    "go": ["Cloud & DevOps", "Web Development", "Data Engineering"],
    "rust": ["Web Development", "Embedded Systems / IoT", "Data Engineering"],
    "swift": ["Mobile Development"],
    "kotlin": ["Mobile Development"],
    "sql": ["Data Engineering", "Data Science & AI", "Web Development"],

    # --- Trí tuệ nhân tạo & Khoa học dữ liệu (Data Science & AI) ---
    "machine-learning": ["Data Science & AI"],
    "deep-learning": ["Data Science & AI"],
    "cnn": ["Data Science & AI"],
    "rnn": ["Data Science & AI"],
    "transformers": ["Data Science & AI"],
    "nlp": ["Data Science & AI"],
    "tensorflow": ["Data Science & AI"],
    "pytorch": ["Data Science & AI"],
    "sagemaker": ["Data Science & AI"], # Công cụ AI trên Cloud
    "azure-ml": ["Data Science & AI"],  # Công cụ AI trên Cloud
    "tensorrt": ["Data Science & AI"],  # Tối ưu hóa AI
    "onnx": ["Data Science & AI"],      # Định dạng AI
    "opencv": ["Data Science & AI"],
    "pandas": ["Data Science & AI", "Data Engineering"],
    "scikit-learn": ["Data Science & AI"],
    "tableau": ["Data Science & AI"],
    "power-bi": ["Data Science & AI"],

    # --- Kỹ thuật dữ liệu (Data Engineering) ---
    "spark": ["Data Engineering"],
    "hadoop": ["Data Engineering"],
    "kafka": ["Data Engineering"],
    "airflow": ["Data Engineering"],
    "dbt": ["Data Engineering"],
    "snowflake": ["Data Engineering"],
    "redshift": ["Data Engineering"],
    "nosql": ["Data Engineering", "Web Development"],
    "mongodb": ["Web Development", "Data Engineering"],
    "postgresql": ["Web Development", "Data Engineering"],

    # --- Hạ tầng & Vận hành (Cloud & DevOps) ---
    "docker": ["Cloud & DevOps", "Data Science & AI", "Web Development"],
    "kubernetes": ["Cloud & DevOps"],
    "aws": ["Cloud & DevOps"],
    "azure": ["Cloud & DevOps"],
    "google-cloud": ["Cloud & DevOps"],
    "terraform": ["Cloud & DevOps"],
    "jenkins": ["Cloud & DevOps"],
    "ansible": ["Cloud & DevOps"],
    "linux": ["Cloud & DevOps", "Embedded Systems / IoT", "IT Support & Networking"],
    "git": ["Web Development", "Mobile Development", "Data Engineering", "Cloud & DevOps"],

    # --- Bảo mật (Cybersecurity) ---
    "wireshark": ["Cybersecurity", "IT Support & Networking"],
    "metasploit": ["Cybersecurity"],
    "nmap": ["Cybersecurity"],
    "firewall": ["Cybersecurity", "IT Support & Networking"],
    "owasp": ["Cybersecurity"],
    "penetration-tester": ["Cybersecurity"],

    # --- Kiểm thử (Software Testing / QA) ---
    "selenium": ["Software Testing / QA"],
    "cypress": ["Software Testing / QA"],
    "postman": ["Software Testing / QA", "Web Development"],
    "jmeter": ["Software Testing / QA"],

    # --- Khác (Game, IoT, Support) ---
    "unity": ["Game Development"],
    "unreal-engine": ["Game Development"],
    "arduino": ["Embedded Systems / IoT"],
    "raspberry-pi": ["Embedded Systems / IoT"],
    "active-directory": ["IT Support & Networking"],
    "cisco": ["IT Support & Networking"]
}


def extract_concepts(cv_text):
    text = cv_text.lower()
    concepts = []

    # Sử dụng ranh giới từ (\b) để tránh false positives
    for k in CONCEPT_TO_CATEGORY.keys():
        # Escape các ký tự đặc biệt nếu có (như c++, c#)
        pattern = r'\b' + re.escape(k) + r'\b'
        if re.search(pattern, text):
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
        return {"category": "Other", "confidence": 0, "concepts": [], "all_scores": {}}

    cv_vec = embed_text(cv_text)
    scores = {}

    # Chỉ so khớp vector với các danh mục ứng viên đã được bóc tách từ CV
    for cat in candidate_cats:
        if cat in CATEGORIES:
            desc = CATEGORIES[cat]
            cat_vec = embed_text(desc)
            sim = cosine_similarity([cv_vec], [cat_vec])[0][0]
            scores[cat] = float(sim)

    if not scores:
        return {"category": "Other", "confidence": 0, "concepts": concepts, "all_scores": {}}

    best_cat = max(scores, key=scores.get)

    # all_scores lúc này chỉ chứa các danh mục xuất hiện trong CV
    return {
        "concepts": concepts,
        "category": best_cat,
        "confidence": round(scores[best_cat] * 100),
        "all_scores": scores
    }

