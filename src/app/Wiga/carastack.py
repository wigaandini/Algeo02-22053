import cv2
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt

def getImgPath(namaFile):
    path = Path().absolute()
    pathFile = str(path) + "\\test\\" + namaFile
    return pathFile

# def getH(imgnorm):
#     b, g, r = imgnorm[:, :, 0], imgnorm[:, :, 1], imgnorm[:, :, 2]
#     Cmin = np.minimum.reduce([r, g, b])
#     Cmax = np.maximum.reduce([r, g, b])
#     delta = Cmax - Cmin

#     hVal = np.zeros_like(delta)
#     hVal = np.where(delta != 0,
#         np.select(
#             [Cmax == r, Cmax == g, Cmax == b],
#             [
#                 60 * (((g - b) / np.maximum(delta, 1e-10))),
#                 60 * (((b - r) / np.maximum(delta, 1e-10)) + 2),
#                 60 * (((r - g) / np.maximum(delta, 1e-10)) + 4),
#             ],
#             default = 0
#         ),
#         0
#     )
#     hVal = np.nan_to_num(hVal)
#     hVal = np.round(hVal)
#     hVal = np.select(
#         [np.logical_or((hVal >= 316) & (hVal <= 360), (hVal == 0)),
#          (hVal >= 1) & (hVal <= 25),
#          (hVal >= 26) & (hVal <= 40),
#          (hVal >= 41) & (hVal <= 120),
#          (hVal >= 121) & (hVal <= 190),
#          (hVal >= 191) & (hVal <= 270),
#          (hVal >= 271) & (hVal <= 295),
#          (hVal >= 296) & (hVal <= 315)],
#         [0, 1, 2, 3, 4, 5, 6, 7]
#     )

#     hVal_flat = hVal.flatten()
#     custom_bins = [0, 1, 2, 3, 4, 5, 6, 7]
#     plt.hist(hVal_flat, bins=custom_bins, color='c', alpha=0.7)
#     hist_hVal, _ = np.histogram(hVal_flat, bins=custom_bins)

#     return (hist_hVal)

# def getS(imgnorm):
#     b, g, r = imgnorm[:, :, 0], imgnorm[:, :, 1], imgnorm[:, :, 2]
#     Cmin = np.minimum.reduce([r, g, b])
#     Cmax = np.maximum.reduce([r, g, b])
#     delta = Cmax - Cmin
 
#     sVal = np.zeros_like(delta)
#     np.divide(delta, np.maximum(Cmax, 1e-10), out=sVal, where=Cmax != 0)
#     sVal = np.select(
#         [
#             (sVal >= 0) & (sVal < 0.2),
#             (sVal >= 0.2) & (sVal < 0.7),
#             (sVal >= 0.7) & (sVal <= 1)
#         ],
#         [0, 1, 2]
#     )    

#     sVal_flat = sVal.flatten()
#     custom_bins = [0, 1, 2]
#     plt.hist(sVal_flat, bins=custom_bins, color='c', alpha=0.7)
#     hist_sVal, _ = np.histogram(sVal_flat, bins=custom_bins)

#     return (hist_sVal)

# def getV(imgnorm):
#     b, g, r = imgnorm[:, :, 0], imgnorm[:, :, 1], imgnorm[:, :, 2]
#     Cmin = np.minimum.reduce([r, g, b])
#     Cmax = np.maximum.reduce([r, g, b])

#     vVal = np.select(
#         [
#             (Cmax >= 0) & (Cmax < 0.2),
#             (Cmax >= 0.2) & (Cmax < 0.7),
#             (Cmax >= 0.7) & (Cmax <= 1)
#         ],
#         [0, 1, 2]
#     )    

#     vVal_flat = vVal.flatten()
#     custom_bins = [0, 1, 2]
#     plt.hist(vVal_flat, bins=custom_bins, color='c', alpha=0.7)
#     hist_vVal, _ = np.histogram(vVal_flat, bins=custom_bins)

#     return (hist_vVal)

