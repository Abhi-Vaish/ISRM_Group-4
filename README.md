<p align="center">
  <h1 align="center">🔒 ISRM — Integrated Security Risk Management</h1>
  <p align="center">
    <strong>A DevSecOps Research Project on Secure Software Development Lifecycle</strong>
  </p>
  <p align="center">
    <em>Student Management System · Vulnerability Assessment · CI/CD Security Pipeline</em>
  </p>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-blue?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Flask-2.3-green?logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/SAST-Bandit-orange?logo=python&logoColor=white" alt="Bandit">
  <img src="https://img.shields.io/badge/DAST-OWASP%20ZAP-red?logo=owasp&logoColor=white" alt="OWASP ZAP">
  <img src="https://img.shields.io/badge/CI%2FCD-Jenkins-D24939?logo=jenkins&logoColor=white" alt="Jenkins">
  <img src="https://img.shields.io/badge/License-MIT-yellow" alt="License">
</p>

---

## 📖 About the Project

This project demonstrates a complete **Information Security & Risk Management (ISRM)** workflow applied to a Flask-based **Student Management System**. It covers the full lifecycle — from intentionally building a vulnerable application, through automated security scanning, to implementing and verifying security fixes.

### Key Highlights

- **14 intentional vulnerabilities** aligned with OWASP Top 10 and CWE standards
- **Automated SAST scanning** using Bandit (static code analysis)
- **Automated DAST scanning** using OWASP ZAP (dynamic application testing)
- **CI/CD Security Pipeline** via Jenkins with a CVSS-based security gate
- **Before/After comparison** — vulnerable code vs. hardened code on separate branches
- **STRIDE threat modeling** and **ALE risk quantification**

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     Developer Workstation                       │
│  ┌──────────┐    ┌──────────┐    ┌──────────────────────────┐  │
│  │  app.py   │───▶│database.py│───▶│  SQLite (vulnerable_app) │  │
│  │  (Flask)  │    │  (ORM)   │    │        .db               │  │
│  └────┬─────┘    └──────────┘    └──────────────────────────┘  │
│       │                                                         │
│  ┌────▼─────┐    ┌──────────┐    ┌──────────────────────────┐  │
│  │templates/ │    │ static/  │    │    config.py              │  │
│  │ (Jinja2)  │    │  (CSS)   │    │    (App Settings)         │  │
│  └──────────┘    └──────────┘    └──────────────────────────┘  │
└────────────────────────┬────────────────────────────────────────┘
                         │
            ┌────────────▼────────────┐
            │     Jenkins Pipeline     │
            │  ┌────────────────────┐  │
            │  │ 0. Checkout        │  │
            │  │ 1. Build & Install │  │
            │  │ 2. Bandit SAST     │  │
            │  │ 3. Report Gen      │  │
            │  │ 4. Security Gate   │──── PASS/FAIL (CVSS > 5)
            │  └────────────────────┘  │
            └──────────────────────────┘
```

> For the detailed architecture diagram, see [docs/ISRM_Architecture.pdf](docs/ISRM_Architecture.pdf).

---

## 🌿 Branch Strategy

| Branch | Purpose | Jenkins Result |
|--------|---------|----------------|
| **`main`** | Vulnerable version — contains 14 intentional security flaws | ❌ **BUILD FAILS** (Security Gate blocks deployment) |
| **`fixed-version`** | Secure version — all critical/high vulnerabilities remediated | ✅ **BUILD PASSES** (Code is safe for deployment) |

This dual-branch approach demonstrates how a DevSecOps pipeline **catches vulnerabilities before they reach production**.

---

## 📋 Prerequisites & Requirements

Before running this project, ensure you have the following tools installed on your system:

### Required Software

| Tool | Version | Download Link | Purpose |
|------|---------|---------------|---------|
| **Python** | 3.9 or higher | [python.org/downloads](https://www.python.org/downloads/) | Application runtime |
| **pip** | Latest | Comes with Python | Python package manager |
| **Git** | 2.30+ | [git-scm.com/downloads](https://git-scm.com/downloads) | Version control |
| **Java JDK** | 11 or 17 | [adoptium.net](https://adoptium.net/) | Required for Jenkins |
| **Jenkins** | 2.400+ | [jenkins.io/download](https://www.jenkins.io/download/) | CI/CD pipeline |
| **OWASP ZAP** | 2.14+ | [zaproxy.org/download](https://www.zaproxy.org/download/) | Dynamic security scanning |

### Python Packages (installed automatically via requirements.txt)

| Package | Version | Purpose |
|---------|---------|---------|
| Flask | 2.3.0 | Web application framework |
| Werkzeug | 2.3.0 | WSGI utilities (used by Flask) |
| MarkupSafe | 2.1.1 | HTML escaping for Jinja2 templates |

### Additional Python Packages (installed manually for security scanning)

| Package | Install Command | Purpose |
|---------|-----------------|---------|
| Bandit | `pip install bandit` | SAST — Python static security analysis |
| Requests | `pip install requests` | Required by `test_vulnerabilities.py` |

### Verify Prerequisites

Run these commands to verify everything is installed:

```bash
# Check Python
python --version
# Expected: Python 3.9.x or higher

