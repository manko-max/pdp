# JWT (JSON Web Token) Authentication

## Table of Contents
1. [Overview](#overview)
2. [What is JWT](#what-is-jwt)
3. [JWT Structure](#jwt-structure)
4. [How to Decrypt JWT](#how-to-decrypt-jwt)
5. [Access and Refresh Tokens](#access-and-refresh-tokens)
6. [JWT Generation](#jwt-generation)
7. [JWT Verification](#jwt-verification)
8. [JWT-Based Authentication](#jwt-based-authentication)
9. [Secure Storage](#secure-storage)
10. [Custom Claims](#custom-claims)
11. [Token Revocation and Expiration](#token-revocation-and-expiration)
12. [Stateless Applications](#stateless-applications)
13. [Single Sign-On (SSO)](#single-sign-on-sso)
14. [API Authentication](#api-authentication)
15. [Monitoring and Logging](#monitoring-and-logging)
16. [Best Practices](#best-practices)
17. [Security Considerations](#security-considerations)

## Overview

JWT (JSON Web Token) is a compact, URL-safe token format for securely transmitting information between parties. It's widely used for authentication and authorization in web applications, APIs, and distributed systems.

## What is JWT

### Definition
JWT is an open standard (RFC 7519) that defines a compact and self-contained way for securely transmitting information between parties as a JSON object. This information can be verified and trusted because it is digitally signed.

### Key Characteristics
- **Compact**: Small size, can be sent via URL, POST parameter, or HTTP header
- **Self-contained**: Contains all necessary information about the user
- **Stateless**: No need to store session information on the server
- **Secure**: Digitally signed to prevent tampering
- **Standardized**: Based on industry standards (RFC 7519)

### Use Cases
- **Authentication**: Verify user identity
- **Authorization**: Control access to resources
- **Information Exchange**: Securely transmit information between parties
- **Single Sign-On (SSO)**: Authenticate across multiple applications
- **API Security**: Secure API endpoints

## JWT Structure

### Three Parts Separated by Dots (.)
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

### 1. Header
```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```
- **alg**: Algorithm used for signing (HS256, RS256, ES256, etc.)
- **typ**: Token type (always "JWT")

### 2. Payload (Claims)
```json
{
  "sub": "1234567890",
  "name": "John Doe",
  "iat": 1516239022,
  "exp": 1516242622,
  "iss": "myapp.com",
  "aud": "myapp-users"
}
```

#### Standard Claims (Registered Claims)
- **iss** (issuer): Who issued the token
- **sub** (subject): Who the token is about
- **aud** (audience): Who the token is intended for
- **exp** (expiration time): When the token expires
- **nbf** (not before): Token not valid before this time
- **iat** (issued at): When the token was issued
- **jti** (JWT ID): Unique identifier for the token

#### Public Claims
- Can be defined at will
- Should be collision-resistant
- Often defined in IANA JWT Registry

#### Private Claims
- Custom claims agreed upon between parties
- Not registered or public

### 3. Signature
```
HMACSHA256(
  base64UrlEncode(header) + "." +
  base64UrlEncode(payload),
  secret
)
```

## How to Decrypt JWT

### Understanding JWT Decryption
JWTs are not encrypted - they are **signed**. The signature ensures integrity and authenticity, but the payload is base64-encoded and readable by anyone.

### Manual Decryption Steps

#### 1. Split the Token
```javascript
const token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c";

const parts = token.split('.');
const header = parts[0];
const payload = parts[1];
const signature = parts[2];
```

#### 2. Decode Header
```javascript
// Base64URL decode
const decodedHeader = JSON.parse(atob(header.replace(/-/g, '+').replace(/_/g, '/')));
console.log(decodedHeader);
// Output: { "alg": "HS256", "typ": "JWT" }
```

#### 3. Decode Payload
```javascript
// Base64URL decode
const decodedPayload = JSON.parse(atob(payload.replace(/-/g, '+').replace(/_/g, '/')));
console.log(decodedPayload);
// Output: { "sub": "1234567890", "name": "John Doe", "iat": 1516239022 }
```

#### 4. Verify Signature (Optional)
```javascript
// This requires the secret key
const expectedSignature = crypto
  .createHmac('sha256', secret)
  .update(header + '.' + payload)
  .digest('base64url');

const isValid = signature === expectedSignature;
```

### Online JWT Decoders
- **jwt.io**: Popular JWT debugger and decoder
- **jwtdecode.com**: Simple JWT decoder
- **jwt.ms**: Microsoft's JWT decoder

### Programmatic Decoding

#### JavaScript/Node.js
```javascript
// Using jsonwebtoken library
const jwt = require('jsonwebtoken');

// Decode without verification
const decoded = jwt.decode(token);
console.log(decoded);

// Verify and decode
const verified = jwt.verify(token, secret);
console.log(verified);
```

#### Python
```python
import jwt

# Decode without verification
decoded = jwt.decode(token, options={"verify_signature": False})
print(decoded)

# Verify and decode
decoded = jwt.decode(token, secret, algorithms=["HS256"])
print(decoded)
```

## Access and Refresh Tokens

### Access Token
- **Purpose**: Authenticate API requests
- **Lifetime**: Short (15 minutes to 1 hour)
- **Storage**: Memory or secure storage
- **Usage**: Included in Authorization header
- **Security**: High risk if compromised

### Refresh Token
- **Purpose**: Obtain new access tokens
- **Lifetime**: Long (days to weeks)
- **Storage**: Secure, HTTP-only cookie or secure storage
- **Usage**: Exchanged for new access tokens
- **Security**: Lower risk, can be revoked

### Token Flow
```
1. User logs in
2. Server issues access token (short-lived) + refresh token (long-lived)
3. Client uses access token for API requests
4. When access token expires, client uses refresh token to get new access token
5. Refresh token can be revoked for security
```

### Implementation Example
```javascript
// Login response
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 3600
}

// API request with access token
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

// Refresh token request
POST /auth/refresh
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

## JWT Generation

### Basic JWT Generation
```javascript
const jwt = require('jsonwebtoken');

const payload = {
  sub: "1234567890",
  name: "John Doe",
  iat: Math.floor(Date.now() / 1000),
  exp: Math.floor(Date.now() / 1000) + (60 * 60) // 1 hour
};

const secret = "your-secret-key";
const token = jwt.sign(payload, secret, { algorithm: 'HS256' });
```

### With Custom Claims
```javascript
const payload = {
  sub: "1234567890",
  name: "John Doe",
  email: "john@example.com",
  role: "admin",
  permissions: ["read", "write", "delete"],
  iat: Math.floor(Date.now() / 1000),
  exp: Math.floor(Date.now() / 1000) + (60 * 60)
};

const token = jwt.sign(payload, secret, { algorithm: 'HS256' });
```

### Different Algorithms
```javascript
// HMAC with SHA-256
const token1 = jwt.sign(payload, secret, { algorithm: 'HS256' });

// RSA with SHA-256
const token2 = jwt.sign(payload, privateKey, { algorithm: 'RS256' });

// ECDSA with SHA-256
const token3 = jwt.sign(payload, privateKey, { algorithm: 'ES256' });
```

## JWT Verification

### Basic Verification
```javascript
const jwt = require('jsonwebtoken');

try {
  const decoded = jwt.verify(token, secret);
  console.log(decoded);
} catch (error) {
  console.error('Invalid token:', error.message);
}
```

### With Options
```javascript
const options = {
  algorithms: ['HS256'],
  issuer: 'myapp.com',
  audience: 'myapp-users',
  clockTolerance: 30 // 30 seconds tolerance
};

const decoded = jwt.verify(token, secret, options);
```

### Middleware Example
```javascript
function authenticateToken(req, res, next) {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];

  if (!token) {
    return res.status(401).json({ error: 'Access token required' });
  }

  jwt.verify(token, secret, (err, user) => {
    if (err) {
      return res.status(403).json({ error: 'Invalid token' });
    }
    req.user = user;
    next();
  });
}
```

## JWT-Based Authentication

### Authentication Flow
```
1. User provides credentials (username/password)
2. Server validates credentials
3. Server generates JWT with user information
4. Server returns JWT to client
5. Client stores JWT and includes it in subsequent requests
6. Server validates JWT on each request
7. Server processes request if JWT is valid
```

### Login Endpoint
```javascript
app.post('/login', async (req, res) => {
  const { username, password } = req.body;
  
  // Validate credentials
  const user = await validateUser(username, password);
  if (!user) {
    return res.status(401).json({ error: 'Invalid credentials' });
  }
  
  // Generate JWT
  const payload = {
    sub: user.id,
    name: user.name,
    email: user.email,
    role: user.role,
    iat: Math.floor(Date.now() / 1000),
    exp: Math.floor(Date.now() / 1000) + (60 * 60) // 1 hour
  };
  
  const token = jwt.sign(payload, secret, { algorithm: 'HS256' });
  
  res.json({
    access_token: token,
    token_type: 'Bearer',
    expires_in: 3600
  });
});
```

### Protected Route
```javascript
app.get('/profile', authenticateToken, (req, res) => {
  res.json({
    user: {
      id: req.user.sub,
      name: req.user.name,
      email: req.user.email,
      role: req.user.role
    }
  });
});
```

## Secure Storage

### Browser Storage Options

#### 1. HTTP-Only Cookies (Recommended)
```javascript
// Server sets cookie
res.cookie('token', token, {
  httpOnly: true,
  secure: true,
  sameSite: 'strict',
  maxAge: 3600000 // 1 hour
});
```

#### 2. Local Storage (Not Recommended for Sensitive Data)
```javascript
// Store token
localStorage.setItem('access_token', token);

// Retrieve token
const token = localStorage.getItem('access_token');
```

#### 3. Session Storage
```javascript
// Store token
sessionStorage.setItem('access_token', token);

// Retrieve token
const token = sessionStorage.getItem('access_token');
```

#### 4. Memory Storage (Most Secure)
```javascript
// Store in memory variable
let accessToken = null;

// Set token
accessToken = token;

// Get token
const token = accessToken;
```

### Security Best Practices
- **Use HTTPS**: Always transmit tokens over HTTPS
- **Short Expiration**: Use short-lived access tokens
- **Secure Storage**: Use HTTP-only cookies when possible
- **Token Rotation**: Implement token refresh mechanism
- **Secure Headers**: Use appropriate security headers

## Custom Claims

### Adding Custom Claims
```javascript
const payload = {
  // Standard claims
  sub: "1234567890",
  iat: Math.floor(Date.now() / 1000),
  exp: Math.floor(Date.now() / 1000) + (60 * 60),
  
  // Custom claims
  user_id: "1234567890",
  username: "johndoe",
  role: "admin",
  permissions: ["read", "write", "delete"],
  department: "engineering",
  team: "backend",
  subscription: "premium",
  features: ["analytics", "export", "api_access"]
};
```

### Using Custom Claims
```javascript
// Middleware to check permissions
function requirePermission(permission) {
  return (req, res, next) => {
    if (!req.user.permissions.includes(permission)) {
      return res.status(403).json({ error: 'Insufficient permissions' });
    }
    next();
  };
}

// Usage
app.delete('/users/:id', authenticateToken, requirePermission('delete'), (req, res) => {
  // Delete user logic
});
```

### Namespaced Claims
```javascript
const payload = {
  sub: "1234567890",
  iat: Math.floor(Date.now() / 1000),
  exp: Math.floor(Date.now() / 1000) + (60 * 60),
  
  // Namespaced custom claims
  "https://myapp.com/claims/user_id": "1234567890",
  "https://myapp.com/claims/role": "admin",
  "https://myapp.com/claims/permissions": ["read", "write", "delete"]
};
```

## Token Revocation and Expiration

### Token Expiration
```javascript
const payload = {
  sub: "1234567890",
  iat: Math.floor(Date.now() / 1000),
  exp: Math.floor(Date.now() / 1000) + (15 * 60), // 15 minutes
  jti: "unique-token-id" // JWT ID for revocation
};
```

### Token Revocation Strategies

#### 1. Blacklist Approach
```javascript
// Store revoked tokens
const revokedTokens = new Set();

// Revoke token
function revokeToken(tokenId) {
  revokedTokens.add(tokenId);
}

// Check if token is revoked
function isTokenRevoked(tokenId) {
  return revokedTokens.has(tokenId);
}

// Middleware to check revocation
function checkTokenRevocation(req, res, next) {
  if (isTokenRevoked(req.user.jti)) {
    return res.status(401).json({ error: 'Token has been revoked' });
  }
  next();
}
```

#### 2. Short Expiration + Refresh
```javascript
// Short-lived access tokens (15 minutes)
const accessToken = jwt.sign({
  sub: "1234567890",
  iat: Math.floor(Date.now() / 1000),
  exp: Math.floor(Date.now() / 1000) + (15 * 60)
}, secret);

// Long-lived refresh tokens (7 days)
const refreshToken = jwt.sign({
  sub: "1234567890",
  type: "refresh",
  iat: Math.floor(Date.now() / 1000),
  exp: Math.floor(Date.now() / 1000) + (7 * 24 * 60 * 60)
}, secret);
```

#### 3. Version-Based Revocation
```javascript
// Include version in token
const payload = {
  sub: "1234567890",
  version: 1, // Increment to revoke all tokens
  iat: Math.floor(Date.now() / 1000),
  exp: Math.floor(Date.now() / 1000) + (60 * 60)
};

// Check version on verification
function verifyToken(token) {
  const decoded = jwt.verify(token, secret);
  if (decoded.version < currentVersion) {
    throw new Error('Token version outdated');
  }
  return decoded;
}
```

## Stateless Applications

### Benefits of Stateless JWT
- **Scalability**: No server-side session storage
- **Performance**: No database lookups for authentication
- **Simplicity**: Self-contained tokens
- **Load Balancing**: Any server can validate tokens

### Implementation
```javascript
// No session storage needed
app.get('/api/data', authenticateToken, (req, res) => {
  // Token contains all necessary user information
  const userId = req.user.sub;
  const userRole = req.user.role;
  
  // Process request without database lookup
  res.json({ data: 'protected data' });
});
```

### Considerations
- **Token Size**: Larger tokens due to embedded data
- **Revocation**: Harder to revoke tokens immediately
- **Security**: Tokens must be kept secure
- **Refresh**: Need refresh mechanism for long sessions

## Single Sign-On (SSO)

### SSO Flow with JWT
```
1. User logs in to Identity Provider (IdP)
2. IdP issues JWT with user information
3. User accesses Service Provider (SP)
4. SP validates JWT with IdP
5. SP grants access based on JWT claims
```

### JWT for SSO
```javascript
// Identity Provider issues JWT
const ssoToken = jwt.sign({
  sub: "1234567890",
  name: "John Doe",
  email: "john@example.com",
  iss: "https://idp.example.com",
  aud: "https://sp.example.com",
  iat: Math.floor(Date.now() / 1000),
  exp: Math.floor(Date.now() / 1000) + (60 * 60)
}, secret, { algorithm: 'RS256' });
```

### Service Provider Validation
```javascript
// Service Provider validates JWT
function validateSSOToken(token) {
  const decoded = jwt.verify(token, publicKey, {
    algorithms: ['RS256'],
    issuer: 'https://idp.example.com',
    audience: 'https://sp.example.com'
  });
  return decoded;
}
```

## API Authentication

### REST API Authentication
```javascript
// API endpoint with JWT authentication
app.get('/api/users', authenticateToken, (req, res) => {
  const userRole = req.user.role;
  const userId = req.user.sub;
  
  // Return data based on user role
  if (userRole === 'admin') {
    res.json(users);
  } else {
    res.json(users.filter(u => u.id === userId));
  }
});
```

### GraphQL Authentication
```javascript
// GraphQL context with JWT
const context = ({ req }) => {
  const token = req.headers.authorization?.split(' ')[1];
  if (token) {
    try {
      const user = jwt.verify(token, secret);
      return { user };
    } catch (error) {
      return { user: null };
    }
  }
  return { user: null };
};
```

### Microservices Authentication
```javascript
// Service-to-service authentication
const serviceToken = jwt.sign({
  sub: "service-a",
  iss: "service-a",
  aud: "service-b",
  iat: Math.floor(Date.now() / 1000),
  exp: Math.floor(Date.now() / 1000) + (60 * 60)
}, serviceSecret, { algorithm: 'HS256' });

// Include in service requests
const response = await fetch('https://service-b/api/data', {
  headers: {
    'Authorization': `Bearer ${serviceToken}`
  }
});
```

## Monitoring and Logging

### JWT Usage Logging
```javascript
// Log JWT usage
function logJWTUsage(req, res, next) {
  const token = req.headers.authorization?.split(' ')[1];
  if (token) {
    try {
      const decoded = jwt.decode(token);
      console.log({
        timestamp: new Date().toISOString(),
        user_id: decoded.sub,
        endpoint: req.path,
        method: req.method,
        ip: req.ip,
        user_agent: req.get('User-Agent')
      });
    } catch (error) {
      console.error('Failed to decode JWT:', error);
    }
  }
  next();
}
```

### Security Monitoring
```javascript
// Monitor for suspicious activity
function monitorJWTSecurity(req, res, next) {
  const token = req.headers.authorization?.split(' ')[1];
  if (token) {
    try {
      const decoded = jwt.verify(token, secret);
      
      // Check for expired tokens
      if (decoded.exp < Math.floor(Date.now() / 1000)) {
        console.warn('Expired token used:', decoded.sub);
      }
      
      // Check for unusual access patterns
      if (isUnusualAccess(decoded.sub, req.ip)) {
        console.warn('Unusual access pattern detected:', decoded.sub);
      }
      
    } catch (error) {
      console.error('Invalid token attempt:', error.message);
    }
  }
  next();
}
```

### Audit Trail
```javascript
// Create audit trail
function createAuditTrail(req, res, next) {
  const originalSend = res.send;
  
  res.send = function(data) {
    // Log the request and response
    const auditLog = {
      timestamp: new Date().toISOString(),
      user_id: req.user?.sub,
      endpoint: req.path,
      method: req.method,
      status_code: res.statusCode,
      ip: req.ip,
      user_agent: req.get('User-Agent')
    };
    
    // Store audit log
    storeAuditLog(auditLog);
    
    originalSend.call(this, data);
  };
  
  next();
}
```

## Best Practices

### 1. **Token Security**
- Use strong, random secrets
- Implement proper key rotation
- Use appropriate algorithms (HS256, RS256)
- Keep secrets secure and never expose them

### 2. **Token Lifetime**
- Use short-lived access tokens (15-60 minutes)
- Implement refresh token mechanism
- Set appropriate expiration times
- Consider user activity for token renewal

### 3. **Storage Security**
- Use HTTP-only cookies when possible
- Implement secure storage mechanisms
- Avoid storing sensitive data in localStorage
- Use secure transmission (HTTPS)

### 4. **Validation**
- Always validate token signature
- Check token expiration
- Verify issuer and audience
- Implement proper error handling

### 5. **Claims Management**
- Use standard claims when possible
- Implement custom claims carefully
- Avoid storing sensitive data in tokens
- Use namespaced claims for custom data

## Security Considerations

### 1. **Token Theft**
- **Risk**: Tokens can be stolen and used maliciously
- **Mitigation**: Use short expiration times, implement token refresh, monitor usage

### 2. **Token Tampering**
- **Risk**: Tokens can be modified if signature is compromised
- **Mitigation**: Use strong secrets, implement proper signature validation

### 3. **Token Replay**
- **Risk**: Stolen tokens can be reused
- **Mitigation**: Use short expiration times, implement token blacklisting

### 4. **Information Disclosure**
- **Risk**: JWT payload is base64-encoded and readable
- **Mitigation**: Don't store sensitive data in tokens, use encryption if needed

### 5. **Algorithm Confusion**
- **Risk**: Attackers might use different algorithms
- **Mitigation**: Specify allowed algorithms explicitly

### 6. **Key Management**
- **Risk**: Compromised keys can lead to token forgery
- **Mitigation**: Implement proper key rotation, use strong key management

---

## Conclusion

JWT is a powerful tool for authentication and authorization in modern web applications. When implemented correctly with proper security measures, it provides a scalable, stateless solution for managing user sessions and API access.

**Key takeaways:**
- JWT is self-contained and stateless
- Always validate tokens properly
- Use short expiration times and refresh tokens
- Implement proper security measures
- Monitor and log JWT usage
- Follow best practices for storage and transmission
