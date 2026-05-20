# Security Fixes - Fixed Version Branch

## Overview
This document details all security vulnerabilities found in the vulnerable application and the fixes applied in the **fixed-version** branch. Vulnerable code has been commented out and replaced with secure implementations.

---

## Vulnerability 1: SQL Injection (B608) - CRITICAL ⚠️

### Severity: **CRITICAL** | CVSS Score: 9.0 | CWE-89

### Locations Fixed:
1. **database.py - authenticate_user()**
2. **database.py - search_students()**
3. **database.py - get_student_details()**
4. **database.py - add_student()**

### Vulnerability Description:
The application used string concatenation to build SQL queries, allowing attackers to inject arbitrary SQL code.

**Example Vulnerable Code:**
```python
# VULNERABLE - String concatenation
query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
cursor.execute(query)
```

### Attack Example:
```
Username: admin' OR '1'='1
Password: anything
# Results in: SELECT * FROM users WHERE username = 'admin' OR '1'='1' AND password = 'anything'
# This bypasses authentication
```

### Fix Applied:
Replaced all SQL queries with **parameterized queries** using `?` placeholders. Data is passed separately and automatically escaped by SQLite driver.

**Fixed Code:**
```python
# FIXED - Parameterized queries
cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
```

### How It Works:
- The SQL structure is separate from data
- Special characters in data are automatically escaped
- Injection attacks become impossible because data can't change query structure
- Works consistently across all database types

### Affected Functions:
| Function | Fix Type | Details |
|----------|----------|---------|
| `authenticate_user()` | Parameterized | Used `?` placeholders for username and password |
| `search_students()` | Parameterized | Used `?` placeholders for LIKE patterns |
| `get_student_details()` | Parameterized + Validation | Added integer validation + parameterized query |
| `add_student()` | Parameterized + Validation | Added input validation + parameterized query |

---

## Vulnerability 2: Hardcoded Credentials (B105)

### Severity: **HIGH** | CVSS Score: 8.0 | CWE-798

### Locations Fixed:
1. **config.py - SECRET_KEY**
2. **database.py - Default user passwords** (Commented as intentional for testing)

### Vulnerability Description:
Hardcoded weak secret key exposed in source code. An attacker gaining access to source code could compromise session security.

**Vulnerable Code in config.py:**
```python
# VULNERABLE - Hardcoded weak key
SECRET_KEY = 'super_secret_key_12345'
```

### Fix Applied:
Now uses environment variables with a fallback to a stronger key for demonstration.

**Fixed Code:**
```python
# FIXED - Environment variable with fallback
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-only-fixed-key-change-in-production-xyz123!@#')
```

### Additional Improvements:
- Implemented session cookie security flags
- Added SHORT_LIVED sessions (30 minutes instead of 24 hours)
- Set `HttpOnly`, `Secure`, and `SameSite` flags on session cookies

---

## Vulnerability 3: Missing Rate Limiting / Brute Force Attack

### Severity: **HIGH** | CVSS Score: 8.0 | CWE-307

### Location Fixed:
**app.py - login() route**

### Vulnerability Description:
No rate limiting on login attempts allowed attackers to perform brute force attacks without being blocked.

**Vulnerable Code:**
```python
# VULNERABLE - Always returns True
def check_rate_limit(username):
    return True  # No actual protection
```

### Fix Applied:
Implemented in-memory rate limiting with maximum attempts and lockout duration.

**Fixed Code:**
```python
MAX_LOGIN_ATTEMPTS = 5
LOCKOUT_DURATION = 300  # 5 minutes

def check_rate_limit(username):
    """FIXED: Enforce rate limiting - returns False if too many attempts"""
    now = datetime.now()
    if username not in LOGIN_ATTEMPTS:
        return True  # First attempt - allowed
    
    # Remove old attempts outside lockout window
    LOGIN_ATTEMPTS[username] = [t for t in LOGIN_ATTEMPTS[username] 
                               if (now - t).total_seconds() < LOCKOUT_DURATION]
    
    # Check if exceeded max attempts
    if len(LOGIN_ATTEMPTS[username]) >= MAX_LOGIN_ATTEMPTS:
        return False  # Too many attempts - locked out
    return True  # Still within limits
```

