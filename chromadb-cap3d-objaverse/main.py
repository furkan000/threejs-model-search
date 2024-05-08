import objaverse
import multiprocessing
import shutil
import chromadb
from flask import Flask, request, jsonify
from flask_cors import CORS
import urllib.parse

uids = objaverse.load_uids()
chroma_client = chromadb.PersistentClient(path="./full.db")
collection = chroma_client.get_collection(name="my_collection")

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route("/", methods=["POST"])
def handle_post():
    text_data = request.data.decode("utf-8")
    print("user: " + text_data)
    response = handle_prompt(text_data)
    return response

def handle_prompt(user_query):
    results = collection.query(query_texts=[user_query], n_results=1)
    top_id = results["ids"][0]
    object_path = download_objects(top_id)
    formatted_path = format_path_to_uri(object_path)
    return formatted_path

def download_objects(ids):
    print("ids: " + str(ids))
    objects = objaverse.load_objects(uids=ids)
    object_path = list(objects.values())[0]
    return object_path

def format_path_to_uri(path):
    # Convert backslashes to forward slashes and prepend the file URI scheme
    uri_path = 'file:///' + path.replace("\\", "/")
    return uri_path

# For testing purposes
# print(handle_prompt("green chair"))


app.run(debug=True, port=5001)

# curl -X POST -d "chair" http://localhost:5001/