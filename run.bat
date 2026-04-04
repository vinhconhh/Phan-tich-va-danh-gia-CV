@echo off
chcp 65001 >nul 2>&1
title Phan tich va danh gia CV

:: Kiem tra da cai dat chua
if not exist ".venv" (
    echo [!] Chua cai dat. Dang chay setup...
    call setup.bat
    if errorlevel 1 exit /b 1
)

:: Activate virtual environment
call .venv\Scripts\activate.bat

:: Thiet lap Poppler path
if exist "poppler-25.12.0\Library\bin" (
    set "POPPLER_PATH=%~dp0poppler-25.12.0\Library\bin"
)

:: Chay ung dung Streamlit
echo.
echo ============================================
echo   KHOI DONG UNG DUNG PHAN TICH CV
echo   Trinh duyet se tu mo tai localhost:8501
echo   Nhan Ctrl+C de dung.
echo ============================================
echo.

streamlit run app.py --server.headless false --browser.gatherUsageStats false
