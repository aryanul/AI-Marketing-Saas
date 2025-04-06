# **AI Marketing SaaS Dashboard** 🚀  

A **B2B SaaS** platform for **Social Media Marketing Analytics**, providing insights into **SEO scores, keyword difficulty, product budgets, and influencer recommendations**.  

---

## **📌 Features**  
✅ **User Authentication:** Sign up and log in securely.  
✅ **SEO & Marketing Analytics:** Visual representation of **SEO scores, keyword difficulty, and budget**.  
✅ **Product Management:** Add, view, and analyze **marketing products**.  
✅ **Reel Idea Integration:** AI-powered **reel ideas** for marketing campaigns.  
✅ **Influencer Recommendations:** AI suggests the best influencers for marketing campaigns.  
✅ **Charts & Graphs:** Visual insights through **progress bars, circular charts, and bar charts**.  

---

## **📂 Project Structure**  

```
AI-Marketing-SaaS/
│── backend/                # Python FastAPI backend  
│   ├── auth.json           # User authentication data  
│   ├── data.json           # Sample data  
│   ├── inf.json            # Influencer data  
│   ├── social.json         # Social media analysis data  
│   ├── test.json           # Test data  
│   ├── jsondb.py           # Database handling script  
│   ├── main.py             # Main API script (FastAPI)  
│   ├── requirements.txt    # Python dependencies  
│   ├── test.py             # Testing script  
│  
│── frontend/               # Frontend UI (HTML, CSS, JS)  
│   │── dashboard/          # Dashboard UI  
│   │   ├── index.html      # Dashboard page  
│   │   ├── script.js       # Dashboard logic  
│   │   ├── styles.css      # Dashboard styling  
│   │  
│   │── login/              # Login page  
│   │   ├── index.html  
│   │   ├── script.js  
│   │   ├── styles.css  
│   │  
│   │── signup/             # Signup page  
│   │   ├── index.html  
│   │   ├── script.js  
│   │   ├── styles.css  
│   │  
│   ├── index.html          # Main landing page  
│   ├── script.js           # Global JavaScript logic  
│   ├── style.css           # Global styles  
│  
│── .gitignore              # Git ignore file  
```

---

## **🛠️ Installation & Setup**  

### **🔹 Backend Setup**  
1️⃣ Install dependencies:  
```bash
pip install -r requirements.txt
```
2️⃣ Run FastAPI server:  
```bash
uvicorn main:app --reload
```

### **🔹 Frontend Setup**  
1️⃣ Open `frontend/index.html` in a browser.  
2️⃣ Ensure the backend is running before testing API calls.  

---

## **📊 Dashboard Overview**  
🔹 **SEO Score Chart** – Displays a **line graph** for SEO score.  
🔹 **Progress Bars** – Tracks **word count, link count, and keyword difficulty**.  
🔹 **Budget Chart** – **Bar chart** comparing product budgets.  
🔹 **Influencer Recommendations** – AI suggests top influencers for marketing.  

---

## **🎥 Video Demonstration**  
📌 _[Add a link to a YouTube demo or Loom video]_  

---

## **🖼️ Screenshots**  
### **🔹 Dashboard View**  
![Dashboard Screenshot](path/to/image.png)  
### **🔹 Product Page**  
![Product Screenshot](path/to/image.png)  

---

## **📩 API Documentation**  

### **🔹 Root Endpoint**  
```http
GET /
```
📌 **Description:** Returns a welcome message or API status.  

---

### **🔹 User Registration**  
```http
POST /register
```
📌 **Description:** Registers a new user.  
📌 **Request Body (JSON):**  
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepassword"
}
```
📌 **Response (Success):**  
```json
{
  "message": "User registered successfully!"
}
```

---

### **🔹 User Login**  
```http
POST /login
```
📌 **Description:** Authenticates a user and returns a token.  
📌 **Request Body (JSON):**  
```json
{
  "email": "john@example.com",
  "password": "securepassword"
}
```
📌 **Response (Success):**  
```json
{
  "token": "your_jwt_token_here"
}
```

---

### **🔹 Get Company Analytics**  
```http
GET /company-analytics/{uid}
```
📌 **Description:** Fetches analytics data for a company.  
📌 **Response Example:**  
```json
{
  "company_name": "XYZ Ltd.",
  "website": "https://xyz.com",
  "keyword_difficulty": 78,
  "website_seo_score": 85,
  "word_count": 1200,
  "link_count": 45
}
```

---

### **🔹 Add Product Idea**  
```http
POST /product-idea/{uid}
```
📌 **Description:** Allows users to submit new product ideas.  
📌 **Request Body (JSON):**  
```json
{
  "product_name": "AI Marketing Tool",
  "description": "Automates social media marketing.",
  "category": "SaaS",
  "budget": 5000
}
```
📌 **Response Example:**  
```json
{
  "message": "Product idea submitted successfully!"
}
```

---

### **🔹 Get Products**  
```http
GET /get-products/{uid}
```
📌 **Description:** Fetches all products added by a user.  
📌 **Response Example:**  
```json
{
  "products": [
    {
      "product_name": "AI Marketing Tool",
      "description": "Automates social media marketing.",
      "category": "SaaS",
      "budget": 5000,
      "hashtags": ["#marketing", "#AI"],
      "keywords": ["social media", "SEO"],
      "reel_idea": "Use AI-generated content for viral marketing!",
      "recommended_influencers": [
        { "name": "John Doe", "photo": "john.jpg", "link": "https://instagram.com/johndoe" }
      ]
    }
  ]
}
```
---

## **🌟 Contributors**  
👨‍💻 **Khandakar Aryanul Haque** (Techno India University)  

---

## **🚀 Future Enhancements**  
🔹 JWT Authentication for secure access.  
🔹 AI-powered **marketing strategy generator**.  
🔹 Advanced analytics with **real-time social media tracking**.  

---

### **💡 Notes:**  
📌 **This README covers everything**—API documentation, features, setup, and future improvements.  
📌 Add **screenshots & a video link** before finalizing.  
📌 If you need **modifications**, just let me know! 😊🚀