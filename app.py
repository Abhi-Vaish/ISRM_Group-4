# Main Flask Application - FIXED VERSION with Security Improvements
from flask import Flask, render_template, request, redirect, session, url_for, send_file, flash
from werkzeug.utils import secure_filename
import os
import database
from config import Config
from datetime import datetime, timedelta
import re
import secrets

app = Flask(__name__)
app.config.from_object(Config)

# FIXED: CSRF Protection - Manual implementation to avoid dependency issues
def generate_csrf_token():
    """Generate a secure CSRF token"""
    if '_csrf_token' not in session:
        session['_csrf_token'] = secrets.token_hex(32)
    return session['_csrf_token']

def validate_csrf_token(token):
    """Validate CSRF token from request"""
    if '_csrf_token' not in session:
        return False
    return secrets.compare_digest(token, session['_csrf_token'])

# Make csrf_token() available in all templates
@app.context_processor
def inject_csrf_token():
    return dict(csrf_token=generate_csrf_token)

# Initialize database
if not os.path.exists(database.DB_NAME):
    database.init_db()

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# FIXED: Rate limiting implementation to prevent brute force attacks
# VULNERABLE (COMMENTED): No rate limiting - allows unlimited brute force attempts
LOGIN_ATTEMPTS = {}
MAX_LOGIN_ATTEMPTS = 5
LOCKOUT_DURATION = 300  # 5 minutes in seconds

def record_login_attempt(username):
    """FIXED: Track login attempts with timestamp for rate limiting"""
    now = datetime.now()
    if username not in LOGIN_ATTEMPTS:
        LOGIN_ATTEMPTS[username] = []
    # Remove old attempts outside the lockout window
    LOGIN_ATTEMPTS[username] = [t for t in LOGIN_ATTEMPTS[username] if (now - t).total_seconds() < LOCKOUT_DURATION]
    LOGIN_ATTEMPTS[username].append(now)

def check_rate_limit(username):
    """FIXED: Enforce rate limiting - returns False if too many attempts"""
    now = datetime.now()
    if username not in LOGIN_ATTEMPTS:
        return True  # First attempt - allowed
    # Remove old attempts
    LOGIN_ATTEMPTS[username] = [t for t in LOGIN_ATTEMPTS[username] if (now - t).total_seconds() < LOCKOUT_DURATION]
    # Check if exceeded max attempts
    if len(LOGIN_ATTEMPTS[username]) >= MAX_LOGIN_ATTEMPTS:
        return False  # Too many attempts - locked out
    return True  # Still within limits


@app.route('/')
def index():
    """Home page"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return f"<h1>Welcome to Vulnerable Student Management System</h1><a href='/logout'>Logout</a><br><a href='/dashboard'>Dashboard</a>"

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    FIXED: Multiple Security Improvements
    1. SQL Injection - Now uses parameterized queries (fixed in database.py)
    2. Rate limiting - Enforces max login attempts
    3. Sensitive error messages - Removed verbose messages
    4. Session timeout - Configured in config.py
    5. Password logging - No longer logs passwords
    """
    if request.method == 'POST':
        # FIXED: CSRF Token Validation
        csrf_token = request.form.get('csrf_token', '')
        if not validate_csrf_token(csrf_token):
            database.log_action('SECURITY_VIOLATION', request.remote_addr, 'CSRF validation failed on login')
            flash('Security validation failed. Please try again.', 'danger')
            return render_template('login.html')
        
        username = request.form.get('username', '').strip()  # FIXED: Input trimming
        password = request.form.get('password', '')
        
        # FIXED: Input validation
        if not username or not password:
            flash('Username and password are required', 'danger')
            return render_template('login.html')
        
        # FIXED: Rate limiting enforcement
        if not check_rate_limit(username):
            database.log_action('SECURITY_WARNING', username, 'Rate limit exceeded during login')
            flash('Too many login attempts. Please try again later.', 'danger')
            return render_template('login.html')
        
        record_login_attempt(username)
        
        # FIXED: Uses parameterized queries (secure from SQL injection)
        user = database.authenticate_user(username, password)
        
        if user:
            # FIXED: Secure session configuration applied
            session['user_id'] = user[0]
            session['username'] = user[1]
            session['email'] = user[3]
            session['role'] = user[4]
            session.permanent = True
            
            # FIXED: Sanitized logging - no password
            database.log_action('LOGIN_SUCCESS', username, 'User logged in successfully')
            
            return redirect(url_for('dashboard'))
        else:
            # FIXED: Generic error message - no information disclosure
            flash('Invalid username or password', 'danger')
            # FIXED: No longer logs password attempts
            database.log_action('LOGIN_FAILED', username, 'Failed login attempt')
            return render_template('login.html')
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    """
    VULNERABILITY: No proper access control
    Anyone with a session can access
    Shows role-based dashboard
    """
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    return render_template('dashboard.html')

