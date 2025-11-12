# Setup Instructions for New Computers 🖥️

Follow these steps to get HotOrNot running on any new computer.

---

## 📋 Prerequisites

1. **Python 3.7 or higher** must be installed
   - Check by running: `python3 --version` (macOS/Linux) or `python --version` (Windows)
   - If not installed, download from: https://www.python.org/downloads/

2. **Internet connection** (for initial setup only)

---

## 🚀 Quick Setup (Recommended)

### Option 1: Automatic Setup Script

#### On macOS/Linux:
```bash
# Navigate to the project folder
cd /path/to/Hot-or-Not-Project

# Run the setup script
./setup.sh
```

#### On Windows:
```batch
# Navigate to the project folder
cd C:\path\to\Hot-or-Not-Project

# Run the setup script
setup.bat
```

The setup script will:
- ✅ Create a virtual environment
- ✅ Install all required packages
- ✅ Verify the installation

**That's it!** After setup completes, you can run the app by double-clicking:
- macOS: `Start_HotOrNot.command` or `HotOrNot.app`
- Windows: `run.bat`

---

## 🔧 Manual Setup (Alternative)

If the automatic setup doesn't work, follow these steps:

### Step 1: Create Virtual Environment
```bash
# macOS/Linux
python3 -m venv venv

# Windows
python -m venv venv
```

### Step 2: Activate Virtual Environment
```bash
# macOS/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
# macOS/Linux
venv/bin/pip install -r requirements.txt

# Windows
venv\Scripts\pip.exe install -r requirements.txt
```

This will install:
- `praw` - Reddit API wrapper
- `matplotlib` - For creating charts
- `transformers` - BERT AI model for advanced sentiment analysis
- `torch` - PyTorch (required for transformers)

**Note:** Installing `torch` and `transformers` may take 5-10 minutes as they're large packages (~2GB total).

### Step 4: Run the Application
```bash
# macOS/Linux
./run.sh
# or
venv/bin/python main.py

# Windows
run.bat
# or
venv\Scripts\python.exe main.py
```

---

## ⚠️ Common Issues & Solutions

### Issue 1: "No module named 'transformers'"

**Problem:** Running with system Python instead of the virtual environment.

**Solution:** Always use the virtual environment Python:
```bash
# ❌ WRONG - uses system Python
python3 main.py

# ✅ CORRECT - uses venv Python
venv/bin/python main.py
# or just use the provided launchers
./run.sh  # macOS/Linux
run.bat   # Windows
```

### Issue 2: "python3: command not found" (macOS/Linux)

**Problem:** Python not installed or not in PATH.

**Solution:** 
- Install Python from https://www.python.org/
- Or use `python` instead of `python3`

### Issue 3: SSL Certificate Errors (macOS)

**Problem:** Python can't verify SSL certificates.

**Solution:**
```bash
# Run Python's certificate installer
/Applications/Python*/Install\ Certificates.command
```

### Issue 4: Setup script won't run (macOS)

**Problem:** Script doesn't have execute permissions.

**Solution:**
```bash
chmod +x setup.sh
chmod +x run.sh
chmod +x Start_HotOrNot.command
./setup.sh
```

### Issue 5: "pip: command not found"

**Problem:** pip not installed with Python.

**Solution:**
```bash
# macOS/Linux
python3 -m ensurepip --upgrade

# Windows
python -m ensurepip --upgrade
```

### Issue 6: BERT model won't download

**Problem:** First run tries to download ~500MB model but fails.

**Solution:** The app will automatically fall back to dictionary-based sentiment analysis. It will still work but with slightly less accurate results. To use BERT:
- Check your internet connection
- Make sure you have ~1GB free disk space
- Try running again - the download will resume where it left off

---

## 📦 What Gets Installed?

| Package | Size | Purpose |
|---------|------|---------|
| praw | ~500KB | Reddit API access |
| matplotlib | ~50MB | Charts and visualizations |
| transformers | ~500MB | BERT AI model library |
| torch | ~200MB | PyTorch machine learning framework |
| *BERT model* | ~500MB | Downloaded on first run (cached) |

**Total:** ~1.2GB for first-time setup

---

## 🎯 Verifying Installation

After setup, verify everything works:

```bash
# Check if venv was created
ls venv/  # Should see bin/ (or Scripts/ on Windows)

# Check installed packages
venv/bin/pip list  # macOS/Linux
venv\Scripts\pip.exe list  # Windows

# Should see: praw, matplotlib, transformers, torch
```

---

## 📤 Sharing the Project

When sharing this project with others:

### Include:
- ✅ All `.py` files
- ✅ `requirements.txt`
- ✅ `config.ini` (with Reddit credentials)
- ✅ `setup.sh` and `setup.bat`
- ✅ All `.command`, `.sh`, and `.bat` launcher files
- ✅ This `SETUP_FOR_NEW_COMPUTERS.md` file

### Don't Include (add to `.gitignore`):
- ❌ `venv/` folder (each computer needs its own)
- ❌ `__pycache__/` folders
- ❌ `*.pyc` files
- ❌ `reddit_sentiment.db` (will be recreated)
- ❌ `.DS_Store` files (macOS)

### Recommended: Create a `.gitignore` file:
```
venv/
__pycache__/
*.pyc
*.pyo
*.db
.DS_Store
*.log
```

---

## 🆘 Still Having Issues?

1. **Delete the venv and try again:**
   ```bash
   rm -rf venv  # macOS/Linux
   rmdir /s venv  # Windows
   ./setup.sh  # or setup.bat on Windows
   ```

2. **Make sure Python version is correct:**
   ```bash
   python3 --version  # Should be 3.7 or higher
   ```

3. **Try installing packages one by one:**
   ```bash
   venv/bin/pip install praw
   venv/bin/pip install matplotlib
   venv/bin/pip install transformers torch
   ```

4. **Check if you have write permissions** in the project folder

5. **Temporarily disable antivirus** if it's blocking pip installations

---

## 📖 Additional Resources

- Python Installation: https://www.python.org/downloads/
- Virtual Environments: https://docs.python.org/3/library/venv.html
- Reddit API Setup: https://www.reddit.com/prefs/apps
- Project README: See `README.md` in this folder

---

**Remember:** After setup completes, you should be able to simply double-click the launcher files to run the app! 🎉

