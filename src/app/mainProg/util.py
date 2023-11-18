import cv2
import numpy as np
from pathlib import Path
import os

def get_img_path(file_name):
    current_path = Path().absolute()
    return os.path.join(str(current_path), "public", "Image", file_name)

def read_img(file_name):
    return cv2.imread(get_img_path(file_name))

def get_dataset_path():
    current_path = Path().absolute()
    return current_path / "public" / "Dataset"

def read_dataset(data_path):
    image_files = [f for f in os.listdir(data_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]  # cuma read yg file image aja
    img_paths = [os.path.join(data_path, file) for file in image_files]
    imgs = np.array([cv2.imread(img_path) for img_path in img_paths])

    return imgs, img_paths

def dot_product_vector(vector1, vector2):
    return np.sum(vector1.astype(float) * vector2.astype(float))

def vector_length(vector):
    vector = np.array(vector)
    return np.sqrt(np.sum(vector.astype(float)**2))

def cosine_similarity(vector_img1, vector_img2):
    vector_img1 = np.array(vector_img1)
    vector_img2 = np.array(vector_img2)

    if vector_length(vector_img1) != 0 and vector_length(vector_img2) != 0:  # ngehindarin pembagian 0
        return (dot_product_vector(vector_img1, vector_img2) /
                (vector_length(vector_img1) * vector_length(vector_img2))) * 100
    else:
        return 0