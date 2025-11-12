@echo off
REM Run the Reddit Sentiment Analysis GUI

REM Check if virtual environment exists
if not exist "venv\Scripts\python.exe" (
    echo.
    echo ======================================================================
    echo   SETUP REQUIRED - Dependencies Not Installed
    echo ======================================================================
    echo.
    echo This is your first time running HotOrNot on this computer.
    echo.
    echo Please run setup.bat first to install dependencies.
    echo.
    echo Or manually:
    echo   python -m venv venv
    echo   venv\Scripts\pip.exe install -r requirements.txt
    echo.
    echo See QUICK_START.txt or SETUP_FOR_NEW_COMPUTERS.md for help.
    echo.
    pause
    exit /b 1
)

echo Starting HotOrNot Sentiment Analyzer...
echo.
venv\Scripts\python.exe main.py

if errorlevel 1 (
    echo.
    echo ======================================================================
    echo An error occurred. Common solutions:
    echo   - If 'No module named transformers': run setup.bat
    echo   - Check QUICK_START.txt for troubleshooting tips
    echo ======================================================================
    echo.
)

pause
