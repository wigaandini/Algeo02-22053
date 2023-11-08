import cv2

# Untuk input 1 file image
def grayscaleImg(imgFile):
    img = cv2.imread(imgFile)
    img_shape = img.shape

    if img_shape[0] != 256:
        img = cv2.resize(img,(256, 256))
    
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_grayscale = [[0 for j in range(256)] for i in range(256)]
    for i in range(256):
        for j in range(256):
            rgb_value = img_rgb[i][j]
            img_grayscale[i][j] = 0.29*rgb_value[0] + 0.587*rgb_value[1] + 0.114*rgb_value[2]
    
    return img_grayscale