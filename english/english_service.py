from flask import Flask, request, jsonify
import base64
from io import BytesIO
from PIL import Image
from ultralytics import YOLO

# Load English model
englishmodel = YOLO("americansign.pt")

def predict_english(img):
    results = englishmodel([img])
    class_name = 'EMPTY'
    prob = 0

    for result in results:
        if result.boxes:
            for box in result.boxes:
                the_prob = box.conf
                if the_prob > prob:
                    prob = the_prob
                    class_name = result.names[int(box.cls)]

    return class_name

app = Flask(__name__)

@app.route('/english_sign', methods=['POST'])
def english_characters():
    try:
        data = request.get_json()
        image_data = data['image']
        image_bytes = base64.b64decode(image_data)
        image = Image.open(BytesIO(image_bytes))
        prediction = predict_english(image)
        return jsonify({'message': prediction}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5052)
