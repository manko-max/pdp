"""
Super Simple Social Authentication Example
Only API methods, no HTML, no frontend
"""

from fastapi import FastAPI, HTTPException
import httpx
import secrets

app = FastAPI(title="Simple Social Auth")

# Simple in-memory storage
users = {}
sessions = {}

# OAuth2 configs (replace with your real credentials)
CONFIGS = {
    "google": {
        "client_id": "your-google-client-id",
        "client_secret": "your-google-client-secret",
        "token_url": "https://oauth2.googleapis.com/token",
        "user_info_url": "https://www.googleapis.com/oauth2/v2/userinfo"
    },
    "github": {
        "client_id": "your-github-client-id",
        "client_secret": "your-github-client-secret",
        "token_url": "https://github.com/login/oauth/access_token",
        "user_info_url": "https://api.github.com/user"
    }
}


@app.get("/auth/{provider}/url")
async def get_auth_url(provider: str):
    """Get authorization URL for the provider"""
    if provider not in CONFIGS:
        raise HTTPException(status_code=404, detail="Provider not supported")

    config = CONFIGS[provider]
    state = secrets.token_urlsafe(16)
    sessions[state] = provider

    if provider == "google":
        auth_url = f"https://accounts.google.com/o/oauth2/auth?client_id={config['client_id']}&redirect_uri=http://localhost:8000/auth/{provider}/callback&scope=openid email profile&response_type=code&state={state}"
    elif provider == "github":
        auth_url = f"https://github.com/login/oauth/authorize?client_id={config['client_id']}&redirect_uri=http://localhost:8000/auth/{provider}/callback&scope=user:email&state={state}"

    return {"auth_url": auth_url, "state": state}


@app.post("/auth/{provider}/callback")
async def handle_callback(provider: str, code: str, state: str):
    """Handle OAuth2 callback and return access token"""
    if provider not in CONFIGS:
        raise HTTPException(status_code=404, detail="Provider not supported")

    if state not in sessions:
        raise HTTPException(status_code=400, detail="Invalid state")

    config = CONFIGS[provider]

    # Exchange code for access token
    async with httpx.AsyncClient() as client:
        token_data = {
            "client_id": config["client_id"],
            "client_secret": config["client_secret"],
            "code": code
        }

        response = await client.post(config["token_url"], data=token_data)
        token_response = response.json()
        access_token = token_response.get("access_token")

        if not access_token:
            raise HTTPException(status_code=400, detail="Failed to get access token")

    # Get user info
    async with httpx.AsyncClient() as client:
        if provider == "google":
            headers = {"Authorization": f"Bearer {access_token}"}
        else:  # github
            headers = {"Authorization": f"token {access_token}"}

        response = await client.get(config["user_info_url"], headers=headers)
        user_info = response.json()

    # Create or get user
    email = user_info.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="Email not provided")

    user_id = f"{provider}_{user_info['id']}"
    if user_id not in users:
        users[user_id] = {
            "id": user_id,
            "email": email,
            "name": user_info.get("name", ""),
            "provider": provider
        }

    # Create session token
    session_token = secrets.token_urlsafe(32)
    sessions[session_token] = user_id

    # Clean up state
    del sessions[state]

    return {
        "access_token": session_token,
        "user": users[user_id]
    }


@app.get("/me")
async def get_current_user(Authorization: str = None):
    """Get current user info"""
    if not Authorization or not Authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="No token provided")

    token = Authorization.split(" ")[1]
    if token not in sessions:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_id = sessions[token]
    if user_id not in users:
        raise HTTPException(status_code=401, detail="User not found")

    return users[user_id]


@app.post("/logout")
async def logout(Authorization: str = None):
    """Logout user"""
    if not Authorization or not Authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="No token provided")

    token = Authorization.split(" ")[1]
    if token in sessions:
        del sessions[token]

    return {"message": "Logged out"}


@app.get("/users")
async def list_users():
    """List all users (for demo)"""
    return {"users": list(users.values())}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
