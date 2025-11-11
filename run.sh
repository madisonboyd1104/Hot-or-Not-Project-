#!/bin/bash
# HotOrNot Sentiment Analyzer Startup Script

# Suppress macOS Tkinter deprecation warning
export TK_SILENCE_DEPRECATION=1

# Run the application using the virtual environment Python
venv/bin/python main.py
