# ISRM Project — Teacher Demo Guide 🎓

> Follow these steps **in order**. Each step includes the command and what to say.

---

## PART A — Vulnerable Version (main branch)

---

### Step 1 — Start the Vulnerable App

```powershell
cd c:\Users\gaura\Downloads\ISRM
git checkout main
.\venv\Scripts\python.exe app.py
```

> **App runs at:** http://127.0.0.1:5000

### 🗣️ What to say:
> *"This is a Student Management System built with Flask. The main branch is intentionally designed with security vulnerabilities for research purposes."*

---

### Step 2 — Show the App

Open browser → http://127.0.0.1:5000 → Login as Admin:

| Field | Value |
|-------|-------|
| Username | `admin` |
| Password | `admin123` |

Show: Dashboard, Student list, Upload page, Logs.

---

### Step 3 — Demo SQL Injection Attack

Logout → On the Login page enter:

| Field | Value |
|-------|-------|
| Username | `' OR '1'='1` |
| Password | `' OR '1'='1` |

**It bypasses login!** You get in without valid credentials.

### 🗣️ What to say:
> *"This SQL Injection attack works because the login form directly concatenates user input into SQL queries without sanitization. This is a Critical vulnerability with CVSS score 9.0."*

---

### Step 4 — Run Bandit SAST Scan

**Open new PowerShell** (keep app running):

```powershell
cd c:\Users\gaura\Downloads\ISRM
.\venv\Scripts\bandit.exe -r . -x ./venv -f screen
```

**Result:** 7 issues found (4 Critical, 2 High, 1 Medium)

### 🗣️ What to say:
> *"Bandit is a Static Analysis tool — it reads the source code without running the app. It found 4 Critical SQL injections in database.py, hardcoded credentials in config.py, and debug mode enabled in app.py."*

---

### Step 5 — Show Jenkins Pipeline (Vulnerable = FAILS ❌)

Open browser → http://localhost:8080 → Login: `admin` / `admin123`

Click **ISRM_Security_Pipeline** → click build number → see stages

**Key message in console:** `VULNERABILITIES FOUND - marking build as FAILED`

### 🗣️ What to say:
> *"Jenkins runs the same Bandit scan automatically. The pipeline has 5 stages. The Security Gate at the end checks for HIGH or CRITICAL vulnerabilities — since it finds them, the build FAILS. This prevents vulnerable code from being deployed."*

---

### Step 6 — Show OWASP ZAP Report (Vulnerable)

Open: `c:\Users\gaura\Downloads\ISRM\reports\zap_report.html`

**ZAP found:**
| Risk | Count |
|------|-------|
| 🔴 High | **1** (SQL Injection) |
| 🟠 Medium | **5** |
| 🟡 Low | **2** |
| 🔵 Info | **2** |

### 🗣️ What to say:
> *"OWASP ZAP is a Dynamic Analysis tool — it actually attacks the running application. It confirmed the SQL Injection by exploiting it, and found missing security headers like CSRF tokens and Content Security Policy."*

---

## PART B — Fixed Version (fixed-version branch)

---

### Step 7 — Switch to Fixed Version

Stop the app (Ctrl+C), then:

```powershell
git stash
git checkout fixed-version
.\venv\Scripts\pip.exe install -r requirements.txt
.\venv\Scripts\python.exe app.py
```

> Notice: **Debug mode: OFF** now (one of the fixes!)

---

### Step 8 — Try the Same SQL Injection (It FAILS now!)

Open browser → http://127.0.0.1:5000 → Enter the same payload:

| Field | Value |
|-------|-------|
| Username | `' OR '1'='1` |
| Password | `' OR '1'='1` |

**It does NOT work!** Login fails with "Invalid credentials."

### 🗣️ What to say:
> *"The fixed version uses parameterized queries instead of string concatenation. The SQL injection payload is now treated as literal text, not SQL code. The attack is completely blocked."*

---

### Step 9 — Show Jenkins Pipeline (Fixed = PASSES ✅)

