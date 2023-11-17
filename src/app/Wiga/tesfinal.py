import cv2
import numpy as np
from pathlib import Path
import time
import os
from multiprocessing import Pool

def get_img_path(file_name):
    current_path = Path().absolute()
    return os.path.join(str(current_path), "public", "Image", file_name)


def read_img(file_name):
    return cv2.imread(get_img_path(file_name))

def get_dataset_path():
    current_path = Path().absolute()
    return current_path / "public" / "Dataset"

def read_dataset(data_path):
    image_files = [f for f in os.listdir(data_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
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

    if vector_length(vector_img1) != 0 and vector_length(vector_img2) != 0:
        return (dot_product_vector(vector_img1, vector_img2) /
                (vector_length(vector_img1) * vector_length(vector_img2))) * 100
    else:
        return 0
from util import *

def get_hsv(img):
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

def hsv_histogram(h_val, s_val, v_val):
    hVal_flat = h_val.flatten()
    sVal_flat = s_val.flatten()
    vVal_flat = v_val.flatten()

    # Jadiin 1 value, such as 711, 120 dst
    combined_values = hVal_flat * 100 + sVal_flat * 10 + vVal_flat
    custom_bins = [0, 1, 2, 10, 11, 12, 20, 21, 22, 100, 101, 102, 110, 111, 112, 120, 121, 122, 200, 201, 202, 210, 211, 212, 220, 221, 222, 300, 301, 302, 310, 311, 312, 320, 321, 322, 400, 401, 402, 410, 411, 412, 420, 421, 422, 500, 501, 502, 510, 511, 512, 520, 521, 522, 600, 601, 602, 610, 611, 612, 620, 621, 622, 700, 701, 702, 710, 711, 712, 720, 721, 722]
    frequency_dict = {key: 0 for key in custom_bins}

    for value in combined_values:
        frequency_dict[value] += 1

    frequency_vector = [frequency_dict[key] for key in custom_bins]
    return frequency_vector

def check_similarity(img, imgs):
    res = np.empty((0, 2))  # Initialize an empty NumPy array for results

    h, s, v = get_hsv(img)
    hsv = hsv_histogram(h, s, v)

    for i, img_i in enumerate(imgs):
        h_i, s_i, v_i = get_hsv(img_i)
        hsv_i = hsv_histogram(h_i, s_i, v_i)
        cs = cosine_similarity(hsv, hsv_i)

        if cs > 60:
            res = np.vstack((res, np.array([i, cs])))

    sorted_res = res[res[:, 1].argsort()[::-1]]  # Sort results by similarity score
    return sorted_res

# def main():
#     file_name = input("Enter the file name (including file type, e.g., Opan.png): \n")
#     start_time = time.time()

    dataset_path = get_dataset_path()
    imgs, img_paths = read_dataset(dataset_path)
    img = read_img(file_name)
    result = check_similarity(img, imgs)
    h, s, v = get_hsv(imgs)
    write_csv(hsv_histogram(h,s,v), img_paths)

    print(result)

    end_time = time.time()
    print("Execution time: {:.2f} seconds".format(end_time - start_time))

# if __name__ == "__main__":
#     main()
