# Authentication & Authorization

## Table of Contents
1. [Authentication Fundamentals](#authentication-fundamentals)
2. [Authentication vs Authorization](#authentication-vs-authorization)
3. [Authentication Factors](#authentication-factors)
4. [Multi-Factor Authentication (MFA)](#multi-factor-authentication-mfa)
5. [JSON Web Tokens (JWT)](#json-web-tokens-jwt)
6. [OAuth](#oauth)
7. [Biometric Authentication](#biometric-authentication)
8. [Password Recovery](#password-recovery)
9. [Session Management](#session-management)
10. [Encryption in Authentication](#encryption-in-authentication)
11. [OpenID Connect](#openid-connect)
12. [Security Risks and Mitigation](#security-risks-and-mitigation)
13. [Two-Factor Authentication (2FA)](#two-factor-authentication-2fa)
14. [Cookies and Tokens](#cookies-and-tokens)
15. [Database Integration](#database-integration)

## Authentication Fundamentals

### What is Authentication?

Authentication is the process of verifying the identity of a user, system, or entity attempting to access a resource. It answers the question: "Who are you?"

**Key Characteristics:**
- Identity verification process
- First step in access control
- Can involve multiple factors
- Establishes trust between user and system

**Common Authentication Methods:**
- Username/password combinations
- Digital certificates
- Biometric data
- Hardware tokens
- SMS codes

## Authentication vs Authorization

### Authentication
- **Purpose**: Verifies identity ("Who are you?")
- **Process**: Validates credentials
- **Result**: Establishes user identity
- **Example**: Login with username/password

### Authorization
- **Purpose**: Determines permissions ("What can you do?")
- **Process**: Checks access rights
- **Result**: Grants or denies access to resources
- **Example**: Checking if user can access admin panel

**Relationship:**
```
Authentication → Authorization → Access
     ↓              ↓            ↓
  "Who are you?" → "What can you do?" → "Access granted/denied"
```

## Authentication Factors

### Three Common Types

#### 1. Something You Know (Knowledge Factor)
- **Definition**: Information only the user should know
- **Examples**:
  - Passwords
  - PINs
  - Security questions
  - Passphrases

#### 2. Something You Have (Possession Factor)
- **Definition**: Physical item in user's possession
- **Examples**:
  - Smart cards
  - Hardware tokens
  - Mobile phones
  - USB security keys

#### 3. Something You Are (Inherence Factor)
- **Definition**: Biometric characteristics unique to the user
- **Examples**:
  - Fingerprints
  - Retina scans
  - Voice recognition
  - Facial recognition

## Multi-Factor Authentication (MFA)

### Definition
Multi-Factor Authentication requires users to provide two or more authentication factors to gain access.

### Why Use MFA?
- **Enhanced Security**: Significantly reduces risk of unauthorized access
- **Compliance**: Required by many regulations (PCI DSS, HIPAA)
- **Risk Mitigation**: Even if one factor is compromised, others remain secure
- **User Trust**: Builds confidence in system security

### MFA Implementation Example
```python
def authenticate_user(username, password, sms_code):
    # Factor 1: Something you know (password)
    if not verify_password(username, password):
        return False
    
    # Factor 2: Something you have (SMS code)
    if not verify_sms_code(username, sms_code):
        return False
    
    return True
```

## JSON Web Tokens (JWT)

### What is JWT?
JWT is a compact, URL-safe token format for securely transmitting information between parties.

### JWT Structure
```
Header.Payload.Signature
```

**Example:**
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

### JWT Components

#### Header
```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

#### Payload
```json
{
  "sub": "1234567890",
  "name": "John Doe",
  "iat": 1516239022,
  "exp": 1516242622
}
```

#### Signature
```
HMACSHA256(
  base64UrlEncode(header) + "." +
  base64UrlEncode(payload),
  secret
)
```

### JWT Usage in Authentication
```python
import jwt
from datetime import datetime, timedelta

def create_access_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=1),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None
```

## OAuth

### What is OAuth?
OAuth is an authorization framework that enables applications to obtain limited access to user accounts on HTTP services.

### OAuth vs Basic Authentication

| Aspect | OAuth | Basic Authentication |
|--------|-------|---------------------|
| **Purpose** | Authorization delegation | Simple authentication |
| **Security** | Token-based, revocable | Username/password in header |
| **Scope** | Granular permissions | Full access or none |
| **User Control** | User can revoke access | Must change password |

### OAuth Flow Example
```python
# OAuth 2.0 Authorization Code Flow
def oauth_flow():
    # 1. Redirect user to authorization server
    auth_url = f"https://auth.example.com/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code"
    
    # 2. User authorizes and returns with code
    authorization_code = request.args.get('code')
    
    # 3. Exchange code for access token
    token_response = requests.post('https://auth.example.com/token', data={
        'grant_type': 'authorization_code',
        'code': authorization_code,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    })
    
    access_token = token_response.json()['access_token']
    return access_token
```

## Biometric Authentication

### Use Cases
- **Mobile Banking**: Fingerprint or face recognition for app access
- **Corporate Security**: Retina scans for high-security areas
- **Healthcare**: Voice recognition for patient identification
- **Government**: Biometric passports and national ID systems

### Implementation Considerations
```python
class BiometricAuth:
    def __init__(self):
        self.biometric_reader = BiometricReader()
    
    def authenticate_user(self, user_id, biometric_data):
        # Store biometric template securely
        stored_template = self.get_user_template(user_id)
        
        # Compare with provided biometric data
        similarity_score = self.biometric_reader.compare(
            stored_template, 
            biometric_data
        )
        
        # Threshold-based authentication
        return similarity_score > 0.95
```

## Password Recovery

### Common Approaches

#### 1. Email-based Recovery
```python
def initiate_password_reset(email):
    # Generate secure reset token
    reset_token = generate_secure_token()
    
    # Store token with expiration
    store_reset_token(email, reset_token, expires_in=3600)
    
    # Send email with reset link
    send_reset_email(email, reset_token)

def reset_password(token, new_password):
    # Verify token validity
    if not is_valid_reset_token(token):
        raise InvalidTokenError()
    
    # Update password
    email = get_email_from_token(token)
    update_user_password(email, new_password)
    
    # Invalidate token
    invalidate_reset_token(token)
```

#### 2. Security Questions
```python
def verify_security_questions(user_id, answers):
    stored_questions = get_user_security_questions(user_id)
    
    for question_id, provided_answer in answers.items():
        stored_answer = stored_questions[question_id]
        if not verify_answer(stored_answer, provided_answer):
            return False
    
    return True
```

## Session Management

### Session Lifecycle
```python
class SessionManager:
    def create_session(self, user_id):
        session_id = generate_session_id()
        session_data = {
            'user_id': user_id,
            'created_at': datetime.utcnow(),
            'last_activity': datetime.utcnow(),
            'expires_at': datetime.utcnow() + timedelta(hours=24)
        }
        
        # Store in secure session store
        self.session_store.set(session_id, session_data)
        
        return session_id
    
    def validate_session(self, session_id):
        session_data = self.session_store.get(session_id)
        
        if not session_data:
            return None
        
        # Check expiration
        if datetime.utcnow() > session_data['expires_at']:
            self.destroy_session(session_id)
            return None
        
        # Update last activity
        session_data['last_activity'] = datetime.utcnow()
        self.session_store.set(session_id, session_data)
        
        return session_data['user_id']
```

### Session Security Best Practices
- Use secure, random session IDs
- Implement session timeout
- Store sessions securely (Redis, database)
- Use HTTPS for session cookies
- Implement session invalidation on logout

## Encryption in Authentication

### Role of Encryption
- **Data Protection**: Encrypts sensitive authentication data
- **Transmission Security**: Secures data in transit
- **Storage Security**: Protects stored credentials
- **Integrity**: Ensures data hasn't been tampered with

### Common Encryption Uses
```python
import bcrypt
from cryptography.fernet import Fernet

class AuthEncryption:
    def __init__(self):
        self.cipher = Fernet(ENCRYPTION_KEY)
    
    def hash_password(self, password):
        # Hash password for storage
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed
    
    def verify_password(self, password, hashed):
        # Verify password against hash
        return bcrypt.checkpw(password.encode('utf-8'), hashed)
    
    def encrypt_sensitive_data(self, data):
        # Encrypt sensitive authentication data
        return self.cipher.encrypt(data.encode('utf-8'))
    
    def decrypt_sensitive_data(self, encrypted_data):
        # Decrypt sensitive data
        return self.cipher.decrypt(encrypted_data).decode('utf-8')
```

## OpenID Connect

### How OpenID Connect Works
OpenID Connect is an identity layer built on top of OAuth 2.0.

### Advantages
- **Standardized**: Industry standard for identity
- **Interoperable**: Works across different providers
- **Secure**: Built on proven OAuth 2.0
- **User-Friendly**: Single sign-on experience

### Implementation Example
```python
def openid_connect_flow():
    # 1. Discovery
    discovery_doc = requests.get('https://accounts.google.com/.well-known/openid_configuration')
    auth_endpoint = discovery_doc.json()['authorization_endpoint']
    
    # 2. Authentication request
    auth_url = f"{auth_endpoint}?client_id={CLIENT_ID}&response_type=code&scope=openid email profile&redirect_uri={REDIRECT_URI}"
    
    # 3. Handle callback and exchange code for tokens
    # 4. Validate ID token
    id_token = validate_id_token(response['id_token'])
    
    return id_token['sub']  # User identifier
```

## Security Risks and Mitigation

### Common Vulnerabilities

#### 1. Password Attacks
**Risks:**
- Brute force attacks
- Dictionary attacks
- Password spraying

**Mitigation:**
```python
class PasswordSecurity:
    def __init__(self):
        self.max_attempts = 5
        self.lockout_duration = 900  # 15 minutes
    
    def check_login_attempts(self, username):
        attempts = self.get_failed_attempts(username)
        if attempts >= self.max_attempts:
            if self.is_locked_out(username):
                raise AccountLockedError()
        
        return True
    
    def record_failed_attempt(self, username):
        self.increment_failed_attempts(username)
        if self.get_failed_attempts(username) >= self.max_attempts:
            self.lock_account(username, self.lockout_duration)
```

#### 2. Session Hijacking
**Risks:**
- Session token theft
- Man-in-the-middle attacks

**Mitigation:**
- Use secure session tokens
- Implement session rotation
- Use HTTPS only
- Set secure cookie flags

#### 3. Token Vulnerabilities
**Risks:**
- JWT signature bypass
- Token replay attacks

**Mitigation:**
```python
def secure_jwt_validation(token):
    try:
        # Verify signature
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        
        # Check expiration
        if datetime.utcnow().timestamp() > payload['exp']:
            raise TokenExpiredError()
        
        # Check issuer
        if payload['iss'] != EXPECTED_ISSUER:
            raise InvalidIssuerError()
        
        # Check audience
        if payload['aud'] != EXPECTED_AUDIENCE:
            raise InvalidAudienceError()
        
        return payload
    except jwt.InvalidTokenError:
        raise InvalidTokenError()
```

## Two-Factor Authentication (2FA)

### How 2FA Improves Security
- **Defense in Depth**: Multiple layers of security
- **Reduced Risk**: Even if password is compromised, second factor protects
- **Compliance**: Meets many regulatory requirements
- **User Confidence**: Users feel more secure

### 2FA Implementation
```python
class TwoFactorAuth:
    def __init__(self):
        self.totp = pyotp.TOTP()
    
    def setup_2fa(self, user_id):
        # Generate secret key
        secret = pyotp.random_base32()
        
        # Generate QR code for authenticator app
        qr_code = pyotp.totp.TOTP(secret).provisioning_uri(
            name=user_id,
            issuer_name="MyApp"
        )
        
        # Store secret securely
        self.store_user_secret(user_id, secret)
        
        return qr_code
    
    def verify_2fa(self, user_id, token):
        secret = self.get_user_secret(user_id)
        totp = pyotp.TOTP(secret)
        
        return totp.verify(token, valid_window=1)
```

## Cookies and Tokens

### Role in Web Authentication

#### Cookies
```python
def set_auth_cookie(response, session_id):
    response.set_cookie(
        'session_id',
        session_id,
        httponly=True,      # Prevent XSS
        secure=True,        # HTTPS only
        samesite='Strict',  # CSRF protection
        max_age=86400       # 24 hours
    )
```

#### Tokens
```python
def token_based_auth(request):
    # Extract token from header
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        raise UnauthorizedError()
    
    token = auth_header.split(' ')[1]
    
    # Validate token
    user_id = validate_jwt_token(token)
    if not user_id:
        raise UnauthorizedError()
    
    return user_id
```

### Comparison

| Aspect | Cookies | Tokens |
|--------|---------|--------|
| **Storage** | Browser-managed | Client-managed |
| **CSRF Risk** | Higher | Lower |
| **XSS Risk** | Lower (httponly) | Higher |
| **Scalability** | Server-side storage | Stateless |
| **Mobile Support** | Limited | Better |

## Database Integration

### Authentication Database Schema
```sql
-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    salt VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    failed_login_attempts INTEGER DEFAULT 0,
    locked_until TIMESTAMP
);

-- Sessions table
CREATE TABLE user_sessions (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    session_token VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address INET,
    user_agent TEXT
);

-- Password reset tokens
CREATE TABLE password_reset_tokens (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    token VARCHAR(255) UNIQUE NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    used BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Database Authentication Service
```python
class DatabaseAuthService:
    def __init__(self, db_connection):
        self.db = db_connection
    
    def authenticate_user(self, username, password):
        # Get user from database
        user = self.db.execute(
            "SELECT * FROM users WHERE username = %s AND is_active = TRUE",
            (username,)
        ).fetchone()
        
        if not user:
            return None
        
        # Check if account is locked
        if user.locked_until and datetime.utcnow() < user.locked_until:
            raise AccountLockedError()
        
        # Verify password
        if not bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
            self.record_failed_login(user.id)
            return None
        
        # Reset failed attempts on successful login
        self.reset_failed_attempts(user.id)
        
        # Update last login
        self.update_last_login(user.id)
        
        return user
    
    def create_session(self, user_id, session_token, expires_at, ip_address, user_agent):
        self.db.execute(
            "INSERT INTO user_sessions (user_id, session_token, expires_at, ip_address, user_agent) VALUES (%s, %s, %s, %s, %s)",
            (user_id, session_token, expires_at, ip_address, user_agent)
        )
        self.db.commit()
    
    def validate_session(self, session_token):
        session = self.db.execute(
            "SELECT * FROM user_sessions WHERE session_token = %s AND expires_at > %s",
            (session_token, datetime.utcnow())
        ).fetchone()
        
        if not session:
            return None
        
        # Update last activity
        self.db.execute(
            "UPDATE user_sessions SET last_activity = %s WHERE id = %s",
            (datetime.utcnow(), session.id)
        )
        self.db.commit()
        
        return session.user_id
```

## Best Practices Summary

### Security Best Practices
1. **Use Strong Authentication**: Implement MFA where possible
2. **Encrypt Sensitive Data**: Hash passwords, encrypt tokens
3. **Implement Rate Limiting**: Prevent brute force attacks
4. **Use Secure Protocols**: HTTPS, secure cookies
5. **Regular Security Audits**: Monitor and update systems
6. **User Education**: Train users on security practices

### Implementation Best Practices
1. **Stateless Design**: Use JWT for scalability
2. **Session Management**: Implement proper session lifecycle
3. **Error Handling**: Don't reveal sensitive information
4. **Logging**: Log authentication events for monitoring
5. **Testing**: Comprehensive security testing
6. **Documentation**: Clear security documentation

### Compliance Considerations
- **GDPR**: User consent, data protection
- **PCI DSS**: Payment card data security
- **HIPAA**: Healthcare data protection
- **SOX**: Financial data security

## Conclusion

Authentication and authorization are fundamental security concepts that form the foundation of secure software systems. Understanding these concepts, their implementation, and associated security risks is crucial for building robust, secure applications.

The key is to implement multiple layers of security, stay updated with best practices, and continuously monitor and improve the authentication system based on evolving threats and requirements.
