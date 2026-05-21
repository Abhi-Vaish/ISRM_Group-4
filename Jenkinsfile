pipeline {
    agent any
    
    environment {
        PYTHON_PATH = "python"
        REPORT_DIR = 'reports'
    }
    
    triggers {
        githubPush()
    }
    
    stages {
        
        stage('0. Checkout') {
            steps {
                echo "========== CHECKOUT STAGE =========="
                cleanWs()
                checkout scm
                bat 'dir'
            }
        }
        
        stage('1. Build') {
            steps {
                echo "========== BUILD STAGE =========="
                
                bat """
                    ${PYTHON_PATH} --version
                    
                    if not exist venv (
                        ${PYTHON_PATH} -m venv venv
                    )
                    
                    call venv\\Scripts\\activate.bat
                    
                    venv\\Scripts\\pip install --upgrade pip
                    venv\\Scripts\\pip install -r requirements.txt
                    venv\\Scripts\\pip install bandit
                """
            }
        }
        
        stage('2. Security Scan') {
            steps {
                echo "========== SECURITY SCANNING =========="
                
                bat """
                    if not exist reports mkdir reports
                    
                    chcp 65001
                    
                    call venv\\Scripts\\activate.bat
                    
                    echo [*] Running Bandit scan...
                    
                    REM  IMPORTANT: Do NOT fail pipeline here
                    venv\\Scripts\\bandit -r . --exclude venv,.venv-1,reports -f json -o reports\\bandit_report.json || exit /b 0
                    venv\\Scripts\\bandit -r . --exclude venv,.venv-1,reports -f html -o reports\\bandit_report.html || exit /b 0
                """
            }
        }
        
        stage('3. Report Generation') {
            steps {
                echo "========== REPORT GENERATION =========="
                
                bat """
                    call venv\\Scripts\\activate.bat
                    ${PYTHON_PATH} generate_vulnerability_report.py
                """
                
                archiveArtifacts artifacts: 'reports/**', allowEmptyArchive: true
            }
        }

        stage('4. Enforce Security Gate (CVSS > 5)') {
            steps {
                echo "========== SECURITY GATE =========="
                
                writeFile file: 'check_security_gate.py', text: '''
import json
import sys
import os

try:
    with open('reports/bandit_report.json') as f:
        data = json.load(f)
except FileNotFoundError:
    print(" Bandit report not found!")
    sys.exit(1)

mapping = {
    'B608': 9.0,
    'B105': 8.0,
    'B607': 8.5,
    'B610': 7.5,
    'B201': 6.5,
    'B104': 6.5,
    'B101': 5.0,
    'B110': 5.0,
    'B102': 5.0
}

fail = False

for v in data.get('results', []):
    test_id = v.get('test_id')
    filename = v.get('filename', '')
    
    # Only check your project files
    if not any(f in filename for f in ['app.py', 'database.py', 'config.py']):
        continue
        
    cvss = mapping.get(test_id, 5.0)
    
    if cvss > 5:
        print(f"[!] High risk vulnerability: {test_id} (CVSS {cvss}) in {os.path.basename(filename)}")
        fail = True

if fail:
    print(" Build FAILED due to CVSS > 5 vulnerabilities")
    sys.exit(1)
else:
    print(" Build PASSED (No CVSS > 5 vulnerabilities found)")
'''
                
                bat """
                    call venv\\Scripts\\activate.bat
                    echo Checking for vulnerabilities with CVSS > 5...
                    ${PYTHON_PATH} check_security_gate.py
                """
            }
        }
    }
    
    post {
        always {
            echo "========== PIPELINE COMPLETE =========="
        }
        success {
            echo "[SUCCESS] No high-risk vulnerabilities"
        }
        failure {
            echo "[FAILURE] High-risk vulnerabilities detected"
        }
    }
}