import json
import hashlib
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()
DATA_FILE = "backend/data.json"
AUTH_FILE = "backend/auth.json"

class RegisterRequest(BaseModel):
    name: str
    email: str
    phone: str
    company: str
    website: str
    category: str
    description: str
    comp_scale: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

def load_data(file):
    try:
        with open(file, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"id": {}}

def save_data(data, file):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

@app.post("/register")
async def register_user(request: RegisterRequest):
    received_dict = request.model_dump()

    data = load_data(DATA_FILE)
    auth_data = load_data(AUTH_FILE)
    hashed_email = hashlib.sha256(request.email.encode()).hexdigest()
    hashed_password = hashlib.sha256(request.password.encode()).hexdigest()

    print("Hashed email:", hashed_email)
    
    if hashed_email in data.get("id", {}):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    if "id" not in data:
        data["id"] = {}
    
    auth_dict = {"email": received_dict["email"], "name": received_dict["name"], "password": hashed_password}
    auth_data["id"][hashed_email] = auth_dict
    received_dict.pop("password")  # Remove password before saving user info
    data["id"][hashed_email] = received_dict
    
    save_data(data, DATA_FILE)
    save_data(auth_data, AUTH_FILE)
    
    return {"message": "Registration successful", "data": received_dict}

@app.post("/login")
async def login_user(request: LoginRequest):
    auth_data = load_data(AUTH_FILE)
    hashed_email = hashlib.sha256(request.email.encode()).hexdigest()
    hashed_password = hashlib.sha256(request.password.encode()).hexdigest()

    if hashed_email not in auth_data.get("id", {}):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    stored_password = auth_data["id"][hashed_email]["password"]
    if hashed_password != stored_password:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    return {"message": "Login successful", "email": hashed_email}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
