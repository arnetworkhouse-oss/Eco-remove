import io
import os
from flask import Flask, render_template, request, send_file
from rembg import remove, new_session
from PIL import Image

app = Flask(__name__)

# Use the smallest model (u2netp) to stay under 512MB RAM
# 'p' stands for portrait/small
try:
    session = new_session("u2netp")
except Exception as e:
    print(f"Error loading model: {e}")
    session = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/remove-bg', methods=['POST'])
def remove_bg():
    if 'file' not in request.files:
        return "No file uploaded", 400
    
    file = request.files['file']
    input_image = file.read()
    
    # Process using the tiny session
    output_image = remove(input_image, session=session)
    
    return send_file(
        io.BytesIO(output_image),
        mimetype='image/png'
    )

if __name__ == '__main__':
    # Render uses the PORT environment variable
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
