from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory
import os
from werkzeug.utils import secure_filename
from PIL import Image
from rembg import remove

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads/'
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_image(file_path):
    # Load the image and remove the background using rembg
    input_image = Image.open(file_path)
    output_image = remove(input_image)

    # Save the processed image to the PROCESSED_FOLDER as PNG
    processed_file_path = os.path.join(app.config['UPLOAD_FOLDER'], f'bg_removed.png')

    # Save as PNG instead of JPEG
    output_image.save(processed_file_path, format='PNG')

    return processed_file_path

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        print(filename)
        # Process the image using rembg
        processed_file_path = process_image(file_path)
        print(processed_file_path)
        os.remove(file_path)
        flash('Here is your image with removed background!')
        return render_template('index.html', filename=f'bg_removed.png')

    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)

@app.route('/display/<filename>')
def display_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
