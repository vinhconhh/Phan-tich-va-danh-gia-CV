import re
import unicodedata

def normalize_text(text):
    text = unicodedata.normalize("NFC", text)
    text = text.lower()

    # chỉ chuẩn hoá space trong mỗi dòng
    lines = [re.sub(r"\s+", " ", l).strip() for l in text.split("\n")]
    return "\n".join(lines)


    # ÉP NGẮT DÒNG NHÂN TẠO
    for k in ["kinh nghiệm", "học vấn", "education", "experience","kỹ năng", "skills", "objective", "mục tiêu"]: text = text.replace(k, "\n" + k + "\n")
    text = re.sub(r"\s+", " ", text)
    return text



def extract_section(text, start_keywords, stop_keywords):
    text = normalize_text(text)

    # CỰC KỲ QUAN TRỌNG: tách theo dòng, không phải theo từ
    lines = text.split("\n")

    result = []
    capture = False

    for line in lines:
        line = line.strip()

        if any(k in line for k in start_keywords):
            capture = True
            continue

        if capture and any(k in line for k in stop_keywords):
            break

        if capture and len(line) > 3:
            result.append(line)

    return result


def extract_name(text):
    lines = text.split("\n")[:5]
    for line in lines:
        if len(line.split()) >= 2 and len(line) < 40:
            return line.strip()
    return "N/A"


def extract_email(text):
    match = re.search(r"[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}", text.lower())
    return match.group(0) if match else "N/A"


def extract_phone(text):
    match = re.search(r"(0|\+84)\d{8,10}", text.replace(" ", ""))
    return match.group(0) if match else "N/A"


def extract_skills(text):
    SKILLS = ["python", "java", "sql", "docker", "aws", "ml", "ai", "javascript", "react", "node", "linux", "git"]
    text = normalize_text(text)
    found = []

    for skill in SKILLS:
        if skill in text:
            found.append(skill)

    return found


def extract_experience(text):
    return extract_section(
        text,
        start_keywords=["kinh nghiệm", "experience"],
        stop_keywords=["học vấn", "education", "kỹ năng", "skills"]
    )


def extract_education(text):
    return extract_section(
        text,
        start_keywords=["học vấn", "education", "trình độ"],
        stop_keywords=["kinh nghiệm", "experience", "kỹ năng", "skills"]
    )


def extract_info(text):
    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text),
        "experience": extract_experience(text),
        "education": extract_education(text)
    }
