from flask import Flask
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, support_credentials=True)

@app.route('/', methods=['GET'])
@cross_origin(supports_credentials=True)
def main():
    return "🥖", 200

if __name__=='__main__':
    app.run(debug=True, host='0.0.0.0')