def getHSV(img):
    imgnorm = img / 255.0
    b, g, r = imgnorm[:, :, 0], imgnorm[:, :, 1], imgnorm[:, :, 2]
    Cmin = np.minimum.reduce([r, g, b])
    Cmax = np.maximum.reduce([r, g, b])
    delta = Cmax - Cmin
    vVal = Cmax*100
    sVal = np.zeros_like(delta)
    sVal = np.divide((Cmax / np.maximum(delta, 1e-10)) * 100, delta, out=np.zeros_like(delta), where=(delta != 0))
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
    return hVal, sVal, vVal
    # vVal = np.select(
    #     [
    #         (Cmax >= 0) & (Cmax < 0.2),
    #         (Cmax >= 0.2) & (Cmax < 0.7),
    #         (Cmax >= 0.7) & (Cmax <= 1)
    #     ],
    #     [0, 1, 2]
    # )    
    # sVal = np.where(delta != 0, Cmax/delta)
    # sVal = np.select(
    #     [
    #         (sVal >= 0) & (sVal < 0.2),
    #         (sVal >= 0.2) & (sVal < 0.7),
    #         (sVal >= 0.7) & (sVal <= 1)
    #     ],
    #     [0, 1, 2]
    # )    
    # hVal = np.nan_to_num(hVal)
    # hVal = np.round(hVal)
    # hVal = np.select(
    #     [np.logical_or((hVal >= 316) & (hVal <= 360), (hVal == 0)),
    #      (hVal >= 1) & (hVal <= 25),
    #      (hVal >= 26) & (hVal <= 40),
    #      (hVal >= 41) & (hVal <= 120),
    #      (hVal >= 121) & (hVal <= 190),
    #      (hVal >= 191) & (hVal <= 270),
    #      (hVal >= 271) & (hVal <= 295),
    #      (hVal >= 296) & (hVal <= 315)],
    #     [0, 1, 2, 3, 4, 5, 6, 7]
    # )

def dotProductVector(vector1, vector2):
    value = np.sum(vector1.astype(float) * vector2.astype(float))
    return value

def HSVHistogram(hVal, sVal, vVal):
    hHist = np.histogram(hVal, bins=[0,26,41,121,191,271,296,316,360])
    sHist = np.histogram(sVal, bins=[0,20,70,100])
    vHist = np.histogram(vVal, bins=[0,20,70,100])
    
    # hHist1 = np.array(hHist, dtype=object)
    # sHist1 = np.array(sHist, dtype=object)
    # vHist1 = np.array(vHist, dtype=object)

    return(np.hstack((hHist, sHist, vHist)))
    plt.show()

def vectorLength(vector):
    value = np.sum(vector.astype(float)**2)
    return np.sqrt(value)

def cosineSimilarity(vector_img1, vector_img2):
    if(vectorLength(vector_img1) != 0 and vectorLength(vector_img2) != 0):
        return (dotProductVector(vector_img1, vector_img2)/(vectorLength(vector_img1)*vectorLength(vector_img2)))
    else :
        return 0
    
def cropImage(img):
    height, width, _ = img.shape

    # crop sampe dia habis dibagi 4 karena mau dibikin block 4x4
    newHeight = height - height % 4
    newWidth = width - width % 4
    croppedImg = img[:newHeight, :newWidth]

    return croppedImg


file1 = input("Masukkan nama file 1 (lengkap dengan type file, e.g : Opan.png): \n")
img1 = cv2.imread(getImgPath(file1))
img1norm = img1 / 255.0
h1, s1, v1 = getHSV(img1norm)
hsv1 = HSVHistogram(h1, s1, v1)

file2 = input("Masukkan nama file 2 (lengkap dengan type file, e.g : Opan.png): \n")
img2 = cv2.imread(getImgPath(file2))
img2norm = img2 / 255.0
h2, s2, v2 = getHSV(img2norm)
hsv2 = HSVHistogram(h2, s2, v2)

print(hsv1)
print()         
print(hsv2)
print()
# print(cosineSimilarity(hsv1, hsv2))
# plt.show()

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