import os
import google.generativeai as genai
from dotenv import load_dotenv
from prompts import CLASSIFIER_PROMPT

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model_name = 'gemini-1.5-flash'
message = "how do i sort a list in python?"

print(f"Testing with model: {model_name}")
try:
    model = genai.GenerativeModel(model_name)
    full_prompt = f"{CLASSIFIER_PROMPT}\n\nUser Message: {message}\n\nReturn ONLY a JSON object."
    
    # Try without specialized generation config first to see raw response
    response = model.generate_content(full_prompt)
    print("RAW RESPONSE TEXT:")
    print(response.text)
except Exception as e:
    print(f"ERROR: {e}")