# Check pip
pip --version
# Expected: pip 21.x or higher

# Check Git
git --version
# Expected: git version 2.30 or higher

# Check Java (required for Jenkins)
java -version
# Expected: openjdk version "11.x.x" or "17.x.x"
```

---

## 🚀 Complete Setup Guide

### Step 1 — Clone the Repository

```bash
git clone https://github.com/gauravjaiswal12/ISRM_Group-4.git
cd ISRM_Group-4
```

### Step 2 — Create and Activate Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1

# Windows (CMD):
venv\Scripts\activate.bat

# Linux / macOS:
source venv/bin/activate
```

> ⚠️ You must activate the virtual environment **every time** you open a new terminal.

### Step 3 — Install Python Dependencies

```bash
# Install Flask and core dependencies
pip install -r requirements.txt

# Install Bandit for SAST security scanning
pip install bandit

# Install Requests for automated vulnerability testing
pip install requests
```

### Step 4 — Run the Application

#### Option A: Run the Vulnerable Version (main branch)

```bash
git checkout main
python app.py
```

**Expected output:**
```
[*] Database initialized successfully
[*] Starting Flask app...
[*] Debug Mode: True
[*] Host: 0.0.0.0:5000
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
```

#### Option B: Run the Fixed Version (fixed-version branch)

```bash
git checkout fixed-version
python app.py
```

**Expected output:**
```
[*] Starting Flask app...
[*] Debug Mode: False
[*] Host: 127.0.0.1:5000
 * Running on http://127.0.0.1:5000
```

> Notice: Debug mode is **OFF** in the fixed version (one of the security fixes).

### Step 5 — Access the Application

Open your browser and go to: **http://127.0.0.1:5000**

You will be redirected to the login page. Use any of these credentials:

| Role | Username | Password | Access Level |
|------|----------|----------|--------------|
| **Admin** | `admin` | `admin123` | Full access — dashboard, students, logs, upload, search |
| **User** | `user` | `password` | Can view students, search, upload files |
| **Student** | `john_student` | `student123` | Can only view own profile and grades |
| **Student** | `sarah_student` | `student456` | Can only view own profile and grades |

### Step 6 — Reset Database (if needed)

If you want to start fresh, delete the database file and restart:

```bash
# Stop the app (Ctrl+C)

# Delete the database
# Windows:
del vulnerable_app.db
# Linux/macOS:
rm vulnerable_app.db

# Restart the app — database auto-regenerates
python app.py
```

---

## 🛡️ Security Scanning — Complete Guide

### 1. SAST — Bandit (Static Analysis)

Bandit scans the **source code** without running the application. It detects security issues by analyzing the Python AST (Abstract Syntax Tree).

#### Installation

```bash
pip install bandit
```

#### Running Bandit

```bash
# Basic screen output
bandit -r . -x ./venv -f screen

# Generate HTML report
bandit -r . -x ./venv -f html -o reports/bandit_report.html

# Generate JSON report (used by Jenkins pipeline)
bandit -r . -x ./venv -f json -o reports/bandit_report.json
```

#### Expected Results

**On `main` branch (Vulnerable):**
```
Run started: ...
Test results:
>> Issue: [B608:hardcoded_sql_expressions] Possible SQL injection vector...
   Severity: Medium   Confidence: Low
   CWE: CWE-89
   Location: database.py:88
   ...

Code scanned:
        Total lines of code: 800+
        Total lines skipped: 0

Run metrics:
        Total issues (by severity):
                Undefined: 0
                Low: 1
                Medium: 2
                High: 4
        Total issues (by confidence):
                ...
```

**On `fixed-version` branch (Secure):**
```
Run metrics:
        Total issues (by severity):
                Undefined: 0
                Low: 0
                Medium: 0
                High: 0
```

#### Generate Vulnerability Assessment CSV

