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

def euclideanDistance(vector1, vector2):
    sum = 0
    for i in range(len(vector2)):
        sum += ((float(vector1[i]) - float(vector2[i])) ** 2)
    return sum

def avgCS(vector1, vector2):
    sum = 0
    for i in range(len(vector1)):
        sum += cosineSimilarity(vector1[i], vector2[i])
    print(sum)
    return sum/len(vector1)