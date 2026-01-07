from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI()
from fastapi.staticfiles import StaticFiles

app.mount("/frontend", StaticFiles(directory="frontend", html=True), name="frontend")



# ---------- STATIK DOSYALAR (login.html, app.js) ----------
app.mount("/", StaticFiles(directory="static", html=True), name="static")

# ---------- TEST ENDPOINT ----------
@app.get("/api/status")
def status():
    return {"status": "ok", "message": "Backend çalışıyor"}

# ---------- LOGIN MODEL ----------
class LoginRequest(BaseModel):
    username: str
    password: str

# ---------- LOGIN ENDPOINT ----------
@app.post("/api/login")
def login(data: LoginRequest):
    if data.username == "admin" and data.password == "1234":
        token = create_token({"sub": data.username})
        return {
            "status": "ok",
            "message": "Giriş başarılı",
            "token": token
        }
    return {"status": "error", "message": "Hatalı giriş"}

