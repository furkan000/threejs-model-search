import requests
from dotenv import load_dotenv
import os
import json
import requests
load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/google/vit-base-patch16-224"
API_URL = "https://api-inference.huggingface.co/models/nlpconnect/vit-gpt2-image-captioning"
# API_URL = "https://api-inference.huggingface.co/models/" + "Salesforce/blip-image-captioning-large"

headers = {"Authorization": f"Bearer {API_TOKEN}"}
def query(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.request("POST", API_URL, headers=headers, data=data)
    return json.loads(response.content.decode("utf-8"))
data = query("weird.jpg")

print(data)
# [{'generated_text': 'a man wearing a helmet and goggles '}]
