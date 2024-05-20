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
app.config['UPLOAD_FOLDER'] = 'files'
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET'])
def list_files():
    files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], f))]
    files.sort()
    # return render_template('index.html', files=files)
    return jsonify({'files': files})

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' in request.files:
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # save the uploaded file
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # update the knowledge base with the newly uploaded file
            update_knowledge_base()
            return jsonify({'message': 'File successfully uploaded', 'filename': filename})
    return jsonify({'message': 'Invalid file or no file uploaded'})

@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        os.remove(file_path)
        return redirect(url_for('list_files'))
    except Exception as e:
        return str(e)
    
    
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
