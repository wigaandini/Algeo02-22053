from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
from os.path import relpath
from werkzeug.utils import secure_filename
from multiprocessing import Pool
from urllib.parse import urlparse, urljoin
from app.Wiga.temp import read_img, get_dataset_path, read_dataset, parallel_check_similarity
from app.Salsa.newmulti import checkTextureSimilarity
import requests
from bs4 import BeautifulSoup
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from PIL import Image

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
                image_paths.append(relpath(path, app.config['UPLOAD_FOLDER']))

    return image_paths

def create_pdf(similarity_results, img_path):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    images_per_page = 2
    image_width = 200
    image_height = 200
    margin = 50
    y_position = 500
    x_positions = [100, 350, 600]  # Adjust as needed
    img_path2 = os.path.join(app.config['UPLOAD_FOLDER'], img_path)
    c.drawString(100, 400,f'Image Query: ')
    c.drawImage(img_path2, 300, 300, width=200, height=200)
    c.showPage()

    for i, result in enumerate(similarity_results, 1):
        if i % images_per_page == 1 and i != 1:
            # Move to the next page
            c.showPage()
            y_position = 500

        image_path = os.path.join(app.config['UPLOAD_FOLDER'], result['image_path'])
        similarity_score = "{:.2f} %".format(result['similarity_score'])  # Format to two decimal places

        # Draw the image
        x_position = x_positions[0]
        c.drawImage(image_path, x_position, y_position, width=image_width, height=image_height)

        # Draw the similarity score next to the image
        c.drawString(x_position + image_width + margin, y_position + image_height / 2, f'Similarity Score: {similarity_score}')

        # Update y_position for the next row
        y_position -= image_height + margin

    c.save()
    buffer.seek(0)
    return buffer.read()

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

    return jsonify({'message': 'Image uploaded successfully', 'image_path': relpath(path, app.config['UPLOAD_FOLDER'])})

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

    return jsonify({'message': 'Folder uploaded successfully', 'image_path': relpath(path, app.config['UPLOAD_FOLDER'])})


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


@app.route('/api/send-attachment', methods=['POST'])
def send_attachment():
    try:
        similarity_results = request.json.get('similarity_results')
        image_path = request.json.get('image_path')

        if similarity_results:
            pdf_content = create_pdf(similarity_results,image_path)

            return send_file(
                BytesIO(pdf_content),
                as_attachment=True,
                download_name='results.pdf',
                mimetype='application/pdf'
            )

        return jsonify({'error': 'No similarity results provided'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)


