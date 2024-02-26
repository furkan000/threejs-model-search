from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
from dotenv import load_dotenv
from openai import OpenAI

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Load environment variables
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Dictionary to store chat histories
chat_histories = {}

client = OpenAI()


@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json(silent=True)  # This returns None if the content is not valid JSON
    if data is None:
        return jsonify({"error": "Request must be in JSON format"}), 400

    chatname = data.get('chatname')
    user_message = data.get('message')
    
    if not chatname or not user_message:
        return jsonify({"error": "Missing chatname or message"}), 400

    # Initialize chat history for new chatname
    if chatname not in chat_histories:
        chat_histories[chatname] = []
        
    # Append the user's message to the chat history
    chat_histories[chatname].append({"role": "user", "content": user_message})

    # Generate a response using OpenAI
    try:
        completion = client.chat.completions.create(
          model="gpt-3.5-turbo",
          messages=chat_histories[chatname]
        )
        # Extract the message from the completion response
        assistant_message = completion.choices[0].message.content
        
        # Save the assistant's response to the chat history
        chat_histories[chatname].append({"role": "assistant", "content": assistant_message})

        return jsonify({"response": assistant_message})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

# USAGE:
# curl -X POST http://127.0.0.1:5000/chat -H "Content-Type: application/json" -d '{"chatname": "example_chat", "message": "Hello"}'
