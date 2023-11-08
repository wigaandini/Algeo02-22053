# from colorbased import *
# import numpy
from pathlib import Path
import cv2
import numpy as np

def getImgPath(namaFile):
    path = Path().absolute()
    pathFile = str(path) + "\\test\\" + namaFile
    return pathFile

def getColorMax(arr):
    red = float(arr[0]/255)
    green = float(arr[1]/255)
    blue = float(arr[2]/255)
    Cmax = red
    if (green > Cmax):
        Cmax = green
    elif (blue > Cmax): 
        Cmax = blue
    return Cmax

def getColorMin(arr):
    red = float(arr[0]/255)
    green = float(arr[1]/255)
    blue = float(arr[2]/255)
    Cmin = red
    if (green < Cmin):
        Cmin = green
    elif (blue < Cmin): 
        Cmin = blue
    return Cmin

def getColorMaxType(arr):
    red = float(arr[0]/255)
    green = float(arr[1]/255)
    blue = float(arr[2]/255)
    if(red >= green and red >= blue):
        return "red"
    elif(green >= red and green >= blue):
        return "green"
    else:
        return "blue"

def getColorMinType(arr):
    red = float(arr[0]/255)
    green = float(arr[1]/255)
    blue = float(arr[2]/255)
    if(red < green and red < blue):
        return "red"
    elif(green < red and green < blue):
        return "green"
    else:
        return "blue"

def getDelta(Cmin, Cmax):
    return Cmax - Cmin

def getH(arr):
    red = float(arr[0]/255)
    green = float(arr[1]/255)
    blue = float(arr[2]/255)
    maxType = getColorMaxType(arr)
    Cmax = getColorMax(arr)
    Cmin = getColorMin(arr)
    delta = getDelta(Cmin, Cmax)
    if(delta == 0):
        h = 0
    elif(maxType == "red"):
        h = 60 * (((green - blue)/delta) % 6)
    elif(maxType == "green"):
        h = 60 * (((blue - red)/delta) + 2)
    elif(maxType == "blue"):
        h = 60 * (((red - green)/delta) + 4)
    return h

def getS(arr):
    Cmax = getColorMax(arr)
    Cmin = getColorMin(arr)
    delta = getDelta(Cmin, Cmax)
    if(Cmax == 0):
        s = 0
    else:
        s = delta/Cmax
    return s

namaFile = input("Masukkan nama file (lengkap dengan type file, e.g : Opan.png): \n")

img = cv2.imread(getImgPath(namaFile))
# cv2.imshow('image', img) 
# cv2.waitKey(0) 
# cv2.destroyAllWindows() 

img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
# print(len(cap[0]))
# print(len(cap))

if(len(img_rgb[0] % 3 != 0)):
    nCol = len(img_rgb[0])/3
if(len(img_rgb) % 3 != 0):
    nRow = len(img_rgb)/3

endRow = int(nRow/3) - 1
# startCol = 0
endCol = int(nCol/3) - 1 

for col in range(endCol):
    for row in range(endRow):
        color = img_rgb[row,col]
        print(color)
        # red = float(color[0]/255)
        # green = float(color[1]/255)
        # blue = float(color[2]/255)
        hVal = getH(color)
        # print("H = ", hVal)
        sVal = getS(color)
        # print("S = ", sVal)
        vVal = getColorMax(color)
        print(hVal, sVal, vVal)