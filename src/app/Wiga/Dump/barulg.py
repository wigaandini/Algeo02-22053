import cv2
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt

def getImgPath(namaFile):
    path = Path().absolute()
    pathFile = str(path) + "\\test\\" + namaFile
    return pathFile

def getHSV(img):
    imgnorm = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) / 255.0
    b, g, r = imgnorm[:, :, 2], imgnorm[:, :, 1], imgnorm[:, :, 0]
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


def vectorLength(h,s,v):
    sum = h**2 + v**2 + s**2
    return sum**(0.5)

    
def cropImage(img):
    height, width, _ = img.shape

    # crop sampe dia habis dibagi 4 karena mau dibikin block 4x4
    newHeight = height - height % 4
    newWidth = width - width % 4
    croppedImg = img[:newHeight, :newWidth]

    return croppedImg

def cropInto16Blocks(image):
    img_height, img_width = image.shape[:2]
    block_height = img_height // 4
    block_width = img_width // 4

    blocks = []
    for r in range(4):
        for c in range(4):
            block = image[r * block_height: (r + 1) * block_height, c * block_width: (c + 1) * block_width]
            blocks.append(block)

    return blocks

def calculate16HSV(imgblocks):
    hAvgs, sAvgs, vAvgs = [], [], []
    for i in range(16):
        h, s, v = getHSV(imgblocks[i])
        hAvg, sAvg, vAvg = (np.mean(h)), (np.mean(s)), (np.mean(v))
        hAvgs.append(hAvg)
        sAvgs.append(sAvg)
        vAvgs.append(vAvg)
    return hAvgs, sAvgs, vAvgs
        # combined_values = hAvg * 100 + sAvg * 10 + vAvg
        # hsvAvg.append(combined_values)
        # print(len(vsv))

def dotProductVector(h1,s1,v1,h2,s2,v2):
    return h1*h2 + s1*s2 + v1*v2

def cosineSimilarity(h1,s1,v1,h2,s2,v2):
    if(vectorLength(h1,s1,v1) != 0 and vectorLength(h2,s2,v2) != 0):
        return (dotProductVector(h1,s1,v1,h2,s2,v2)/(vectorLength(h1,s1,v1)*vectorLength(h2,s2,v2)))
    else :
        return 0
    
def cosineSimilarity16Block(h1,s1,v1,h2,s2,v2):
    cs = []
    for i in range(16):
        csblock = cosineSimilarity(h1[i],s1[i],v1[i],h2[i],s2[i],v2[i])
        cs.append(csblock)
        # print(csblock)
    return cs

def avgCS(CS16Block):
    sum = 0
    for i in range(16):
        sum += CS16Block[i]
    # return sum/16
    # sum = (CS16Block[0] + CS16Block[4] + CS16Block[8] + CS16Block[12] + CS16Block[3] + CS16Block[7] + CS16Block[11] + CS16Block[15]) + (2*(CS16Block[1] + CS16Block[2] + CS16Block[13] + CS16Block[14])) + + (8*(CS16Block[5] + CS16Block[6] + CS16Block[9] + CS16Block[10]))
    # sum = ((CS16Block[0] + CS16Block[3] + CS16Block[12] + CS16Block[15])) + (8*(CS16Block[5] + CS16Block[6] + CS16Block[9] + CS16Block[10])) + ((CS16Block[1] + CS16Block[2] + CS16Block[4] + CS16Block[7] + CS16Block[8] + CS16Block[11] + CS16Block[13] + CS16Block[14]))
    return (sum/16) * 100

file1 = input("Masukkan nama file 1 (lengkap dengan type file, e.g : Opan.png): \n")
img1 = cv2.imread(getImgPath(file1))
img1c = cropInto16Blocks(cropImage(img1))
# hsv1 = calculate16HSV(img1c)
h1, s1, v1 = calculate16HSV(img1c)
# print(len(hsv1))

file2 = input("Masukkan nama file 2 (lengkap dengan type file, e.g : Opan.png): \n")
img2 = cv2.imread(getImgPath(file2))
img2c = cropInto16Blocks(cropImage(img2))
# hsv2 = calculate16HSV(img2c)
h2, s2, v2 = calculate16HSV(img2c)

cs16 = cosineSimilarity16Block(h1,s1,v1,h2,s2,v2)
print(h1)
print(v1)
print(s1)
# print(hsv1)
print()         
print(h2)
print(s2)
print(v2)
# print(hsv2)
print()
print(cs16)
print()
print(avgCS(cs16))