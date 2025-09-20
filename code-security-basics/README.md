# Code Security Basic Principles

## Table of Contents
1. [Overview](#overview)
2. [Input Validation](#input-validation)
3. [SQL Injection Prevention](#sql-injection-prevention)
4. [Secure Session Management](#secure-session-management)
5. [Session Fixation Prevention](#session-fixation-prevention)
6. [Authentication and Authorization](#authentication-and-authorization)
7. [Access Control Implementation](#access-control-implementation)
8. [Best Practices](#best-practices)
9. [Common Vulnerabilities](#common-vulnerabilities)
10. [Security Testing](#security-testing)

## Overview

Code security is the practice of writing secure code that protects applications from various threats and vulnerabilities. This document covers the fundamental principles of secure coding, focusing on input validation, session management, and authentication/authorization.

## Input Validation

### What is Input Validation?

Input validation is the process of checking and sanitizing all data that enters an application from external sources (users, APIs, files, etc.) to ensure it meets expected criteria and doesn't contain malicious content.

### Why is Input Validation Important?

1. **Prevents Injection Attacks**: SQL injection, NoSQL injection, command injection
2. **Prevents XSS Attacks**: Cross-site scripting attacks
3. **Data Integrity**: Ensures data conforms to expected format
4. **Business Logic Protection**: Prevents bypassing application logic
5. **System Stability**: Prevents crashes from unexpected data

### Types of Input Validation

#### 1. **Client-Side Validation**
```javascript
// HTML5 validation
<input type="email" required pattern="[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$">

// JavaScript validation
function validateEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function validateInput(input) {
    if (!input || input.trim().length === 0) {
        return false;
    }
    if (input.length > 100) {
        return false;
    }
    return true;
}
```

#### 2. **Server-Side Validation**
```python
from flask import request, jsonify
import re

def validate_user_input(data):
    errors = []
    
    # Required field validation
    if not data.get('username'):
        errors.append('Username is required')
    
    # Length validation
    if data.get('username') and len(data['username']) > 50:
        errors.append('Username must be less than 50 characters')
    
    # Format validation
    if data.get('email'):
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, data['email']):
            errors.append('Invalid email format')
    
    # Character validation
    if data.get('username'):
        if not re.match(r'^[a-zA-Z0-9_]+$', data['username']):
            errors.append('Username can only contain letters, numbers, and underscores')
    
    return errors

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    errors = validate_user_input(data)
    
    if errors:
        return jsonify({'errors': errors}), 400
    
    # Process valid data
    return jsonify({'message': 'Registration successful'})
```

#### 3. **Whitelist vs Blacklist Approach**

**Whitelist (Recommended):**
```python
# Allow only specific characters
def validate_username(username):
    allowed_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_')
    return all(c in allowed_chars for c in username)

# Allow only specific values
def validate_status(status):
    allowed_statuses = ['active', 'inactive', 'pending']
    return status in allowed_statuses
```

**Blacklist (Not Recommended):**
```python
# Block specific characters (can be bypassed)
def validate_input(input_str):
    dangerous_chars = ['<', '>', '"', "'", '&', ';', '|', '`']
    return not any(char in input_str for char in dangerous_chars)
```

### Input Validation Best Practices

1. **Validate on Both Client and Server**: Client-side for UX, server-side for security
2. **Use Whitelist Approach**: Allow only known good values
3. **Validate Length**: Prevent buffer overflow attacks
4. **Validate Format**: Use regex patterns for structured data
5. **Sanitize Output**: Clean data before displaying
6. **Use Parameterized Queries**: Prevent SQL injection
7. **Implement Rate Limiting**: Prevent abuse

## SQL Injection Prevention

### What is SQL Injection?

SQL injection is a code injection technique where malicious SQL statements are inserted into an application's database query, allowing attackers to manipulate the database.

### Example of SQL Injection

**Vulnerable Code:**
```python
# DANGEROUS - Vulnerable to SQL injection
def get_user(username, password):
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    return execute_query(query)

# If username = "admin' OR '1'='1"
# Query becomes: SELECT * FROM users WHERE username = 'admin' OR '1'='1' AND password = 'anything'
```

### Prevention Methods

#### 1. **Parameterized Queries (Prepared Statements)**
```python
import sqlite3

# SECURE - Using parameterized queries
def get_user_secure(username, password):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Parameterized query
    query = "SELECT * FROM users WHERE username = ? AND password = ?"
    cursor.execute(query, (username, password))
    
    result = cursor.fetchone()
    conn.close()
    return result

# Using SQLAlchemy ORM
from sqlalchemy import text

def get_user_orm(username, password):
    query = text("SELECT * FROM users WHERE username = :username AND password = :password")
    result = db.session.execute(query, {"username": username, "password": password})
    return result.fetchone()
```

#### 2. **Input Validation and Sanitization**
```python
import re

def validate_sql_input(input_str):
    # Remove or escape dangerous characters
    dangerous_patterns = [
        r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|UNION)\b)",
        r"(--|#|/\*|\*/)",
        r"('|;|\"|\\|`|%)"
    ]
    
    for pattern in dangerous_patterns:
        if re.search(pattern, input_str, re.IGNORECASE):
            raise ValueError("Invalid input detected")
    
    return input_str.strip()

def safe_get_user(username, password):
    # Validate inputs
    safe_username = validate_sql_input(username)
    safe_password = validate_sql_input(password)
    
    # Use parameterized query
    query = "SELECT * FROM users WHERE username = ? AND password = ?"
    return execute_query(query, (safe_username, safe_password))
```

#### 3. **Database Access Control**
```python
# Use least privilege principle
def create_database_user():
    # Create user with minimal permissions
    create_user_sql = """
    CREATE USER 'app_user'@'localhost' IDENTIFIED BY 'strong_password';
    GRANT SELECT, INSERT, UPDATE ON myapp.users TO 'app_user'@'localhost';
    GRANT SELECT ON myapp.products TO 'app_user'@'localhost';
    -- No DROP, CREATE, ALTER permissions
    """
    return create_user_sql
```

#### 4. **Input Length Limits**
```python
def validate_input_length(input_str, max_length=100):
    if len(input_str) > max_length:
        raise ValueError(f"Input too long. Maximum {max_length} characters allowed.")
    return input_str

def safe_search(search_term):
    # Limit input length
    safe_term = validate_input_length(search_term, 50)
    
    # Use parameterized query
    query = "SELECT * FROM products WHERE name LIKE ?"
    search_pattern = f"%{safe_term}%"
    return execute_query(query, (search_pattern,))
```

### SQL Injection Prevention Checklist

- [ ] Use parameterized queries/prepared statements
- [ ] Validate and sanitize all inputs
- [ ] Implement proper error handling
- [ ] Use least privilege database accounts
- [ ] Enable database logging and monitoring
- [ ] Regular security testing and code reviews
- [ ] Keep database software updated

## Secure Session Management

### What are Sessions?

Sessions are a way to maintain state between HTTP requests. Since HTTP is stateless, sessions allow applications to remember information about users across multiple requests.

### Why is Secure Session Management Crucial?

1. **User Authentication**: Maintain login state
2. **Data Protection**: Prevent unauthorized access to user data
3. **Attack Prevention**: Stop session hijacking and fixation
4. **Privacy**: Protect user information
5. **Compliance**: Meet security regulations

### Session Security Components

#### 1. **Secure Session ID Generation**
```python
import secrets
import hashlib
import time

def generate_secure_session_id():
    # Generate cryptographically secure random session ID
    random_bytes = secrets.token_bytes(32)
    timestamp = str(int(time.time()))
    
    # Combine random data with timestamp
    combined = random_bytes + timestamp.encode()
    
    # Hash the combined data
    session_id = hashlib.sha256(combined).hexdigest()
    
    return session_id

# Example usage
session_id = generate_secure_session_id()
print(f"Secure session ID: {session_id}")
```

#### 2. **Session Storage Security**
```python
import redis
import json
from datetime import datetime, timedelta

class SecureSessionManager:
    def __init__(self):
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)
        self.session_timeout = 3600  # 1 hour
    
    def create_session(self, user_id, user_data):
        session_id = generate_secure_session_id()
        
        session_data = {
            'user_id': user_id,
            'created_at': datetime.utcnow().isoformat(),
            'last_activity': datetime.utcnow().isoformat(),
            'ip_address': self.get_client_ip(),
            'user_agent': self.get_user_agent(),
            'data': user_data
        }
        
        # Store with expiration
        self.redis_client.setex(
            f"session:{session_id}",
            self.session_timeout,
            json.dumps(session_data)
        )
        
        return session_id
    
    def validate_session(self, session_id):
        session_key = f"session:{session_id}"
        session_data = self.redis_client.get(session_key)
        
        if not session_data:
            return None
        
        session = json.loads(session_data)
        
        # Check if session is still valid
        last_activity = datetime.fromisoformat(session['last_activity'])
        if datetime.utcnow() - last_activity > timedelta(seconds=self.session_timeout):
            self.redis_client.delete(session_key)
            return None
        
        # Update last activity
        session['last_activity'] = datetime.utcnow().isoformat()
        self.redis_client.setex(session_key, self.session_timeout, json.dumps(session))
        
        return session
    
    def destroy_session(self, session_id):
        session_key = f"session:{session_id}"
        self.redis_client.delete(session_key)
```

#### 3. **Session Cookie Security**
```python
from flask import Flask, session, request, make_response
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Strong secret key

@app.before_request
def setup_session():
    # Configure secure session cookies
    app.config.update(
        SESSION_COOKIE_SECURE=True,      # HTTPS only
        SESSION_COOKIE_HTTPONLY=True,    # No JavaScript access
        SESSION_COOKIE_SAMESITE='Lax',   # CSRF protection
        PERMANENT_SESSION_LIFETIME=3600  # 1 hour
    )

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    if validate_credentials(username, password):
        # Regenerate session ID to prevent fixation
        session.permanent = True
        session['user_id'] = get_user_id(username)
        session['username'] = username
        session['login_time'] = datetime.utcnow().isoformat()
        
        return redirect('/dashboard')
    else:
        return 'Invalid credentials', 401

@app.route('/logout')
def logout():
    # Clear session data
    session.clear()
    return redirect('/login')
```

## Session Fixation Prevention

### What is Session Fixation?

Session fixation is an attack where an attacker forces a user to use a specific session ID, then hijacks that session after the user authenticates.

### How Session Fixation Works

1. Attacker obtains a valid session ID
2. Attacker tricks victim into using that session ID
3. Victim logs in with the fixed session ID
4. Attacker uses the same session ID to access victim's account

### Prevention Methods

#### 1. **Session ID Regeneration**
```python
from flask import session
import secrets

def regenerate_session_id():
    """Regenerate session ID after successful authentication"""
    # Store current session data
    old_data = dict(session)
    
    # Clear current session
    session.clear()
    
    # Generate new session ID
    new_session_id = secrets.token_urlsafe(32)
    
    # Restore data with new session ID
    for key, value in old_data.items():
        session[key] = value
    
    return new_session_id

@app.route('/login', methods=['POST'])
def secure_login():
    username = request.form['username']
    password = request.form['password']
    
    if validate_credentials(username, password):
        # Regenerate session ID to prevent fixation
        regenerate_session_id()
        
        session['user_id'] = get_user_id(username)
        session['authenticated'] = True
        
        return redirect('/dashboard')
    else:
        return 'Invalid credentials', 401
```

#### 2. **Session Validation**
```python
def validate_session_security(session_id, client_ip, user_agent):
    """Validate session against security parameters"""
    session_data = get_session_data(session_id)
    
    if not session_data:
        return False
    
    # Check IP address
    if session_data.get('ip_address') != client_ip:
        # Log suspicious activity
        log_security_event('IP_MISMATCH', session_id, client_ip)
        return False
    
    # Check User-Agent
    if session_data.get('user_agent') != user_agent:
        # Log suspicious activity
        log_security_event('USER_AGENT_MISMATCH', session_id, user_agent)
        return False
    
    # Check session age
    if is_session_expired(session_data):
        return False
    
    return True

@app.before_request
def check_session_security():
    if 'user_id' in session:
        session_id = session.get('_id')
        client_ip = request.remote_addr
        user_agent = request.headers.get('User-Agent')
        
        if not validate_session_security(session_id, client_ip, user_agent):
            session.clear()
            return redirect('/login')
```

#### 3. **Secure Session Creation**
```python
def create_secure_session(user_id):
    """Create a new secure session"""
    # Generate new session ID
    session_id = generate_secure_session_id()
    
    # Get client information
    client_ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    
    # Create session data
    session_data = {
        'user_id': user_id,
        'session_id': session_id,
        'ip_address': client_ip,
        'user_agent': user_agent,
        'created_at': datetime.utcnow().isoformat(),
        'last_activity': datetime.utcnow().isoformat()
    }
    
    # Store session
    store_session(session_id, session_data)
    
    # Set secure cookie
    response = make_response(redirect('/dashboard'))
    response.set_cookie(
        'session_id',
        session_id,
        secure=True,      # HTTPS only
        httponly=True,    # No JavaScript access
        samesite='Lax'    # CSRF protection
    )
    
    return response
```

## Authentication and Authorization

### What is Authentication?

Authentication is the process of verifying the identity of a user, system, or entity. It answers the question "Who are you?"

### What is Authorization?

Authorization is the process of determining what resources and actions a user is allowed to access. It answers the question "What can you do?"

### Key Differences

| Aspect | Authentication | Authorization |
|--------|----------------|---------------|
| **Purpose** | Verify identity | Control access |
| **Question** | "Who are you?" | "What can you do?" |
| **Process** | Login, credentials | Permission checking |
| **Result** | User identity | Access rights |
| **Example** | Username/password | Role-based access |

### Authentication Implementation

#### 1. **Basic Authentication**
```python
from werkzeug.security import check_password_hash, generate_password_hash
import secrets

class UserAuth:
    def __init__(self):
        self.users = {}  # In production, use database
    
    def register_user(self, username, password, email):
        """Register a new user"""
        if username in self.users:
            return False, "Username already exists"
        
        # Hash password
        password_hash = generate_password_hash(password)
        
        # Store user
        self.users[username] = {
            'password_hash': password_hash,
            'email': email,
            'role': 'user',
            'created_at': datetime.utcnow().isoformat()
        }
        
        return True, "User registered successfully"
    
    def authenticate_user(self, username, password):
        """Authenticate user credentials"""
        if username not in self.users:
            return False, "Invalid credentials"
        
        user = self.users[username]
        
        if not check_password_hash(user['password_hash'], password):
            return False, "Invalid credentials"
        
        return True, "Authentication successful"
    
    def generate_auth_token(self, username):
        """Generate authentication token"""
        user = self.users[username]
        token_data = {
            'username': username,
            'role': user['role'],
            'issued_at': datetime.utcnow().isoformat(),
            'expires_at': (datetime.utcnow() + timedelta(hours=1)).isoformat()
        }
        
        # In production, use JWT or similar
        token = secrets.token_urlsafe(32)
        store_auth_token(token, token_data)
        
        return token
```

#### 2. **Multi-Factor Authentication**
```python
import pyotp
import qrcode
from io import BytesIO
import base64

class MFA:
    def __init__(self):
        self.user_secrets = {}
    
    def setup_mfa(self, username):
        """Setup MFA for user"""
        # Generate secret key
        secret = pyotp.random_base32()
        self.user_secrets[username] = secret
        
        # Generate QR code
        totp_uri = pyotp.totp.TOTP(secret).provisioning_uri(
            name=username,
            issuer_name="MyApp"
        )
        
        # Create QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(totp_uri)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()
        
        return {
            'secret': secret,
            'qr_code': img_str,
            'backup_codes': self.generate_backup_codes(username)
        }
    
    def verify_mfa(self, username, token):
        """Verify MFA token"""
        if username not in self.user_secrets:
            return False
        
        secret = self.user_secrets[username]
        totp = pyotp.TOTP(secret)
        
        return totp.verify(token, valid_window=1)
    
    def generate_backup_codes(self, username):
        """Generate backup codes for MFA"""
        codes = [secrets.token_hex(4) for _ in range(10)]
        store_backup_codes(username, codes)
        return codes
```

### Authorization Implementation

#### 1. **Role-Based Access Control (RBAC)**
```python
class RBAC:
    def __init__(self):
        self.roles = {
            'admin': ['read', 'write', 'delete', 'manage_users'],
            'moderator': ['read', 'write', 'moderate'],
            'user': ['read', 'write_own'],
            'guest': ['read']
        }
        
        self.resources = {
            'users': ['read', 'write', 'delete'],
            'posts': ['read', 'write', 'delete', 'moderate'],
            'comments': ['read', 'write', 'delete']
        }
    
    def check_permission(self, user_role, resource, action):
        """Check if user role has permission for action on resource"""
        if user_role not in self.roles:
            return False
        
        role_permissions = self.roles[user_role]
        
        # Check if role has the required permission
        if action not in role_permissions:
            return False
        
        # Check if resource supports the action
        if resource in self.resources:
            if action not in self.resources[resource]:
                return False
        
        return True
    
    def get_user_permissions(self, user_role):
        """Get all permissions for a user role"""
        return self.roles.get(user_role, [])

# Usage
rbac = RBAC()

def require_permission(resource, action):
    def decorator(func):
        def wrapper(*args, **kwargs):
            user_role = session.get('user_role')
            
            if not rbac.check_permission(user_role, resource, action):
                return jsonify({'error': 'Insufficient permissions'}), 403
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

@app.route('/admin/users')
@require_permission('users', 'manage_users')
def admin_users():
    return jsonify({'users': get_all_users()})

@app.route('/posts/<int:post_id>')
@require_permission('posts', 'read')
def get_post(post_id):
    return jsonify({'post': get_post_by_id(post_id)})
```

#### 2. **Attribute-Based Access Control (ABAC)**
```python
class ABAC:
    def __init__(self):
        self.policies = [
            {
                'name': 'admin_full_access',
                'conditions': {
                    'user.role': 'admin'
                },
                'permissions': ['*']
            },
            {
                'name': 'user_own_posts',
                'conditions': {
                    'user.role': 'user',
                    'resource.owner': 'user.id'
                },
                'permissions': ['read', 'write', 'delete']
            },
            {
                'name': 'time_based_access',
                'conditions': {
                    'time.hour': {'gte': 9, 'lte': 17},
                    'user.department': 'engineering'
                },
                'permissions': ['read', 'write']
            }
        ]
    
    def evaluate_access(self, user, resource, action, context):
        """Evaluate access based on attributes"""
        for policy in self.policies:
            if self.matches_conditions(policy['conditions'], user, resource, context):
                if action in policy['permissions'] or '*' in policy['permissions']:
                    return True
        
        return False
    
    def matches_conditions(self, conditions, user, resource, context):
        """Check if conditions match current context"""
        for key, expected_value in conditions.items():
            if key.startswith('user.'):
                attr_name = key.split('.', 1)[1]
                actual_value = getattr(user, attr_name, None)
            elif key.startswith('resource.'):
                attr_name = key.split('.', 1)[1]
                actual_value = getattr(resource, attr_name, None)
            elif key.startswith('time.'):
                attr_name = key.split('.', 1)[1]
                actual_value = getattr(context.get('time'), attr_name, None)
            else:
                actual_value = context.get(key)
            
            if not self.compare_values(actual_value, expected_value):
                return False
        
        return True
    
    def compare_values(self, actual, expected):
        """Compare actual value with expected value"""
        if isinstance(expected, dict):
            if 'gte' in expected:
                return actual >= expected['gte']
            if 'lte' in expected:
                return actual <= expected['lte']
            if 'eq' in expected:
                return actual == expected['eq']
        else:
            return actual == expected
```

## Access Control Implementation

### Example: Secure Web Page Access

```python
from flask import Flask, request, session, redirect, url_for, jsonify
from functools import wraps
import jwt
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'your-secret-key'

# Mock user database
users = {
    'admin': {
        'password': 'admin123',
        'role': 'admin',
        'permissions': ['read', 'write', 'delete', 'manage_users']
    },
    'user1': {
        'password': 'user123',
        'role': 'user',
        'permissions': ['read', 'write_own']
    },
    'moderator': {
        'password': 'mod123',
        'role': 'moderator',
        'permissions': ['read', 'write', 'moderate']
    }
}

def login_required(f):
    """Decorator to require authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def require_role(required_role):
    """Decorator to require specific role"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                return redirect(url_for('login'))
            
            user_role = session.get('user_role')
            if user_role != required_role:
                return jsonify({'error': 'Insufficient permissions'}), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def require_permission(required_permission):
    """Decorator to require specific permission"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                return redirect(url_for('login'))
            
            user_permissions = session.get('permissions', [])
            if required_permission not in user_permissions:
                return jsonify({'error': 'Insufficient permissions'}), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in users and users[username]['password'] == password:
            # Create secure session
            session['user_id'] = username
            session['user_role'] = users[username]['role']
            session['permissions'] = users[username]['permissions']
            session['login_time'] = datetime.utcnow().isoformat()
            
            return redirect(url_for('dashboard'))
        else:
            return 'Invalid credentials', 401
    
    return '''
    <form method="post">
        <input type="text" name="username" placeholder="Username" required>
        <input type="password" name="password" placeholder="Password" required>
        <button type="submit">Login</button>
    </form>
    '''

@app.route('/dashboard')
@login_required
def dashboard():
    return f'''
    <h1>Welcome, {session['user_id']}!</h1>
    <p>Role: {session['user_role']}</p>
    <p>Permissions: {', '.join(session['permissions'])}</p>
    <a href="/admin">Admin Panel</a> | 
    <a href="/profile">Profile</a> | 
    <a href="/logout">Logout</a>
    '''

@app.route('/admin')
@login_required
@require_role('admin')
def admin_panel():
    return '''
    <h1>Admin Panel</h1>
    <p>This page is only accessible to administrators.</p>
    <a href="/dashboard">Back to Dashboard</a>
    '''

@app.route('/profile')
@login_required
@require_permission('read')
def profile():
    return f'''
    <h1>User Profile</h1>
    <p>Username: {session['user_id']}</p>
    <p>Role: {session['user_role']}</p>
    <p>Login Time: {session['login_time']}</p>
    <a href="/dashboard">Back to Dashboard</a>
    '''

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
```

## Best Practices

### 1. **Input Validation**
- Validate all inputs on both client and server side
- Use whitelist approach instead of blacklist
- Implement proper error handling
- Sanitize outputs before displaying

### 2. **Session Security**
- Use secure session ID generation
- Implement session timeout
- Regenerate session IDs after authentication
- Use secure cookie settings
- Validate session integrity

### 3. **Authentication**
- Use strong password policies
- Implement multi-factor authentication
- Hash passwords properly
- Use secure token generation
- Implement account lockout policies

### 4. **Authorization**
- Follow principle of least privilege
- Implement role-based access control
- Use attribute-based access control when needed
- Regular permission audits
- Implement proper access logging

### 5. **General Security**
- Keep software updated
- Use HTTPS everywhere
- Implement proper logging and monitoring
- Regular security testing
- Follow secure coding guidelines

## Common Vulnerabilities

### 1. **Injection Attacks**
- SQL injection
- NoSQL injection
- Command injection
- LDAP injection

### 2. **Cross-Site Scripting (XSS)**
- Stored XSS
- Reflected XSS
- DOM-based XSS

### 3. **Cross-Site Request Forgery (CSRF)**
- State-changing operations
- Missing CSRF tokens
- Insecure cookie settings

### 4. **Session Management Issues**
- Session fixation
- Session hijacking
- Insecure session storage
- Missing session timeout

### 5. **Authentication Bypass**
- Weak authentication mechanisms
- Missing authentication
- Insecure password storage
- Brute force attacks

## Security Testing

### 1. **Static Analysis**
- Code review
- Automated security scanning
- Dependency vulnerability scanning
- Configuration review

### 2. **Dynamic Analysis**
- Penetration testing
- Vulnerability scanning
- Security testing tools
- Manual testing

### 3. **Security Monitoring**
- Log analysis
- Intrusion detection
- Anomaly detection
- Incident response

---

## Conclusion

Code security is essential for protecting applications and user data. By implementing proper input validation, secure session management, and robust authentication/authorization mechanisms, developers can significantly reduce security risks.

**Key takeaways:**
- Always validate and sanitize inputs
- Use parameterized queries to prevent SQL injection
- Implement secure session management with proper timeout and regeneration
- Use strong authentication mechanisms
- Implement proper authorization controls
- Follow security best practices
- Regular security testing and monitoring
