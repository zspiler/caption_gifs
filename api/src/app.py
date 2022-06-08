from flask import Flask, request
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
import os
import random
import string
from pathlib import Path
from caption import caption_gif


app = Flask(__name__)
CORS(app, support_credentials=True)

app.config['UPLOAD_DIR'] = './gifs/uploaded'
app.config['CAPTIONS_DIR'] = './gifs/captioned'


def valid_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'gif'


def generate_random_filename(filename):
    random_str = ''.join(random.choice(string.ascii_lowercase)
                         for _ in range(16))
    return f"{filename.split('.')[0]}_{random_str}.gif"


@app.route('/', methods=['POST'])
def upload_gif():
    if request.method == 'POST':
        if 'file' not in request.files or request.files['file'] == '':
            return 'Missing file in request', 400

        file = request.files['file']

        if file and valid_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(
                app.config['UPLOAD_DIR'], generate_random_filename(filename))
            file.save(filepath)
            return {'filename': filename}

    return 'Not found', 404


@app.route('/', methods=['GET'])
def get_caption():

    if request.json == None or 'filename' not in request.json or 'text' not in request.json:
        return "Bad request", 400

    filename = request.json['filename']
    text = request.json['text']

    if not valid_file(filename):
        return 'Invalid filename', 400

    filepath = os.path.join(app.config['UPLOAD_DIR'], filename)

    if not Path(filepath).is_file():
        return 'File not found', 404

    out = os.path.join(app.config['CAPTIONS_DIR'], filename)

    try:
        caption_gif(text, filepath, out)
    except:
        return 'Server Error', 500
    return {'filename': filename}


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
