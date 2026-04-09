Bước 1: Tải mô hình AI (BẮT BUỘC)
Truy cập link: https://huggingface.co/bartowski/google_gemma-3-4b-it-GGUF/blob/main/google_gemma-3-4b-it-Q4_K_M.gguf

Tải file google_gemma-3-4b-it-Q4_K_M.gguf về máy.

Chép file vừa tải vào thư mục: services/ (Lưu ý: Giữ đúng tên file để ứng dụng nhận diện).

CÁCH 1: Sử dụng script tự động (Khuyên dùng)
Đảm bảo đã cài Python 3.10+ (Tick vào ô "Add Python to PATH").
Chạy file setup.bat -> Chờ cài đặt môi trường ảo và thư viện (5-15 phút).
Sau khi chạy xong cài môi trường C++ qua vsBuildtool và chạy lại file setup.bat.
Chạy file run.bat -> Ứng dụng sẽ tự động khởi chạy trên trình duyệt.

CÁCH 2: Cài đặt thủ công
Cài Poppler (Để đọc PDF): https://github.com/oschwartz10612/poppler-windows/releases/tag/v25.12.0-0
Windows: Giải nén Poppler và thêm thư mục Library\bin vào PATH hệ thống.
Tạo môi trường ảo và cài thư viện:
Bash
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt

Chạy ứng dụng:
Bash
streamlit run app.py
HƯỚNG DẪN SỬ DỤNG:
Khởi động: Mở ứng dụng, hệ thống sẽ tự động load mô hình SBERT và Gemma 3.
Upload: Kéo thả CV (PDF/DOCX) vào vùng upload (hỗ trợ nhiều file cùng lúc).
Phân tích: Nhấn "Phân Tích CV" -> Xem kết quả tại các Tab: Thông tin, So khớp, Chấm điểm.
Đánh giá AI: Tại Tab 4 "Đánh giá", nhấn "Xem đánh giá AI". Hệ thống sẽ dùng mô hình Gemma 3 chạy trực tiếp trên máy bạn để nhận xét ưu/nhược điểm của ứng viên.

CẤU TRÚC THƯ MỤC:
app.py : Giao diện chính Streamlit.
setup.bat / run.bat : Script tự động hóa.
services/ : Thư mục chứa các module xử lý chính.
extractor.py : Trích xuất văn bản từ PDF/DOCX.
infor_extractor.py : Trích xuất thông tin thực thể (tên, kỹ năng...).
classifier.py : Phân loại ngành nghề IT (SBERT).
matcher.py : So khớp CV với JD (Cosine Similarity).
local_llm_reviewer.py : Đánh giá CV bằng mô hình Gemma 3.
google_gemma-3-4b-it-Q4_K_M.gguf : (File mô hình AI - Cần tải về).
poppler-25.12.0/ : Thư viện hỗ trợ xử lý file PDF.

MÔ TẢ TÍNH NĂNG:
Phân loại: Tự động xếp CV vào các nhóm (Web, AI, Mobile, DevOps...).
Trích xuất: Nhận diện thông tin cá nhân và bộ kỹ năng cứng/mềm.
So khớp: Tính toán mức độ phù hợp (%) giữa ứng viên và mô tả công việc.
Chấm điểm: Đánh giá dựa trên 5 tiêu chí định lượng.
Review AI Local: Nhận xét chi tiết bằng ngôn ngữ tự nhiên thông qua Gemma 3 (Không cần Internet, không cần API Key).
Xuất dữ liệu: Hỗ trợ xuất báo cáo tổng hợp ra file Excel.

THƯ VIỆN CHÍNH:
streamlit : Giao diện người dùng.
llama-cpp-python : Thư viện để chạy mô hình GGUF (Gemma 3).
sentence-transformers : Mô hình SBERT Embedding.
pdfplumber, python-docx : Đọc dữ liệu văn bản.
torch, numpy : Xử lý tính toán vector.

LƯU Ý:
Phần cứng: Khuyến nghị máy tính có ít nhất 8GB RAM và có GPU NVIDIA (nếu muốn AI phản hồi nhanh).
Internet: Chỉ cần thiết để tải thư viện lần đầu. Sau khi đã có file .gguf, ứng dụng có thể chạy Offline 100%.
Tính bảo mật: Toàn bộ quá trình phân tích diễn ra trên máy cá nhân, không có dữ liệu nào bị gửi lên Cloud.
