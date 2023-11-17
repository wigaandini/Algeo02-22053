from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
from os.path import relpath
from bs4 import BeautifulSoup
from werkzeug.utils import secure_filename
from multiprocessing import Pool
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from urllib.parse import urlparse, urljoin
from io import BytesIO
from app.Wiga.temp import read_img, get_dataset_path, read_dataset, parallel_check_similarity
from app.Salsa.tesmultitexture import checkTextureSimilarity

app = Flask(__name__)
CORS(app)  # Initialize CORS with default options

UPLOAD_FOLDER = 'public'
SEED_FOLDER = 'SEED'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SEED_FOLDER'] = SEED_FOLDER

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

def get_current_seed():
    seed_file_path = os.path.join(app.config['SEED_FOLDER'], 'seed.txt')
    if os.path.exists(seed_file_path):
        with open(seed_file_path, 'r') as seed_file:
            return seed_file.read().strip()
    else:
        return None

def update_current_seed(new_seed):
    seed_file_path = os.path.join(app.config['SEED_FOLDER'], 'seed.txt')
    with open(seed_file_path, 'w') as seed_file:
        seed_file.write(str(new_seed))

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

    seed = request.form.get('seed')

    # Check if it's a new dataset by comparing with the current seed
    current_seed = get_current_seed()
    destination_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'Dataset')
    if seed != current_seed:
        create_directory(destination_dir)
        delete_directory_contents(destination_dir)
        update_current_seed(seed)

    paths = []
    for image in images:
        filename = secure_filename(image.filename)
        path = os.path.join(destination_dir, filename)
        image.save(path)
        paths.append(path)
    cached_file_path = "vector2_list_cache.csv"
    if os.path.exists(cached_file_path):
        os.remove(cached_file_path)

    cached_file_path2 = "vector2_list_cache_texture.csv"
    if os.path.exists(cached_file_path2):
        os.remove(cached_file_path2)

    return jsonify({'message': 'Folder uploaded successfully', 'paths': paths})


@app.route('/api/process_image_similarity/Color', methods=['POST'])
def process_image_similarity():
    try:
        file_name = request.form.get('file_name')
        img = read_img(file_name)

        dataset_path = get_dataset_path()
        imgs, img_paths = read_dataset(dataset_path)
        result = parallel_check_similarity(img, imgs)

        similarity_results = [{'image_path': relpath(img_paths[int(index)], app.config['UPLOAD_FOLDER']), 'similarity_score': float(score)} for index, score in result]

        return jsonify({'similarity_results': similarity_results}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/process_image_similarity/Texture', methods=['POST'])
def process_image_similarity_texture():
    try:
        file_name = request.form.get('file_name')
        img = read_img(file_name)

        dataset_path = get_dataset_path()
        imgs, img_paths = read_dataset(dataset_path)
        result = checkTextureSimilarity(img, imgs)

        similarity_results = [{'image_path': relpath(img_paths[int(index)], app.config['UPLOAD_FOLDER']), 'similarity_score': float(score)} for index, score in result]

        return jsonify({'similarity_results': similarity_results}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

def scrape_images_from_website(url, destination_dir):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    img_tags = soup.find_all('img')
    image_paths = []

    for img_tag in img_tags:
        img_url = img_tag.get('src')
        if img_url:
            img_url = urljoin(url, img_url)
            img_response = requests.get(img_url)

            if img_response.ok:
                filename = secure_filename(os.path.basename(urlparse(img_url).path))
                path = os.path.join(destination_dir, filename)
                with open(path, 'wb') as img_file:
                    img_file.write(img_response.content)
                image_paths.append(path)

    return image_paths

@app.route('/api/scrape-website', methods=['POST'])
def scrape_website():
    try:
        website_url = request.form.get('website_url')
        destination_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'Dataset')

        create_directory(destination_dir)
        delete_directory_contents(destination_dir)

        cached_file_path = "vector2_list_cache.csv"
        if os.path.exists(cached_file_path):
            os.remove(cached_file_path)

        cached_file_path2 = "vector2_list_cache_texture.csv"
        if os.path.exists(cached_file_path2):
            os.remove(cached_file_path2)

        scraped_image_paths = scrape_images_from_website(website_url, destination_dir)

        return jsonify({'message': 'Website images scraped successfully', 'image_paths': scraped_image_paths}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)


