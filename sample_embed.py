import os
import json
import requests

from dotenv import load_dotenv
from pathlib import Path

import urllib3

# Suppress only after understanding the risk (you already do this at home)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# # Find the project root (parent of the "Learning" folder)
#PROJECT_ROOT = Path(__file__).resolve().parents[1]  # one level up from Learning

#DOTENV_PATH = PROJECT_ROOT / ".env"

# Point to .env in the same directory as this script
DOTENV_PATH = Path(__file__).resolve().parent / ".env"
load_dotenv(DOTENV_PATH)

# Load .env
load_dotenv(DOTENV_PATH)  # now env vars from .env are available


# 1) Read API Key from enviorment variable
# api_key = os.environ['SPIRARE_API_KEY']
API_KEY = os.environ.get("OPENAI_API_KEY") # coming from .env
if not API_KEY:
    raise RuntimeError("OPENAI_API_KEY is not set")


# 2)Embedding Endpoint

# === IMPORTANT: pick the endpoint that is reachable from your location ===
# Option A: Internet-facing gateway (typical for WFH)
#EMBEDDING_ENDPOINT = "https://chatops.sg.uobnet.com/spirare-api/embedding/v1/embeddings"
EMBEDDING_ENDPOINT = "https://api.openai.com/v1/embeddings"

# 3) Headers
headers = {
    "Authorization" : f"Bearer {API_KEY}",
    "Content-Type" : "application/json",
}

text = "Apple is a fruit."

# payload = {
#     "input" : text,
#     "model" : "/data/genai/models/bge-m3",
#     "encoding_format" : "float",
#     "input_type" : "passage"
# }

payload = {
    "input" : text,
    "model": "text-embedding-3-small"  # or "text-embedding-3-large"
}

try:

    resp = requests.post(EMBEDDING_ENDPOINT,
                        headers = headers,
                        json=payload,
                        timeout=30,
                        verify=False  # only because you’re WFH; prefer verify=True on corp network
                        )


    print("HTTP Status:", resp.status_code)
    resp.raise_for_status()

    data = resp.json()
    vec = data["data"][0]["embedding"]

    print("Type:", type(vec))
    print("Vector length:", len(vec))
    print("First 5 numbers:", vec[:5])


except requests.exceptions.ConnectionError as e:
    print("Connection error. Are you off VPN or is the endpoint internal-only?")
    raise
except requests.exceptions.HTTPError as e:
    print("HTTP error:", resp.text)
    raise
except Exception as e:
    print("Unexpected error:", str(e))
    raise



