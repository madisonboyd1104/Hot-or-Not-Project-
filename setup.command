#!/bin/bash
# HotOrNot Sentiment Analyzer - Setup Script
# Created by Howard Ames III
# This script will automatically set up your virtual environment and install dependencies

echo " Setting up HotOrNot Sentiment Analyzer..."
echo ""

# Navigate to the script's directory
cd "$(dirname "$0")"

# Check if virtual environment already exists
if [ -d "venv" ]; then
    echo "  Virtual environment already exists."
    read -p "Do you want to recreate it? (y/n): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "  Removing existing virtual environment..."
        rm -rf venv
    else
        echo "  Using existing virtual environment."
    fi
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo " Creating virtual environment..."
    python3 -m venv venv
    
    if [ $? -ne 0 ]; then
        echo " Error: Failed to create virtual environment."
        echo "Please make sure Python 3 is installed on your system."
        read -p "Press any key to exit..."
        exit 1
    fi
    echo " Virtual environment created successfully!"
else
    echo " Virtual environment ready!"
fi

echo ""
echo " Installing required packages..."
source venv/bin/activate

# Upgrade pip first
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo " Error: Failed to install required packages."
    read -p "Press any key to exit..."
    exit 1
fi

echo ""
echo " Setup complete!"
echo ""
echo "To run the application, use:"
echo "  ./run.sh"
echo ""
echo "Or manually activate the virtual environment with:"
echo "  source venv/bin/activate"
echo "  python main.py"
echo ""
read -p "Press any key to close this window..."

