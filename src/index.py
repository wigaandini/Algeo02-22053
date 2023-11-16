from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)
CORS(app)  # Initialize CORS with default options

UPLOAD_FOLDER = 'UPLOAD'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def create_directory(directory):
    try:
        os.makedirs(directory)
    except FileExistsError:
        pass

def delete_directory_contents(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            os.remove(os.path.join(root, file))
        for dir in dirs:
            shutil.rmtree(os.path.join(root, dir))

@app.route('/api/upload-image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'})

    image = request.files['image']

    if image.filename == '':
        return jsonify({'error': 'No selected file'})

    destination_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'Image')
    create_directory(destination_dir)
    delete_directory_contents(destination_dir)

    filename = secure_filename(image.filename)
    path = os.path.join(destination_dir, filename)
    image.save(path)

    return jsonify({'message': 'Image uploaded successfully', 'path': path})

@app.route('/api/upload-folder', methods=['POST'])
def upload_folder():
    if 'imagedataset' not in request.files:
        return jsonify({'error': 'No file part'})

    images = request.files.getlist('imagedataset')
    
    if not images:
        return jsonify({'error': 'No selected files'})

    destination_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'Dataset')
    create_directory(destination_dir)
    delete_directory_contents(destination_dir)
    # Do not delete existing contents

    paths = []
    for image in images:
        filename = secure_filename(image.filename)
        path = os.path.join(destination_dir, filename)
        image.save(path)
        paths.append(path)

    return jsonify({'message': 'Folder uploaded successfully', 'paths': paths})


@app.route('/api/process_image', methods=['POST'])
def process_images():
    try:
        degrees = int(request.form.get('degrees', 90))  # Default rotation is 90 degrees
        image_files = request.files.getlist('imagedataset')
        print(image_files)
        
        rotated_images = []

        for image_file in image_files:
            rotated_image_data = rotate_image(image_file.read(), degrees)
            rotated_images.append(base64.b64encode(rotated_image_data).decode('utf-8'))

        return jsonify({'rotated_images': rotated_images}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
