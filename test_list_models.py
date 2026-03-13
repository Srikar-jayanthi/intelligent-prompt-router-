import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"

response = requests.get(url)
print(f"Status: {response.status_code}")
data = response.json()
if 'models' in data:
    for m in data['models']:
        print(m['name'])
else:
    print(data)
