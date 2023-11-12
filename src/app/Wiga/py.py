import cv2
import numpy as np
from pathlib import Path

def getImgPath(namaFile):
    path = Path().absolute()
    pathFile = str(path) + "\\test\\" + namaFile
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
                (60 * (((g - b) / np.maximum(delta, 1e-10)))),
                (60 * (((b - r) / np.maximum(delta, 1e-10)) + 2)),
                (60 * (((r - g) / np.maximum(delta, 1e-10)) + 4)),
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

def getHSVBlock(img, nRowStart, nRowEnd, nColStart, nColEnd):
    block = img[nRowStart:nRowEnd, nColStart:nColEnd, :]
    h, s, v = getHSV(block)
    
    hAvg = np.mean(h)
    sAvg = np.mean(s)
    vAvg = np.mean(v)

    return hAvg, sAvg, vAvg

def getVector(img_rgb):
    nCol = len(img_rgb[0]) // 3 * 3
    nRow = len(img_rgb) // 3 * 3

    nRowDiv3 = nRow // 3
    nColDiv3 = nCol // 3

    hsv = np.zeros((9, 3), dtype = float)
    
    check = 0
    for startRow in range(0, nRow, nRowDiv3):
        endRow = startRow + nRowDiv3 - 1

        for startCol in range(0, nCol, nColDiv3):
            endCol = startCol + nColDiv3 - 1

            hsv[check, :] = getHSVBlock(img_rgb, startRow, endRow, startCol, endCol)
            check += 1

    hsv = np.round(hsv).astype(int)
    return hsv

def vectorLength(vector):
    value = 0

    for i in range(len(vector)):
        value += (float(vector[i]))**2
    
    return value**(0.5)

def dotProductVector(vector1, vector2):
    value = 0

    for i in range(len(vector1)):
        value += float(vector1[i])*float(vector2[i])
    
    return value

def cosineSimilarity(vector_img1, vector_img2):
    return dotProductVector(vector_img1, vector_img2)/(vectorLength(vector_img1)*vectorLength(vector_img2))

def avgCS(vector1, vector2):
    sum = 0
    for i in range(len(vector1)):
        sum += cosineSimilarity(vector1[i], vector2[i])
    print(sum)
    return sum/len(vector1)

el = [[0 for j in range(6)] for i in range(10)]
for i in range(10):
    for j in range(6):
        el[i][j] = int(input())
print(el)

sparse = getVector(el)
print(sparse)