from flask import Flask, request, jsonify, render_template
from ultralytics import YOLO
import os
import uuid

app = Flask(__name__)

# بارگذاری مدل YOLO
model = YOLO("yolov8n-seg.pt")  # مدل YOLOv8 برای segmentation

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    # ذخیره فایل موقت
    file_path = os.path.join('static', file.filename)
    file.save(file_path)
    
    # انجام پیش‌بینی با YOLO
    results = model.predict(source=file_path, save=True, project="static", name="results")
    
    # پردازش نتایج
    prediction = results[0].names[results[0].probs.top1]  # نام کلاس پیش‌بینی شده
    image_url = f"static/results/{file.filename}"  # مسیر تصویر پردازش‌شده
    
    return jsonify({
        'prediction': prediction,
        'image_url': image_url
    })

if __name__ == '__main__':
    app.run(debug=True)