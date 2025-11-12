#!/bin/bash
# HotOrNot Sentiment Analyzer Startup Script

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
    echo "Please install dependencies: python3 -m venv venv && venv/bin/pip install -r requirements.txt"
    exit 1
fi

# Run the application using the virtual environment Python
$PYTHON_PATH main.py
