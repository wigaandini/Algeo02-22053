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

def convertH(hVal):
    if(hVal >= 316 and hVal <= 360):
        return 0
    elif(hVal == 0):
        return 0
    elif(hVal >= 1 and hVal <= 25):
        return 1
    elif(hVal >= 26 and hVal <= 40):
        return 2
    elif(hVal >= 41 and hVal <= 120):
        return 3
    elif(hVal >= 121 and hVal <= 190):
        return 4
    elif(hVal >= 191 and hVal <= 270):
        return 5
    elif(hVal >= 271 and hVal <= 295):
        return 6
    elif(hVal <= 295 and hVal >= 315):
        return 7 

def convertS(sVal):
    if(sVal >= 0 and sVal < 0.2):
        return 0
    elif(sVal >= 0.2 and sVal < 0.7):
        return 1
    elif(sVal >= 0.7 and sVal <= 1):
        return 2
    
def convertV(vVal):
    if(vVal >= 0 and vVal < 0.2):
        return 0
    elif(vVal >= 0.2 and vVal < 0.7):
        return 1
    elif(vVal >= 0.7 and vVal <= 1):
        return 2

def getHSVBlock(img_rgb, nRowStart, nRowEnd, nColStart, nColEnd):
    countH = 0
    countS = 0
    countV = 0
    hVal = 0
    sVal = 0
    vVal = 0
    for col in range(nColStart, nColEnd - 1, 1):
        for row in range(nRowStart, nRowEnd - 1, 1):
            color = img_rgb[row,col]
            hVal += getH(color)
            countH += 1
            sVal += getS(color)
            countS += 1
            vVal += getColorMax(color)
            countV += 1
    hAvg = hVal/countH
    hConv = convertH(round(hAvg))
    # print(round(hAvg))
    sAvg = sVal/countS
    sConv = convertS(sAvg)
    # print(sAvg)
    vAvg = vVal/countV
    vConv = convertV(vAvg)
    # print(vAvg)
    return(str(hConv) + str(sConv) + str(vConv))