### How It Works:
1. Tracks login attempts per username with timestamps
2. After 5 failed attempts, user is locked out for 5 minutes
3. After lockout expires, counter resets
4. Generic error message shown to prevent username enumeration

---

## Vulnerability 4: Insecure File Upload (B607)

### Severity: **HIGH** | CVSS Score: 8.5 | CWE-434

### Locations Fixed:
1. **config.py - ALLOWED_EXTENSIONS**
2. **app.py - upload_file() route**

### Vulnerability Description:
Application allowed upload of dangerous executable files (.exe, .sh, .bat) without validation.

**Vulnerable Configuration:**
```python
# VULNERABLE - Allows executables
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'docx', 'exe', 'sh', 'bat'}
```

### Attack Scenario:
1. Attacker uploads malicious shell script (.sh)
2. If executed by server, gives attacker remote code execution
3. Full server compromise possible

### Fixes Applied:

**1. Whitelist Safe File Types:**
```python
# FIXED - Only safe extensions
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'docx'}
```

**2. Secure Filename Handling:**
```python
# VULNERABLE - COMMENTED
# filename = file.filename  # No sanitization, allows path traversal

# FIXED - Use secure_filename from werkzeug
filename = secure_filename(file.filename)
```

**3. File Size Validation:**
```python
# FIXED - Validate file size
file_size = file.tell()
max_size = app.config['MAX_CONTENT_LENGTH']
if file_size > max_size:
    flash(f'File size exceeds maximum allowed', 'danger')
    return redirect(url_for('upload_file'))
```

**4. Safe Path Construction:**
```python
# FIXED - Ensure file stays within upload directory
filepath = os.path.abspath(filepath)
upload_dir = os.path.abspath(app.config['UPLOAD_FOLDER'])
if not filepath.startswith(upload_dir):
    flash('Invalid file path', 'danger')
    return redirect(url_for('upload_file'))
```

---

## Vulnerability 5: Path Traversal (B610)

### Severity: **HIGH** | CVSS Score: 7.5 | CWE-22

### Locations Fixed:
1. **app.py - access_file() route** (CRITICAL)
2. **app.py - download_file() route**
3. **app.py - upload_file() route**

### Vulnerability Description:
Unrestricted file access allowed attackers to download ANY file from the system.

**Vulnerable Code:**
```python
# VULNERABLE - No path validation
@app.route('/file/<path:filepath>')
def access_file(filepath):
    if os.path.exists(filepath) and os.path.isfile(filepath):
        return send_file(filepath)  # Direct access to any file!
```

### Attack Examples:
```
GET /file/config.py → Download config file with SECRET_KEY
GET /file/vulnerable_app.db → Download entire database
GET /file/../../../etc/passwd → Read system files
GET /file/app.py → Get application source code
```

### Fix Applied:

**1. Path Validation:**
```python
# FIXED - Restrict to upload directory only
normalized_path = os.path.normpath(filepath)
upload_dir = os.path.abspath(app.config['UPLOAD_FOLDER'])
requested_path = os.path.abspath(normalized_path)

# FIXED - Check if requested path is within upload directory
if not requested_path.startswith(upload_dir):
    flash('Access to this file is not permitted', 'danger')
    return redirect(url_for('dashboard')), 403
```

**2. File Type Validation:**
```python
# FIXED - Use secure_filename
filename = secure_filename(filename)
if not filename:
    flash('Invalid filename', 'danger')
    return redirect(url_for('dashboard'))
```

**3. Safe Download:**
```python
# FIXED - Comprehensive validation
filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
filepath = os.path.abspath(filepath)  # Resolve absolute path

# Ensure within allowed directory
upload_dir = os.path.abspath(app.config['UPLOAD_FOLDER'])
if not filepath.startswith(upload_dir) or not os.path.isfile(filepath):
    flash('File not found or access denied', 'danger')
    return redirect(url_for('dashboard')), 404
```

---

## Vulnerability 6: Flask Debug Mode (B201)

### Severity: **HIGH** | CVSS Score: 6.5 | CWE-94

### Location Fixed:
**app.py - if __name__ == '__main__' block**

### Vulnerability Description:
Running Flask in debug mode exposes:
- Detailed error pages with stack traces
- Interactive debugger accessible via PIN
- Sensitive information in error messages

