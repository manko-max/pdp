# Social Authentication

## Table of Contents
1. [Overview](#overview)
2. [OAuth1 vs OAuth2](#oauth1-vs-oauth2)
3. [Simple Implementation](#simple-implementation)
4. [How It Works](#how-it-works)
5. [Setup](#setup)

## Overview

Social authentication allows users to sign in using their existing accounts from Google, Facebook, GitHub, etc. No need to create new accounts or remember passwords.

## OAuth1 vs OAuth2

### **OAuth1.0a (2009)**
**How it works:**
1. App requests "request token" from provider
2. User authorizes with this token
3. Provider returns "verifier"
4. App exchanges request token + verifier for access token
5. Uses access token for API calls

**Features:**
- More complex process (3 steps instead of 2)
- Signs every request
- Works only over HTTPS
- Harder to implement

**Used by:** Twitter (partially), some legacy APIs

### **OAuth2 (2012)**
**How it works:**
1. App redirects user to provider
2. User authorizes
3. Provider returns authorization code
4. App exchanges code for access token
5. Uses access token for API calls

**Features:**
- Easier to implement
- No request signing required
- Works over HTTPS
- More flexible

**Used by:** Google, Facebook, GitHub, most modern APIs

### **Key Differences:**

| Aspect | OAuth1.0a | OAuth2 |
|--------|-----------|---------|
| **Complexity** | Complex (3 steps) | Simple (2 steps) |
| **Security** | Request signing | HTTPS only |
| **Tokens** | Request token → Access token | Authorization code → Access token |
| **Implementation** | Complex | Simple |
| **Usage** | Legacy | Modern standard |

## Simple Implementation

### **Only 5 API methods:**

1. **`GET /auth/{provider}/url`** - get authorization URL
2. **`POST /auth/{provider}/callback`** - handle provider callback  
3. **`GET /me`** - get current user information
4. **`POST /logout`** - logout user
5. **`GET /users`** - list all users (for demo)

### **Usage example:**

```bash
# 1. Get authorization URL
curl http://localhost:8000/auth/google/url
# Response: {"auth_url": "https://accounts.google.com/...", "state": "..."}

# 2. After authorization - handle callback
curl -X POST "http://localhost:8000/auth/google/callback?code=...&state=..."
# Response: {"access_token": "...", "user": {...}}

# 3. Get user information
curl -H "Authorization: Bearer your_token" http://localhost:8000/me

# 4. Logout
curl -X POST -H "Authorization: Bearer your_token" http://localhost:8000/logout
```

## How It Works

### **OAuth2 Flow (simplified):**

1. **Get URL** - `GET /auth/google/url`
   - Generate random `state` (CSRF protection)
   - Return URL for Google authorization

2. **User authorization**
   - User visits the URL
   - Authorizes in Google
   - Google redirects back with `code`

3. **Handle callback** - `POST /auth/google/callback`
   - Exchange `code` for `access_token`
   - Get user data via Google API
   - Create/update user in our system
   - Issue our own `session_token`

4. **Use token**
   - All subsequent requests with `Authorization: Bearer session_token`
   - Validate token and return user data

### **What happens inside:**

```python
# 1. Generate URL
state = secrets.token_urlsafe(16)  # CSRF protection
auth_url = f"https://accounts.google.com/o/oauth2/auth?client_id={client_id}&..."

# 2. Exchange code for token
token_data = {"client_id": client_id, "client_secret": client_secret, "code": code}
response = await client.post("https://oauth2.googleapis.com/token", data=token_data)
access_token = response.json()["access_token"]

# 3. Get user data
headers = {"Authorization": f"Bearer {access_token}"}
response = await client.get("https://www.googleapis.com/oauth2/v2/userinfo", headers=headers)
user_info = response.json()

# 4. Create session
session_token = secrets.token_urlsafe(32)
sessions[session_token] = user_id
```

## Setup

### **1. Provider setup:**

#### **Google:**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable Google+ API
4. Create OAuth2 credentials
5. Set authorized redirect URIs: `http://localhost:8000/auth/google/callback`
6. Note down Client ID and Client Secret

#### **GitHub:**
1. Go to GitHub Settings > Developer settings
2. Create a new OAuth App
3. Set Authorization callback URL: `http://localhost:8000/auth/github/callback`
4. Note down Client ID and Client Secret

### **2. Configure credentials:**

```python
# In simple_social_auth.py replace:
CONFIGS = {
    "google": {
        "client_id": "your-google-client-id",
        "client_secret": "your-google-client-secret",
        # ...
    },
    "github": {
        "client_id": "your-github-client-id",
        "client_secret": "your-github-client-secret",
        # ...
    }
}
```

### **3. Run:**

```bash
# Install dependencies
pip install fastapi uvicorn httpx

# Run the application
python simple_social_auth.py
```

### **4. Testing:**

Open http://localhost:8000/docs for interactive API documentation.

---

## Conclusion

Social authentication is a simple way to let users sign in to your application using their existing social media accounts.

**Key points:**
- OAuth2 is simpler than OAuth1.0a
- Only 5 API methods for full implementation
- Use HTTPS and validate state parameter
- Store credentials in environment variables
- Test with real providers
