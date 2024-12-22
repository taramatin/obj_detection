import os

def save_image_paths_to_txt(folder_path, output_file):
    # List of valid image extensions
    valid_extensions = {".png", ".jpg", ".jpeg"}
    
    # Check if folder exists
    if not os.path.isdir(folder_path):
        print(f"Error: The folder '{folder_path}' does not exist.")
        return

    # Open the output file for writing
    with open(output_file, "w") as file:
        for root, _, files in os.walk(folder_path):
            for filename in files:
                # Get file extension and check if it's a valid image
                if os.path.splitext(filename)[1].lower() in valid_extensions:
                    # Write the full path of the image to the file
                    file.write(os.path.join(root, filename) + "\n")

    print(f"Image paths saved to '{output_file}'.")

# Example usage
folder_path = "path/to/your/folder/"  # Replace with the path to your folder
output_file = "path/to/your/folder//output.txt"  # Replace with your desired output file name
save_image_paths_to_txt(folder_path, output_file)
