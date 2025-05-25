import os
from flask import Flask, request, render_template, jsonify
import requests
import base64

app = Flask(__name__)


ARABIC_HOST = os.environ.get("ARABIC_SERVICE_HOST", "arabic_service")
ENGLISH_HOST = os.environ.get("ENGLISH_SERVICE_HOST", "english_service")


ARABIC_URL = f"http://{ARABIC_HOST}:5051/arabic_sign"
ENGLISH_URL = f"http://{ENGLISH_HOST}:5052/english_sign"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detect', methods=['POST'])
def detect():
    image = request.files['image']
    language = request.form['language']
    image_data = base64.b64encode(image.read()).decode('utf-8')
    payload = {'image': image_data}

    url = ARABIC_URL if language == 'arabic' else ENGLISH_URL

    try:
        response = requests.post(url, json=payload)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)