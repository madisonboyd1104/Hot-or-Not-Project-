#!/bin/bash
# HotOrNot Sentiment Analyzer - Double-Click to Run
# This .command file can be double-clicked on macOS

# Get the directory where this script is located
cd "$(dirname "$0")"

# Suppress macOS Tkinter deprecation warning
export TK_SILENCE_DEPRECATION=1

# Check if virtual environment exists in current or parent directory
if [ -d "venv" ]; then
    PYTHON_PATH="venv/bin/python"
elif [ -d "../tt5.1/venv" ]; then
    echo "Using shared virtual environment from parent directory..."
    PYTHON_PATH="../tt5.1/venv/bin/python"
else
    echo "Virtual environment not found."
    echo "Please install dependencies by running:"
    echo "  python3 -m venv venv"
    echo "  venv/bin/pip install -r requirements.txt"
    echo ""
    echo "Press any key to exit..."
    read -n 1
    exit 1
fi

# Run the application
echo "Starting HotOrNot Sentiment Analyzer..."
$PYTHON_PATH main.py

# Keep terminal open if there's an error
if [ $? -ne 0 ]; then
    echo ""
    echo "An error occurred. Press any key to exit..."
    read -n 1
fi

