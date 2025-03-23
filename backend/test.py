import requests
import time
import whois
import tldextract
from bs4 import BeautifulSoup
from jsondb import *
import requests
import json
import re  # Import regex module
import os
import dotenv



dotenv.load_dotenv()

# Get API keys from environment variables
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


def get_website_analytics(url):
    analytics = {"url": url}
    seo_score = 100  # Start with a perfect score

    # Measure load time
    start_time = time.time()
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        load_time = round(time.time() - start_time, 2)
        analytics["status_code"] = response.status_code
        analytics["load_time"] = f"{load_time} sec"
        
        # Deduct points for slow loading
        if load_time > 3:
            seo_score -= 10
    except requests.exceptions.RequestException as e:
        analytics["error"] = str(e)
        return analytics

    # Parse HTML
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract page details
    analytics["title"] = soup.title.string if soup.title else "No Title"
    analytics["meta_description"] = (
        soup.find("meta", attrs={"name": "description"})["content"]
        if soup.find("meta", attrs={"name": "description"})
        else "No Description"
    )
    
    # Deduct points if no meta description
    if analytics["meta_description"] == "No Description":
        seo_score -= 15

    # Count words & links
    word_count = len(soup.get_text().split())
    link_count = len(soup.find_all("a"))
    analytics["word_count"] = word_count
    analytics["link_count"] = link_count
    
    # Check word count (ideal content length is 300+ words)
    if word_count < 300:
        seo_score -= 20
    
    # Check link count (avoid excessive links, ideal: 20-100)
    if link_count < 5:
        seo_score -= 10
    elif link_count > 100:
        seo_score -= 10

    # Extract domain info
    extracted = tldextract.extract(url)
    domain = f"{extracted.domain}.{extracted.suffix}"
    
    try:
        domain_info = whois.whois(domain)
        analytics["domain_registrar"] = domain_info.registrar
        analytics["domain_creation_date"] = str(domain_info.creation_date)
        analytics["domain_expiry_date"] = str(domain_info.expiration_date)
    except Exception as e:
        analytics["domain_info_error"] = str(e)

    # Add SEO score
    analytics["seo_score"] = max(seo_score, 0)  # Ensure score is not negative

    return analytics


# print(get_website_analytics("https://kavier.store/"))

def get_keyword_analysis(keyword, country="us"):
    """Fetch Google search data and estimate keyword difficulty."""
    
    def get_google_results(keyword, country):
        """Fetch top search results, related keywords, and PAA questions."""
        url = "https://google.serper.dev/search"
        payload = json.dumps({"q": keyword, "gl": country})
        
        headers = {
            "X-API-KEY": SERPER_API_KEY,
            "Content-Type": "application/json"
        }
        
        response = requests.post(url, headers=headers, data=payload)
        
        if response.status_code == 200:
            data = response.json()
            return {
                "top_urls": [res["link"] for res in data.get("organic", [])[:10]],
                "related_keywords": [kw["query"] for kw in data.get("relatedSearches", [])[:10]],
                "people_also_ask": [paa["question"] for paa in data.get("peopleAlsoAsk", [])[:5]]
            }
        return {}

    def estimate_keyword_difficulty(urls):
        """Estimate keyword difficulty based on authority domains."""
        authority_domains = ["wikipedia.org", "forbes.com", "hubspot.com", "moz.com"]
        difficulty_score = sum(1 for url in urls if any(domain in url for domain in authority_domains))
        return min(100, difficulty_score * 10)  # Scale to 100

    # Fetch search data
    search_data = get_google_results(keyword, country)
    
    if search_data:
        difficulty = estimate_keyword_difficulty(search_data["top_urls"])
        search_data["keyword_difficulty"] = difficulty
    else:
        search_data = {"error": "No search results found."}

    return search_data



import google.generativeai as genai

# Set up Gemini API Key
API_KEY = GEMINI_API_KEY  # Replace with your actual API key
genai.configure(api_key=API_KEY)

# Initialize Gemini Model
model = genai.GenerativeModel("gemini-2.0-flash")

def ask_gemini(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text  # Return response as a string
    except Exception as e:
        return f"Error: {str(e)}"
    


def extract_json(response):
    """Extract JSON content safely from AI response using regex"""
    json_pattern = r"\{.*\}"  # Regex pattern to find JSON object
    match = re.search(json_pattern, response, re.DOTALL)  # Search for JSON in response

    if match:
        json_content = match.group(0)  # Extract matched JSON string
        try:
            return json.loads(json_content)  # Convert JSON string to dictionary
        except json.JSONDecodeError:
            return json_content  # Return as raw JSON string if parsing fails
    return response  # Return raw response if no JSON found

def get_gpt_response(product):
    """Generate a social media strategy for a product using Gemini AI"""

    # 1️⃣ Get the reel/short video idea
    prompt_idea = (
        f"Think of yourself as a Social Media Consultant. "
        f"Provide ONE reels/short video idea for the product '{product}'. "
        f"Give the response in JSON format: {{ 'reel_idea': 'your idea here' }}"
    )
    reel_idea = extract_json(ask_gemini(prompt_idea))

    # 2️⃣ Get 5-10 hashtags
    prompt_hashtags = (
        f"Generate 5-10 trending hashtags for the product '{product}'. "
        f"Give the response in JSON format: {{ 'hashtags': ['#hashtag1', '#hashtag2'] }}"
    )
    hashtags = extract_json(ask_gemini(prompt_hashtags))

    # 3️⃣ Get product keywords
    prompt_keywords = (
        f"Generate a list of product-related keywords for '{product}'. "
        f"Give the response in JSON format: {{ 'keywords': ['keyword1', 'keyword2'] }}"
    )
    keywords = extract_json(ask_gemini(prompt_keywords))

    # Combine the results
    final_response = {
        "product": product,
        "reel_idea": reel_idea.get("reel_idea", reel_idea),
        "hashtags": hashtags.get("hashtags", hashtags),
        "keywords": keywords.get("keywords", keywords),
    }

    return final_response


# Load influencer data from JSON file
def load_influencer_data(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

# Function to filter influencers based on category & budget and return full details
def get_influencers(category, budget, file_path="backend/inf.json"):
    data = load_influencer_data(file_path)

    # Ensure the category exists in the data
    if category not in data["Influencers"]:
        return {"error": f"No influencers found for category: {category}"}

    matched_influencers = []

    # Iterate over influencers in the given category
    for influencer, details in data["Influencers"][category].items():
        # Extract budget range and convert to integers
        budget_min = int(details["budget_min"].replace("$", "").replace(",", ""))
        budget_max = int(details["budget_max"].replace("$", "").replace(",", ""))

        # Check if the given budget falls within the range
        if budget_min <= budget <= budget_max:
            matched_influencers.append(details)

    # Return results
    return matched_influencers if matched_influencers else {"error": "No influencers found within this budget."}

# Example Usage # Pretty print the output