from fastapi.testclient import TestClient
from app.main import app

client=TestClient(app)

def test_health():
    response=client.get("/health")
    assert response.status_code==200
    assert response.json()=={"status":"ok"}

def test_pages():
    for path in ["/","/login","/register","/dashboard","/history","/home","/party","/jewelry"]:
        response=client.get(path)
        assert response.status_code==200

def test_static_js():
    response=client.get("/static/js/app.js")
    assert response.status_code==200

def test_register_login():
    email="test@example.com"
    response=client.post("/api/auth/register",json={"name":"Test User","email":email,"password":"password123"})
    assert response.status_code in (200,409)
    if response.status_code==409:
        response=client.post("/api/auth/login",json={"email":email,"password":"password123"})
    assert response.status_code==200
    token=response.json()["token"]
    me=client.get("/api/auth/me",headers={"Authorization":f"Bearer {token}"})
    assert me.status_code==200

def test_protected_without_token():
    assert client.get("/api/session-data").status_code==401
