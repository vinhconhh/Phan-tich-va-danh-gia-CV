TÊN SẢN PHẨM: Hệ thống phân tích và đánh giá CV bằng AI

HƯỚNG DẪN CÀI ĐẶT VÀ CHẠY:

  CÁCH 1: Sử dụng script tự động (khuyên dùng)
  ─────────────────────────────────────────────
  1. Đảm bảo đã cài Python 3.10+ (tick "Add Python to PATH")
  2. Double-click "setup.bat" → chờ cài đặt tự động (5-15 phút lần đầu)
  3. Double-click "run.bat" → ứng dụng tự mở trên trình duyệt

  CÁCH 2: Cài thủ công
  ─────────────────────
  1. Cài Python 3.10.11

  2. Cài Poppler (cần thiết để đọc PDF):
     - Windows: Tải tại https://github.com/oschwartz10612/poppler-windows/releases
       Sau đó thêm thư mục bin vào PATH, hoặc set biến môi trường:
       POPPLER_PATH=D:\poppler\Library\bin
     - Linux/Mac: sudo apt install poppler-utils / brew install poppler

  3. Mở terminal tại thư mục project

  4. Cài thư viện:
     pip install -r requirements.txt

  5. Chạy ứng dụng:
     streamlit run app.py

  6. Mở trình duyệt tại:
     http://localhost:8501

HƯỚNG DẪN SỬ DỤNG GEMINI AI:
  1. Lấy API Key miễn phí tại: https://aistudio.google.com/apikey
  2. Mở ứng dụng → nhập API Key vào ô bên sidebar trái
  3. Upload CV → Nhấn "Phân Tích CV" → Vào Tab 4 "Đánh giá"
  4. Nhấn "Xem đánh giá AI" cho từng CV để xem kết quả

CẤU TRÚC THƯ MỤC:
   app.py                  - Giao diện chính Streamlit
   setup.bat               - Script cài đặt tự động
   run.bat                 - Script chạy ứng dụng
   services/
     extractor.py          - Trích xuất text từ PDF/DOCX (pdfplumber + OCR fallback)
     infor_extractor.py    - Trích xuất thông tin (tên, email, SĐT, kỹ năng...)
     classifier.py         - Phân loại CV theo lĩnh vực IT (SBERT)
     matcher.py            - So khớp CV với Job Description (SBERT cosine similarity)
     score.py              - Chấm điểm CV
     embedding.py          - Mô hình SBERT (multilingual-e5-base)
     gemini_reviewer.py    - Đánh giá tính khách quan bằng Gemini AI

MÔ TẢ TÍNH NĂNG:
   - Phân loại CV theo 10 lĩnh vực IT (Web, AI, DevOps, Cybersecurity...)
   - Trích xuất thông tin: tên, email, SĐT, học vấn, kinh nghiệm, kỹ năng
   - So khớp CV với Job Description bằng SBERT (multilingual)
   - Chấm điểm CV theo 5 tiêu chí: kỹ năng, kinh nghiệm, học vấn, độ dài, từ khoá
   - Đánh giá tính khách quan bằng Gemini AI (cần API Key + Internet)
   - Xuất kết quả ra file Excel (.xlsx)
   - Hỗ trợ upload nhiều CV cùng lúc (PDF, DOCX)
   - Đóng gói chạy offline (trừ tính năng Gemini AI)

THƯ VIỆN SỬ DỤNG:
   - streamlit            Giao diện web
   - sentence-transformers Mô hình SBERT embedding
   - scikit-learn         Cosine similarity
   - pdfplumber           Đọc PDF có embedded text
   - pdf2image + easyocr  OCR cho PDF scan
   - python-docx          Đọc file DOCX
   - numpy                Xử lý vector
   - openpyxl             Xuất Excel
   - torch                Backend cho SBERT
   - google-genai         Gọi Gemini AI API

LƯU Ý:
   - Lần đầu chạy sẽ tải mô hình SBERT (~1GB), cần kết nối internet
   - PDF dạng scan sẽ chậm hơn do phải qua OCR
   - Khuyến nghị dùng GPU để tăng tốc (tự động detect)
   - Gemini AI cần kết nối Internet, các tính năng khác chạy offline