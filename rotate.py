import cv2  # OpenCV for image processing
import os   # To handle file paths

# Define input and output directories
input_dir = 'path_to_images'  # Replace with the folder containing your images
output_dir = 'path_to_save_transformed_images'  # Replace with the folder to save rotated images

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Function to rotate an image by a given angle
def rotate_image(image, angle):
    (h, w) = image.shape[:2]  # Get image dimensions
    center = (w // 2, h // 2)  # Compute the center of the image
    matrix = cv2.getRotationMatrix2D(center, angle, 1.0)  # Generate the rotation matrix
    return cv2.warpAffine(image, matrix, (w, h))  # Perform the rotation

# Loop through all images in the input directory
for filename in os.listdir(input_dir):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):  # Check for image files
        filepath = os.path.join(input_dir, filename)  # Get the full file path
        image = cv2.imread(filepath)  # Read the image
        if image is None:  # Skip if the image can't be read
            continue
        rotated_image = rotate_image(image, 30)  # Rotate the image (e.g., 90 degrees)
        save_path = os.path.join(output_dir, filename)  # Define the save path
        cv2.imwrite(save_path, rotated_image)  # Save the rotated image
