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

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- pip (Python package manager)
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/gauravjaiswal12/ISRM_Group-4.git
cd ISRM_Group-4

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Application

```bash
# Run the vulnerable version (main branch)
git checkout main
python app.py

# Run the fixed version
git checkout fixed-version
python app.py
```

The application runs at **http://127.0.0.1:5000**

### Test Credentials

| Role | Username | Password |
|------|----------|----------|
| Admin | `admin` | `admin123` |
| User | `user` | `password` |
| Student | `john_student` | `student123` |

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

## 🛡️ Security Scanning

### SAST — Bandit (Static Analysis)

```bash
# Install Bandit
pip install bandit

# Run scan (exclude virtual environment)
bandit -r . -x ./venv -f screen
```

### DAST — OWASP ZAP (Dynamic Analysis)

Pre-generated scan reports are available in the [`reports/`](reports/) directory:
- [`zap_report.html`](reports/zap_report.html) — Vulnerable version scan
- [`zap_report_fixed.html`](reports/zap_report_fixed.html) — Fixed version scan

### CI/CD — Jenkins Pipeline

The [`Jenkinsfile`](Jenkinsfile) defines a 5-stage pipeline:

1. **Checkout** — Pull source code
2. **Build** — Set up virtual environment and install dependencies
3. **Security Scan** — Run Bandit SAST scan, generate JSON + HTML reports
4. **Report Generation** — Create vulnerability assessment CSV with CVSS scores
5. **Security Gate** — Fail the build if any vulnerability has CVSS > 5.0

---

## 📁 Project Structure

```
ISRM_Group-4/
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── .gitignore                   # Git ignore rules
├── Jenkinsfile                  # CI/CD pipeline definition
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

| Category | Tool | Purpose |
|----------|------|---------|
| **Backend** | Flask 2.3 | Web application framework |
| **Database** | SQLite | Lightweight relational database |
| **SAST** | Bandit | Python static security analysis |
| **DAST** | OWASP ZAP | Dynamic web application security testing |
| **CI/CD** | Jenkins | Automated build and security pipeline |
| **VCS** | Git + GitHub | Version control and collaboration |

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [VULNERABILITIES.md](docs/VULNERABILITIES.md) | Complete catalog of 14 intentional vulnerabilities with CWE IDs, CVSS scores, attack examples, and STRIDE mappings |
| [SECURITY_FIXES.md](docs/SECURITY_FIXES.md) | Detailed before/after code comparisons for every fix applied in the `fixed-version` branch |
| [DEMO_GUIDE.md](docs/DEMO_GUIDE.md) | Step-by-step demo instructions with commands, expected output, and talking points |
| [ISRM_Architecture.pdf](docs/ISRM_Architecture.pdf) | Visual architecture diagram of the system and security pipeline |

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

---

## 📝 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.
