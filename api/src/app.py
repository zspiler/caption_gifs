from flask import Flask, request, render_template, jsonify, flash, redirect, url_for
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
CORS(app, support_credentials=True)

app.config['UPLOAD_DIR'] = './gifs/uploaded'
app.config['CAPTIONS_DIR'] = './gifs/captioned'


def valid_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'gif'


@app.route('/', methods=['POST'])
@cross_origin(supports_credentials=True)
def upload_gif():
    if request.method == 'POST':
        if 'file' not in request.files or request.files['file'] == '':
            return 'Missing file in request', 400

        file = request.files['file']

        if file and valid_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_DIR'], filename))
            return 'Upload successful'

    return 404, 'Not found'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
