import os
import json
import logging
from openai import OpenAI
from dotenv import load_dotenv
from prompts import SYSTEM_PROMPTS, CLASSIFIER_PROMPT, CLARIFICATION_PROMPT

# Load environment variables
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

LOG_FILE = "route_log.jsonl"
CONFIDENCE_THRESHOLD = 0.7

def classify_intent(message: str) -> dict:
    """
    Classifies the user's intent using an LLM call.
    Returns a dictionary with 'intent' and 'confidence'.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Using a lightweight model for classification
            messages=[
                {"role": "system", "content": CLASSIFIER_PROMPT},
                {"role": "user", "content": message}
            ],
            response_format={"type": "json_object"}
        )
        
        content = response.choices[0].message.content
        data = json.loads(content)
        
        # Validate structure
        if "intent" not in data or "confidence" not in data:
            raise ValueError("Invalid JSON structure from LLM")
            
        return data
    except Exception as e:
        print(f"Error in classification: {e}")
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
        response = client.chat.completions.create(
            model="gpt-4o",  # Using a more capable model for the expert response
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error in expert generation: {e}")
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
    # Optional Manual Override stretch goal
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
