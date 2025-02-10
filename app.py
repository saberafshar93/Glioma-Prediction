from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

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
        
        # Here you can add your image processing logic
        # For example, let's just copy the uploaded image as the result
        result_filename = 'processed_image.jpg'
        result_filepath = os.path.join(app.config['UPLOAD_FOLDER'], result_filename)
        os.rename(filepath, result_filepath)
        
        return {'success': True}

@app.route('/result')
def show_result():
    return render_template('result.html')

@app.route('/static/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)