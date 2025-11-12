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
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║         ⚠️  Setup Required - Dependencies Not Installed        ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo ""
    echo "This is your first time running HotOrNot on this computer."
    echo ""
    echo "Please run the setup script first:"
    echo "  1. Open Terminal"
    echo "  2. Navigate to this folder: cd \"$(pwd)\""
    echo "  3. Run: ./setup.sh"
    echo ""
    echo "Or manually install:"
    echo "  python3 -m venv venv"
    echo "  venv/bin/pip install -r requirements.txt"
    echo ""
    echo "📖 See QUICK_START.txt or SETUP_FOR_NEW_COMPUTERS.md for help."
    echo ""
    echo "Press any key to exit..."
    read -n 1
    exit 1
fi

# Run the application
echo "Starting HotOrNot Sentiment Analyzer..."
echo ""
$PYTHON_PATH main.py

# Keep terminal open if there's an error
if [ $? -ne 0 ]; then
    echo ""
    echo "════════════════════════════════════════════════════════════════"
    echo "An error occurred. Common solutions:"
    echo "  • If 'No module named transformers': run ./setup.sh"
    echo "  • Check QUICK_START.txt for troubleshooting tips"
    echo "════════════════════════════════════════════════════════════════"
    echo ""
    echo "Press any key to exit..."
    read -n 1
fi

