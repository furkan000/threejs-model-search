import objaverse
import chromadb
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

uids = objaverse.load_uids()
chroma_client = chromadb.PersistentClient(path="./full.db")
collection = chroma_client.get_collection(name="my_collection")

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Enable CORS for all routes

@app.route('/receive_text', methods=['POST'])
def receive_text():
    text_data = request.data.decode('utf-8')  # Decoding from bytes to string
    print("Received Text:", text_data)
    return "Text received successfully", 200

if __name__ == '__main__':
    app.run(debug=True, port=5555)
