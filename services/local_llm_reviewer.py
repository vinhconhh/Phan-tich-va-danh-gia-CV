from llama_cpp import Llama
import os
import streamlit as st
import torch  # Thêm thư viện này để kiểm tra phần cứng

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "gemma-3-4b-it-Q4_K_M.gguf"
)

@st.cache_resource(show_spinner=False)
def _load_llm() -> Llama:
    """Load model 1 lần duy nhất, tự động thích ứng với phần cứng."""

    # 1. Tự động phát hiện GPU có khả dụng hay không
    has_gpu = torch.cuda.is_available()

    # 2. Nếu có GPU -> Đẩy 100% model lên GPU (-1). Nếu không -> Chạy 100% trên CPU (0)
    gpu_layers = -1 if has_gpu else 0

    # 3. Quản lý luồng CPU:
    # Nếu GPU đã gánh hết tính toán, CPU chỉ cần 1-2 luồng để "chỉ đạo".
    # Nếu không có GPU, bung toàn bộ sức mạnh của CPU để xử lý.
    threads = 2 if has_gpu else (os.cpu_count() or 8)

    return Llama(
        model_path=MODEL_PATH,
        n_ctx=4096,
        n_threads=threads,
        n_gpu_layers=gpu_layers,
        n_batch=512,
        use_mmap=True,
        use_mlock=False,
        verbose=False,
    )


def review_cv_with_local_llm(
    cv_text: str,
    score_result: dict,
    extract_result: dict,
    classify_result: dict,
    jd_text: str,
) -> str:
    llm = _load_llm()

    # Cắt CV để tránh vượt context window
    cv_snippet = cv_text[:1800].strip()

    # Tóm gọn thông tin đầu vào
    skills     = ", ".join(extract_result.get("skills", [])[:15]) or "N/A"
    exp_lines  = "; ".join(extract_result.get("experience", [])[:4]) or "N/A"
    edu_lines  = "; ".join(extract_result.get("education", [])[:3]) or "N/A"
    category   = classify_result.get("category", "N/A")
    confidence = classify_result.get("confidence", 0)
    total      = score_result.get("total_score", 0)
    bd         = score_result.get("breakdown", {})

    jd_snippet = (jd_text or "")[:500].strip() or "Không có JD"

    prompt = f"""Bạn là HR chuyên nghiệp. Đánh giá CV ngắn gọn, súc tích.

## Tổng điểm: {total}/100
Breakdown – Kỹ năng: {round(bd.get('skills',0)*30)}/30 | Kinh nghiệm: {round(bd.get('experience',0)*30)}/30 | Học vấn: {round(bd.get('education',0)*15)}/15 | Keywords: {round(bd.get('keywords',0)*15)}/15 | Độ dài: {round(bd.get('length',0)*10)}/10

## Phân loại: {category} ({confidence}%)
## Kỹ năng: {skills}
## Kinh nghiệm: {exp_lines}
## Học vấn: {edu_lines}

## JD (tóm tắt):
{jd_snippet}

## Trích đoạn CV:
{cv_snippet}

---
Hãy trả lời theo cấu trúc:
**Điểm mạnh:** (2-3 điểm)
**Điểm yếu:** (2-3 điểm)
**Gợi ý cải thiện:** (2-3 điểm)
**Mức độ phù hợp JD:** (1 câu tóm tắt)
"""

    response = llm.create_chat_completion(
        messages=[
            {
                "role": "system",
                "content": "Bạn là phần mềm trích xuất dữ liệu tuyển dụng IT. Tuân thủ tuyệt đối cấu trúc được giao. KHÔNG ĐƯỢC CHÀO HỎI. KHÔNG DÙNG LỜI DẪN (như 'Dưới đây là...', 'Tuyệt vời'). Bắt đầu câu trả lời trực tiếp vào nội dung."
            },
            {
                "role": "user",
                "content": prompt + "\n\nLưu ý quan trọng: Bắt đầu ngay lập tức bằng '**Điểm mạnh:**'. Không in ra bất kỳ từ nào trước đó."
            },
        ],
        temperature=0.1,
        max_tokens=600,
    )

    return response["choices"][0]["message"]["content"]