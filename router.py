import os
import json
import logging
import google.generativeai as genai
from dotenv import load_dotenv
from prompts import SYSTEM_PROMPTS, CLASSIFIER_PROMPT, CLARIFICATION_PROMPT

# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

LOG_FILE = "route_log.jsonl"
CONFIDENCE_THRESHOLD = 0.7
DEFAULT_MODEL = "gemini-2.5-flash"

def classify_intent(message: str) -> dict:
    """
    Classifies the user's intent using Gemini.
    Returns a dictionary with 'intent' and 'confidence'.
    """
    try:
        model = genai.GenerativeModel(DEFAULT_MODEL)
        full_prompt = f"{CLASSIFIER_PROMPT}\n\nUser Message: {message}\n\nReturn ONLY a JSON object."
        
        # Try with JSON mode if supported
        try:
            response = model.generate_content(
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    response_mime_type="application/json",
                )
            )
            content = response.text.strip()
            data = json.loads(content)
            return data
        except Exception as json_err:
            # Fallback to standard generation and manual cleaning
            response = model.generate_content(full_prompt)
            content = response.text.strip()
            
            # Extract JSON from markdown if present
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            data = json.loads(content)
            return data

    except Exception as e:
        # Final fallback for any error
        return {"intent": "unclear", "confidence": 0.0}

def route_and_respond(message: str, intent_data: dict) -> str:
    """
    Routes the message to the appropriate persona and returns the response.
    """
    intent = intent_data.get("intent", "unclear")
    confidence = intent_data.get("confidence", 0.0)
    
    # Check confidence threshold or if intent is explicitly unclear
    if intent == "unclear" or confidence < CONFIDENCE_THRESHOLD:
        return CLARIFICATION_PROMPT
        
    system_prompt = SYSTEM_PROMPTS.get(intent)
    
    if not system_prompt:
        return CLARIFICATION_PROMPT
        
    try:
        # Use system_instruction if possible, otherwise prepend
        try:
            model = genai.GenerativeModel(
                model_name=DEFAULT_MODEL,
                system_instruction=system_prompt
            )
            response = model.generate_content(message)
            return response.text
        except:
            model = genai.GenerativeModel(DEFAULT_MODEL)
            full_msg = f"{system_prompt}\n\nUser Message: {message}"
            response = model.generate_content(full_msg)
            return response.text
            
    except Exception as e:
        return "I'm sorry, I encountered an error while processing your request."

def log_request(intent: str, confidence: float, user_message: str, final_response: str):
    """
    Logs the request details to a JSON Lines file.
    """
    log_entry = {
        "intent": intent,
        "confidence": confidence,
        "user_message": user_message,
        "final_response": final_response
    }
    
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

def process_message(message: str) -> str:
    """
    Orchestrates the classification, routing, and logging.
    """
    # Manual Override
    if message.startswith("@"):
        parts = message.split(" ", 1)
        prefix = parts[0][1:].lower()
        if prefix in SYSTEM_PROMPTS:
            intent_data = {"intent": prefix, "confidence": 1.0}
            msg_to_process = parts[1] if len(parts) > 1 else ""
            response = route_and_respond(msg_to_process, intent_data)
            log_request(prefix, 1.0, message, response)
            return response

    intent_data = classify_intent(message)
    response = route_and_respond(message, intent_data)
    log_request(intent_data["intent"], intent_data["confidence"], message, response)
    return response
