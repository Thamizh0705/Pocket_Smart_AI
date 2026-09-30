from fastapi import APIRouter, Depends, HTTPException
from ..auth import create_token, hash_password, verify_password
from ..database import get_connection
from ..dependencies import get_current_user
from ..models import User
from ..schemas import LoginRequest, RegisterRequest

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/register")
def register(data: RegisterRequest):
    email = data.email.lower().strip()
    conn = get_connection()
    try:
        if conn.execute("SELECT id FROM users WHERE email=?", (email,)).fetchone():
            raise HTTPException(status_code=409, detail="Email already registered")
        cur = conn.execute("INSERT INTO users(name,email,password_hash) VALUES(?,?,?)", (data.name.strip(), email, hash_password(data.password)))
        conn.commit()
        user_id = cur.lastrowid
    finally:
        conn.close()
    return {"message":"Account created successfully","token":create_token(user_id),"user":{"id":user_id,"name":data.name.strip(),"email":email}}

@router.post("/login")
def login(data: LoginRequest):
    email = data.email.lower().strip()
    conn = get_connection()
    try:
        row = conn.execute("SELECT id,name,email,password_hash FROM users WHERE email=?", (email,)).fetchone()
    finally:
        conn.close()
    if row is None or not verify_password(data.password, row["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return {"message":"Login successful","token":create_token(row["id"]),"user":{"id":row["id"],"name":row["name"],"email":row["email"]}}

@router.post("/logout")
def logout():
    return {"message":"Logged out successfully"}

@router.get("/me")
def me(user: User = Depends(get_current_user)):
    return {"id":user.id,"name":user.name,"email":user.email}
