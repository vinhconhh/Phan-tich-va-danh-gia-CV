import re

def extract_email(text):
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    res = re.findall(pattern, text)
    return res[0] if res else "N/A"

def extract_phone(text):
    pattern = r'(\+84|0)[0-9]{9,10}'
    res = re.findall(pattern, text)
    return res[0] if res else "N/A"

def extract_skills(text):
    skills = ["python","java","sql","docker","aws","react","ml","ai"]
    found = []
    text_lower = text.lower()
    for s in skills:
        if s in text_lower:
            found.append(s)
    return found

def extract_education(text):
    edu_keywords = ["bachelor", "master", "phd", "đại học", "cao đẳng", "university"]
    lines = text.split("\n")
    result = []
    for line in lines:
        if any(k in line.lower() for k in edu_keywords):
            result.append(line.strip())
    return result

def extract_experience(text):
    exp_keywords = ["experience", "worked", "company", "project", "kinh nghiệm"]
    lines = text.split("\n")
    result = []
    for line in lines:
        if any(k in line.lower() for k in exp_keywords):
            result.append(line.strip())
    return result

def extract_info(text):
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    name = lines[0] if lines else "N/A"

    return {
        "name": name,
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text),
        "education": extract_education(text),     # BẮT BUỘC
        "experience": extract_experience(text)    # BẮT BUỘC
    }
