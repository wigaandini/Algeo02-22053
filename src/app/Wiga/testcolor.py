from  colorbased import *

namaFile = input("Masukkan nama file (lengkap dengan type file, e.g : Opan.png): \n")

img = cv2.imread(getImgPath(namaFile))
# cv2.imshow('image', img) 
# cv2.waitKey(0) 
# cv2.destroyAllWindows() 

img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
# cv2.imshow('image', img_rgb) 
# cv2.waitKey(0) 
# cv2.destroyAllWindows() 
# print(img_rgb)
# print("\n")

#You're free to do a resize or not, just for the example
# img_shape = img_rgb.shape
# print(img_shape)
# print(len(img_rgb[0]), "\n")
# print(len(img_rgb),"\n")
# cap = cv2.resize(img_rgb, (256,256))
# # print(cap)

if(len(img_rgb[0] % 3 != 0)):
    nCol = ((len(img_rgb[0]))//3) * 3
if(len(img_rgb) % 3 != 0):
    nRow = ((len(img_rgb))//3) * 3

check = 0
startRow = 0
endRow = (nRow//3) - 1
startCol = 0
endCol = (nCol//3) - 1 

print(len(img_rgb))
print(len(img_rgb[0]))
print(nRow)
print(nCol)

# getHSVBlock(img_rgb, 98, 195, 0, 157)

# res = getHSVBlock(img_rgb, startRow, endRow, startCol, endCol)
# print(res)

hsv = ["" for check in range(9)]

while(check < 9):
    while(endRow < nRow):
        while(endCol < nCol):
            hsv[check] = getHSVBlock(img_rgb, startRow, endRow, startCol, endCol)
            # print(startRow, endRow)
            # print(startCol, endCol)
            # print(check)
            # print(hsv)
            check += 1
            startCol += (nCol//3)
            endCol = startCol + (nCol//3) - 1 
        startRow += (nRow//3)
        endRow = startRow + (nRow//3) - 1 
        startCol= 0
        endCol = (nCol//3) - 1
    #     print(startRow, endRow)
    #     print(startCol, endCol)
    #     print(check)
    #     print(hsv)
    # print(startRow, endRow)
    # print(startCol, endCol)
    # print(check)
    # print(hsv)

# print(hsv)

blockNumber = [1, 2, 3, 4, 5, 6, 7, 8, 9]
tupleHSV = list(zip(blockNumber, hsv))
print(tupleHSV)


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
