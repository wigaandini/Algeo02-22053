import cv2
import math
import numpy as np

def elmtSumMatrix(matrix):
    elmt_sum = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            elmt_sum += matrix[i][j]
    
    return elmt_sum

def transposeMatrix(matrix):
    transposed_matrix = [[0 for j in range(len(matrix[0]))] for i in range(len(matrix))]

    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            transposed_matrix[i][j] = matrix[j][i]
    
    return np.array(transposed_matrix)

def symmetricMatrix(matrix):
    transposed_matrix = transposeMatrix(matrix)
    symmetric_matrix = np.add(matrix, transposed_matrix)
    
    return np.array(symmetric_matrix)

def normalizedMatrix(matrix):
    elmt_sum = elmtSumMatrix(matrix)
    normalized_matrix = [[0 for j in range(len(matrix[0]))] for i in range(len(matrix))]

    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            normalized_matrix[i][j] = matrix[i][j]/elmt_sum

    return np.array(normalized_matrix)

def grayscaleImg(imgFile):
    img = cv2.imread(imgFile)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    img_grayscale = np.round(0.299 * img_rgb[:, :, 0] + 0.587 * img_rgb[:, :, 1] + 0.114 * img_rgb[:, :, 2]).astype(np.uint8)
    
    return img_grayscale

def createGLCM0(img, distance=1):
    glcm = [[0 for j in range(256)] for i in range(256)]

    for i in range(len(img)):
        for j in range(len(img[0])-distance):
            glcm[img[i][j]][img[i][j+distance]] += 1
    
    return np.array(glcm)

def createGLCM90(img):
    glcm = [[0 for j in range(256)] for i in range(256)]

    for j in range(len(img[0])):
        for i in range(len(img)-1, 0, -1):
            glcm[img[i][j]][img[i-1][j]] += 1
    
    return np.array(glcm)

def createGLCM45(img):
    glcm = [[0 for j in range(256)] for i in range(256)]

    for i in range(1, len(img)):
        tempi = i
        j = 0
        while tempi > 0 and j < len(img[0])-1:
            glcm[img[tempi][j]][img[tempi-1][j+1]] += 1
            tempi -= 1
            j += 1
    
    for j in range(1, len(img[0])-1):
        tempj = j
        i = len(img)-1
        while tempj < len(img[0])-1 and i > 0:
            glcm[img[i][tempj]][img[i-1][tempj+1]] += 1
            i -= 1
            tempj += 1
    
    return np.array(glcm)

def createGLCM135(img):
    glcm = [[0 for j in range(256)] for i in range(256)]

    for i in range(1, len(img)):
        tempi = i
        j = len(img[0])-1
        while tempi > 0 and j > 0:
            glcm[img[tempi][j]][img[tempi-1][j-1]] += 1
            tempi -= 1
            j -= 1

    for j in range(len(img[0])-2, 0, -1):
        tempj = j
        i = len(img)-1
        while tempj > 0 and i > 0:
            glcm[img[i][tempj]][img[i-1][tempj-1]] += 1
            i -= 1
            tempj -= 1
    
    return np.array(glcm)

def energy(matrix):
    value = 0

    for i in range(256):
        for j in range(256):
            value += (matrix[i][j])**2
    
    return value**(0.5)

def dissimilarity(matrix):
    value = 0

    for i in range(256):
        for j in range(256):
            value += matrix[i][j]*abs(i-j)
    
    return value

def entropy(matrix):
    value = 0

    for i in range(256):
        for j in range(256):
            if matrix[i][j] != 0:
                value -= matrix[i][j]*(math.log(matrix[i][j]))
    
    return value

def contrast(matrix):
    value = 0

    for i in range(256):
        for j in range(256):
            value += matrix[i][j]*((i-j)**2)
    
    return value

def homogeneity(matrix):
    value = 0

    for i in range(256):
        for j in range(256):
            value += matrix[i][j]/(1+((i-j)**2))
    
    return value

def mui(matrix):
    value = 0

    for i in range(256):
        for j in range(256):
            value += i*matrix[i][j]
    
    return value

def muj(matrix):
    value = 0

    for i in range(256):
        for j in range(256):
            value += j*matrix[i][j]

    return value

def sigmai(matrix):
    value = 0
    meani = mui(matrix)

    for i in range(256):
        for j in range(256):
            value += matrix[i][j]*((i-meani)**2)
    
    return value**0.5

def sigmaj(matrix): #standard deviation
    value = 0
    meanj = muj(matrix)

    for i in range(256):
        for j in range(256):
            value += matrix[i][j]*((j-meanj)**2)
    
    return value**0.5

def correlation(matrix):
    value = 0
    meani = mui(matrix)
    meanj = muj(matrix)
    stdi = sigmai(matrix)
    stdj = sigmaj(matrix)

    for i in range(256):
        for j in range(256):
            if (((stdi**2)*(stdj**2))**0.5) != 0:
                value += matrix[i][j]*(((i-meani)*(j-meanj))/(((stdi**2)*(stdj**2))**0.5))

    return value

def textureBasedVector(matrix):
    vector = [0 for i in range(6)]
    vector[0] = contrast(matrix)
    vector[1] = homogeneity(matrix)
    vector[2] = entropy(matrix)
    vector[3] = energy(matrix)
    vector[4] = correlation(matrix)
    vector[5] = dissimilarity(matrix)
    
    return vector

def normalizedGLCM(glcm):
    normalized_glcm = symmetricMatrix(glcm)
    normalized_glcm = normalizedMatrix(normalized_glcm)

    return np.array(normalized_glcm)