Open browser → http://localhost:8080

Click **ISRM_Fixed_Pipeline** → click build #1 → see stages

**Key message:** `No HIGH/CRITICAL vulnerabilities found - BUILD PASSES`

**Result:** `[SUCCESS] Secure build passed - Code is safe for deployment!`

### 🗣️ What to say:
> *"The exact same pipeline, same Bandit scan, same security gate — but on the fixed code. This time all stages pass and the build is marked SUCCESS. The code is now safe for deployment."*

---

### Step 10 — Show OWASP ZAP Report (Fixed)

Open: `c:\Users\gaura\Downloads\ISRM\reports\zap_report_fixed.html`

**ZAP found:**
| Risk | Count |
|------|-------|
| 🔴 High | **0** ← was 1 |
| 🟠 Medium | **5** |
| 🟡 Low | **1** ← was 2 |
| 🔵 Info | **5** |

### 🗣️ What to say:
> *"ZAP no longer finds the SQL Injection — it's been fixed. The remaining Medium alerts are mostly CSP header refinements which are configuration-level, not code vulnerabilities."*

---

### Step 11 — Switch Back to Main (for further demo if needed)

```powershell
# Stop the app (Ctrl+C)
git checkout main
git stash pop
.\venv\Scripts\python.exe app.py
```

---

## THE KEY COMPARISON TABLE

Show this to your teacher — this is the research finding:

| Metric | Vulnerable (`main`) | Fixed (`fixed-version`) | Improvement |
|--------|-------------------|----------------------|-------------|
| **Jenkins Build** | ❌ FAILURE | ✅ SUCCESS | Security gate works |
| **Bandit HIGH/CRITICAL** | 6 issues | 0 issues | **100% reduction** |
| **ZAP High Alerts** | 1 | 0 | **SQL Injection fixed** |
| **ZAP Medium Alerts** | 5 | 5 | Header config remaining |
| **SQL Injection** | ✅ Exploitable | ❌ Blocked | Parameterized queries |
| **Debug Mode** | ON (info leak) | OFF (secure) | Config hardened |
| **CSRF Protection** | None | Added | CSRF tokens added |
| **Path Traversal** | ✅ Exploitable | ❌ Blocked | Input validation |

---

## Quick Reference — All Commands

### Vulnerable Version
```powershell
cd c:\Users\gaura\Downloads\ISRM
git checkout main
.\venv\Scripts\python.exe app.py                              # Start app
.\venv\Scripts\bandit.exe -r . -x ./venv -f screen            # Run Bandit
.\venv\Scripts\python.exe generate_vulnerability_report.py     # Generate CSV
# Jenkins: http://localhost:8080 → ISRM_Security_Pipeline
# ZAP report: reports\zap_report.html
```

### Fixed Version
```powershell
cd c:\Users\gaura\Downloads\ISRM
git stash
git checkout fixed-version
.\venv\Scripts\python.exe app.py                              # Start app
.\venv\Scripts\bandit.exe -r . -x ./venv -f screen            # Run Bandit
# Jenkins: http://localhost:8080 → ISRM_Fixed_Pipeline
# ZAP report: reports\zap_report_fixed.html
```

### Switch Back
```powershell
git checkout main
git stash pop
```

---

## 5 Key Talking Points

1. **SAST vs DAST** — Bandit scans code (static), ZAP attacks the running app (dynamic). Both are needed for complete coverage.
2. **Security Gate** — Jenkins automatically blocks vulnerable code from reaching production. Vulnerable branch FAILS, fixed branch PASSES.
3. **Parameterized Queries** — The #1 fix: using `?` placeholders instead of f-strings in SQL queries eliminates SQL injection.
4. **Defense in Depth** — The fixed version adds CSRF tokens, input validation, debug mode off, secure headers — multiple layers of security.
5. **DevSecOps** — This pipeline mirrors real industry practices: automated SAST + DAST + CI/CD gates = security built into the development process.
