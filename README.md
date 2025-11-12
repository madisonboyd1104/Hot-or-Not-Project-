# Hot-or-Not-Project

A Reddit sentiment analysis tool that compares public opinion on iPhone vs Samsung using Reddit posts.

## Features
- Fetches posts from multiple tech-related subreddits
- **BERT-powered sentiment analysis** using transformer models
- Dictionary-based fallback analysis
- GUI interface with Tkinter
- SQLite database for storing posts
- Comparative pie chart visualizations

## Setup Instructions

### 🚀 Quick Setup (Recommended)

Run the automated setup script:

**macOS/Linux:**
```bash
./setup.sh
```

**Windows:**
```bash
setup.bat
```

This will automatically create a virtual environment and install all dependencies.

### 📋 Manual Setup (Alternative)

If the automatic setup doesn't work:

```bash
# Create virtual environment
python3 -m venv venv

# Install dependencies
venv/bin/pip install -r requirements.txt
```

**Note:** First run will download a ~500MB BERT model for sentiment analysis (cached for future use).

**📖 For detailed setup instructions (especially for new computers), see `SETUP_FOR_NEW_COMPUTERS.md`**

### 2. Configure Reddit API
1. Create a Reddit app at https://www.reddit.com/prefs/apps
2. Copy `config.ini.example` to `config.ini`
3. Fill in your Reddit API credentials in `config.ini`:
   - `client_id`
   - `client_secret`
   - `user_agent`
   - `username`
   - `password`

### 3. Run the Application

**🚀 Easy Launch (Just Double-Click!):**

- **macOS:** Double-click `Start_HotOrNot.command` or `HotOrNot.app`
- **Windows:** Double-click `run.bat`

**Command Line:**
```bash
# macOS/Linux
./run.sh

# Windows
run.bat

# Or directly with Python
venv/bin/python main.py
```

## Login Credentials
Default login:
- Username: `admin`
- Password: `password`

## Requirements
- Python 3.7+
- ~500MB disk space for BERT model (downloaded automatically on first run)
- See `requirements.txt` for package dependencies:
  - praw (Reddit API)
  - matplotlib (visualizations)
  - transformers (BERT sentiment analysis)
  - torch (PyTorch backend for transformers)

## Troubleshooting

### "No module named 'transformers'" Error
If you get this error, ensure you've installed dependencies in a virtual environment:
```bash
python3 -m venv venv
venv/bin/pip install -r requirements.txt
```

### macOS Security Warning
When first running `Start_HotOrNot.command` or `HotOrNot.app`:
1. Right-click the file → **Open**
2. Click **Open** in the security dialog
3. After this, you can double-click normally
