@echo off
chcp 65001 >nul 2>&1
title Setup - He thong phan tich CV va Cai dat C++

echo ============================================
echo   CAI DAT HE THONG VA MOI TRUONG C++
echo ============================================
echo.

:: --- BUOC 0: CAI DAT TRINH BIEN DICH C++ (MOI BO SUNG) ---
echo [0/6] Kiem tra moi truong C++ (Build Tools)...
where cl >nul 2>&1
if %errorlevel% == 0 (
    echo [INFO] Da tim thay trinh bien dich C++.
) else (
    echo [INFO] Khong tim thay C++ Compiler. Bat dau tai va cai dat...
    echo [!] Qua trinh nay co the mat 10-15 phut tuy vao mang...

    :: Su dung PowerShell de tai va cai dat Build Tools rut gon qua Chocolatey (neu co)
    :: hoac tai truc tiep tu Microsoft.
    :: Duoi day la lenh tai goi Microsoft C++ Build Tools am tham (silent install):
    powershell -Command "Start-Process https://aka.ms/vs/17/release/vs_BuildTools.exe -ArgumentList '--add Microsoft.VisualStudio.Workload.VCTools --includeRecommended --passive --norestart' -Wait"

    echo [OK] Da gui lenh cai dat C++. Vui long doi den khi trinh cai dat bien mat.
)

set "PYTHON_EXE="
where python >nul 2>&1
if not errorlevel 1 (
    set "PYTHON_EXE=python"
    goto :found_python
)

:found_python
echo [INFO] Su dung Python tai: %PYTHON_EXE%
echo %PYTHON_EXE%> .python_path

:: --- BAT DAU CAI DAT CAC BUOC TIEP THEO ---

echo [1/6] Dang tao virtual environment...
if not exist ".venv" (
    "%PYTHON_EXE%" -m venv .venv
)
call .venv\Scripts\activate.bat

echo [2/6] Dang cap nhat cong cu cai dat...
python -m pip install --upgrade pip setuptools wheel --quiet

echo [3/6] Dang cai dat Llama-CPP va Torch...
nvidia-smi >nul 2>&1
if %errorlevel% == 0 (
    echo [INFO] Phat hien GPU. Cai ban ho tro CUDA...
    pip install torch torchvision --extra-index-url https://download.pytorch.org/whl/cu121
    pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cu121
) else (
    echo [INFO] Khong co GPU. Cai ban CPU...
    pip install torch --extra-index-url https://download.pytorch.org/whl/cpu
    pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu
)

echo [4/6] Dang cai dat requirements.txt...
pip install -r requirements.txt --quiet

echo [5/6] Dang tai mo hinh AI...
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('intfloat/multilingual-e5-base')"

echo [6/6] Kiem tra Poppler...
if exist "poppler-25.12.0" (echo [INFO] Da co Poppler.) else (echo [!] Thieu Poppler.)

echo ============================================
echo   CAI DAT HOAN TAT!
echo ============================================
pause