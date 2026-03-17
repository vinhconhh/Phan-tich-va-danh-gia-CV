TÊN SẢN PHẨM: Hệ thống phân tích và đánh giá CV bằng AI

HƯỚNG DẪN CÀI ĐẶT VÀ CHẠY:

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

CẤU TRÚC THƯ MỤC:
   app.py                  - Giao diện chính Streamlit
   services/
     extractor.py          - Trích xuất text từ PDF/DOCX (pdfplumber + OCR fallback)
     infor_extractor.py    - Trích xuất thông tin (tên, email, SĐT, kỹ năng...)
     classifier.py         - Phân loại CV theo lĩnh vực IT (SBERT)
     matcher.py            - So khớp CV với Job Description (SBERT cosine similarity)
     score.py              - Chấm điểm CV
     embedding.py          - Mô hình SBERT (multilingual-e5-base)
     suggestion.py         - Gợi ý cải thiện CV

MÔ TẢ TÍNH NĂNG:
   - Phân loại CV theo 10 lĩnh vực IT (Web, AI, DevOps, Cybersecurity...)
   - Trích xuất thông tin: tên, email, SĐT, học vấn, kinh nghiệm, kỹ năng
   - So khớp CV với Job Description bằng SBERT (multilingual)
   - Chấm điểm CV theo 5 tiêu chí: kỹ năng, kinh nghiệm, học vấn, độ dài, từ khoá
   - Xuất kết quả ra file Excel (.xlsx)
   - Hỗ trợ upload nhiều CV cùng lúc (PDF, DOCX)

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

LƯU Ý:
   - Lần đầu chạy sẽ tải mô hình SBERT (~1GB), cần kết nối internet
   - PDF dạng scan sẽ chậm hơn do phải qua OCR
   - Khuyến nghị dùng GPU để tăng tốc (tự động detect)