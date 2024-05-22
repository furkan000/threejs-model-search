import requests
from dotenv import load_dotenv
import os

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/bert-base-uncased"

headers = {"Authorization": f"Bearer {API_TOKEN}"}
def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()
data = query({"inputs": "The answer to the universe is [MASK]."})

print(data)