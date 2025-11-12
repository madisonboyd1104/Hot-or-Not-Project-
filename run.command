#!/bin/bash
# HotOrNot Sentiment Analyzer Startup Script

# Navigate to the script's directory
cd "$(dirname "$0")"

# Suppress macOS Tkinter deprecation warning
export TK_SILENCE_DEPRECATION=1

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Error: Virtual environment not found!"
    echo "Please run setup.command first to install dependencies."
    read -p "Press any key to exit..."
    exit 1
fi

# Run the application using the virtual environment Python
venv/bin/python main.py

