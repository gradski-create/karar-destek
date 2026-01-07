from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from jose import jwt
from datetime import datetime, timedelta
import os

SECRET_KEY = os.getenv("SECRET_KEY", "LOCAL_DEV_SECRET")
ALGORITHM = "HS256"

app = FastAPI()

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
    db = SessionLocal()
    user = db.query(User).filter(User.username == data.username.strip()).first()
    db.close()

    if not user or not verify_password(data.password, user.password_hash):
        return {"status": "error", "message": "Hatalı giriş"}

    token = create_token({
        "sub": user.username,
        "role": user.role
    })

    return {
        "status": "ok",
        "token": token,
        "role": user.role
    }

# ---------- STATIC (EN SON!) ----------
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app.mount(
    "/frontend",
    StaticFiles(directory=os.path.join(BASE_DIR, "frontend"), html=True),
    name="frontend"
)



