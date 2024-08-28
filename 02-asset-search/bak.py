import objaverse
import multiprocessing
import shutil
import chromadb
from flask import Flask, request, jsonify
from flask_cors import CORS

uids = objaverse.load_uids()
chroma_client = chromadb.PersistentClient(path="./database/thirty-thousand.db")
collection = chroma_client.get_collection(name="my_collection")

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Enable CORS for all routes

@app.route("/search", methods=["POST"])
def search():
    text_data = request.data.decode("utf-8")
    print("user: " + text_data)
    response = handlePrompt(text_data)
    return response

def handlePrompt(user_query):
    print("user: " + user_query)
    results = collection.query(query_texts=[user_query], n_results=1)
    flatten = lambda l: [item for sublist in l for item in sublist]
    top_id = results["ids"][0]
    object_name = download_objects(top_id)
    print("object_name: " + object_name)
    return str(object_name)

def download_objects(ids):
    print("ids: " + str(ids))
    objects = objaverse.load_objects( uids=ids ) # download_processes=processes
    object_path = list(objects.values())[0]
    # get file name
    object_name = object_path.split("/")[-1]
    # copy file object_pathng path to ../threejs/models/downloaded
    shutil.copy(object_path, "../downloaded_models")
    return object_name

# handlePrompt("green chair")
app.run(host="0.0.0.0", debug=True, port=5001)
