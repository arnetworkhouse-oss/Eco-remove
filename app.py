import io
from flask import Flask, render_template, request, send_file
from rembg import remove, new_session
from PIL import Image

app = Flask(__name__)

# This part is key for Render Free Tier:
session = new_session("u2netp") 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/remove-bg', methods=['POST'])
def remove_bg():
    if 'file' not in request.files:
        return "No file", 400
    
    file = request.files['file'].read()
    
    # Use the 'session' we created above
    output = remove(file, session=session)
    
    return send_file(io.BytesIO(output), mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
