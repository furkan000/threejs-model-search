from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/echo', methods=['POST'])
def echo():
    data = request.json
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
