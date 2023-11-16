import numpy as np

def get_stacked_histograms(data1, data2, data3, bins=30):
    """
    Compute stacked histograms for three sets of data.

    Parameters:
    - data1, data2, data3 (array-like): The data for each histogram.
    - bins (int, optional): Number of bins in the histogram. Default is 30.

    Returns:
    - hist1, bin_edges1 (tuple): Histogram values and bin edges for data1.
    - hist2, bin_edges2 (tuple): Histogram values and bin edges for data2.
    - hist3, bin_edges3 (tuple): Histogram values and bin edges for data3.
    """
    hist1, bin_edges1 = np.histogram(data1, bins=bins)
    hist2, bin_edges2 = np.histogram(data2, bins=bins)
    hist3, bin_edges3 = np.histogram(data3, bins=bins)

    return (hist1, bin_edges1), (hist2, bin_edges2), (hist3, bin_edges3)

# Example usage:
# Replace data1, data2, and data3 with your own data
data1 = np.random.randn(1000)
data2 = np.random.randn(1000) + 3
data3 = np.random.randn(1000) - 3

histogram_values = get_stacked_histograms(data1, data2, data3)

# Access the histogram values and bin edges for each dataset
hist1, bin_edges1 = histogram_values[0]
hist2, bin_edges2 = histogram_values[1]
hist3, bin_edges3 = histogram_values[2]

print(f"Histogram 1 values: {hist1}")
print(f"Histogram 1 bin edges: {bin_edges1}")

print(f"Histogram 2 values: {hist2}")
print(f"Histogram 2 bin edges: {bin_edges2}")

print(f"Histogram 3 values: {hist3}")
print(f"Histogram 3 bin edges: {bin_edges3}")
# import cv2
# import numpy as np
# from pathlib import Path
# import matplotlib.pyplot as plt

# def cropInto16Blocks(image):
#     img_height, img_width = image.shape[:2]
#     block_height = img_height // 4
#     block_width = img_width // 4

#     blocks = []
#     for r in range(4):
#         for c in range(4):
#             block = image[r * block_height: (r + 1) * block_height, c * block_width: (c + 1) * block_width]
#             blocks.append(block)

#     return blocks

# def getImgPath(namaFile):
#     path = Path().absolute()
#     pathFile = str(path) + "\\test\\" + namaFile
#     return pathFile

# def cropImage(img):
#     height, width, _ = img.shape

#     # crop sampe dia habis dibagi 4 karena mau dibikin block 4x4
#     newHeight = height - height % 4
#     newWidth = width - width % 4
#     croppedImg = img[:newHeight, :newWidth]

#     return croppedImg


# # Example usage:
# # Replace 'your_image_path.jpg' with the path to your image
# file1 = input("Masukkan nama file 1 (lengkap dengan type file, e.g : Opan.png): \n")
# img1 = cv2.imread(getImgPath(file1))
# img1c = cropImage(img1)

# # Convert the image to RGB format (OpenCV reads images in BGR format)
# original_image_rgb = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)

# # Crop the image into 4x4 blocks
# blocks = cropInto16Blocks(original_image_rgb)

# # Display the original and cropped images
# fig, axes = plt.subplots(4, 4, figsize=(10, 10))

# axes[0, 0].imshow(original_image_rgb)
# axes[0, 0].set_title('Original Image')

# for r in range(4):
#     for c in range(4):
#         axes[r, c].imshow(blocks[r * 4 + c])
#         axes[r, c].set_title(f'Block {r * 4 + c + 1}')

# plt.show()



# # def create_frequency_vector(input_values, bins):
# #     frequency_dict = {key: 0 for key in bins}

# #     for value in input_values:
# #         frequency_dict[value] += 1

# #     frequency_vector = [frequency_dict[key] for key in bins]
# #     return frequency_vector

# # # Example usage
# # custom_bins = [0, 1, 2, 10, 11, 12, 20, 21, 22, 100, 101, 102, 110, 111, 112, 120, 121, 122, 200, 201, 202, 210, 211, 212, 220, 221, 222, 300, 301, 302, 310, 311, 312, 320, 321, 322, 400, 401, 402, 410, 411, 412, 420, 421, 422, 500, 501, 502, 510, 511, 512, 520, 521, 522, 600, 601, 602, 610, 611, 612, 620, 621, 622, 700, 701, 702, 710, 711, 712, 720, 721, 722]
# # input_values = [1, 0, 12, 12, 11, 722, 721, 722, 722, 501]
# # frequency_vector = create_frequency_vector(input_values, custom_bins)
# # print(frequency_vector)

import cv2  # Assuming you have OpenCV installed

def load_image_with_path(file_path):
    image = cv2.imread(file_path)
    return {'path': file_path, 'image': image}

# Example usage:
image_data = load_image_with_path("path/to/your/image.jpg")
print("File Path:", image_data['path'])
print("Image