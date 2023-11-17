import numpy as np
import numpy.ma as ma
import sys
sys.path.insert(0, 'c:/Users/Salsabiila/Kuliah/Semester3/Algeo/Tubes-2/Algeo02-22053')
from src.app.Wiga.util import *

def grayscaleImg(img):
    img_grayscale = np.round(0.299 * img[:, :, 2] + 0.587 * img[:, :, 1] + 0.114 * img[:, :, 0]).astype(np.uint8)
    
    return img_grayscale

def createGLCM0(img, distance=1):
    rows, cols = img.shape
    glcm = np.zeros((256, 256), dtype=int)

    for i in range(rows):
        for j in range(cols - distance):
            glcm[img[i, j], img[i, j + distance]] += 1
    
    return glcm

def createGLCM90(img):
    rows, cols = img.shape
    glcm = np.zeros((256, 256), dtype=int)

    for j in range(cols):
        for i in range(rows - 1, 0, -1):
            glcm[img[i, j], img[i-1, j]] += 1
    
    return glcm

def createGLCM45(img):
    rows, cols = img.shape
    glcm = np.zeros((256, 256), dtype=int)

    for i in range(1, rows):
        tempi = i
        j = 0
        while tempi > 0 and j < cols - 1:
            glcm[img[tempi, j], img[tempi-1, j+1]] += 1
            tempi -= 1
            j += 1

    for j in range(1, cols - 1):
        tempj = j
        i = rows - 1
        while tempj < cols - 1 and i > 0:
            glcm[img[i, tempj], img[i-1, tempj+1]] += 1
            i -= 1
            tempj += 1
    
    return glcm

def createGLCM135(img):
    rows, cols = img.shape
    glcm = np.zeros((256, 256), dtype=int)

    for i in range(1, rows):
        tempi = i
        j = cols - 1
        while tempi > 0 and j > 0:
            glcm[img[tempi, j], img[tempi-1, j-1]] += 1
            tempi -= 1
            j -= 1

    for j in range(cols - 2, 0, -1):
        tempj = j
        i = rows - 1
        while tempj > 0 and i > 0:
            glcm[img[i, tempj], img[i-1, tempj-1]] += 1
            i -= 1
            tempj -= 1
    
    return glcm

def normalizedSymmetricGLCM(glcm):
    normalized_glcm = np.transpose(glcm)
    normalized_glcm = np.add(glcm, normalized_glcm)

    elmt_sum = np.sum(normalized_glcm)
    return normalized_glcm/elmt_sum

def energy(glcm):
    return np.sqrt(np.sum(np.square(glcm)))

def dissimilarity(glcm):
    i, j = np.indices(glcm.shape)

    return np.sum(glcm * np.abs(i - j))

def entropy(glcm):
    non_zero_entries = ma.masked_equal(glcm, 0)
    logarithms = ma.log(non_zero_entries)
    
    return -np.sum(glcm * logarithms)

def contrast(glcm):
    i, j = np.indices(glcm.shape)

    return np.sum(glcm * (i - j)**2)

def homogeneity(glcm):
    i, j = np.indices(glcm.shape)

    return np.sum(glcm / (1 + (i - j)**2))

def correlation(glcm):
    i, j = np.indices(glcm.shape)
    meani = np.sum(i * glcm) / np.sum(glcm)
    meanj = np.sum(j * glcm) / np.sum(glcm)
    stdi = np.sqrt(np.sum(glcm * (i - meani)**2) / np.sum(glcm))
    stdj = np.sqrt(np.sum(glcm * (j - meanj)**2) / np.sum(glcm))
    
    correlation_matrix = ((i - meani) * (j - meanj)) / np.where((stdi != 0) & (stdj != 0), (stdi * stdj), 1)
    correlation_matrix = np.nan_to_num(correlation_matrix)
    
    return np.sum(glcm * correlation_matrix)

def textureBasedVector(glcm):
    vector = np.array([contrast(glcm), homogeneity(glcm), entropy(glcm), energy(glcm), correlation(glcm), dissimilarity(glcm)])
    
    return vector

def checkTextureSimilarity(img, imgs, imgpath):
    res = []
    glcm = normalizedSymmetricGLCM(createGLCM0(grayscaleImg(img)))

    for i in range(len(imgs)):
        glcmi = normalizedSymmetricGLCM(createGLCM0(grayscaleImg(imgs[i])))
        cs = cosineSimilarity(glcm , glcmi)
        print(cs)
        resi = (imgpath[i], cs)
        if cs > 60:
            res.append(resi)
    sorted_res = sorted(res, key=lambda x: x[1], reverse=True)
    return sorted_res