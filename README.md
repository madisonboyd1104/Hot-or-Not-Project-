# Hot-or-Not-Project

A Reddit sentiment analysis tool that compares public opinion on iPhone vs Samsung using Reddit posts.

## Features
- Fetches posts from multiple tech-related subreddits
- Analyzes sentiment using a custom dictionary-based approach
- GUI interface with Tkinter
- SQLite database for storing posts
- Comparative pie chart visualizations

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

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
```bash
python HotOrNot_sentiment5.0.py
```

Or use the provided scripts:
- **macOS/Linux:** `./run.sh`
- **Windows:** `run.bat`

## Login Credentials
Default login:
- Username: `admin`
- Password: `password`

## Requirements
- Python 3.7+
- See `requirements.txt` for package dependencies
