from flask import Flask, request, jsonify
import base64
from io import BytesIO
from PIL import Image
from ultralytics import YOLO

# Load Arabic model
arabicmodel = YOLO("arabicsign.pt")
arabic_dic = {
    'Ain': 'ع', 'Al': 'ال', 'Alef': 'أ', 'Beh': 'ب', 'Dad': 'ض',
    'Dal': 'د', 'Feh': 'ف', 'Ghain': 'غ', 'Hah': 'ه', 'Heh': 'ح',
    'Kaf': 'ك', 'Khah': 'خ', 'Laa': 'لا', 'Meem': 'م', 'Noon': 'ن',
    'Reh': 'ر', 'Sad': 'ص', 'Sheen': 'ش', 'Teh': 'ت', 'Thal': 'ذ',
    'Yeh': 'ئ', 'Zain': 'ز'
}

def predict_arabic(img):
    results = arabicmodel([img])
    class_name = 'EMPTY'
    prob = 0

    for result in results:
        if result.boxes:
            for box in result.boxes:
                the_prob = box.conf
                if the_prob > prob:
                    prob = the_prob
                    class_name = arabic_dic[result.names[int(box.cls)]]

    return class_name

app = Flask(__name__)

@app.route('/arabic_sign', methods=['POST'])
def arabic_characters():
    try:
        data = request.get_json()
        image_data = data['image']
        image_bytes = base64.b64decode(image_data)
        image = Image.open(BytesIO(image_bytes))
        prediction = predict_arabic(image)
        return jsonify({'message': prediction}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5051)