# import numpy
from pathlib import Path
import cv2
import numpy as np

def getImgPath(namaFile):
    path = Path().absolute()
    pathFile = str(path) + "\\test\\" + namaFile
    return pathFile

def getColorMax(arr):
    red = float(arr[2]/255)
    green = float(arr[1]/255)
    blue = float(arr[0]/255)
    Cmax = red
    if (green > Cmax):
        Cmax = green
    elif (blue > Cmax): 
        Cmax = blue
    return Cmax

def getColorMin(arr):
    red = float(arr[2]/255)
    green = float(arr[1]/255)
    blue = float(arr[0]/255)
    Cmin = red
    if (green < Cmin):
        Cmin = green
    elif (blue < Cmin): 
        Cmin = blue
    return Cmin

def getColorMaxType(arr):
    red = float(arr[2]/255)
    green = float(arr[1]/255)
    blue = float(arr[0]/255)
    if(red >= green and red >= blue):
        return "red"
    elif(green >= red and green >= blue):
        return "green"
    else:
        return "blue"

def getColorMinType(arr):
    red = float(arr[2]/255)
    green = float(arr[1]/255)
    blue = float(arr[0]/255)
    if(red < green and red < blue):
        return "red"
    elif(green < red and green < blue):
        return "green"
    else:
        return "blue"

def getDelta(Cmin, Cmax):
    return Cmax - Cmin

def getH(arr):
    red = float(arr[2]/255)
    green = float(arr[1]/255)
    blue = float(arr[0]/255)
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
    elif(hVal >= 295 and hVal <= 315):
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

# def getHSVBlock(img_rgb, nRowStart, nRowEnd, nColStart, nColEnd):
#     countH = 0
#     countS = 0
#     countV = 0
#     hVal = 0
#     sVal = 0
#     vVal = 0
#     for col in range(nColStart, nColEnd - 1, 1):
#         for row in range(nRowStart, nRowEnd - 1, 1):
#             color = img_rgb[row,col]
#             h = getH(color)
#             hConv = convertH(round(h))
#             s = getS(color)
#             sConv = convertS(s)
#             v = getColorMax(color)
#             vConv = convertV(v)
#             hVal += hConv
#             countH += 1
#             sVal += sConv
#             countS += 1
#             vVal += vConv
#             countV += 1
#     hAvg = hVal/countH
#     # hConv = (round(hAvg))
#     # print(round(hAvg))
#     sAvg = sVal/countS
#     # sConv = convertS(sAvg)
#     # print(sAvg)
#     vAvg = vVal/countV
#     # vConv = convertV(vAvg)
#     # print(vAvg)
#     return(str(hAvg) + str(sAvg) + str(vAvg))

# def getVector(img_rgb):
#     if(len(img_rgb[0] % 3 != 0)):
#         nCol = ((len(img_rgb[0]))//3) * 3
#     if(len(img_rgb) % 3 != 0):
#         nRow = ((len(img_rgb))//3) * 3

#     check = 0
#     startRow = 0
#     endRow = (nRow//3) - 1
#     startCol = 0
#     endCol = (nCol//3) - 1 

#     # print(len(img_rgb))
#     # print(len(img_rgb[0]))
#     # print(nRow)
#     # print(nCol)

#     # getHSVBlock(img_rgb, 98, 195, 0, 157)

#     # res = getHSVBlock(img_rgb, startRow, endRow, startCol, endCol)
#     # print(res)

#     hsv = ["" for check in range(9)]

#     while(check < 9):
#         while(endRow < nRow):
#             while(endCol < nCol):
#                 hsv[check] = getHSVBlock(img_rgb, startRow, endRow, startCol, endCol)
#                 # print(startRow, endRow)
#                 # print(startCol, endCol)
#                 # print(check)
#                 # print(hsv)
#                 check += 1
#                 startCol += (nCol//3)
#                 endCol = startCol + (nCol//3) - 1 
#             startRow += (nRow//3)
#             endRow = startRow + (nRow//3) - 1 
#             startCol= 0
#             endCol = (nCol//3) - 1
#         #     print(startRow, endRow)
#         #     print(startCol, endCol)
#         #     print(check)
#         #     print(hsv)
#         # print(startRow, endRow)
#         # print(startCol, endCol)
#         # print(check)
#         # print(hsv)

#     # print(hsv)

#     # blockNumber = [1, 2, 3, 4, 5, 6, 7, 8, 9]
#     # tupleHSV = list(zip(blockNumber, hsv))
#     # print(tupleHSV)
#     return hsv

def getHSVBlock(img_rgb, nRowStart, nRowEnd, nColStart, nColEnd):
    countH = 0
    countS = 0
    countV = 0
    hVal = 0
    sVal = 0
    vVal = 0
    for col in range(nColStart, nColEnd, 1):
        for row in range(nRowStart, nRowEnd, 1):
            color = img_rgb[row,col]
            h = getH(color)
            hRound = round(h)
            hConv = convertH(hRound)
            hVal += hConv
            countH += 1
            s = getS(color)
            sConv = convertS(s)
            sVal += sConv
            countS += 1
            v = getColorMax(color)
            vConv = convertV(v)
            vVal += vConv
            countV += 1
    hAvg = hVal/countH
    sAvg = sVal/countS
    vAvg = vVal/countV
    return(hAvg, sAvg, vAvg)

# def getSBlock(img_rgb, nRowStart, nRowEnd, nColStart, nColEnd):
#     countS = 0
#     sVal = 0
#     for col in range(nColStart, nColEnd, 1):
#         for row in range(nRowStart, nRowEnd, 1):
#             color = img_rgb[row,col]
#             s = getS(color)
#             sConv = convertS(s)
#             sVal += sConv
#             countS += 1
#     sAvg = sVal/countS
#     return(sAvg)

# def getVBlock(img_rgb, nRowStart, nRowEnd, nColStart, nColEnd):
#     countV = 0
#     vVal = 0
#     for col in range(nColStart, nColEnd, 1):
#         for row in range(nRowStart, nRowEnd, 1):
#             color = img_rgb[row,col]
#             v = getColorMax(color)
#             vConv = convertV(v)
#             vVal += vConv
#             countV += 1
#     vAvg = vVal/countV
#     return(vAvg)

# def getVectorHSV(img_rgb, nRowStart, nRowEnd, nColStart, nColEnd):
#     h, s, v = getHSVBlock(img_rgb, nRowStart, nRowEnd, nColStart, nColEnd)
#     return (str(h) + str(s) + str(v))

def getVector(img_rgb):
    nCol = len(img_rgb[0]) // 3 * 3
    nRow = len(img_rgb) // 3 * 3

    nRowDiv3 = nRow // 3
    nColDiv3 = nCol // 3

    check = 0
    startRow = 0
    endRow = nRowDiv3 - 1
    startCol = 0
    endCol = nColDiv3 - 1 

    hsv = np.zeros((9, 3), dtype=int)

    while check < 9:
        while endRow < nRow:
            while endCol < nCol:
                for i in range(3):
                    hsv[check][0], hsv[check][1], hsv[check][2] = getHSVBlock(img_rgb, startRow, endRow, startCol, endCol)
                check += 1
                startCol += nColDiv3
                endCol = startCol + nColDiv3 - 1 
            startRow += nRowDiv3
            endRow = startRow + nRowDiv3 - 1 
            startCol = 0
            endCol = nColDiv3 - 1

    return hsv