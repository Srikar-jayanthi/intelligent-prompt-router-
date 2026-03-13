import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model_names = ['gemini-pro', 'models/gemini-pro', 'gemini-1.5-flash', 'models/gemini-1.5-flash']

for name in model_names:
    try:
        print(f"Testing {name}...")
        model = genai.GenerativeModel(name)
        response = model.generate_content("Say test")
        print(f"SUCCESS with {name}: {response.text}")
        break
    except Exception as e:
        print(f"FAILED with {name}: {e}")
