@echo off
chcp 65001 >nul 2>&1
title Setup - He thong phan tich CV

echo ============================================
echo   CAI DAT HE THONG PHAN TICH VA DANH GIA CV
echo ============================================
echo.

:: Tim Python - thu nhieu duong dan pho bien
set "PYTHON_EXE="

:: 1. Thu tu PATH truoc
where python >nul 2>&1
if not errorlevel 1 (
    set "PYTHON_EXE=python"
    goto :found_python
)

:: 2. Thu cac duong dan pho bien tren C: va D:
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

:: 3. Khong tim thay -> hoi nguoi dung nhap duong dan
echo [CANH BAO] Khong tim thay Python tu dong!
echo.
echo Vui long nhap duong dan den python.exe
echo Vi du: D:\Python310\python.exe
echo.
set /p PYTHON_EXE="Nhap duong dan python.exe: "

if not exist "%PYTHON_EXE%" (
    echo [LOI] Khong tim thay file: %PYTHON_EXE%
    echo Vui long cai Python 3.10.11 tai: https://www.python.org/downloads/release/python-31011/
    pause
    exit /b 1
)

:found_python
echo [INFO] Su dung Python tai: %PYTHON_EXE%

:: Kiem tra phien ban
for /f "tokens=2 delims= " %%v in ('"%PYTHON_EXE%" --version 2^>^&1') do set PYVER=%%v
echo [INFO] Phien ban Python: %PYVER%

if NOT "%PYVER%"=="3.10.11" (
    echo.
    echo [CANH BAO] Yeu cau Python 3.10.11, nhung phat hien Python %PYVER%
    echo Vui long cai dung Python 3.10.11 tai:
    echo   https://www.python.org/downloads/release/python-31011/
    echo.
    echo Nhan phim bat ky de tiep tuc hoac dong cua so de dung.
    pause
)
echo.

:: Luu duong dan Python vao file de run.bat su dung
echo %PYTHON_EXE%> .python_path
echo [INFO] Da luu duong dan Python vao .python_path
echo.

:: Tao virtual environment
echo [1/4] Dang tao virtual environment...
if not exist ".venv" (
    "%PYTHON_EXE%" -m venv .venv
    echo       Da tao .venv thanh cong!
) else (
    echo       .venv da ton tai, bo qua.
)
echo.

:: Cai dat thu vien
echo [2/4] Dang cai dat thu vien (co the mat 5-15 phut)...
call .venv\Scripts\activate.bat
pip install -r requirements.txt
echo.

:: Tai mo hinh SBERT
echo [3/4] Dang tai mo hinh AI (SBERT multilingual-e5-base)...
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('intfloat/multilingual-e5-base'); print('Da tai model thanh cong!')"
echo.

:: Kiem tra Poppler
echo [4/4] Kiem tra Poppler...
if exist "poppler-25.12.0" (
    echo       Da phat hien Poppler, se tu dong cau hinh khi chay.
) else (
    echo       [CANH BAO] Khong tim thay thu muc poppler-25.12.0
    echo       Can Poppler de doc PDF scan. Tai tai:
    echo       https://github.com/oschwartz10612/poppler-windows/releases
)
echo.

echo ============================================
echo   CAI DAT HOAN TAT!
echo   Chay "run.bat" de khoi dong ung dung.
echo ============================================
pause