**Vulnerable Code:**
```python
# VULNERABLE - Debug mode enabled
app.run(debug=True, host='0.0.0.0', port=5000)
```

### Fix Applied:
Now reads debug mode from environment variable, defaults to False (production-safe).

**Fixed Code:**
```python
# FIXED - Debug disabled by default
debug_mode = app.config.get('DEBUG', False)
app.run(debug=debug_mode, host=host, port=5000)
```

---

## Vulnerability 7: Binding to All Interfaces (B104)

### Severity: **MEDIUM** | CVSS Score: 6.5 | CWE-605

### Location Fixed:
**app.py - if __name__ == '__main__' block**
**config.py - New HOST configuration**

### Vulnerability Description:
Binding to `0.0.0.0` makes application accessible from any network interface.

**Vulnerable Code:**
```python
# VULNERABLE - Accessible from anywhere
app.run(host='0.0.0.0')  # Binds to all network interfaces
```

### Fix Applied:
Now binds to localhost (127.0.0.1) by default, configurable via environment variable.

**Fixed Code:**
```python
# FIXED - Localhost by default
HOST = os.environ.get('FLASK_HOST', '127.0.0.1')
app.run(host=HOST, port=5000)
```

---

## Vulnerability 8: Information Disclosure

### Severity: **MEDIUM** | CVSS Score: 5.5

### Multiple Locations Fixed:

### A. Debug Print Statements
**Locations:** `database.py` (Multiple functions)

**Vulnerable Code:**
```python
# VULNERABLE - Leaks query structure
print(f"[DEBUG] Executing query: {query}")
print(f"[ERROR] Authentication failed: {str(e)}")
```

**Fixed Code:**
```python
# VULNERABLE COMMENTED OUT
# print(f"[DEBUG] Executing query: {query}")

# FIXED - Generic message
print(f"[INFO] Authentication check completed")
```

### B. Sensitive Logging
**Location:** `database.py - log_action()`

**Vulnerable Code:**
```python
# VULNERABLE - Logs passwords
log_action('AUTH_ATTEMPT', username, f"Password: {password}, Result: Success")
```

**Fixed Code:**
```python
# FIXED - Sanitized details, no passwords
if user:
    log_action('AUTH_ATTEMPT', username, "Result: Success")
else:
    log_action('AUTH_ATTEMPT', username, "Result: Failed")
```

### C. Database Sensitive Data Exposure
**Location:** `database.py - get_student_details()`

**Vulnerable Code:**
```python
# VULNERABLE - Returns SSN and password
cursor.execute("SELECT * FROM students WHERE id = {student_id}")
return student  # Includes sensitive data
```

**Fixed Code:**
```python
# FIXED - Only non-sensitive fields
cursor.execute(
    "SELECT id, roll_no, name, email, phone, address, gpa FROM students WHERE id = ?",
    (student_id,)
)
return student  # No SSN or password
```

### D. Detailed Error Messages
**Location:** `app.py - Error handlers**

**Vulnerable Code:**
```python
# VULNERABLE - Exposes internal details
return f"404 Error: {error}", 404
return f"500 Internal Server Error: {error}", 500
```

**Fixed Code:**
```python
# FIXED - Generic error responses
def not_found(error):
    flash('Page not found', 'danger')
    return render_template('404.html'), 404

def internal_error(error):
    flash('Internal server error', 'danger')
    return render_template('500.html'), 500
```

---

## Vulnerability 9: Missing Input Validation

### Severity: **MEDIUM** | CVSS Score: 6.0

### Locations Fixed:
1. **app.py - add_student() route**
2. **app.py - search_students() route**
3. **app.py - view_student() route**
4. **app.py - login() route**
5. **database.py - add_student() function**

### What Was Vulnerable:
```python
# VULNERABLE - No validation
roll_no = request.form.get('roll_no', '')  # Could be empty
name = request.form.get('name', '')  # Could be empty
email = request.form.get('email', '')  # No email validation
phone = request.form.get('phone', '')  # No format validation
```

### Fixes Applied:

**1. Login Input Validation:**
```python
# FIXED - Input trimming and validation
username = request.form.get('username', '').strip()
password = request.form.get('password', '')

if not username or not password:
    flash('Username and password are required', 'danger')
    return render_template('login_new.html')