```bash
# Run the report generator (creates reports/vulnerability_assessment.csv)
python generate_vulnerability_report.py
```

This produces a CSV file with: Test ID, Vulnerability Name, Severity, CVSS Score, CWE, File, Line, Description.

---

### 2. DAST — OWASP ZAP (Dynamic Analysis)

OWASP ZAP scans the **running application** by actually sending attack payloads and analyzing responses.

#### Installation

1. Download OWASP ZAP from: **https://www.zaproxy.org/download/**
2. Install and launch the application
3. The ZAP GUI will open

#### Running a ZAP Scan

1. **Start the Flask application** (in a separate terminal):
   ```bash
   python app.py
   ```

2. **Open OWASP ZAP** and configure the scan:
   - Click **"Automated Scan"**
   - Enter the target URL: `http://127.0.0.1:5000`
   - Click **"Attack"**

3. **Wait for the scan to complete** (typically 5-15 minutes)

4. **Export the report:**
   - Go to **Report** → **Generate HTML Report**
   - Save as `reports/zap_report.html` (for vulnerable version)
   - Or save as `reports/zap_report_fixed.html` (for fixed version)

#### ZAP Scan with Authentication (for deeper scan)

To scan authenticated pages (dashboard, students, etc.):

1. In ZAP, go to **Sites** panel
2. Right-click `http://127.0.0.1:5000` → **Include in Context**
3. Go to **Session Properties** → **Authentication**:
   - Method: **Form-based Authentication**
   - Login URL: `http://127.0.0.1:5000/login`
   - POST Data: `username={%username%}&password={%password%}`
   - Login Page Indicator: `Login`
   - Logged In Indicator: `Dashboard`
4. Add users in **Users** section:
   - Username: `admin`, Password: `admin123`
5. Run the scan again with the context selected

#### Pre-Generated Reports

We have already scanned both versions and included the reports:
- [`reports/zap_report.html`](reports/zap_report.html) — Vulnerable version scan results
- [`reports/zap_report_fixed.html`](reports/zap_report_fixed.html) — Fixed version scan results

**Vulnerable Version Results:**
| Risk Level | Count | Details |
|------------|-------|---------|
| 🔴 High | 1 | SQL Injection confirmed |
| 🟠 Medium | 5 | Missing CSP, CSRF, Anti-clickjacking headers |
| 🟡 Low | 2 | Cookie security issues |
| 🔵 Info | 2 | Information disclosure |

**Fixed Version Results:**
| Risk Level | Count | Details |
|------------|-------|---------|
| 🔴 High | 0 | SQL Injection eliminated |
| 🟠 Medium | 5 | CSP header refinements remaining |
| 🟡 Low | 1 | Reduced from 2 |
| 🔵 Info | 5 | Non-security informational alerts |

---

### 3. CI/CD — Jenkins Pipeline Setup

Jenkins automates the entire security scanning process. The pipeline runs Bandit, generates reports, and enforces a security gate.

#### Jenkins Installation

1. **Download Jenkins:**
   - Go to: **https://www.jenkins.io/download/**
   - Download the **Windows installer (.msi)** or **Generic Java (.war)** package

2. **Install and start Jenkins:**
   ```bash
   # Option 1: If using .war file
   java -jar jenkins.war --httpPort=8080

   # Option 2: If installed as a service (Windows)
   # Jenkins starts automatically at http://localhost:8080
   ```

3. **Initial setup:**
   - Open **http://localhost:8080** in your browser
   - Find the initial admin password:
     ```bash
     # Windows:
     type "C:\Users\<YourUsername>\.jenkins\secrets\initialAdminPassword"

     # Linux/macOS:
     cat ~/.jenkins/secrets/initialAdminPassword
     ```
   - Install **suggested plugins**
   - Create an admin user (e.g., `admin` / `admin123`)

#### Creating the Jenkins Pipeline Job

1. **Create a new job:**
   - Click **"New Item"** on Jenkins dashboard
   - Name: `ISRM_Security_Pipeline`
   - Type: **Pipeline**
   - Click **OK**

2. **Configure the pipeline:**
   - Scroll to **Pipeline** section
   - Definition: **Pipeline script from SCM**
   - SCM: **Git**
   - Repository URL: `https://github.com/gauravjaiswal12/ISRM_Group-4.git`
   - Branch Specifier: `*/main` (for vulnerable) or `*/fixed-version` (for fixed)
   - Script Path: `Jenkinsfile`
   - Click **Save**

3. **Run the pipeline:**
   - Click **"Build Now"**
   - Watch the stages execute in real-time

