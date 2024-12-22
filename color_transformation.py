import cv2  # OpenCV for image processing
import os   # To handle file paths

# Define input and output directories
input_dir = 'path_to_dataset'  # Replace with your dataset path
output_dir = 'path_to_save_transformed_images'  # Replace with your output path
os.makedirs(output_dir, exist_ok=True)  # Create output directory if not exists

# Function to apply grayscale transformation
def apply_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convert image to grayscale

# Function to apply sepia transformation
def apply_sepia(image):
    # Sepia filter transformation matrix
    sepia_filter = cv2.transform(image, 
        cv2.Mat([[0.272, 0.534, 0.131],
                 [0.349, 0.686, 0.168],
                 [0.393, 0.769, 0.189]]))
    return sepia_filter

# Loop through all images in the input directory
for filename in os.listdir(input_dir):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):  # Check for valid image files
        filepath = os.path.join(input_dir, filename)  # Full path to the image
        image = cv2.imread(filepath)  # Read the image
        if image is None:  # Skip if the image can't be read
            continue
        
        # Apply grayscale transformation
        transformed_image = apply_grayscale(image)
        # OR apply sepia transformation:
        # transformed_image = apply_sepia(image)
        
        save_path = os.path.join(output_dir, filename)  # Save path for the transformed image
        cv2.imwrite(save_path, transformed_image)  # Save the transformed image
