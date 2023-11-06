# import numpy
from pathlib import Path
import cv2
import numpy as np

def getImgPath(namaFile):
    path = Path().absolute()
    pathFile = str(path) + "\\test\\" + namaFile
    return pathFile

namaFile = input("Masukkan nama file (lengkap dengan type file, e.g : Opan.png): \n")

img = cv2.imread(getImgPath(namaFile))
# cv2.imshow('image', img) 
# cv2.waitKey(0) 
# cv2.destroyAllWindows() 

img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
# cv2.imshow('image', img_rgb) 
# cv2.waitKey(0) 
# cv2.destroyAllWindows() 

#You're free to do a resize or not, just for the example
cap = cv2.resize(img_rgb, (340,480))
max = cap[0,0]
min = cap[0,0]
for x in range (0,340,1):
    for y in range(0,480,1):
        color = cap[y,x]
        red = float(color[0]/255)
        green = float(color[1]/255)
        blue = float(color[2]/255)
        # if :
        #     max = color
        # if color.red < max.red and color.green < max.green and color.blue < max.blue:
        #     min = color
        # print(red)
        # print(green)
        # print(blue)
        # print(color)



# rgbImage = rand(3,3,3);
# maxVal = max(img_rgb,[],3)
# minVal = min(img_rgb,[],3)
# print(maxVal)
# print(minVal)
# color = image_rgb[255,255]

# img1 = cv2.imread(getImgPath(namaFile), cv2.IMREAD_UNCHANGED)
# b,g,r = (img1[300, 300])
# print (r)
# print (g)
# print (b)



# import cv2
# import numpy as np

# # Load the image
# image_path = 'path_to_your_image.jpg'  # Replace with the path to your image
# image = cv2.imread(image_path)

# # Convert the image to the HSV color space
# hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# # Define the lower and upper bounds for the red color in HSV
# lower_red = np.array([0, 50, 50])
# upper_red = np.array([10, 255, 255])

# # Create a mask to detect the red color
# mask = cv2.inRange(hsv_image, lower_red, upper_red)

# # Bitwise-AND mask and original image
# res = cv2.bitwise_and(image, image, mask=mask)

# # Display the original image and the result
# cv2.imshow('Original Image', image)
# cv2.imshow('Red Detection Result', res)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
