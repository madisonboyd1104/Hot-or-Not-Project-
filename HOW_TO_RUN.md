# How to Run HotOrNot Sentiment Analyzer 🚀

## Quick Start (Double-Click!)

### On macOS:
Choose one of these options:

1. **Recommended: Application Bundle**
   - Double-click `HotOrNot.app`
   - You can move this to your Applications folder or add to your Dock!

2. **Command File**
   - Double-click `Start_HotOrNot.command`

3. **Shell Script**
   - Double-click `run.sh` (or run `./run.sh` in Terminal)

### On Windows:
- Double-click `run.bat`

---

## First Time Setup

### macOS Security Note
The first time you run the app on macOS:
1. Right-click the file (e.g., `Start_HotOrNot.command` or `HotOrNot.app`)
2. Choose **"Open"** from the menu
3. Click **"Open"** in the security dialog that appears
4. After this, you can simply double-click the file normally!

### Install Dependencies (if needed)
If you get an error about missing packages:

```bash
# Create virtual environment
python3 -m venv venv

# Install all dependencies
venv/bin/pip install -r requirements.txt
```

**Note:** The first run will download a ~500MB BERT model for advanced sentiment analysis. This is cached for future use, so subsequent runs will be much faster!

---

## What Each File Does

| File | Description |
|------|-------------|
| `HotOrNot.app` | Native macOS application bundle (most convenient) |
| `Start_HotOrNot.command` | macOS Terminal launcher with error handling |
| `run.sh` | Shell script for macOS/Linux |
| `run.bat` | Batch script for Windows |
| `main.py` | Main Python entry point |

---

## Troubleshooting

### "Virtual environment not found"
The app will automatically use the shared virtual environment from the parent directory (`../tt5.1/venv`). If this doesn't exist, create a new one:
```bash
python3 -m venv venv
venv/bin/pip install -r requirements.txt
```

### "No module named 'transformers'"
This means the dependencies aren't installed. Run:
```bash
venv/bin/pip install -r requirements.txt
```

### SSL Certificate Errors (macOS)
If you get SSL errors during installation, try:
```bash
/Applications/Python*/Install\ Certificates.command
```

Or install packages from the parent directory's venv (which the launcher will use automatically).

---

## Advanced Usage

### Run from Command Line
```bash
# Activate virtual environment
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Run the application
python main.py
```

### Check if Dependencies are Installed
```bash
venv/bin/pip list | grep -E "(praw|matplotlib|transformers|torch)"
```

---

## Need Help?

Check the main `README.md` for full setup instructions and Reddit API configuration.