@app.route('/students')
def students():
    """
    VULNERABILITY: No access control - any authenticated user can see all data
    Exposes sensitive information (SSN, passwords)
    FIXED: Restrict to admin and user roles only (not students)
    """
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    role = session.get('role', 'user')
    if role == 'student':
        database.log_action('UNAUTHORIZED_ACCESS', session.get('username'), 'Attempted to access all students list')
        return "Access Denied: Students cannot view all student records", 403
    
    conn = database.sqlite3.connect(database.DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT id, roll_no, name, email, phone, ssn FROM students')
    students_list = cursor.fetchall()
    conn.close()
    
    return render_template('students.html', students=students_list)

@app.route('/student/<student_id>')
def view_student(student_id):
    """
    FIXED: Multiple Security Issues
    1. SQL Injection - Uses parameterized queries
    2. Sensitive Data Exposure - No longer exposes SSN/password
    3. Access Control - Prevents students from viewing others' records
    4. Input Validation - Validates student_id format
    """
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    role = session.get('role', 'user')
    if role == 'student':
        database.log_action('UNAUTHORIZED_ACCESS', session.get('username'), f'Attempted to view other student record (ID: {student_id})')
        flash('Access Denied: Students cannot view other student records', 'danger')
        return redirect(url_for('dashboard')), 403
    
    # FIXED: Input validation - ensure ID is numeric
    try:
        student_id = int(student_id)
    except (ValueError, TypeError):
        database.log_action('SECURITY_WARNING', session.get('username'), f'Invalid student ID format: {student_id}')
        flash('Invalid student ID', 'danger')
        return redirect(url_for('students')), 400
    
    # FIXED: Uses parameterized queries (secure from SQL injection)
    student = database.get_student_details(student_id)
    
    if not student:
        flash('Student not found', 'danger')
        return redirect(url_for('students')), 404
    
    return render_template('student_detail.html', student=student)

@app.route('/student/profile')
def student_profile():
    """
    Student can view only their own profile
    Restricts access based on email matching between user and student record
    """
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    role = session.get('role', 'user')
    if role != 'student':
        return "Access Denied: Only students can view their profile", 403
    
    user_email = session.get('email')  # Requires email to be stored in session
    
    conn = database.sqlite3.connect(database.DB_NAME)
    cursor = conn.cursor()
    # Use parameterized query here (matching email)
    cursor.execute('SELECT id, roll_no, name, email, phone, address, gpa FROM students WHERE email = ?', (user_email,))
    student = cursor.fetchone()
    conn.close()
    
    if not student:
        return "Your student record not found", 404
    
    return render_template('student_profile.html', student=student)

@app.route('/student/grades')
def student_grades():
    """
    Student can view only their own grades and GPA
    Restricts access to student role only
    """
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    role = session.get('role', 'user')
    if role != 'student':
        return "Access Denied: Only students can view their grades", 403
    
    user_email = session.get('email')
    
    conn = database.sqlite3.connect(database.DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT roll_no, name, gpa FROM students WHERE email = ?', (user_email,))
    student = cursor.fetchone()
    conn.close()
    
    if not student:
        return "Your student record not found", 404
    
    return render_template('student_grades.html', student=student)

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    """
    FIXED: Multiple Security Issues
    1. SQL Injection - Uses parameterized queries (fixed in database.py)
    2. Input validation - All fields validated before submission
    3. Access control - Admin only
    """
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    role = session.get('role', 'user')
    if role != 'admin':
        database.log_action('UNAUTHORIZED_ACCESS', session.get('username'), 'Attempted to access add_student page')
        flash('Access Denied: Only admins can add students', 'danger')
        return redirect(url_for('dashboard')), 403
    
    if request.method == 'POST':
        # FIXED: CSRF Token Validation
        csrf_token = request.form.get('csrf_token', '')
        if not validate_csrf_token(csrf_token):
            database.log_action('SECURITY_VIOLATION', session.get('username'), 'CSRF validation failed on add_student')
            flash('Security validation failed. Please try again.', 'danger')
            return render_template('add_student.html')
        
        # FIXED: Input validation for all fields
        roll_no = request.form.get('roll_no', '').strip()
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        address = request.form.get('address', '').strip()
        ssn = request.form.get('ssn', '').strip()
        gpa = request.form.get('gpa', '0')
        
        # FIXED: Comprehensive input validation
        errors = []
        if not roll_no:
            errors.append('Roll number is required')
        if not name or len(name) < 2:
            errors.append('Valid name is required')
        if not email or '@' not in email:
            errors.append('Valid email is required')
        if not phone or not phone.isdigit() or len(phone) != 10:
            errors.append('Valid 10-digit phone number is required')
        if not address or len(address) < 5:
            errors.append('Valid address is required')
        if not ssn or not re.match(r'^\d{3}-\d{2}-\d{4}$', ssn):
            errors.append('Valid SSN format (XXX-XX-XXXX) is required')
        
        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('add_student_new.html')
        
        # FIXED: Uses parameterized queries (secure from SQL injection)
        if database.add_student(roll_no, name, email, phone, address, ssn, gpa):
            flash('Student added successfully!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Error adding student', 'danger')
            return redirect(url_for('add_student'))
    
    return render_template('add_student.html')

@app.route('/search', methods=['GET', 'POST'])
def search_students():
    """
    FIXED: SQL Injection vulnerability
    Now uses parameterized queries
    Access control prevents students from searching
    """
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    role = session.get('role', 'user')
    if role == 'student':
        database.log_action('UNAUTHORIZED_ACCESS', session.get('username'), 'Attempted to search students')
        flash('Access Denied: Students cannot search student records', 'danger')
        return redirect(url_for('dashboard')), 403
    
    results = []
    if request.method == 'POST':
        # FIXED: CSRF Token Validation
        csrf_token = request.form.get('csrf_token', '')
        if not validate_csrf_token(csrf_token):
            database.log_action('SECURITY_VIOLATION', session.get('username'), 'CSRF validation failed on search')
            flash('Security validation failed. Please try again.', 'danger')
            return render_template('search.html', results=[])
        
        search_term = request.form.get('search', '').strip()  # FIXED: Input trimming
        
        # FIXED: Input validation
        if not search_term or len(search_term) < 1:
            flash('Search term cannot be empty', 'warning')
        elif len(search_term) > 100:
            flash('Search term is too long', 'danger')
        else:
            # FIXED: Uses parameterized queries (secure from SQL injection)
            results = database.search_students(search_term)
    
    return render_template('search.html', results=results)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    """
    FIXED: Multiple File Upload Issues
    1. Proper file type validation - only safe extensions
    2. Path traversal prevention - using secure_filename
    3. File size limit enforcement
    4. Proper access control (prevents students)
    """
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    role = session.get('role', 'user')
    if role == 'student':
        database.log_action('UNAUTHORIZED_ACCESS', session.get('username'), 'Attempted to access file upload')
        flash('Access Denied: Only admin and users can upload files', 'danger')
        return redirect(url_for('dashboard')), 403
    
    if request.method == 'POST':
        # FIXED: CSRF Token Validation
        csrf_token = request.form.get('csrf_token', '')
        if not validate_csrf_token(csrf_token):
            database.log_action('SECURITY_VIOLATION', session.get('username'), 'CSRF validation failed on file upload')
            flash('Security validation failed. Please try again.', 'danger')
            return redirect(url_for('upload_file'))
        
        if 'file' not in request.files:
            flash('No file selected', 'danger')
            return redirect(url_for('upload_file'))
        
        file = request.files['file']
        
        if file.filename == '':
            flash('No file selected', 'danger')
            return redirect(url_for('upload_file'))
        
        # FIXED: Secure filename handling
        filename = secure_filename(file.filename)
        
        # FIXED: Validate file extension
        if not filename or '.' not in filename:
            flash('Invalid filename', 'danger')
            return redirect(url_for('upload_file'))
        
        file_ext = filename.rsplit('.', 1)[1].lower()
        if file_ext not in app.config['ALLOWED_EXTENSIONS']:
            if file_ext in ['exe', 'bat', 'sh', 'cmd', 'ps1', 'php', 'py', 'vbs', 'scr']:
                database.log_action('MALICIOUS_UPLOAD_ATTEMPT', session.get('username'), f'Attempted to upload dangerous file type: {filename}')
            else:
                database.log_action('SECURITY_WARNING', session.get('username'), f'Attempted to upload disallowed file type: {filename}')
            flash(f'File type .{file_ext} not allowed. Allowed types: {", ".join(app.config["ALLOWED_EXTENSIONS"])}', 'danger')
            return redirect(url_for('upload_file'))
        
        # FIXED: Validate file size (max 5MB)
        file.seek(0, os.SEEK_END)  # Seek to end
        file_size = file.tell()
        file.seek(0)  # Seek back to start
        
        max_size = app.config['MAX_CONTENT_LENGTH']
        if file_size > max_size:
            database.log_action('SECURITY_WARNING', session.get('username'), f'Attempted to upload oversized file: {filename} ({file_size} bytes)')
            flash(f'File size exceeds maximum allowed size of {max_size / (1024*1024):.1f}MB', 'danger')
            return redirect(url_for('upload_file'))
        
        # FIXED: Safe path construction
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        filepath = os.path.abspath(filepath)  # Resolve to absolute path
        
        # FIXED: Ensure filepath is within UPLOAD_FOLDER
        upload_dir = os.path.abspath(app.config['UPLOAD_FOLDER'])
        if not filepath.startswith(upload_dir):
            database.log_action('SECURITY_VIOLATION', session.get('username'), f'Path traversal attempt blocked during upload: {filename}')
            flash('Invalid file path', 'danger')
            return redirect(url_for('upload_file'))
        
        try:
            file.save(filepath)
            # FIXED: Sanitized logging
            database.log_action('FILE_UPLOAD', session.get('username'), f'Uploaded file: {filename}')
            flash(f'File "{filename}" uploaded successfully!', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            flash('Error uploading file', 'danger')
            return redirect(url_for('upload_file'))
    
    return render_template('upload.html')

@app.route('/download/<filename>')
def download_file(filename):
    """
    FIXED: Path Traversal vulnerability
    Validates filename before accessing filesystem
    """
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    filename = secure_filename(filename)
    if not filename:
        flash('Invalid filename', 'danger')
        return redirect(url_for('dashboard'))
    
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    filepath = os.path.abspath(filepath)  # Resolve to absolute path
    
    upload_dir = os.path.abspath(app.config['UPLOAD_FOLDER'])
    if not filepath.startswith(upload_dir) or not os.path.isfile(filepath):
        database.log_action('SECURITY_VIOLATION', session.get('username'), f'Attempted to access restricted or missing file: {filename}')
        flash('File not found or access denied', 'danger')
        return redirect(url_for('dashboard')), 404
    
    try:
        database.log_action('FILE_DOWNLOAD', session.get('username'), f'Downloaded file: {filename}')
        return send_file(filepath)
    except Exception:
        flash('Error downloading file', 'danger')
        return redirect(url_for('dashboard')), 500

@app.route('/file/<path:filepath>')
def access_file(filepath):
    """
    FIXED: Unrestricted File Path Access vulnerability
    Now validates and restricts file access properly
    Only allows access to files within permitted directories
    """
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    normalized_path = os.path.normpath(filepath)
    upload_dir = os.path.abspath(app.config['UPLOAD_FOLDER'])
    requested_path = os.path.abspath(normalized_path)
    
    if not requested_path.startswith(upload_dir):
        database.log_action('SECURITY_VIOLATION', session.get('username'), f'Attempted path traversal on file access: {filepath}')
        flash('Access to this file is not permitted', 'danger')
        return redirect(url_for('dashboard')), 403
    
    if not os.path.isfile(requested_path):
        flash('File not found', 'danger')
        return redirect(url_for('dashboard')), 404
    
    try:
        database.log_action('FILE_ACCESS', session.get('username'), 'Accessed file')
        return send_file(requested_path)
    except Exception:
        flash('Error accessing file', 'danger')
        return redirect(url_for('dashboard')), 500

@app.route('/view_logs')
def view_logs():
    """
    VULNERABILITY: Information Disclosure + Sensitive Data Exposure
    No access control - any user can see logs with passwords
    FIXED: Restrict to admin only
    """
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    role = session.get('role', 'user')
    if role != 'admin':
        database.log_action('UNAUTHORIZED_ACCESS', session.get('username'), 'Attempted to access system logs')
        return "Access Denied: Only admins can view logs", 403
    
    # VULNERABILITY: No role-based access control
    # Should be admin-only
    
    conn = database.sqlite3.connect(database.DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM logs ORDER BY created_at DESC LIMIT 100')
    logs = cursor.fetchall()
    conn.close()
    
    return render_template('logs.html', logs=logs)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    """FIXED: CSRF token protection on logout (for POST requests)"""
    if request.method == 'POST':
        # FIXED: CSRF Token Validation
        csrf_token = request.form.get('csrf_token', '')
        if not validate_csrf_token(csrf_token):
            database.log_action('SECURITY_VIOLATION', session.get('username'), 'CSRF validation failed on logout')
            flash('Security validation failed.', 'danger')
            return redirect(url_for('dashboard'))
    
    username = session.get('username')
    session.clear()
    if username:
        database.log_action('LOGOUT', username, 'User logged out successfully')
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('login'))

@app.after_request
def add_security_headers(response):
    """FIXED: Added HTTP Security Headers to resolve ZAP warnings"""
    # Prevents clickjacking (Missing Anti-clickjacking Header)
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    
    # Prevents MIME-sniffing (X-Content-Type-Options Header Missing)
    response.headers['X-Content-Type-Options'] = 'nosniff'
    
    # Restricts resource loading (Content Security Policy)
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; object-src 'none'; base-uri 'self';"
    
    # Masks server version (Server Leaks Version Information)
    response.headers['Server'] = 'ISRM-Secure-Server'
    
    return response

@app.errorhandler(404)
def not_found(error):
    # FIXED: Generic error message - no detailed errors
    flash('Page not found', 'danger')
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    # FIXED: Generic error message - no stack trace exposure
    flash('Internal server error', 'danger')
    return render_template('500.html'), 500

if __name__ == '__main__':
    # FIXED: Debug disabled, localhost binding, secure settings
    debug_mode = app.config.get('DEBUG', False)
    host = app.config.get('HOST', '127.0.0.1')
    print(f"[*] Starting Flask app...")
    print(f"[*] Debug Mode: {debug_mode}")
    print(f"[*] Host: {host}:5000")
    app.run(debug=debug_mode, host=host, port=5000, use_reloader=False)

