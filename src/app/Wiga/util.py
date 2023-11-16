import cv2
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import time
import os

def getImgPath(namaFile):
    path = Path().absolute()
    pathFile = str(path) + "\\src\\" + "\\UPLOAD\\" + "\\Image\\" + namaFile
    return pathFile

def readImg(namaFile):
    return cv2.imread(getImgPath(namaFile))

def getDatasetPath():
    path = Path().absolute()
    pathData = str(path) + "\\src\\" + "\\UPLOAD\\" + "Dataset"
    return pathData

def readDataset(dataPath):
    # List all files in the dataset path
    image_files = [f for f in os.listdir(dataPath) if f.endswith(('.jpg', '.jpeg', '.png'))]
    imgs = []
    imgpath = []
    # Loop through each image file
    for image_file in image_files:
        # Construct the full path to the image
        image_path = os.path.join(dataPath, image_file)
        imgpath.append(image_path)

        # Read the image using OpenCV
        img = cv2.imread(image_path)
        imgs.append(img)

    return imgs, imgpath

def dotProductVector(vector1, vector2):
    vector1 = np.array(vector1)
    vector2 = np.array(vector2)
    value = np.sum(vector1.astype(float) * vector2.astype(float))
    return value

def vectorLength(vector):
    if isinstance(vector, list):
        vector = np.array(vector)
    value = np.sum(vector.astype(float)**2)
    return np.sqrt(value)

def cosineSimilarity(vector_img1, vector_img2):
    if(vectorLength(vector_img1) != 0 and vectorLength(vector_img2) != 0):
        return (dotProductVector(vector_img1, vector_img2)/(vectorLength(vector_img1)*vectorLength(vector_img2))) * 100
    else :
        return 0