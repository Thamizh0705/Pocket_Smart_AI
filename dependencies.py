from fastapi import Depends, Header, HTTPException
from .auth import decode_access_token
from .database import get_connection
from .models import User


def get_current_user(authorization: str | None = Header(default=None)) -> User:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Authentication required")
    token = authorization.split(" ", 1)[1].strip()
    user_id = decode_access_token(token)
    conn = get_connection()
    try:
        row = conn.execute("SELECT id,name,email,password_hash FROM users WHERE id=?", (user_id,)).fetchone()
    finally:
        conn.close()
    if row is None:
        raise HTTPException(status_code=401, detail="User not found")
    return User(id=row["id"], name=row["name"], email=row["email"], password_hash=row["password_hash"])

current_user = get_current_user
