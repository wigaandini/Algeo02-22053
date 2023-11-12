from  colorbased import *
import matplotlib.pyplot as plt
from util import *

# namaFile = input("Masukkan nama file (lengkap dengan type file, e.g : Opan.png): \n")

# img = cv2.imread(getImgPath(namaFile))
# # cv2.imshow('image', img) 
# # cv2.waitKey(0) 
# # cv2.destroyAllWindows() 
# # plt.imshow(img)
# # plt.show()
# # print(img)

# img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
# cv2.imshow('image', img) 
# cv2.waitKey(0) 
# cv2.destroyAllWindows() 
# plt.imshow(img)
# plt.show()
# print(img_rgb)
# print("\n")

#You're free to do a resize or not, just for the example
# img_shape = img_rgb.shape
# print(img_shape)
# print(len(img_rgb[0]), "\n")
# print(len(img_rgb),"\n")
# cap = cv2.resize(img_rgb, (256,256))
# # print(cap)

# for col in range(0, (nCol/3) + 1, 1):
#     for row in range(nRow):
#         color = img_rgb[row,col]
#         # red = float(color[0]/255)
#         # green = float(color[1]/255)
#         # blue = float(color[2]/255)
#         hVal = getH(color)
#         print("H = ", hVal)
#         sVal = getS(color)
#         print("S = ", sVal)
#         vVal = getColorMax(color)
#         print("V = ", vVal)

# for i in range(8):
#     for j in range(3):
#         for k in range(3):
#             print(str(i) + str(j) + str(k))


        # if :
        #     max = color
        # if color.red < max.red and color.green < max.green and color.blue < max.blue:
        #     min = color
        # print(red)
        # print(green)
        # print(blue)
        # print(color)

# max_channels = np.amax([np.amax(img[:,:,0]), np.amax(img[:,:,1]), np.amax(img[:,:,2])])
# print(max_channels)



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
from PIL import Image, ImageTk
import tkinter as tk
file1 = input("Masukkan nama file 1 (lengkap dengan type file, e.g : Opan.png): \n")
file2 = input("Masukkan nama file 2 (lengkap dengan type file, e.g : Opan.png): \n")
# img1 = cv2.imread(getImgPath(file1))
# plt.imshow(img1)
# plt.show()
# # img1rgb = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB) 
# img2 = cv2.imread(getImgPath(file2))
# plt.imshow(img2)
# plt.show()

img1 = Image.open(getImgPath(file1))
img2 = Image.open(getImgPath(file2))
im_matrix1 = np.array(img1)
im_matrix2 = np.array(img2)
# print(im_matrix1)
print(len(im_matrix1))
print(len(im_matrix1[0]))
# root = tk.Tk()
# # img = Image.open("image.gif")
# tkimage = ImageTk.PhotoImage(im)
# tk.Label(root, image=tkimage).pack()
# root.mainloop()
# h1 = getHBlock(im_matrix1, 0, 624, 0, 538)
# print(h1)

# img2rgb = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB) 
hsv1 = getVector(im_matrix1)
print(hsv1)
hsv2 = getVector(im_matrix2)
print(hsv2)
# print(cosineSimilarity(hsv1[0], hsv2[0]))
# print(cosineSimilarity(hsv1[1], hsv2[1]))
# print(cosineSimilarity(hsv1[2], hsv2[2]))
# print(cosineSimilarity(hsv1[3], hsv2[3]))
# print(cosineSimilarity(hsv1[4], hsv2[4]))
# print(cosineSimilarity(hsv1[5], hsv2[5]))
# print(cosineSimilarity(hsv1[6], hsv2[6]))
# print(cosineSimilarity(hsv1[7], hsv2[7]))
# print(cosineSimilarity(hsv1[8], hsv2[8]))
# # print(compare)
print(avgCS(hsv1,hsv2))
# print(euclideanDistance(hsv1, hsv2))

# import numpy as np

# # Assuming you have two image arrays img1 and img2
# # Calculate the Euclidean distance
# # distance = euclideanDistance(hsv1, hsv2)
# distance = np.linalg.norm(img2 - img1)
# print(distance)

# # Define a threshold to determine the similarity percentage
# threshold = 100  # Adjust this value based on your needs

# # Calculate the similarity percentage
# similarity_percentage = 100 - (distance / threshold) * 100
# if similarity_percentage < 0:
#     similarity_percentage = 0

# print(f"The similarity percentage between the images is: {similarity_percentage}%")


# import cv2
# import numpy as np

# # Load the images
# # img1 = cv2.imread('path_to_image_1.jpg')
# # img2 = cv2.imread('path_to_image_2.jpg')

# # Resize the images to have the same dimensions for comparison
# img1 = cv2.resize(img1, (300, 300))
# img2 = cv2.resize(img2, (300, 300))

# # Convert images to the LAB color space
# img1_lab = cv2.cvtColor(img1, cv2.COLOR_BGR2LAB)
# img2_lab = cv2.cvtColor(img2, cv2.COLOR_BGR2LAB)

# # Calculate the Mean Squared Error (MSE) between the two images
# mse = np.mean((img1_lab - img2_lab) ** 2)

# # Define a threshold value based on your requirements
# threshold = 100  # Adjust this value as needed

# # Check color similarity based on the MSE value
# if mse < threshold:
#     print("The images are similar in terms of color.")
# else:
#     print("The images are not similar in terms of color.")

# # Display the Mean Squared Error value
# print(f"The Mean Squared Error (MSE) between the images is: {mse}")