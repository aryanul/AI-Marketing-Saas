import json
import hashlib
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from jsondb import *
from test import get_website_analytics, get_keyword_analysis, get_gpt_response,get_influencers

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_FILE = "data.json"
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

class ProductRequest(BaseModel):
    product_name: str
    description: str
    category: str  # New: Category field for influencer search
    budget: int    # New: Budget field for influencer search

@app.get("/")
async def root():
    return {"message": "Server running 😄"}

@app.post("/register")
async def register_user(request: RegisterRequest):
    received_dict = request.model_dump()

    data = load_data(DATA_FILE)
    auth_data = load_data(AUTH_FILE)
    hashed_email = hashlib.sha256(request.email.encode()).hexdigest()
    hashed_password = hashlib.sha256(request.password.encode()).hexdigest()

    if hashed_email in data.get("id", {}):
        raise HTTPException(status_code=400, detail="Email already registered")

    if "id" not in data:
        data["id"] = {}

    if "id" not in auth_data:
        auth_data["id"] = {}

    auth_dict = {"email": received_dict["email"], "name": received_dict["name"], "password": hashed_password}
    auth_data["id"][hashed_email] = auth_dict
    received_dict.pop("password")
    data["id"][hashed_email] = received_dict

    save_data(data, DATA_FILE)
    save_data(auth_data, AUTH_FILE)

    return {"message": "Registration successful", "id": hashed_email}

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

@app.get("/company-analytics/{uid}")
async def company_analytics(uid: str):
    data = load_data(DATA_FILE)

    if uid not in data.get("id", {}):
        raise HTTPException(status_code=404, detail="User not found")

    # Check if analytics data already exists
    if "analytics" in data["id"][uid]:
        return data["id"][uid]["analytics"]

    company_name = data["id"][uid].get("company", "")
    website = data["id"][uid].get("website", "")

    if not company_name or not website:
        raise HTTPException(status_code=400, detail="Company name or website missing")

    # Fetch keyword analysis and website SEO data
    keyword_analysis = get_keyword_analysis(company_name)
    website_analysis = get_website_analytics(website)

    # Construct analysis data
    analysis_data = {
        "company_name": company_name,
        "keyword_difficulty": keyword_analysis.get("keyword_difficulty"),
        "related_questions": keyword_analysis.get("people_also_ask", []),  # Include PAA questions
        "website_seo_score": website_analysis.get("seo_score"),
        "word_count": website_analysis.get("word_count"),
        "link_count": website_analysis.get("link_count"),
    }

    # Store in data.json
    data["id"][uid]["analytics"] = analysis_data
    save_data(data, DATA_FILE)

    return analysis_data


@app.post("/product-idea/{uid}")
async def product_idea(uid: str, request: ProductRequest):
    data = load_data(DATA_FILE)

    if uid not in data.get("id", {}):
        raise HTTPException(status_code=404, detail="User not found")

    # Check if product idea already exists
    if "product_ideas" in data["id"][uid]:
        for idea in data["id"][uid]["product_ideas"]:
            if idea["product_name"] == request.product_name:
                return idea  # Return stored data if found

    # Generate product idea using GPT
    prompt = f"{request.product_name}: {request.description}"
    gpt_response = get_gpt_response(prompt)

    # Fetch recommended influencers
    recommended_influencers = get_influencers(request.category, request.budget)

    # Store all details in data.json
    product_data = {
        "product_name": request.product_name,
        "description": request.description,
        "reel_idea": gpt_response["reel_idea"],
        "hashtags": gpt_response["hashtags"],
        "keywords": gpt_response["keywords"],
        "recommended_influencers": recommended_influencers,
        "category": request.category,
        "budget": request.budget
    }

    if "product_ideas" not in data["id"][uid]:
        data["id"][uid]["product_ideas"] = []

    data["id"][uid]["product_ideas"].append(product_data)
    save_data(data, DATA_FILE)  # Save updated data

    return product_data

@app.get("/get-products/{uid}")
async def get_products(uid: str):
    data = load_data(DATA_FILE)

    if uid not in data.get("id", {}):
        raise HTTPException(status_code=404, detail="User not found")

    # Fetch all products for the user
    product_ideas = data["id"][uid].get("product_ideas", [])

    if not product_ideas:
        return {"message": "No products found"}

    return {"products": product_ideas}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
