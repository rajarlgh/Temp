import os
import json
import requests

from dotenv import load_dotenv
from pathlib import Path

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# # Find the project root (parent of the "Learning" folder)
PROJECT_ROOT = Path(__file__).resolve().parents[1]  # one level up from Learning

DOTENV_PATH = PROJECT_ROOT / ".env"

# Point to .env in the same directory as this script
#DOTENV_PATH = Path(__file__).resolve().parent / ".env"
load_dotenv(DOTENV_PATH)

# Load .env
load_dotenv(DOTENV_PATH)  # now env vars from .env are available


# 1) Read API Key from enviorment variable
# api_key = os.environ['SPIRARE_API_KEY']
API_KEY = os.environ.get("OPENAI_API_KEY") # coming from .env
if not API_KEY:
    raise RuntimeError("OPENAI_API_KEY is not set")

# 2) Endpoint (use the one you have access to in your env)
# CHAT_COMPLETION_ENDPOINT = "https://chatops.sg.uobnet.com/spirare-api/nlp/v1/chat/completions"
# Endpoint URL (OpenAI)
CHAT_COMPLETION_ENDPOINT = "https://api.openai.com/v1/chat/completions"


# 3) Headers
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

# 4) Minimal body
payload = {
      "model": "gpt-4o-mini",   # or "gpt-4o", "gpt-3.5-turbo"
      "messages" : [
        {
            "role": "system",
            "content": "Connectivity Check..."
        },
        {
            "role": "user",
            "content": "Hello Spirare, can you hear me? "
        },
    ],
}

# 5. Send request
resp = requests.post(CHAT_COMPLETION_ENDPOINT,
                     headers=headers,
                     json=payload,
                     timeout=30,
                     verify=False #This is necessary if work from home
                     )

print("HTTP Status : ", resp.status_code)

# 6) Parse JSON safely and print the assistant message only

try:
    data = resp.json()
    # Navitage choices => Message ==> Content (adjust if your instance differs)
    assistant_text = data["choices"][0]["message"]["content"]
    print(f"\n Assistant reply:\n {assistant_text}")

except Exception as e:
    print("Failed to parse response Json. Raw content.")
    print(resp.text)
    raise
