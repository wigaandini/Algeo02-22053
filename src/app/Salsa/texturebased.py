import numpy as np
import numpy.ma as ma
import sys
sys.path.insert(0, 'c:/Users/Salsabiila/Kuliah/Semester3/Algeo/Tubes-2/Algeo02-22053')
from src.app.Wiga.util import *

def createTextureVect(img):
    img_grayscale = np.round(0.299 * img[:, :, 2] + 0.587 * img[:, :, 1] + 0.114 * img[:, :, 0]).astype(np.uint8)

    glcm = np.zeros((256, 256), dtype=int)
    glcm[img_grayscale[1:, :], img_grayscale[:-1, :]] += 1
    normalized_glcm = np.transpose(glcm)
    normalized_glcm = np.add(glcm, normalized_glcm)
    elmt_sum = np.sum(normalized_glcm)
    normalized_glcm = normalized_glcm / elmt_sum
    vector = np.array([contrast(normalized_glcm), homogeneity(normalized_glcm), entropy(normalized_glcm), energy(normalized_glcm), correlation(normalized_glcm), dissimilarity(normalized_glcm)])
    return vector

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

def checkTextureSimilarity(img, imgs):
    res = []
    textureVector = createTextureVect(img)

    for i in range(len(imgs)):
        textureVectori = createTextureVect(imgs[i])
        cs = cosineSimilarity(textureVector , textureVectori)
        resi = (imgpath[i], cs)
        if cs > 60:
            res.append(resi)
    sorted_res = sorted(res, key=lambda x: x[1], reverse=True)
    return sorted_res