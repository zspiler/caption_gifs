
import os
import random
import string
from flask import Flask, request, send_from_directory, send_file
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
from time import time
from pathlib import Path
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

from caption import caption_gif


app = Flask(__name__)
CORS(app, support_credentials=True)

app.config['UPLOAD_DIR'] = './gifs/uploaded'
app.config['CAPTIONS_DIR'] = './gifs/captioned'
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024  # 20 MB file size limit


def valid_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'gif'


def generate_random_filename(filename):
    random_str = ''.join(random.choice(string.ascii_lowercase)
                         for _ in range(16))
    return f"{filename.split('.')[0]}_{random_str}.gif"


@app.route('/upload', methods=['POST'])
@cross_origin()
def upload_gif():
    if request.method == 'POST':
        if 'file' not in request.files or request.files['file'] == '':
            return 'Missing file in request', 400

        file = request.files['file']

        if file and valid_file(file.filename):
            filename = secure_filename(file.filename)
            filename = generate_random_filename(filename)
            filepath = os.path.join(
                app.config['UPLOAD_DIR'], filename)
            file.save(filepath)
            return {'filename': filename}

    return 'Not found', 404


@app.route('/caption', methods=['POST'])
@cross_origin()
def get_captioned_gif():
    if request.json == None or 'filename' not in request.json or 'text' not in request.json or len(request.json['text']) == 0:
        return "Bad request", 400

    filename = request.json['filename']
    text = request.json['text']

    if not valid_file(filename):
        return 'Invalid filename', 400

    filepath = os.path.join(app.config['UPLOAD_DIR'], filename)

    if not Path(filepath).is_file():
        return 'File not found', 404

    output_path = os.path.join(app.config['CAPTIONS_DIR'], filename)

    try:
        caption_gif(text, filepath, output_path)
        os.remove(filepath)

    except Exception as e:
        print(e)
        return 'Server Error', 500
    return {'filename': filename}


@app.route('/captioned/<filename>')
def serve_captioned_gifs(filename):
    return send_from_directory(app.config['CAPTIONS_DIR'], filename)


def remove_old_gifs():
    directory = app.config['CAPTIONS_DIR']
    for filename in os.listdir(directory):
        file = os.path.join(directory, filename)
        if os.path.isfile(file):
            os.remove(file)


sched = BackgroundScheduler(daemon=True)
sched.add_job(remove_old_gifs, 'cron', hour=8)
sched.start()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
