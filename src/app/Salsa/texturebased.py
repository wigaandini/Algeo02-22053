import cv2
import math

def isElmtList(list, elmt):
    for i in range(len(list)):
        if list[i] == elmt:
            return True
    
    return False

def sortList(list):
    swap = True
    while swap:
        swap = False
        for i in range(len(list)-1):
            if list[i] > list[i+1]:
                list[i], list[i+1] = list[i+1], list[i]
                swap = True

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
    
    return transposed_matrix

def symmetricMatrix(matrix):
    transposed_matrix = transposeMatrix(matrix)
    symmetric_matrix = [[0 for j in range(len(matrix[0]))] for i in range(len(matrix))]
    
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            symmetric_matrix[i][j] = matrix[i][j] + transposed_matrix[i][j]
    
    return symmetric_matrix

def normalizedMatrix(matrix):
    elmt_sum = elmtSumMatrix(matrix)
    normalized_matrix = [[0 for j in range(len(matrix[0]))] for i in range(len(matrix))]

    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            normalized_matrix[i][j] = matrix[i][j]/elmt_sum

    return normalized_matrix

# Untuk input 1 file image
def grayscaleImg(imgFile):
    img = cv2.imread(imgFile)
    
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_grayscale = [[0 for j in range(len(img[0]))] for i in range(len(img))]
    for i in range(len(img)):
        for j in range(len(img[0])):
            rgb_value = img_rgb[i][j]
            img_grayscale[i][j] = round(0.29*rgb_value[0] + 0.587*rgb_value[1] + 0.114*rgb_value[2])
    
    return img_grayscale

# def createGLCM0(img):
#     gray_tone = []

#     for i in range(len(img)):
#         for j in range(len(img[0])):
#             if not isElmtList(gray_tone, img[i][j]):
#                 gray_tone.append(img[i][j])
    
#     glcm = [[0 for j in range(len(gray_tone))] for i in range(len(gray_tone))]

#     sortList(gray_tone)
#     gray_tone_dictionary = {gray_tone[i] : i for i in range(len(gray_tone))}

#     for i in range(len(img)):
#         for j in range(len(img)-1):
#             glcm[gray_tone_dictionary[img[i][j]]][gray_tone_dictionary[img[i][j+1]]] += 1
    
#     return glcm

def getGrayTone(img):
    gray_tone = []

    for i in range(len(img)):
        for j in range(len(img[0])):
            if not isElmtList(gray_tone, img[i][j]):
                gray_tone.append(img[i][j])
    
    glcm = [[0 for j in range(len(gray_tone))] for i in range(len(gray_tone))]

    sortList(gray_tone)
    gray_tone_dictionary = {gray_tone[i] : i for i in range(len(gray_tone))}

    return gray_tone_dictionary

def createGLCM0(img, gray_tone_dictionary, distance=1):
    glcm = [[0 for j in range(len(gray_tone_dictionary))] for i in range(len(gray_tone_dictionary))]

    for i in range(len(img)):
        for j in range(len(img)-distance):
            glcm[gray_tone_dictionary[img[i][j]]][gray_tone_dictionary[img[i][j+distance]]] += 1
    
    return glcm

def createGLCM90(img, gray_tone_dictionary):
    glcm = [[0 for j in range(len(gray_tone_dictionary))] for i in range(len(gray_tone_dictionary))]

    for j in range(len(img)):
        for i in range(len(img)-1, 0, -1):
            glcm[gray_tone_dictionary[img[i][j]]][gray_tone_dictionary[img[i-1][j]]] += 1
    
    return glcm

def createGLCM45(img, gray_tone_dictionary):
    glcm = [[0 for j in range(len(gray_tone_dictionary))] for i in range(len(gray_tone_dictionary))]

    for i in range(1, len(img)):
        tempi = i
        j = 0
        while tempi > 0:
            glcm[gray_tone_dictionary[img[tempi][j]]][gray_tone_dictionary[img[tempi-1][j+1]]] += 1
            tempi -= 1
            j += 1
    
    for j in range(1, len(img)-1):
        tempj = j
        i = len(img)-1
        while tempj < len(img)-1:
            glcm[gray_tone_dictionary[img[i][tempj]]][gray_tone_dictionary[img[i-1][tempj+1]]] += 1
            i -= 1
            tempj += 1
    
    return glcm

def createGLCM135(img, gray_tone_dictionary):
    glcm = [[0 for j in range(len(gray_tone_dictionary))] for i in range(len(gray_tone_dictionary))]

    for i in range(1, len(img)):
        tempi = i
        j = len(img)-1
        while tempi > 0:
            glcm[gray_tone_dictionary[img[tempi][j]]][gray_tone_dictionary[img[tempi-1][j-1]]] += 1
            tempi -= 1
            j -= 1
    
    for j in range(len(img)-2, 0, -1):
        tempj = j
        i = len(img)-1
        while tempj > 0:
            glcm[gray_tone_dictionary[img[i][tempj]]][gray_tone_dictionary[img[i-1][tempj-1]]] += 1
            i -= 1
            tempj -= 1
    
    return glcm

def energy(matrix):
    value = 0

    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            value += (matrix[i][j])**2
    
    return value**(0.5)

def dissimilarity(matrix):
    value = 0

    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            value += matrix[i][j]*abs(i-j)
    
    return value

def entropy(matrix):
    value = 0

    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] != 0:
                value += matrix[i][j]*(math.log10(matrix[i][j]))
    
    return value*(-1)

def contrast(matrix):
    value = 0

    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            value += matrix[i][j]*((i-j)**2)
    
    return value

def homogeneity(matrix):
    value = 0

    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            value += matrix[i][j]/(1+((i-j)**2))
    
    return value

def mui(matrix):
    value = 0

    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            value += i*matrix[i][j]
    
    return value

def muj(matrix):
    value = 0

    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            value += j*matrix[i][j]

    return value

def sigmai(matrix):
    value = 0
    meani = mui(matrix)

    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            value += matrix[i][j]*((i-meani)**2)
    
    return value**0.5

def sigmaj(matrix): #standard deviation
    value = 0
    meanj = muj(matrix)

    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            value += matrix[i][j]*((j-meanj)**2)
    
    return value**0.5

def correlation(matrix):
    value = 0
    meani = mui(matrix)
    meanj = muj(matrix)
    stdi = sigmai(matrix)
    stdj = sigmaj(matrix)

    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
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

    return normalized_glcm