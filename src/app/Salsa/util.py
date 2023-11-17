def vectorLength(vector):
    value = 0

    for i in range(len(vector)):
        value += (vector[i])**2
    
    return value**(0.5)

def dotProductVector(vector1, vector2):
    value = 0

    for i in range(len(vector1)):
        value += vector1[i]*vector2[i]
    
    return value

def cosineSimilarity(vector_img1, vector_img2):
    return dotProductVector(vector_img1, vector_img2)/(vectorLength(vector_img1)*vectorLength(vector_img2))