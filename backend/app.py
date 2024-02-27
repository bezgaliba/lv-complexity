from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

app.config['DEBUG'] = os.environ.get('FLASK_DEBUG')

@app.route('/', methods=['GET'])
def submit():

    text = request.args.get('text')

    if 'text' is None:
        return jsonify(error='Missing argument - text'), 400

    response = {
        'input_text': text,
        'random_score': 3
    }

    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == '__main__':
    app.run()
