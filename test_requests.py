import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={api_key}"

payload = {
    "contents": [{
        "parts": [{"text": "Say hello"}]
    }]
}

response = requests.post(url, json=payload)
print(f"Status: {response.status_code}")
print(f"Body: {response.text}")
