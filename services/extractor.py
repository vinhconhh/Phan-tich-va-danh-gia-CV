import os
import io
import docx
import numpy as np
import pdfplumber

# ── Tỉ lệ cột trái (sidebar) của template TopCV / các CV 2 cột phổ biến ──
LEFT_COL_RATIO = 0.33


def _extract_pdf_native(file_bytes: bytes) -> str:
    pages_text = []
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            w, h = page.width, page.height

            # Thử tách 2 cột
            left_page  = page.crop((0,          0, w * LEFT_COL_RATIO, h))
            right_page = page.crop((w * LEFT_COL_RATIO, 0, w,          h))

            left_text  = left_page.extract_text()  or ""
            right_text = right_page.extract_text() or ""

            # Nếu cả 2 cột đều có nội dung → PDF 2 cột
            if len(left_text.strip()) > 30 and len(right_text.strip()) > 30:
                pages_text.append(left_text + "\n" + right_text)
            else:
                # PDF 1 cột → đọc toàn trang
                full = page.extract_text() or ""
                pages_text.append(full)

    return "\n\n".join(pages_text)


def _extract_pdf_ocr(file_bytes: bytes) -> str:
    """Fallback: OCR cho PDF scan (không có embedded text)."""
    from pdf2image import convert_from_bytes
    import easyocr, torch

    poppler_path = os.environ.get("POPPLER_PATH", None)
    images = convert_from_bytes(file_bytes, poppler_path=poppler_path)

    gpu = torch.cuda.is_available()
    reader = easyocr.Reader(['vi', 'en'], gpu=gpu)
    full_text = []
    for img in images:
        img_np = np.array(img)
        results = reader.readtext(img_np)
        results.sort(key=lambda x: (x[0][0][1], x[0][0][0]))
        full_text.extend(t for (_, t, p) in results if p > 0.3)
    return "\n".join(full_text)


def ocr_pdf(file) -> str:
    file_bytes = file.read()
    text = _extract_pdf_native(file_bytes)
    # Nếu text quá ít → PDF scan → dùng OCR
    if len(text.strip()) < 100:
        text = _extract_pdf_ocr(file_bytes)
    return text


def extract_text_from_docx(file) -> str:
    doc = docx.Document(file)
    return "\n".join(p.text for p in doc.paragraphs if p.text.strip())


def extract_text(file) -> str:
    name = file.name.lower()
    if name.endswith(".pdf"):
        file.seek(0)
        return ocr_pdf(file)
    elif name.endswith((".docx", ".doc")):
        return extract_text_from_docx(file)
    else:
        return file.read().decode("utf-8")