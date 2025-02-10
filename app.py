from flask import Flask, request, jsonify, render_template
import os
import requests

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def CT():
    return render_template('CT.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    file = request.files['image']
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # ارسال تصویر به Google Colab
    colab_url = "https://colab.research.google.com/drive/1PEgph989YvsOZnkLEbJwoKp-CHn9jolz"
    with open(file_path, 'rb') as f:
        response = requests.post(colab_url, files={'image': f})

    if response.status_code == 200:
        processed_image_url = response.json().get('processed_image_url')
        return jsonify({'image_url': processed_image_url})
    else:
        return jsonify({'error': 'Failed to process image'}), 500

@app.route('/result')
def result():
    image_url = request.args.get('image_url')
    return render_template('result.html', image_url=image_url)

if __name__ == '__main__':
    app.run(debug=True)