from flask import Flask, request, jsonify

app = Flask(__name__)

# تابع برای اجرای کد پایتون
def run_python_code(code):
    try:
        # اجرای کد پایتون
        exec(code)
        return "Code executed successfully!"
    except Exception as e:
        return f"Error: {str(e)}"

# ایجاد یک API برای دریافت و اجرای کد
@app.route('/run-code', methods=['POST'])
def run_code():
    data = request.json  # دریافت کد از کاربر
    code = data.get('code')
    
    # اجرای کد و دریافت نتیجه
    result = run_python_code(code)
    
    # بازگرداندن نتیجه به کاربر
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)