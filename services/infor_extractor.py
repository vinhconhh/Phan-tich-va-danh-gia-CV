import re
import unicodedata

SKILL_DB = [
    "python", "java", "sql", "docker", "aws", "tensorflow", "pytorch",
    "react", "node", "linux", "git", "kubernetes", "excel", "power bi",
    "spark", "kafka", "airflow", "mongodb", "postgresql", "redis",
    "fastapi", "flask", "django", "c++", "c#", "golang", "rust"
]

SECTION_MAP = [
    ("work experience",          "experience"),
    ("kinh nghiệm làm việc",     "experience"),
    ("kinh nghiem lam viec",     "experience"),
    ("kinh nghiệm",              "experience"),
    ("kinh nghiem",              "experience"),
    ("experience",               "experience"),
    ("trình độ học vấn",         "education"),
    ("trinh do hoc van",         "education"),
    ("học vấn",                  "education"),
    ("hoc van",                  "education"),
    ("education",                "education"),
    ("technical skills",         "skills"),
    ("công nghệ sử dụng",        "skills"),
    ("kỹ năng",                  "skills"),
    ("ky nang",                  "skills"),
    ("skills",                   "skills"),
    ("dự án",                    "projects"),
    ("du an",                    "projects"),
    ("projects",                 "projects"),
    ("tóm tắt",                  "summary"),
    ("mục tiêu",                 "summary"),
    ("summary",                  "summary"),
    ("objective",                "summary"),
    ("certifications",           "ignore"),
    ("chứng chỉ",                "ignore"),
    ("chung chi",                "ignore"),
    ("honors",                   "ignore"),
    ("danh hiệu",                "ignore"),
    ("awards",                   "ignore"),
    ("activities",               "ignore"),
    ("hoạt động",                "ignore"),
    ("references",               "ignore"),
    ("người giới thiệu",         "ignore"),
    ("nguoi gioi thieu",         "ignore"),
    ("interests",                "ignore"),
    ("sở thích",                 "ignore"),
    ("so thich",                 "ignore"),
    ("languages",                "ignore"),
    ("ngôn ngữ",                 "ignore"),
]


FORBIDDEN_NAMES = {
    "học vấn", "education", "kinh nghiệm", "experience",
    "kỹ năng", "skills", "dự án", "projects", "tóm tắt", "summary",
    "gmail", "email", "phone", "điện thoại", "họ tên", "họ và tên",
    "thông tin", "cá nhân", "personal", "profile", "objective",
    "chuyên ngành", "nghề thông tin", "nghệ thông tin",
}

NOISE_PATTERNS = [
    r"^[^a-zA-ZÀ-ỹ0-9]{3,}$",
    r"^\s*[\|\-\_\=\.]{2,}\s*$",
    r"^\s*\d{1,2}\s*$",
    r"^.{0,2}$",
]

def is_noise(line: str) -> bool:
    return any(re.match(p, line.strip()) for p in NOISE_PATTERNS)

def is_email_line(line: str) -> bool:
    return bool(re.search(r"[a-z0-9._%+\-]+@[a-z0-9.\-]+\.[a-z]{2,}", line.lower()))

def is_phone_line(line: str) -> bool:
    c = re.sub(r"[\s\.\-]", "", line)
    return bool(re.search(r"(\+84|0)(3[2-9]|5[25689]|7\d|8[0-9]|9[0-9])\d{6,7}", c))

def is_date_line(line: str) -> bool:
    return bool(re.match(r"^\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{4}$", line.strip()))

def detect_section(line: str):
    ll = unicodedata.normalize("NFC", line).lower().strip().rstrip(":")
    for keyword, section in SECTION_MAP:
        if ll == keyword or ll.startswith(keyword):
            return section
    return None

def parse_sections(raw_text: str) -> dict:
    text = unicodedata.normalize("NFC", raw_text)
    text = re.sub(r"[•●▪►▶✓✔]", "-", text)
    text = re.sub(r"\r\n|\r", "\n", text)

    sections = {"header": [], "experience": [], "education": [], "ignore": [],
                "skills": [], "projects": [], "summary": []}
    current = "header"

    for line in text.split("\n"):
        line = re.sub(r"\s+", " ", line).strip()
        if not line or is_noise(line):
            continue
        sec = detect_section(line)
        if sec:
            current = sec
            continue
        if current == "experience" and (is_email_line(line) or is_date_line(line)):
            continue
        sections[current].append(line)

    return sections

