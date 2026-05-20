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

> ⚠️ **You are on the `main` branch — this is the VULNERABLE version.**
> This branch contains **14 intentional security vulnerabilities** for educational and research purposes.
> Switch to the [`fixed-version`](../../tree/fixed-version) branch to see the secure implementation.

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

## 🌿 Branch Strategy

| Branch | Purpose | Jenkins Result |
|--------|---------|----------------|
| **`main`** ← _you are here_ | Vulnerable version — contains 14 intentional security flaws | ❌ **BUILD FAILS** (Security Gate blocks deployment) |
| **`fixed-version`** | Secure version — all critical/high vulnerabilities remediated | ✅ **BUILD PASSES** (Code is safe for deployment) |

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
python app.py
```

The application runs at **http://127.0.0.1:5000** (or `http://0.0.0.0:5000` on this vulnerable branch).

### Test Credentials

| Role | Username | Password |
|------|----------|----------|
| Admin | `admin` | `admin123` |
| User | `user` | `password` |
| Student | `john_student` | `student123` |

---

## 🔴 Vulnerabilities in This Branch

This branch contains **14 intentional security vulnerabilities**:

| # | Vulnerability | CWE | CVSS | Severity |
|---|---|---|---|---|
| 1 | SQL Injection (4 locations) | CWE-89 | 9.0 | **Critical** |
| 2 | Brute Force / Credential Stuffing | CWE-307 | 7.5 | High |
| 3 | Weak Authentication / Hardcoded Credentials | CWE-798 | 8.2 | High |
| 4 | Insecure Password Storage | CWE-256 | 8.0 | High |
| 5 | Sensitive Data Exposure | CWE-200 | 8.1 | High |
| 6 | Insecure File Upload | CWE-434 | 8.5 | High |
| 7 | Path Traversal | CWE-22 | 7.5 | High |
| 8 | Session Hijacking | CWE-384 | 8.0 | High |
| 9 | Cross-Site Request Forgery (CSRF) | CWE-352 | 7.0 | High |
| 10 | Information Disclosure | CWE-209 | 6.5 | Medium |
| 11 | Missing Access Control | CWE-284 | 7.2 | High |
| 12 | Privilege Escalation | CWE-269 | 8.8 | High |
| 13 | Command Injection (Potential) | CWE-78 | 9.0 | Critical |
| 14 | Insecure Deserialization | CWE-502 | 6.0 | Medium |

> 📄 See [docs/VULNERABILITIES.md](docs/VULNERABILITIES.md) for detailed descriptions, attack examples, and STRIDE mappings.

### SQL Injection Demo

```
Username: ' OR '1'='1
Password: ' OR '1'='1
→ Bypasses authentication!
```

---

## 🔍 Vulnerability Comparison (main vs. fixed-version)

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

---

## 📁 Project Structure

```
ISRM_Group-4/  (main branch)
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── .gitignore                   # Git ignore rules
├── Jenkinsfile                  # CI/CD pipeline definition
├── LICENSE                      # MIT License
├── csrf_attack.html             # CSRF attack demonstration
│
├── app.py                       # Main Flask app (VULNERABLE)
├── config.py                    # Configuration (VULNERABLE)
├── database.py                  # Database operations (VULNERABLE)
├── generate_vulnerability_report.py  # CSV report generator
├── test_vulnerabilities.py      # Automated vulnerability test suite
│
├── templates/                   # Jinja2 HTML templates
│   ├── base.html, login.html, dashboard.html, ...
│
├── static/                      # Static assets
│   └── style.css
│
├── reports/                     # Security scan reports
│   ├── bandit_report.html       # Bandit SAST findings
│   ├── zap_report.html          # OWASP ZAP findings
│   └── ...
│
├── docs/                        # Documentation
│   ├── VULNERABILITIES.md       # Detailed vulnerability catalog
│   └── DEMO_GUIDE.md            # Demo walkthrough
│
└── uploads/                     # File upload directory (runtime)
```

---

## 🛡️ Security Scanning

### SAST — Bandit

```bash
pip install bandit
bandit -r . -x ./venv -f screen
```

**Expected output:** 7 issues (4 Critical, 2 High, 1 Medium)

### DAST — OWASP ZAP

Scan report: [`reports/zap_report.html`](reports/zap_report.html)

---

## 🛠️ Technology Stack

| Category | Tool | Purpose |
|----------|------|---------|
| **Backend** | Flask 2.3 | Web application framework |
| **Database** | SQLite | Lightweight relational database |
| **SAST** | Bandit | Python static security analysis |
| **DAST** | OWASP ZAP | Dynamic web application security testing |
| **CI/CD** | Jenkins | Automated build and security pipeline |

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

> This application is provided **solely for authorized security testing and educational purposes**. It contains **serious security flaws** — do **NOT** deploy it to production or expose it to untrusted networks. Unauthorized access to computer systems is illegal.

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
