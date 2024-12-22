import os

def rename_images_and_labels(folder_path):
    # Get the list of all files in the specified folder
    files = os.listdir(folder_path)
    
    # Filter images based on their extensions
    image_extensions = ['.jpg', '.jpeg', '.png']  # Supported image formats
    images = [f for f in files if os.path.splitext(f)[1].lower() in image_extensions]
    
    # Filter label files (assumed to be .txt files)
    labels = [f for f in files if f.endswith('.txt')]

    # Sort the image and label files to maintain order
    images.sort()
    labels.sort()

    # Loop through the images and rename them sequentially
    for idx, image_name in enumerate(images, start=1):
        new_name = f"{idx:06d}"  # Generate a zero-padded name (e.g., 000001)
        image_extension = os.path.splitext(image_name)[1]  # Get the file extension
        new_image_name = new_name + image_extension  # Construct the new image name

        # Rename the image file
        os.rename(
            os.path.join(folder_path, image_name),
            os.path.join(folder_path, new_image_name)
        )

        # Check if a corresponding label file exists
        label_name = os.path.splitext(image_name)[0] + ".txt"  # Derive the label name
        if label_name in labels:
            new_label_name = new_name + ".txt"  # Generate the new label name
            # Rename the label file
            os.rename(
                os.path.join(folder_path, label_name),
                os.path.join(folder_path, new_label_name)
            )
    
    # Print a success message once renaming is complete
    print("All images and labels have been successfully renamed.")

# Specify the folder containing images and label files
folder_path = "path/to/your/folder"  # Replace with your folder path
rename_images_and_labels(folder_path)
