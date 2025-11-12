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
    echo "⚠️  Setup Required - Virtual environment not found."
    echo ""
    echo "Please run the setup script first: ./setup.sh"
    echo "Or manually: python3 -m venv venv && venv/bin/pip install -r requirements.txt"
    echo ""
    echo "📖 See QUICK_START.txt for help."
    exit 1
fi

# Run the application using the virtual environment Python
echo "Starting HotOrNot Sentiment Analyzer..."
$PYTHON_PATH main.py

# Show helpful message if error
if [ $? -ne 0 ]; then
    echo ""
    echo "⚠️  Error occurred. If 'No module named transformers', run: ./setup.sh"
fi
