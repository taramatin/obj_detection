import os
import random
import shutil

def split_dataset(folder_path):
    # Verify the folder path
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"The folder path {folder_path} does not exist.")

    print("Folder Path:", folder_path)
    print("Files in Folder:", os.listdir(folder_path))

    # Create train and valid folders with subfolders for images and labels
    os.makedirs(os.path.join(folder_path, "train/images"), exist_ok=True)
    os.makedirs(os.path.join(folder_path, "train/labels"), exist_ok=True)
    os.makedirs(os.path.join(folder_path, "valid/images"), exist_ok=True)
    os.makedirs(os.path.join(folder_path, "valid/labels"), exist_ok=True)

    # Define supported image extensions
    image_extensions = ['.jpg', '.jpeg', '.png']
    
    # List all image files in the folder
    images = [f for f in os.listdir(folder_path) if os.path.splitext(f)[1].lower() in image_extensions]
    
    # List all label files in the folder
    labels = [f for f in os.listdir(folder_path) if f.endswith('.txt')]

    print("Found Images:", images)
    print("Found Labels:", labels)

    # Pair images and labels (only if corresponding label exists)
    paired_files = [
        (image, os.path.splitext(image)[0] + ".txt") 
        for image in images 
        if os.path.splitext(image)[0] + ".txt" in labels
    ]
    
    # Shuffle the paired files randomly
    random.shuffle(paired_files)

    # Split the data into 80% train and 20% validation
    split_index = int(len(paired_files) * 0.8)  # 80% for training
    train_files = paired_files[:split_index]
    valid_files = paired_files[split_index:]

    # Move training files to the train folder
    for image, label in train_files:
        shutil.move(
            os.path.join(folder_path, image), 
            os.path.join(folder_path, "train/images", image)
        )
        shutil.move(
            os.path.join(folder_path, label), 
            os.path.join(folder_path, "train/labels", label)
        )

    # Move validation files to the valid folder
    for image, label in valid_files:
        shutil.move(
            os.path.join(folder_path, image), 
            os.path.join(folder_path, "valid/images", image)
        )
        shutil.move(
            os.path.join(folder_path, label), 
            os.path.join(folder_path, "valid/labels", label)
        )

    print("Dataset split completed successfully.")

# Specify the folder containing images and labels
folder_path = "path_to_dataset"  # Replace with your folder path
split_dataset(folder_path)
