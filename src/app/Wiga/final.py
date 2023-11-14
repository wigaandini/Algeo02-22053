import cv2
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import time
import os
from util import *

def getImgPath(namaFile):
    path = Path().absolute()
    pathFile = str(path) + "\\test\\" + "\\Image\\" + namaFile
    return pathFile

def getHSV(img):
    imgnorm = img / 255.0
    b, g, r = imgnorm[:, :, 0], imgnorm[:, :, 1], imgnorm[:, :, 2]
    Cmin = np.minimum.reduce([r, g, b])
    Cmax = np.maximum.reduce([r, g, b])
    delta = Cmax - Cmin
    vVal = np.select(
        [
            (Cmax >= 0) & (Cmax < 0.2),
            (Cmax >= 0.2) & (Cmax < 0.7),
            (Cmax >= 0.7) & (Cmax <= 1)
        ],
        [0, 1, 2]
    )    
    sVal = np.zeros_like(delta)
    np.divide(delta, np.maximum(Cmax, 1e-10), out=sVal, where=Cmax != 0)
    sVal = np.select(
        [
            (sVal >= 0) & (sVal < 0.2),
            (sVal >= 0.2) & (sVal < 0.7),
            (sVal >= 0.7) & (sVal <= 1)
        ],
        [0, 1, 2]
    )    
    hVal = np.zeros_like(delta)
    hVal = np.where(delta != 0,
        np.select(
            [Cmax == r, Cmax == g, Cmax == b],
            [
                60 * (((g - b) / np.maximum(delta, 1e-10))),
                60 * (((b - r) / np.maximum(delta, 1e-10)) + 2),
                60 * (((r - g) / np.maximum(delta, 1e-10)) + 4),
            ],
            default = 0
        ),
        0
    )
    hVal = np.nan_to_num(hVal)
    hVal = np.round(hVal)
    hVal = np.select(
        [np.logical_or((hVal >= 316) & (hVal <= 360), (hVal == 0)),
         (hVal >= 1) & (hVal <= 25),
         (hVal >= 26) & (hVal <= 40),
         (hVal >= 41) & (hVal <= 120),
         (hVal >= 121) & (hVal <= 190),
         (hVal >= 191) & (hVal <= 270),
         (hVal >= 271) & (hVal <= 295),
         (hVal >= 296) & (hVal <= 315)],
        [0, 1, 2, 3, 4, 5, 6, 7]
    )
    return hVal, sVal, vVal

def HSVHistogram(hVal, sVal, vVal):
    hVal_flat = hVal.flatten()
    sVal_flat = sVal.flatten()
    vVal_flat = vVal.flatten()

    # Jadiin 1 value, such as 711, 120 dst
    combined_values = hVal_flat * 100 + sVal_flat * 10 + vVal_flat
    custom_bins = [0, 1, 2, 10, 11, 12, 20, 21, 22, 100, 101, 102, 110, 111, 112, 120, 121, 122, 200, 201, 202, 210, 211, 212, 220, 221, 222, 300, 301, 302, 310, 311, 312, 320, 321, 322, 400, 401, 402, 410, 411, 412, 420, 421, 422, 500, 501, 502, 510, 511, 512, 520, 521, 522, 600, 601, 602, 610, 611, 612, 620, 621, 622, 700, 701, 702, 710, 711, 712, 720, 721, 722]
    frequency_dict = {key: 0 for key in custom_bins}

    for value in combined_values:
        frequency_dict[value] += 1

    frequency_vector = [frequency_dict[key] for key in custom_bins]
    return frequency_vector

def readImg(namaFile):
    return cv2.imread(getImgPath(namaFile))

def getDatasetPath(namaFolder):
    path = Path().absolute()
    pathData = str(path) + "\\test\\" + namaFolder
    return pathData

def readDataset(dataPath):
    # List all files in the dataset path
    image_files = [f for f in os.listdir(dataPath) if f.endswith(('.jpg', '.jpeg', '.png'))]
    imgs = []
    # Loop through each image file
    for image_file in image_files:
        # Construct the full path to the image
        image_path = os.path.join(dataPath, image_file)

        # Read the image using OpenCV
        img = cv2.imread(image_path)
        imgs.append(img)

    return imgs

def checkSimilarity(img, imgs):
    res = []
    h, s, v = getHSV(img)
    hsv = HSVHistogram(h,s,v)
    for i in range(len(imgs)):
        hi, si, vi = getHSV(imgs[i])
        hsvi = HSVHistogram(hi,si,vi)
        cs = cosineSimilarity(hsv , hsvi)
        resi = (i, cs)
        # print(cs)
        if cs > 60:
            res.append(resi)
    sorted_res = sorted(res, key=lambda x: x[1], reverse=True)
    return sorted_res

folder = input("Nama folder dataset: ")
# print(imgs)

file1 = input("Masukkan nama file 1 (lengkap dengan type file, e.g : Opan.png): \n")
# file2 = input("Masukkan nama file 2 (lengkap dengan type file, e.g : Opan.png): \n")
# # # img1c = cropInto16Blocks(cropImage(img1))
# # # hsv1 = calculate16HSV(img1c)
# # # print(len(hsv1))

start = time.time()
dataset_path = getDatasetPath(folder)
imgs = readDataset(dataset_path)
# print(len(imgs))
img1 = readImg(file1)
res = checkSimilarity(img1, imgs)
print(res)
# img1 = cv2.imread(getImgPath(file1))
# img2 = cv2.imread(getImgPath(file2))
# # # img2c = cropInto16Blocks(cropImage(img2))
# # # hsv2 = calculate16HSV(img2)
# h1, s1, v1 = getHSV(img1)
# hsv1 = HSVHistogram(h1, s1, v1)
# h2, s2, v2 = getHSV(img2)
# hsv2 = HSVHistogram(h2, s2, v2)

# # print(len(hsv1))
# # print(hsv1)
# # print()  
# # print(len(hsv2))       
# # print(hsv2)
# # print()
# print(cosineSimilarity(hsv1, hsv2) * 100)
# # print()
end = time.time()
 
# # print the difference between start 
# # and end time in milli. secs
print("The time of execution of above program is :",
      (end-start), "s")

# print(cosineSimilarity(hsv1[0], hsv2[0]))
# print(cosineSimilarity(hsv1[1], hsv2[1]))
# print(cosineSimilarity(hsv1[2], hsv2[2]))
# print(cosineSimilarity(hsv1[3], hsv2[3]))
# print(cosineSimilarity(hsv1[4], hsv2[4]))
# print(cosineSimilarity(hsv1[5], hsv2[5]))
# print(cosineSimilarity(hsv1[6], hsv2[6]))
# print(cosineSimilarity(hsv1[7], hsv2[7]))
# print(cosineSimilarity(hsv1[8], hsv2[8]))
# print(vectorLength(hsv1))
# print(vectorLength(hsv2))
# print(dotProductVector(hsv1,hsv2))