import numpy as np
from numpy import dot
from numpy.linalg import norm
from testcolor import *

vector1 = np.array([4.0, 1.0, 1.6456548795665862])
vector2 = np.array([3.4035172659309363, 1.99374866500534, 1.591812032751869])

cosine_similarity = dot(vector1, vector2) / (norm(vector1) * norm(vector2))
# print(cosine_similarity)

h2 = np.array(hsv2)
# print(h2)