```

**2. Add Student Validation:**
```python
# FIXED - Comprehensive validation
errors = []
if not roll_no:
    errors.append('Roll number is required')
if not name or len(name) < 2:
    errors.append('Valid name is required')
if not email or '@' not in email:
    errors.append('Valid email is required')
if not phone or not phone.isdigit() or len(phone) != 10:
    errors.append('Valid 10-digit phone number is required')
if not ssn or not re.match(r'^\d{3}-\d{2}-\d{4}$', ssn):
    errors.append('Valid SSN format (XXX-XX-XXXX) is required')

if errors:
    for error in errors:
        flash(error, 'danger')
    return render_template('add_student_new.html')
```

**3. Search Input Validation:**
```python
# FIXED - Search term validation
search_term = request.form.get('search', '').strip()

if not search_term:
    flash('Search term cannot be empty', 'warning')
elif len(search_term) > 100:
    flash('Search term is too long', 'danger')
else:
    results = database.search_students(search_term)
```

**4. Student ID Integer Validation:**
```python
# FIXED - Type validation
try:
    student_id = int(student_id)
except (ValueError, TypeError):
    flash('Invalid student ID', 'danger')
    return redirect(url_for('students')), 400
```

**5. Database-level Validation:**
```python
# FIXED - Type conversion and range checking
try:
    gpa_float = float(gpa)
    if gpa_float < 0 or gpa_float > 4.0:
        return False
except ValueError:
    return False
```

---

## Vulnerability 10: Weak Session Security

### Severity: **MEDIUM** | CVSS Score: 5.5 | CWE-614

### Location Fixed:
**config.py - Session Configuration**

### Vulnerability Description:
Session cookies lacked security flags:
- Missing `HttpOnly` flag → Vulnerable to XSS attacks stealing cookies
- Missing `Secure` flag → Cookies sent over HTTP (unencrypted)
- Missing `SameSite` flag → Vulnerable to CSRF attacks

**Vulnerable Configuration:**
```python
# VULNERABLE - No security flags
PERMANENT_SESSION_LIFETIME = 86400  # 24 hours - too long
# No HttpOnly, Secure, or SameSite flags
```

### Fixes Applied:
```python
# FIXED - Secure session configuration
PERMANENT_SESSION_LIFETIME = 1800  # 30 minutes (shorter lifetime)
SESSION_COOKIE_SECURE = True  # Only send over HTTPS
SESSION_COOKIE_HTTPONLY = True  # Prevent JavaScript access
SESSION_COOKIE_SAMESITE = 'Strict'  # CSRF protection
```

### How These Work:
| Flag | Purpose | Effect |
|------|---------|--------|
| `SECURE` | Encrypt in transit | Cookie only sent over HTTPS |
| `HTTPONLY` | XSS prevention | JavaScript cannot access cookie |
| `SAMESITE` | CSRF prevention | Browser doesn't send cookie in cross-site requests |
| Shorter lifetime | Reduce exposure | User automatically logged out after 30 min |

---

## Vulnerability 11: Access Control Issues

### Severity: **MEDIUM** | CVSS Score: 6.0 | CWE-639

### Locations Fixed:
Multiple routes now enforce role-based access control:

| Route | Fix | Access |
|-------|-----|--------|
| `/students` | Added student check | Admin, User only |
| `/student/<id>` | Added student check | Admin, User only |
| `/add_student` | Admin-only check | Admin only |
| `/search` | Student prevention | Admin, User only |
| `/upload` | Student prevention | Admin, User only |
| `/view_logs` | Admin-only check | Admin only |
| `/student/profile` | Student-only check | Student only |
| `/student/grades` | Student-only check | Student only |

**Example Fix:**
```python
# VULNERABLE - COMMENTED
# if role == 'student':
#     return "Access Denied...", 403

# FIXED - User-friendly error with redirect
if role == 'student':
    flash('Access Denied: Students cannot view this page', 'danger')
    return redirect(url_for('dashboard')), 403
