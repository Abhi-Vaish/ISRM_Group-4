#!/bin/bash
# ============================================================
#  ISRM Project — One-Click Launcher (Linux / macOS)
#  Run this file to automatically set up and start the app.
#  Usage:  ./run.sh           (starts the Flask app)
#          ./run.sh --scan    (starts app + runs Bandit SAST scan)
# ============================================================

set -e

# Colors for terminal output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo ""
echo -e "${CYAN}============================================================${NC}"
echo -e "${CYAN} ISRM - Integrated Security Risk Management${NC}"
echo -e "${CYAN} One-Click Setup and Launcher${NC}"
echo -e "${CYAN}============================================================${NC}"
echo ""

# ------------------------------------------------------------------
# 1. Check Python is installed
# ------------------------------------------------------------------
echo -e "${GREEN}[1/5]${NC} Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo -e "${RED}[ERROR] Python is not installed.${NC}"
        echo "Please install Python 3.9+ from https://www.python.org/downloads/"
        exit 1
    fi
    PYTHON_CMD="python"
else
    PYTHON_CMD="python3"
fi
PY_VER=$($PYTHON_CMD --version 2>&1)
echo "        $PY_VER found."

# ------------------------------------------------------------------
# 2. Detect current branch
# ------------------------------------------------------------------
echo -e "${GREEN}[2/5]${NC} Detecting branch..."
BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")
echo "        Branch: $BRANCH"

if [ "$BRANCH" = "main" ]; then
    echo ""
    echo -e "${RED}============================================================${NC}"
    echo -e "${RED} WARNING: You are on the MAIN branch (VULNERABLE version).${NC}"
    echo -e "${RED} This version contains intentional security flaws.${NC}"
    echo -e "${RED} For the secure version: git checkout fixed-version${NC}"
    echo -e "${RED}============================================================${NC}"
    echo ""
fi

if [ "$BRANCH" = "fixed-version" ]; then
    echo ""
    echo -e "${GREEN}============================================================${NC}"
    echo -e "${GREEN} You are on the FIXED-VERSION branch (SECURE version).${NC}"
    echo -e "${GREEN} All critical/high vulnerabilities have been remediated.${NC}"
    echo -e "${GREEN}============================================================${NC}"
    echo ""
fi

# ------------------------------------------------------------------
# 3. Create virtual environment if it doesn't exist
# ------------------------------------------------------------------
echo -e "${GREEN}[3/5]${NC} Setting up virtual environment..."
if [ ! -d "venv" ]; then
    echo "        Creating virtual environment..."
    $PYTHON_CMD -m venv venv
    echo "        Virtual environment created."
else
    echo "        Virtual environment already exists."
fi

# Activate virtual environment
source venv/bin/activate

# ------------------------------------------------------------------
# 4. Install dependencies
# ------------------------------------------------------------------
echo -e "${GREEN}[4/5]${NC} Installing dependencies..."
pip install -r requirements.txt --quiet --disable-pip-version-check 2>/dev/null || \
    pip install -r requirements.txt --disable-pip-version-check
echo "        Dependencies installed."

# Install Bandit for security scanning
pip install bandit --quiet --disable-pip-version-check 2>/dev/null || true
echo "        Bandit (SAST scanner) installed."

# ------------------------------------------------------------------
# 5. Ensure folders and database
# ------------------------------------------------------------------
if [ -f "vulnerable_app.db" ]; then
    echo "        Database found: vulnerable_app.db"
else
    echo "        Database will be created on first run."
fi

mkdir -p uploads

# ------------------------------------------------------------------
# Handle --scan flag
# ------------------------------------------------------------------
if [ "$1" = "--scan" ]; then
    echo ""
    echo -e "${CYAN}============================================================${NC}"
    echo -e "${CYAN} Running Bandit SAST Security Scan...${NC}"
    echo -e "${CYAN}============================================================${NC}"
    echo ""
    bandit -r . -x ./venv -f screen || true
    echo ""
    echo -e "${CYAN}============================================================${NC}"
    echo -e "${CYAN} Scan complete. Starting application...${NC}"
    echo -e "${CYAN}============================================================${NC}"
    echo ""
fi

# ------------------------------------------------------------------
# 6. Launch the application
# ------------------------------------------------------------------
echo -e "${GREEN}[5/5]${NC} Starting Flask application..."
echo ""
echo -e "${CYAN}============================================================${NC}"
echo -e "${CYAN} Application starting on http://127.0.0.1:5000${NC}"
echo -e "${CYAN} Press Ctrl+C to stop the server.${NC}"
echo -e "${CYAN}============================================================${NC}"
echo ""

$PYTHON_CMD app.py

# ------------------------------------------------------------------
# After app exits
# ------------------------------------------------------------------
echo ""
echo "Application stopped."
deactivate 2>/dev/null || true
