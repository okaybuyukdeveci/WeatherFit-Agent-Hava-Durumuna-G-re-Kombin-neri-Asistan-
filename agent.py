# agent.py
import requests
from config import OLLAMA_URL, MODEL_NAME

def get_outfit_recommendation(weather: dict, context: dict) -> str:
    temperature = weather["temperature"]

    if temperature <= 5:
        temp_rule = "It's very cold. Thick outerwear is essential. Short-sleeved or thin clothing is NOT RECOMMENDED."
    elif temperature <= 15:
        temp_rule = "The weather is cool. A light coat, jacket, or sweater would be suitable."
    else:
        temp_rule = "The weather is mild or warm. Light clothing is suitable."

    prompt = f"""
You are a PROFESSIONAL fashion stylist with real-world experience.
You give practical, realistic, wearable outfit suggestions.

Weather conditions:
- Temperature: {temperature}°C
- Condition: {weather["condition"]}

User context:
- Event: {context["event"]}
- Style: {context["style"]}
- Mood: {context["mood"]}

TEMPERATURE RULE:
{temp_rule}

STRICT CONSTRAINTS (VERY IMPORTANT):
- Use ONLY real clothing items that exist in daily life
- Do NOT invent words
- Do NOT repeat the same word excessively
- English language only
- Short and clear sentences

OUTPUT FORMAT (MUST MATCH EXACTLY, NO EXTRA TEXT):

Upper Garments: 
Lower Garments: 
Shoes: 
Accessories: 
"""

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.3,   # daha az saçmalama
            "top_p": 0.9
        }
    }

    response = requests.post(OLLAMA_URL, json=payload)
    response.raise_for_status()

    return response.json()["response"].strip()
