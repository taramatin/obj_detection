import cv2  # OpenCV for image processing
import os   # To handle file paths

# Define input and output directories
input_dir = 'path_to_dataset'  # Replace with your dataset folder path
output_dir = 'path_to_save_transformed_images'  # Replace with your output folder path

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Function to crop an image to a specific size
def crop_image(image, crop_width, crop_height):
    height, width = image.shape[:2]  # Get the original dimensions
    start_x = max((width - crop_width) // 2, 0)  # Calculate x starting point (centered)
    start_y = max((height - crop_height) // 2, 0)  # Calculate y starting point (centered)
    end_x = start_x + crop_width
    end_y = start_y + crop_height
    return image[start_y:end_y, start_x:end_x]  # Crop the image

# Define different crop sizes (width, height)
crop_sizes = [
    (300, 300),  # Example 1: 300x300
    (500, 500),  # Example 2: 500x500
    (100, 200)   # Example 3: 100x200 (custom aspect ratio)
]

# Loop through all images in the input directory
for filename in os.listdir(input_dir):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):  # Check for valid image files
        filepath = os.path.join(input_dir, filename)  # Get the full file path
        image = cv2.imread(filepath)  # Read the image
        if image is None:  # Skip if the image can't be read
            print(f"Skipping invalid image: {filename}")
            continue

        for crop_width, crop_height in crop_sizes:  # Loop through each crop size
            # Skip if the crop size is larger than the image size
            if crop_width > image.shape[1] or crop_height > image.shape[0]:
                print(f"Skipping crop size {crop_width}x{crop_height} for {filename} (too large)")
                continue

            cropped_image = crop_image(image, crop_width, crop_height)  # Crop the image
            # Save with a unique name based on the crop size
            save_name = f"{os.path.splitext(filename)[0]}_{crop_width}x{crop_height}{os.path.splitext(filename)[1]}"
            save_path = os.path.join(output_dir, save_name)
            cv2.imwrite(save_path, cropped_image)  # Save the cropped image
            print(f"Saved: {save_path}")
