@echo off
:: ============================================================
::  ISRM Project — One-Click Launcher (Windows)
::  Run this file to automatically set up and start the app.
::  Usage:  run.bat           (starts the Flask app)
::          run.bat --scan    (starts app + runs Bandit SAST scan)
:: ============================================================

title ISRM - Student Management System
color 0A

echo.
echo  ============================================================
echo   ISRM - Integrated Security Risk Management
echo   One-Click Setup and Launcher
echo  ============================================================
echo.

:: ------------------------------------------------------------------
:: 1. Check Python is installed
:: ------------------------------------------------------------------
echo [1/5] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo  [ERROR] Python is not installed or not in PATH.
    echo  Please install Python 3.9+ from https://www.python.org/downloads/
    echo  Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)
for /f "tokens=2" %%V in ('python --version 2^>^&1') do set PYTHON_VER=%%V
echo         Python %PYTHON_VER% found.

:: ------------------------------------------------------------------
:: 2. Detect current branch
:: ------------------------------------------------------------------
echo [2/5] Detecting branch...
for /f "tokens=*" %%B in ('git branch --show-current 2^>nul') do set BRANCH=%%B
if "%BRANCH%"=="" (
    echo         [WARNING] Not a git repository or git not found.
    set BRANCH=unknown
) else (
    echo         Branch: %BRANCH%
)

if "%BRANCH%"=="main" (
    echo.
    echo  ============================================================
    echo   WARNING: You are on the MAIN branch ^(VULNERABLE version^).
    echo   This version contains intentional security flaws.
    echo   For the secure version, run: git checkout fixed-version
    echo  ============================================================
    echo.
)

if "%BRANCH%"=="fixed-version" (
    echo.
    echo  ============================================================
    echo   You are on the FIXED-VERSION branch ^(SECURE version^).
    echo   All critical/high vulnerabilities have been remediated.
    echo  ============================================================
    echo.
)

:: ------------------------------------------------------------------
:: 3. Create virtual environment if it doesn't exist
:: ------------------------------------------------------------------
echo [3/5] Setting up virtual environment...
if not exist "venv\Scripts\activate.bat" (
    echo         Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo  [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )
    echo         Virtual environment created.
) else (
    echo         Virtual environment already exists.
)

:: Activate virtual environment
call venv\Scripts\activate.bat

:: ------------------------------------------------------------------
:: 4. Install dependencies
:: ------------------------------------------------------------------
echo [4/5] Installing dependencies...
pip install -r requirements.txt --quiet --disable-pip-version-check 2>nul
if errorlevel 1 (
    echo         [WARNING] Some dependencies may have failed. Retrying...
    pip install -r requirements.txt --disable-pip-version-check
)
echo         Dependencies installed.

:: Install Bandit for security scanning (optional but useful)
pip install bandit --quiet --disable-pip-version-check 2>nul
echo         Bandit (SAST scanner) installed.

:: ------------------------------------------------------------------
:: 5. Clean up old database (optional auto-regeneration)
:: ------------------------------------------------------------------
if exist "vulnerable_app.db" (
    echo         Database found: vulnerable_app.db
) else (
    echo         Database will be created on first run.
)

:: Create uploads folder if missing
if not exist "uploads" mkdir uploads

:: ------------------------------------------------------------------
:: Handle --scan flag
:: ------------------------------------------------------------------
if "%1"=="--scan" (
    echo.
    echo  ============================================================
    echo   Running Bandit SAST Security Scan...
    echo  ============================================================
    echo.
    bandit -r . -x ./venv -f screen
    echo.
    echo  ============================================================
    echo   Scan complete. Starting application...
    echo  ============================================================
    echo.
)

:: ------------------------------------------------------------------
:: 6. Launch the application
:: ------------------------------------------------------------------
echo [5/5] Starting Flask application...
echo.
echo  ============================================================
echo   Application starting on http://127.0.0.1:5000
echo   Press Ctrl+C to stop the server.
echo  ============================================================
echo.

python app.py

:: ------------------------------------------------------------------
:: After app exits
:: ------------------------------------------------------------------
echo.
echo  Application stopped.
call venv\Scripts\deactivate.bat 2>nul
pause
