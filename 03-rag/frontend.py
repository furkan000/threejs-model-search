from flask import Flask, render_template, redirect, url_for, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from backend import ask_question, update_knowledge_base
import os
# cors
from flask_cors import CORS



app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)



# Configuration for file uploads
app.config['UPLOAD_FOLDER'] = ''
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/<folder>/', methods=['GET'])
def list_files(folder):
    folder_path = os.path.join(app.config['UPLOAD_FOLDER'], folder)
    if not os.path.exists(folder_path):
        return jsonify({'message': 'Folder not found'}), 404
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    files.sort()
    return jsonify({'files': files})

@app.route('/<folder>/upload', methods=['POST'])
def upload_file(folder):
    folder_path = os.path.join(app.config['UPLOAD_FOLDER'], folder)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    if 'file' in request.files:
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(folder_path, filename))
        
        if file and allowed_file(file.filename):
            update_knowledge_base()
            return jsonify({'message': 'File successfully uploaded', 'filename': filename})
    return jsonify({'message': 'Invalid file or no file uploaded'})


@app.route('/<folder>/update', methods=['POST'])
def update_knowledge_base_with_text(folder):
    # Extract text data from the request
    text_data = request.form.get('text', None)
    
    if text_data:
        # Here, implement the logic to update the knowledge base with the received text
        # For example, update_knowledge_base(text_data)
        
        return jsonify({'message': 'Knowledge base successfully updated with the provided text'})
    else:
        return jsonify({'message': 'Invalid or no text provided'})



@app.route('/<folder>/delete/<filename>', methods=['POST'])
def delete_file(folder, filename):
    folder_path = os.path.join(app.config['UPLOAD_FOLDER'], folder)
    file_path = os.path.join(folder_path, filename)
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            return redirect(url_for('list_files', folder=folder))
        except Exception as e:
            return jsonify({'message': str(e)}), 500
    return jsonify({'message': 'File not found'}), 404
    
    
@app.route('/ask', methods=['POST'])
def ask():
    prompt = request.form['prompt']
    result = ask_question(prompt)
    return jsonify({'result': result})


@app.route('/last_files', methods=['GET'])
def last_files():
    files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], f))]
    if not files:
        return 'No files found'
    files.sort(key=lambda x: os.path.getmtime(os.path.join(app.config['UPLOAD_FOLDER'], x)), reverse=True)
    last_files = files[:10]
    return ', '.join(last_files)


@app.route('/<folder>/download/<filename>', methods=['GET'])
def download_file(folder, filename):
    folder_path = os.path.join(app.config['UPLOAD_FOLDER'], folder)
    file_path = os.path.join(folder_path, filename)
    if os.path.exists(file_path):
        return send_from_directory(folder_path, filename, as_attachment=True)
    return jsonify({'message': 'File not found'}), 404



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
