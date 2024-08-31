import objaverse
import multiprocessing
import shutil
import chromadb
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import urllib.parse
import chromadb.utils.embedding_functions as embedding_functions
import openai
from openai import OpenAI
import os

# Set this variable to True to use OpenAI embeddings, or False to use a different method
use_openai_embedding = False  # Set to False for example
database_path = "./databases/thirty-thousand.db"

# Load API key directly from environment variables if necessary
if use_openai_embedding:
    openai_api_key = os.environ.get('OPENAI_API_KEY')
    if openai_api_key is None:
        raise ValueError("OPENAI_API_KEY environment variable not set")

    openai_ef = embedding_functions.OpenAIEmbeddingFunction(
        api_key=openai_api_key,
        model_name="text-embedding-3-small"
    )
    client = OpenAI(api_key=openai_api_key)

uids = objaverse.load_uids()
chroma_client = chromadb.PersistentClient(path=database_path)
collection = chroma_client.get_collection(name="my_collection")

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Enable CORS for all routes

@app.route("/find", methods=["POST"])
def find():
    text_data = request.data.decode("utf-8")  # Decode the raw byte data
    print("Received Text:", text_data)
    response = handle_prompt(text_data)
    return response, 200

def text_embedding(text) -> None:
    if use_openai_embedding:
        # Use OpenAI embedding if the flag is set
        return client.embeddings.create(input=[text], model="text-embedding-3-small").data[0].embedding
    else:
        # Here you could implement an alternative embedding method
        raise NotImplementedError("Alternative embedding method is not implemented")

def handle_prompt(user_query):
    if use_openai_embedding:
        # Get embedding using OpenAI API
        user_query_embedding = text_embedding(user_query)   
        results = collection.query(query_texts=[user_query_embedding], n_results=1)
    else:
        # Assume user_query is already an embedding if not using OpenAI
        results = collection.query(query_embeddings=user_query, n_results=1)
    
    print("results: " + str(results))
    top_id = results["ids"][0]
    object_path = download_objects(top_id)
    formatted_path = format_path_to_uri(object_path)
    return formatted_path

@app.route("/search", methods=["POST"])
def search():
    text_data = request.data.decode("utf-8")

    if use_openai_embedding: 
        text_data = text_embedding(text_data)

    results = collection.query(query_texts=[text_data], n_results=6)

    ids = results["ids"][0]
    annotations = objaverse.load_annotations(uids=ids)
    generated_descriptions = results["documents"][0]
    titles = []
    descriptions = []
    thumbnails_url = []

    for annotation in iter(annotations.values()):
        title = annotation["name"]
        titles.append(title)
        description = annotation["description"]
        descriptions.append(description)
        thumbnails = annotation["thumbnails"]["images"]    
        first_thumbnail = thumbnails[0]
        first_thumbnail_url = first_thumbnail["url"]
        thumbnails_url.append(first_thumbnail_url)

    combined_data = [
        {
            "id": id,
            "generatedDescription": gen_desc,
            "title": title,
            "description": desc,
            "thumbnail": thumb_url
        }
        for id, gen_desc, title, desc, thumb_url in zip(ids, generated_descriptions, titles, descriptions, thumbnails_url)
    ]
    
    return jsonify(combined_data)

@app.route("/download/<id>", methods=["GET"])
def download(id):
    url = download_objects([id])
    url = url.replace("\\", "/")
    return send_file(url, as_attachment=True)
    
def download_objects(ids):
    objects = objaverse.load_objects(uids=ids)
    object_path = list(objects.values())[0]
    return object_path

def format_path_to_uri(path):
    # Convert backslashes to forward slashes and prepend the file URI scheme
    uri_path = 'file:///' + path.replace("\\", "/")
    return uri_path

# Uncomment for testing purposes
# print(handle_prompt("green chair"))

app.run(debug=True, port=5001)

# Example command to test the find route:
# curl -X POST http://localhost:5001/find -d "Hello, Flask!" -H "Content-Type: text/plain"