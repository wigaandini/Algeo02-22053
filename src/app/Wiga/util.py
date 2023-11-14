import numpy as np
import matplotlib.pyplot as plt

def dotProductVector(vector1, vector2):
    vector1 = np.array(vector1)
    vector2 = np.array(vector2)
    value = np.sum(vector1.astype(float) * vector2.astype(float))
    return value

def vectorLength(vector):
    if isinstance(vector, list):
        vector = np.array(vector)
    value = np.sum(vector.astype(float)**2)
    return np.sqrt(value)

def cosineSimilarity(vector_img1, vector_img2):
    if(vectorLength(vector_img1) != 0 and vectorLength(vector_img2) != 0):
        return (dotProductVector(vector_img1, vector_img2)/(vectorLength(vector_img1)*vectorLength(vector_img2))) * 100
    else :
        return 0