# ── Tên ──
def extract_name(raw_text: str) -> str:
    lines = raw_text.split("\n")[:20]

    for line in lines:
        m = re.match(
            r"^(họ\s*(?:và\s*)?tên|full\s*name|name)\s*[:\-]\s*(.+)$",
            line.strip(), re.IGNORECASE | re.UNICODE
        )
        if m:
            candidate = m.group(2).strip()
            if candidate and candidate.lower() not in FORBIDDEN_NAMES:
                return candidate

    for i, line in enumerate(lines):
        if re.match(r"^(họ\s*(?:và\s*)?tên|full\s*name|name)\s*[:\-]?\s*$",
                    line.strip(), re.IGNORECASE):
            for j in range(i + 1, min(i + 4, len(lines))):
                c = lines[j].strip()
                if (c and c.lower() not in FORBIDDEN_NAMES
                        and not is_email_line(c) and not is_phone_line(c)):
                    return c

    for line in lines:
        line = line.strip()
        if any(fw in line.lower() for fw in FORBIDDEN_NAMES):
            continue
        words = line.split()
        if (2 <= len(words) <= 5
                and len(line) < 50
                and "@" not in line
                and "http" not in line.lower()
                and not re.search(r"\d{3,}", line)
                and re.match(r"^[A-ZÀ-Ỵa-zà-ỵ\s]+$", line)
                and re.search(r"[A-ZÀ-Ỵ]", line)):
            line = re.sub(r"\s+[A-ZÀ-Ỵ]$", "", line).strip()
            return line

    return "N/A"

# ── Email ──
def extract_email(raw_text: str) -> str:
    m = re.search(r"[a-z0-9._%+\-]+@[a-z0-9.\-]+\.[a-z]{2,}", raw_text.lower())
    return m.group(0) if m else "N/A"

# ── Phone: FIX regex bao phủ đủ đầu số VN ──
def extract_phone(raw_text: str) -> str:
    cleaned = re.sub(r"[\s\.\-]", "", raw_text)
    # 7\d bao phủ 070-079 thay vì chỉ 7[06-9]
    m = re.search(
        r"(\+84|0)(3[2-9]|5[25689]|7\d|8[0-9]|9[0-9])\d{6,7}",
        cleaned
    )
    return m.group(0) if m else "N/A"

# ── Skills ──
def extract_skills(raw_text: str) -> list:
    t = unicodedata.normalize("NFC", raw_text).lower()
    return sorted({s for s in SKILL_DB if s in t})
_HEADING_END_RE = re.compile(
    r'(\d{4}\s*[-]\s*(\d{4}|nay|present|hien\s*tai|hi\u1ec7n\s*t\u1ea1i)|'
    r'\d{2}[/]\d{4}\s*[-]\s*(\d{2}[/]\d{4}|hi\u1ec7n\s*t\u1ea1i|present|nay))\s*$',
    re.IGNORECASE
)
_CONTINUATION_RE = re.compile(
    r'^([a-z\u00e0-\u1ef9%\(\[\{\d]|HTML|CSS|API|SDK|SQL|ETL|ELT|AWS|GCP|EC2|SLA|KPI|DAG|URL|DynamoDB|ML|Hive|Redis|Kafka|Spark|Airflow|Docker|GitFlow|Analytics|Associate|Azure|Google|Microsoft)'
)

def merge_wrapped_lines(lines):
    if not lines:
        return lines
    merged = [lines[0]]
    for line in lines[1:]:
        prev = merged[-1]
        if _HEADING_END_RE.search(prev):
            merged.append(line)
            continue
        prev_complete = bool(re.search(r'[.!?;]\s*$', prev))
        curr_fragment = bool(_CONTINUATION_RE.match(line))
        prev_ends_arrow = bool(re.search(r'\u2192\s*$', prev))
        if (not prev_complete or prev_ends_arrow) and curr_fragment:
            merged[-1] = prev.rstrip() + ' ' + line.lstrip()
        else:
            merged.append(line)
    return merged

def clean_lines(lines: list, min_len: int = 5, max_len: int = 300) -> list:
    result = []
    for line in lines:
        line = line.strip(" -–•")
        if line.startswith("©") or "topcv.vn" in line.lower():
            continue
        if (min_len <= len(line) <= max_len
                and not is_noise(line)
                and not is_email_line(line)
                and not is_date_line(line)):
            result.append(line)
    return merge_wrapped_lines(result)

def extract_info(raw_text: str) -> dict:
    sections = parse_sections(raw_text)
    return {
        "name":       extract_name(raw_text),
        "email":      extract_email(raw_text),
        "phone":      extract_phone(raw_text),
        "skills":     extract_skills(raw_text),
        "experience": clean_lines(sections["experience"]),
        "education":  clean_lines(sections["education"]),
    }