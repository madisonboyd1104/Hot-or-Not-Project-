#!/bin/bash
# HotOrNot Sentiment Analyzer - Setup Script
# Run this script once on any new computer to install dependencies

echo "=================================="
echo "HotOrNot Setup - Installing Dependencies"
echo "=================================="
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed."
    echo "Please install Python 3 from https://www.python.org/"
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

echo ""
echo "Installing dependencies (this may take a few minutes)..."
echo "Note: First-time BERT model download is ~500MB (happens on first run)"
echo ""

# Upgrade pip
venv/bin/pip install --upgrade pip --quiet

# Install requirements
venv/bin/pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo ""
    echo "=================================="
    echo "✅ Setup complete!"
    echo "=================================="
    echo ""
    echo "You can now run the application by:"
    echo "  • Double-clicking: Start_HotOrNot.command (or HotOrNot.app)"
    echo "  • Command line: ./run.sh"
    echo "  • Manual: venv/bin/python main.py"
    echo ""
else
    echo ""
    echo "❌ Installation failed. Please check your internet connection."
    echo "You may need to run: pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt"
    exit 1
fi

