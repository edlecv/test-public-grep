# 🐍 Python Installation Guide for Hashdive Dashboard

## Python is Required

Your system doesn't have Python installed. Here are the installation options:

## Option 1: Install Python from Microsoft Store (Easiest)

1. **Open Microsoft Store**
2. **Search for "Python"**
3. **Install "Python 3.11" or "Python 3.12"** (latest stable version)
4. **Wait for installation to complete**

## Option 2: Install Python from Official Website

1. **Go to**: https://www.python.org/downloads/
2. **Click "Download Python 3.11.x"** (latest version)
3. **Run the installer**
4. **IMPORTANT**: Check "Add Python to PATH" during installation
5. **Click "Install Now"**

## Option 3: Quick Command Line Installation

Open PowerShell as Administrator and run:
```powershell
# Install Python via winget (Windows Package Manager)
winget install Python.Python.3.11

# Or install via Chocolatey (if you have it)
choco install python
```

## After Python Installation

### Step 1: Verify Python is Installed
Open a new Command Prompt or PowerShell and run:
```bash
python --version
```
You should see something like: `Python 3.11.x`

### Step 2: Install Required Packages
```bash
pip install Flask==2.3.3 Flask-CORS==4.0.0 requests==2.31.0 Werkzeug==2.3.7
```

### Step 3: Start Your Hashdive Dashboard
```bash
python hashdive_server.py
```

### Step 4: Open Dashboard
Go to: http://localhost:5000

## Alternative: No-Install Browser Solution

If you don't want to install Python, you can use the simple HTML version:

1. **Open**: `simple_hashdive_test.html` in your browser
2. **Note**: This version has CORS limitations but can still test some endpoints

## Troubleshooting

### If `python` command doesn't work:
- Try `python3` instead
- Try `py` instead
- Restart your terminal/command prompt
- Check if Python was added to PATH during installation

### If `pip` doesn't work:
- Try `python -m pip install ...`
- Try `py -m pip install ...`

### If you get permission errors:
- Run Command Prompt as Administrator
- Or add `--user` flag: `pip install --user Flask Flask-CORS requests`

## What You'll Have After Installation

✅ **Python 3.11+** - Programming language runtime  
✅ **Flask** - Web framework for the dashboard  
✅ **Flask-CORS** - Cross-origin request handling  
✅ **Requests** - HTTP library for API calls  
✅ **Werkzeug** - Web server utilities  

Then you can run your professional Hashdive data analysis dashboard!