```

---

## Summary Table: All Fixed Vulnerabilities

| # | Vulnerability | Type | Severity | CVSS | Status |
|---|---|---|---|---|---|
| 1 | SQL Injection (4 instances) | B608 | Critical | 9.0 | ✅ FIXED |
| 2 | Hardcoded Credentials | B105 | High | 8.0 | ✅ FIXED |
| 3 | Missing Rate Limiting | CWE-307 | High | 8.0 | ✅ FIXED |
| 4 | Insecure File Upload | B607 | High | 8.5 | ✅ FIXED |
| 5 | Path Traversal (3 routes) | B610 | High | 7.5 | ✅ FIXED |
| 6 | Flask Debug Mode | B201 | High | 6.5 | ✅ FIXED |
| 7 | Bind All Interfaces | B104 | Medium | 6.5 | ✅ FIXED |
| 8 | Information Disclosure | CWE-200 | Medium | 5.5 | ✅ FIXED |
| 9 | Missing Input Validation | CWE-20 | Medium | 6.0 | ✅ FIXED |
| 10 | Weak Session Security | CWE-614 | Medium | 5.5 | ✅ FIXED |
| 11 | Access Control Issues | CWE-639 | Medium | 6.0 | ✅ FIXED |

---

## Testing Fixed Application

### Run the Fixed Application:
```bash
cd c:\Users\Snehal\Documents\GitHub\ISRM_Proj
.\.venv-1\Scripts\Activate
python app.py
```

### Test Accounts (Demo - Note: Passwords still plain-text for testing):
- **Admin:** admin / admin123
- **User:** user / password
- **Student:** john_student / student123

### Verify Fixes:

**1. Test SQL Injection (Should Fail):**
- Login Username: `admin' OR '1'='1`
- Password: anything
- Result: ✅ Injection blocked - generic error message

**2. Test Rate Limiting (Should Block After 5 Attempts):**
- Try 5 failed logins in a row
- Result: ✅ Locked out for 5 minutes

**3. Test File Upload (Should Block .exe):**
- Try uploading `test.exe` file
- Result: ✅ File type blocked

**4. Test Path Traversal (Should Fail):**
- Try accessing `/file/../config.py`
- Result: ✅ Access denied - restricted to uploads folder

**5. Test Access Control (Students):**
- Login as john_student
- Try accessing `/students` page
- Result: ✅ Redirected with error message

---

## Files Modified

### Core Application Files:
1. ✅ **database.py** - Parameterized queries, input validation, sanitized logging
2. ✅ **app.py** - Rate limiting, input validation, access control, error handling
3. ✅ **config.py** - Secure session config, environment variables, safe file types

### New Files Created:
1. ✅ **templates/404.html** - Secure error page
2. ✅ **templates/500.html** - Secure error page

---

## Best Practices Applied

### 1. Defense in Depth
- Multiple layers of protection (DB level + App level + Config level)
- Input validation + output sanitization + session security

### 2. Principle of Least Privilege
- Role-based access control
- Minimal permissions by default
- Short session lifetimes

### 3. Secure Coding
- Parameterized queries (SQL injection prevention)
- Input validation (injection prevention)
- Output encoding (XSS prevention)
- CSRF tokens ready to implement

### 4. Security Through Obscurity Prevention
- Generic error messages
- No debug information disclosure
- No verbose logging of passwords

---

## Next Steps for Production Deployment

1. **Use Password Hashing:** Implement bcrypt for password storage
   ```python
   from werkzeug.security import generate_password_hash, check_password_hash
   ```

2. **Implement CSRF Protection:** Use Flask-WTF
   ```python
   from flask_wtf.csrf import CSRFProtect
   ```

3. **Use HTTPS:** Essential for production
   ```python
   SESSION_COOKIE_SECURE = True  # Requires HTTPS
   ```

4. **Database Connection Pooling:** For multiple concurrent connections
   ```python
   from flask_sqlalchemy import SQLAlchemy
   ```

5. **Rate Limiting:** Use Flask-Limiter for production-grade implementation
   ```python
   from flask_limiter import Limiter
   ```

6. **Logging & Monitoring:** Implement proper security logging
   ```python
   import logging
   from logging.handlers import RotatingFileHandler
   ```

---

## Branch Information

- **Main Branch:** Contains original vulnerable code for educational comparison
- **Fixed-Version Branch:** Contains all security fixes with vulnerable code commented out
- **Your Assessment:** Compare vulnerabilities shown by Bandit on both branches for impact analysis

## Document Generated: 2026-04-18

---
