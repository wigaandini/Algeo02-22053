import numpy as np
import os
import multiprocessing
import csv
from app.mainProg.util import *

def hsv_histogram(img):
    imgnorm = img / 255.0 # normalisasi rgb 0-255 ke 0-1
    b, g, r = imgnorm[:, :, 0], imgnorm[:, :, 1], imgnorm[:, :, 2]

    Cmin = np.minimum.reduce([r, g, b])
    Cmax = np.maximum.reduce([r, g, b])
    delta = Cmax - Cmin

    vVal = np.digitize(Cmax, [0, 0.2, 0.7, 1]) - 1
    sVal = np.digitize(delta / np.maximum(Cmax, 1e-10), [0, 0.2, 0.7, 1]) - 1   # dikasi 1e-10 buat ngehindarin pembagian 0

    hVal = np.zeros_like(delta)
    non_zero_delta = delta != 0

    hVal[non_zero_delta] = np.select(
        [Cmax == r, Cmax == g, Cmax == b],
        [
            60 * (((g - b) / np.maximum(delta, 1e-10))),        # dikasi 1e-10 buat ngehindarin pembagian 0
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

    # Jadiin 1 value, such as 711, 120 dst
    combined_values = hVal * 100 + sVal * 10 + vVal
    custom_bins = range(0, 723)  # Range 0 sampai 722
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
            header = next(reader)
            vector2_list = [list(map(float, row)) for row in reader]
    else:
        with multiprocessing.Pool() as pool:
            vector2_list = pool.map(parallel_hsv_histogram, [(img_i,) for img_i in imgs])

        with open(cached_file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['img_vector'])
            writer.writerows(vector2_list)

    res = np.empty((0, 2))
    for i, vector2 in enumerate(vector2_list):
        cs = cosine_similarity(vector1,vector2)
        if cs > 60:
            res = np.vstack((res, np.array([i, cs])))

    sorted_res = res[res[:, 1].argsort()[::-1]]
    return sorted_res