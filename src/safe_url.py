import os

import httpx
from dotenv import load_dotenv

API_URL = "https://safebrowsing.googleapis.com/v4/threatMatches:find"

async def is_safe(url: str):
    _ = load_dotenv()  # reads .env into os.environ — do this first
    
    api_key = os.environ.get("SAFE_BROWSING_API_KEY")
    
    if not api_key:
        raise KeyError
    
    payload = {
            "client": {
                "clientId": "my-portfolio-app",
                "clientVersion": "1.0.0",
            },
            "threatInfo": {
                "threatTypes": [
                    "MALWARE",
                    "SOCIAL_ENGINEERING",
                    "UNWANTED_SOFTWARE",
                    "POTENTIALLY_HARMFUL_APPLICATION",
                ],
                "platformTypes": ["ANY_PLATFORM"],
                "threatEntryTypes": ["URL"],
                "threatEntries": [{"url": url}],
            },
        }

    response = httpx.post(API_URL, params={"key": api_key}, json=payload, timeout=10)
    response.raise_for_status()
    return not "matches" in response.json()