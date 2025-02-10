from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
from process_image import process_image

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['RESULT_FOLDER'] = 'static/results'

@app.route('/')
def index():
    return render_template('CT.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return {'success': False, 'message': 'No file part'}
    
    file = request.files['image']
    if file.filename == '':
        return {'success': False, 'message': 'No selected file'}
    
    if file:
        filename = 'uploaded_image.jpg'
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return {'success': True}

@app.route('/processing')
def processing():
    return render_template('processing.html')

@app.route('/process')
def process_image_route():
    try:
        # مسیر عکس آپلود شده
        uploaded_filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'uploaded_image.jpg')
        
        # پردازش عکس
        result_path = process_image(uploaded_filepath)
        
        return {'success': True, 'result_path': result_path}
    except Exception as e:
        return {'success': False, 'message': str(e)}

@app.route('/result')
def show_result():
    result_path = request.args.get('result_path')
    return render_template('result.html', result_path=result_path)

@app.route('/static/results/<filename>')
def result_file(filename):
    return send_from_directory(app.config['RESULT_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)