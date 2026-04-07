@echo off
chcp 65001 >nul 2>&1
title Setup - He thong phan tich CV

echo ============================================
echo   CAI DAT HE THONG PHAN TICH VA DANH GIA CV
echo ============================================
echo.

:: --- PHẦN TÌM PYTHON (GIỮ NGUYÊN CỦA BẠN) ---
set "PYTHON_EXE="
where python >nul 2>&1
if not errorlevel 1 (
    set "PYTHON_EXE=python"
    goto :found_python
)
for %%d in (C D E) do (
    for %%p in (
        "%%d:\Python310\python.exe"
        "%%d:\Python\Python310\python.exe"
        "%%d:\Program Files\Python310\python.exe"
        "%%d:\Program Files (x86)\Python310\python.exe"
        "%%d:\Users\%USERNAME%\AppData\Local\Programs\Python\Python310\python.exe"
    ) do (
        if exist %%p (
            set "PYTHON_EXE=%%~p"
            goto :found_python
        )
    )
)
echo [CANH BAO] Khong tim thay Python tu dong!
set /p PYTHON_EXE="Nhap duong dan python.exe: "
if not exist "%PYTHON_EXE%" (
    echo [LOI] Khong tim thay file: %PYTHON_EXE%
    pause
    exit /b 1
)

:found_python
echo [INFO] Su dung Python tai: %PYTHON_EXE%
for /f "tokens=2 delims= " %%v in ('"%PYTHON_EXE%" --version 2^>^&1') do set PYVER=%%v
echo [INFO] Phien ban Python: %PYVER%
echo %PYTHON_EXE%> .python_path

:: --- BẮT ĐẦU CÀI ĐẶT ---

echo [1/5] Dang tao virtual environment...
if not exist ".venv" (
    "%PYTHON_EXE%" -m venv .venv
    echo       Da tao .venv thanh cong!
) else (
    echo       .venv da ton tai.
)

:: Kích hoạt môi trường ảo
call .venv\Scripts\activate.bat

echo [2/5] Dang cap nhat cong cu cai dat (Pip, Setuptools)...
python -m pip install --upgrade pip setuptools wheel --quiet

echo [3/5] Dang cai dat PyTorch va Llama-CPP (Ban Build san)...
:: Cài Torch bản CPU ổn định trước để tránh lỗi "No matching distribution"
pip install torch --extra-index-url https://download.pytorch.org/whl/cpu --quiet
:: Cài llama-cpp-python bản Pre-built để KHÔNG CẦN C++ Build Tools
pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu --quiet

echo [4/5] Dang cai dat cac thu vien con lai tu requirements.txt...
:: Lúc này requirements.txt sẽ chỉ cài các thư viện nhẹ (Streamlit, pdfplumber...)
pip install -r requirements.txt --quiet

echo [5/5] Dang tai mo hinh AI (SBERT multilingual-e5-base)...
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('intfloat/multilingual-e5-base'); print('      Da tai model SBERT thanh cong!')"

:: Kiem tra Poppler (Giữ nguyên)
echo.
if exist "poppler-25.12.0" (
    echo [INFO] Da phat hien Poppler.
) else (
    echo [CANH BAO] Khong tim thay poppler-25.12.0. Can thiet de doc PDF scan!
)

echo ============================================
echo   CAI DAT HOAN TAT!
echo   Chay "run.bat" de khoi dong ung dung.
echo ============================================
pause