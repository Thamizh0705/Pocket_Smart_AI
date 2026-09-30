import json
import requests
from .config import settings
from .fallback import home_recommendations, party_recommendations, jewelry_recommendations
from .catalog import search_links


def _fallback(kind, data):
    return {"home":home_recommendations,"party":party_recommendations,"jewelry":jewelry_recommendations}[kind](data)


def generate_recommendations(kind: str, data: dict, image_bytes: bytes | None = None, mime_type: str | None = None) -> dict:
    fallback = _fallback(kind, data)
    if not settings.gemini_api_key:
        return fallback

    prompt = f"""You are PocketSmart AI. Generate budget-aware recommendations for a {kind} planner. Return ONLY JSON with keys summary, allocations, recommendations, tips. Each recommendation must contain name, category, estimated_price, reason, platforms. Platforms must be chosen only from Amazon, Flipkart, IKEA, Swiggy, Zomato, OYO. Do not claim live inventory or exact live prices. Respect the user's total budget. User data: {json.dumps(data)}"""
    parts = [{"text": prompt}]
    if image_bytes and mime_type:
        import base64
        parts.append({"inline_data":{"mime_type":mime_type,"data":base64.b64encode(image_bytes).decode()}})

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{settings.gemini_model}:generateContent?key={settings.gemini_api_key}"
    body = {"contents":[{"parts":parts}],"generationConfig":{"temperature":0.3,"responseMimeType":"application/json"}}
    try:
        response = requests.post(url, json=body, timeout=45)
        response.raise_for_status()
        payload = response.json()
        text = payload["candidates"][0]["content"]["parts"][0]["text"]
        result = json.loads(text)
        result["source"] = "gemini"
        for rec in result.get("recommendations", []):
            platforms = rec.pop("platforms", [])
            rec["links"] = search_links(rec.get("name", ""), platforms)
        return result
    except Exception:
        return fallback