#### Jenkins Pipeline Stages

The [`Jenkinsfile`](Jenkinsfile) defines a 5-stage pipeline:

| Stage | What It Does | Duration |
|-------|-------------|----------|
| **0. Checkout** | Clones the repository and cleans workspace | ~5 sec |
| **1. Build** | Creates venv, installs dependencies + Bandit | ~30 sec |
| **2. Security Scan** | Runs Bandit scan, generates JSON + HTML reports | ~10 sec |
| **3. Report Generation** | Creates vulnerability assessment CSV with CVSS scores | ~5 sec |
| **4. Security Gate** | Checks for CVSS > 5 vulnerabilities — PASS or FAIL | ~3 sec |

#### Expected Pipeline Results

**On `main` branch:** ❌ **BUILD FAILS**
```
[!] High risk vulnerability: B608 (CVSS 9.0) in database.py
[!] High risk vulnerability: B105 (CVSS 8.0) in config.py
Build FAILED due to CVSS > 5 vulnerabilities
```

**On `fixed-version` branch:** ✅ **BUILD PASSES**
```
Build PASSED (No CVSS > 5 vulnerabilities found)
[SUCCESS] Secure build passed - Code is safe for deployment!
```

---

### 4. Automated Vulnerability Testing

The included test suite simulates real attacks against the running application:

```bash
# Make sure the app is running in another terminal first!
python app.py

# In a new terminal, run the test suite
python test_vulnerabilities.py
```

This script tests:
| Test | What It Checks |
|------|---------------|
| `test_weak_credentials()` | Tries default admin/admin123 login |
| `test_sql_injection_login()` | Injects `' OR '1'='1` in login form |
| `test_sql_injection_search()` | SQL injection in search endpoint |
| `test_brute_force_protection()` | Sends 10 rapid login attempts |
| `test_file_upload()` | Uploads `.exe`, `.sh`, `.php` files |
| `test_path_traversal()` | Tries to download `config.py` via path traversal |
| `test_missing_access_control()` | Checks if regular users can access admin pages |
| `test_sensitive_data_exposure()` | Checks if SSN is visible in student list |
| `test_session_security()` | Checks cookie security flags |
| `test_information_disclosure()` | Looks for debug info in responses |

---

## 🔍 Vulnerability Comparison

| Metric | Vulnerable (`main`) | Fixed (`fixed-version`) | Improvement |
|--------|---------------------|------------------------|-------------|
| **Jenkins Build** | ❌ FAILURE | ✅ SUCCESS | Security gate works |
| **Bandit HIGH/CRITICAL** | 6 issues | 0 issues | **100% reduction** |
| **ZAP High Alerts** | 1 | 0 | **SQL Injection fixed** |
| **SQL Injection** | ✅ Exploitable | ❌ Blocked | Parameterized queries |
| **Debug Mode** | ON (info leak) | OFF (secure) | Config hardened |
| **CSRF Protection** | None | Token-based | CSRF tokens added |
| **Path Traversal** | ✅ Exploitable | ❌ Blocked | Input validation |
| **File Upload** | Allows `.exe` | Safe types only | Extension whitelist |
| **Rate Limiting** | None | 5 attempts / 5 min | Brute-force blocked |
| **Session Security** | Insecure cookies | Secure flags set | HttpOnly + SameSite |

---

## 📁 Project Structure

```
ISRM_Group-4/
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── .gitignore                   # Git ignore rules
├── Jenkinsfile                  # CI/CD pipeline definition
├── LICENSE                      # MIT License
├── csrf_attack.html             # CSRF attack demonstration
│
├── app.py                       # Main Flask application
├── config.py                    # Application configuration
├── database.py                  # Database operations module
├── generate_vulnerability_report.py  # CSV report generator script
├── test_vulnerabilities.py      # Automated vulnerability test suite
│
├── templates/                   # Jinja2 HTML templates
│   ├── base.html                # Base layout (shared across pages)
│   ├── login.html               # Login page
│   ├── dashboard.html           # Admin/User dashboard
│   ├── students.html            # Student list view
│   ├── student_detail.html      # Individual student details
│   ├── student_profile.html     # Student self-service profile
│   ├── student_grades.html      # Student grades view
│   ├── add_student.html         # Add new student form
│   ├── search.html              # Search students
│   ├── upload.html              # File upload page
│   ├── logs.html                # System activity logs
│   ├── 404.html                 # Not found error page
│   └── 500.html                 # Server error page
│
├── static/                      # Static assets
│   └── style.css                # Application stylesheet
│
├── reports/                     # Security scan reports
│   ├── bandit_report.html       # Bandit SAST report (HTML)
│   ├── bandit_report.json       # Bandit SAST report (JSON)
│   ├── zap_report.html          # OWASP ZAP report (vulnerable)
│   ├── zap_report_fixed.html    # OWASP ZAP report (fixed)
│   └── vulnerability_assessment.csv  # CVSS-scored findings
│
├── docs/                        # Project documentation
│   ├── VULNERABILITIES.md       # Detailed vulnerability catalog
│   ├── SECURITY_FIXES.md        # Remediation details (fixed branch)
│   ├── DEMO_GUIDE.md            # Step-by-step demo instructions
│   └── ISRM_Architecture.pdf    # System architecture diagram
│
├── ci/                          # CI/CD configuration
│   ├── jenkins_vulnerable_config.xml  # Jenkins job (vulnerable scan)
│   └── jenkins_fixed_config.xml       # Jenkins job (fixed scan)
│
└── uploads/                     # File upload directory (runtime)
    └── .gitkeep
```

