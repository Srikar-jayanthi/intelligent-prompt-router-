import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
print(f"API Key exists: {bool(api_key)}")
print(f"API Key starts with: {api_key[:10] if api_key else 'None'}")

client = OpenAI(api_key=api_key)
try:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "say hello"}],
        max_tokens=5
    )
    print("API Call Success:", response.choices[0].message.content)
except Exception as e:
    print("API Call Failed:", e)
