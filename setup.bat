@echo off
REM HotOrNot Sentiment Analyzer - Setup Script for Windows
REM Run this script once on any new computer to install dependencies

echo ==================================
echo HotOrNot Setup - Installing Dependencies
echo ==================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed.
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

echo Python found:
python --version
echo.

REM Create virtual environment if it doesn't exist
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created
) else (
    echo Virtual environment already exists
)

echo.
echo Installing dependencies (this may take a few minutes)...
echo Note: First-time BERT model download is ~500MB (happens on first run)
echo.

REM Upgrade pip
venv\Scripts\python.exe -m pip install --upgrade pip --quiet

REM Install requirements
venv\Scripts\python.exe -m pip install -r requirements.txt

if %errorlevel% equ 0 (
    echo.
    echo ==================================
    echo Setup complete!
    echo ==================================
    echo.
    echo You can now run the application by:
    echo   - Double-clicking: run.bat
    echo   - Command line: venv\Scripts\python.exe main.py
    echo.
) else (
    echo.
    echo Installation failed. Please check your internet connection.
    exit /b 1
)

pause

