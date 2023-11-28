import objaverse
import multiprocessing
import shutil


# import random

uids = objaverse.load_uids()
# processes = multiprocessing.cpu_count()
# random_object_uids = random.sample(uids, 5)

# print("finished loading uids")

# objects = objaverse.load_objects(
#     uids=random_object_uids,
#     download_processes=processes
# )

# print("finished loading objects")

# objects = objaverse.load_objects(uids=random_object_uids)


## Endpoint


import chromadb
from flask import Flask, request, jsonify
from flask_cors import CORS

chroma_client = chromadb.PersistentClient(path="./thirty-thousand.db")
collection = chroma_client.get_collection(name="my_collection")


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


@app.route("/", methods=["POST"])
def handlePost():
    text_data = request.data.decode("utf-8")
    print("user: " + text_data)
    response = handlePrompt(text_data)
    return response


def handlePrompt(user_query):
    results = collection.query(query_texts=[user_query], n_results=1)
    flatten = lambda l: [item for sublist in l for item in sublist]
    top_id = results["ids"][0]
    return download_objects(top_id)


    # return str(results)


# app.run(debug=True, port=5001)


# print(flatten(results["documents"]))
# print(flatten(results["distances"]))


def download_objects(ids):
    # object = collection.get_object(id)
    # object.download()
    # return jsonify(object)

    print("ids: " + str(ids))

    objects = objaverse.load_objects( uids=ids ) # download_processes=processes
    object_path = list(objects.values())[0]
    # copy file object_pathng path to ../threejs/models/downloaded
    shutil.copy(object_path, "../threejs/models/downloaded")


    
    print(objects)



handlePrompt("green chair")
