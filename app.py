from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from jose import jwt
from datetime import datetime, timedelta
import os

SECRET_KEY = os.getenv("SECRET_KEY", "LOCAL_DEV_SECRET")
ALGORITHM = "HS256"

app = FastAPI()

from fastapi.responses import RedirectResponse

@app.get("/")
def root():
    return RedirectResponse(url="/frontend/login.html")


# ---------- MODELLER ----------
class LoginRequest(BaseModel):
    username: str
    password: str

# ---------- TOKEN ----------
def create_token(data: dict):
    expire = datetime.utcnow() + timedelta(minutes=60)
    data.update({"exp": expire})
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

# ---------- API (ÖNCE!) ----------
@app.post("/api/login")
def login(data: LoginRequest):
    username = data.username.strip()
    password = data.password.strip()

    if username == "admin" and password == "1234":
        token = create_token({"sub": username})
        return {
            "status": "ok",
            "message": "Giriş başarılı",
            "token": token
        }

    return {
        "status": "error",
        "message": "Hatalı giriş"
    }



# ---------- STATIC (EN SON!) ----------
app.mount("/frontend", StaticFiles(directory="frontend", html=True), name="frontend")