---

## 🛠️ Technology Stack

| Category | Tool | Version | Purpose |
|----------|------|---------|---------|
| **Backend** | Flask | 2.3.0 | Web application framework |
| **Database** | SQLite | Built-in | Lightweight relational database |
| **Templating** | Jinja2 | Built-in with Flask | HTML template rendering |
| **SAST** | Bandit | Latest | Python static security analysis |
| **DAST** | OWASP ZAP | 2.14+ | Dynamic web application security testing |
| **CI/CD** | Jenkins | 2.400+ | Automated build and security pipeline |
| **VCS** | Git + GitHub | Latest | Version control and collaboration |
| **Runtime** | Python | 3.9+ | Application runtime environment |

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [VULNERABILITIES.md](docs/VULNERABILITIES.md) | Complete catalog of 14 intentional vulnerabilities with CWE IDs, CVSS scores, attack examples, and STRIDE mappings |
| [SECURITY_FIXES.md](docs/SECURITY_FIXES.md) | Detailed before/after code comparisons for every fix applied in the `fixed-version` branch |
| [DEMO_GUIDE.md](docs/DEMO_GUIDE.md) | Step-by-step demo instructions with commands, expected output, and talking points |
| [ISRM_Architecture.pdf](docs/ISRM_Architecture.pdf) | Visual architecture diagram of the system and security pipeline |

---

## ❓ Troubleshooting

### Common Issues and Solutions

| Problem | Cause | Solution |
|---------|-------|----------|
| `ModuleNotFoundError: No module named 'flask'` | Virtual env not activated or dependencies not installed | Run `venv\Scripts\activate` then `pip install -r requirements.txt` |
| `Address already in use` on port 5000 | Another app is using port 5000 | Stop the other app or change port in `app.py` |
| Database errors after switching branches | Different schema between branches | Delete `vulnerable_app.db` and restart the app |
| Jenkins can't find Python | Python not in system PATH | Set the `PYTHON_PATH` variable in Jenkinsfile to your Python path |
| ZAP scan shows 0 results | App not running during scan | Start the app first, then run ZAP scan |
| `bandit: command not found` | Bandit not installed | Run `pip install bandit` |
| Permission denied on Windows | PowerShell execution policy | Run `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned` |
| Login not working after DB reset | Database not re-initialized | Delete `vulnerable_app.db`, restart app — default credentials are recreated |

---

## 👥 Team — Group 4

<!-- Add team members here -->
| Name | Role |
|------|------|
| *Team Member 1* | *Role* |
| *Team Member 2* | *Role* |
| *Team Member 3* | *Role* |
| *Team Member 4* | *Role* |

---

## ⚠️ Disclaimer

> This application is provided **solely for authorized security testing and educational purposes**. The vulnerable version (`main` branch) contains **serious security flaws** — do **NOT** deploy it to production or expose it to untrusted networks. Unauthorized access to computer systems is illegal.

---

## 📖 References

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Common Weakness Enumeration (CWE)](https://cwe.mitre.org/)
- [STRIDE Threat Modeling](https://en.wikipedia.org/wiki/STRIDE_(security))
- [CVSS v3.1 Calculator](https://www.first.org/cvss/calculator/3.1)
- [Bandit Documentation](https://bandit.readthedocs.io/)
- [OWASP ZAP](https://www.zaproxy.org/)
- [Jenkins Documentation](https://www.jenkins.io/doc/)
- [Flask Documentation](https://flask.palletsprojects.com/)

---

## 📝 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.
