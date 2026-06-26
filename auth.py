"""
ARIA Auth — Simple JWT-based auth using Supabase
"""
import os
import hashlib
import secrets
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

def get_db():
    from supabase import create_client
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    return create_client(url, key)

def hash_password(password: str, salt: str = None):
    if not salt:
        salt = secrets.token_hex(16)
    hashed = hashlib.sha256((password + salt).encode()).hexdigest()
    return hashed, salt

def create_token(user_id: int, email: str, name: str) -> str:
    import base64
    payload = json.dumps({
        "user_id": user_id,
        "email": email,
        "name": name,
        "exp": (datetime.utcnow() + timedelta(days=30)).isoformat()
    })
    return base64.urlsafe_b64encode(payload.encode()).decode()

def verify_token(token: str) -> dict | None:
    import base64
    try:
        payload = json.loads(base64.urlsafe_b64decode(token.encode()).decode())
        exp = datetime.fromisoformat(payload["exp"])
        if datetime.utcnow() > exp:
            return None
        return payload
    except:
        return None

def signup(name: str, email: str, password: str) -> dict:
    db = get_db()
    existing = db.table("users").select("id").eq("email", email).execute().data
    if existing:
        raise ValueError("Email already registered!")
    hashed, salt = hash_password(password)
    result = db.table("users").insert({
        "name": name,
        "email": email,
        "password_hash": hashed,
        "password_salt": salt
    }).execute()
    user = result.data[0]
    token = create_token(user["id"], email, name)
    return {"access_token": token, "user": {"id": user["id"], "name": name, "email": email}}

def login(email: str, password: str) -> dict:
    db = get_db()
    rows = db.table("users").select("*").eq("email", email).execute().data
    if not rows:
        raise ValueError("Email not found!")
    user = rows[0]
    hashed, _ = hash_password(password, user["password_salt"])
    if hashed != user["password_hash"]:
        raise ValueError("Incorrect password!")
    token = create_token(user["id"], email, user["name"])
    return {"access_token": token, "user": {"id": user["id"], "name": user["name"], "email": email}}