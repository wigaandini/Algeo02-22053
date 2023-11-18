import cv2
import numpy as np
from pathlib import Path
import time
import os
import multiprocessing
import csv

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

def hsv_histogram(img):
    imgnorm = img / 255.0
    b, g, r = imgnorm[:, :, 0], imgnorm[:, :, 1], imgnorm[:, :, 2]

    Cmin = np.minimum.reduce([r, g, b])
    Cmax = np.maximum.reduce([r, g, b])
    delta = Cmax - Cmin

    vVal = np.digitize(Cmax, [0, 0.2, 0.7, 1]) - 1
    sVal = np.digitize(delta / np.maximum(Cmax, 1e-10), [0, 0.2, 0.7, 1]) - 1

    hVal = np.zeros_like(delta)
    non_zero_delta = delta != 0

    hVal[non_zero_delta] = np.select(
        [Cmax == r, Cmax == g, Cmax == b],
        [
            60 * (((g - b) / np.maximum(delta, 1e-10))),
            60 * (((b - r) / np.maximum(delta, 1e-10)) + 2),
            60 * (((r - g) / np.maximum(delta, 1e-10)) + 4),
        ],
        default=0
    )[non_zero_delta]

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
    
    hVal_flat = hVal.flatten()
    sVal_flat = sVal.flatten()
    vVal_flat = vVal.flatten()

    # Jadiin 1 value, such as 711, 120 dst
    combined_values = hVal * 100 + sVal * 10 + vVal
    custom_bins = range(0, 723)  # Assuming the range is 0 to 722
    frequency_vector, _ = np.histogram(combined_values.flatten(), bins=custom_bins)

    return frequency_vector.tolist()

def parallel_hsv_histogram(args):
    img_i, = args
    return hsv_histogram(img_i)

def parallel_check_similarity(img, imgs):
    vector1 = hsv_histogram(img)
    cached_file_path = "vector2_list_cache.csv"

    if os.path.exists(cached_file_path):
        with open(cached_file_path, 'r') as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader)  # Skip the header
            vector2_list = [list(map(float, row)) for row in reader]
    else:
        with multiprocessing.Pool() as pool:
            vector2_list = pool.map(parallel_hsv_histogram, [(img_i,) for img_i in imgs])

        # Write vector2_list to cache
        with open(cached_file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['img_vector'])
            writer.writerows(vector2_list)

    res = np.empty((0, 2))
    
    for i, vector2 in enumerate(vector2_list):
        cs = cosine_similarity(vector1, vector2)
        if cs > 60:
            res = np.vstack((res, np.array([i, cs])))

    sorted_res = res[res[:, 1].argsort()[::-1]]  # Sort results by similarity score
    return sorted_res


