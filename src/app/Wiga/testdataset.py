import cv2
import os

def read_images_from_dataset(dataset_path):
    """
    Read images from a dataset and display them using OpenCV.

    Parameters:
    - dataset_path (str): The path to the dataset containing image files.

    Returns:
    - None
    """
    # Check if the dataset path exists
    if not os.path.exists(dataset_path):
        print(f"Error: The dataset path '{dataset_path}' does not exist.")
        return

    # List all files in the dataset path
    image_files = [f for f in os.listdir(dataset_path) if f.endswith(('.jpg', '.jpeg', '.png'))]

    # Loop through each image file
    for image_file in image_files:
        # Construct the full path to the image
        image_path = os.path.join(dataset_path, image_file)

        # Read the image using OpenCV
        img = cv2.imread(image_path)

        # Check if the image was successfully loaded
        if img is not None:
            # Display or process the image as needed
            cv2.imshow('Image', img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            print(f"Error: Unable to read image '{image_path}'")

# Example usage:
dataset_path = 'D:\ITB\SEM 3\Algeo\Tugas Besar\Tubes 2\Algeo02-22053\test\Dataset'
read_images_from_dataset(dataset_path)
