import cv2
import numpy as np

# Load YOLO model and configuration
net = cv2.dnn.readNet("yolov3.weights", "cfg/yolov3.cfg")  # Load pre-trained YOLO weights and configuration file

# Load class labels from file
classes = []
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]  # Read and store object classes

# Get names of the YOLO model's layers
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]  # Identify output layers for detection

# Load the input video file
cap = cv2.VideoCapture(0)  # Replace "your_video.mp4" with the path to your video

# Process video frame by frame
while True:
    ret, frame = cap.read()  # Read a frame from the video
    if not ret:
        break  # Exit the loop if the video ends

    # Resize the frame to speed up processing
    frame = cv2.resize(frame, None, fx=0.4, fy=0.4)  # Resize frame to 40% of its original size
    height, width, channels = frame.shape  # Get dimensions of the frame

    # Prepare the frame for YOLO by creating a blob
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)  
    # Scale the pixel values, resize to 416x416, and normalize the image
    net.setInput(blob)  # Set the blob as input to the YOLO network

    # Forward pass to get the detections
    outs = net.forward(output_layers)  # Get output predictions from YOLO's output layers

    # Initialize lists to store detection information
    class_ids = []  # Store detected class IDs
    confidences = []  # Store confidence scores for detections
    boxes = []  # Store bounding box coordinates

    # Process each detection from the network
    for out in outs:
        for detection in out:
            scores = detection[5:]  # Get confidence scores for each class
            class_id = np.argmax(scores)  # Get the index of the class with the highest score
            confidence = scores[class_id]  # Get the highest confidence score
            if confidence > 0.5:  # Filter out weak detections
                center_x = int(detection[0] * width)  # Scale x-coordinate of the center
                center_y = int(detection[1] * height)  # Scale y-coordinate of the center
                w = int(detection[2] * width)  # Scale width of the bounding box
                h = int(detection[3] * height)  # Scale height of the bounding box
                x = int(center_x - w / 2)  # Calculate top-left x-coordinate
                y = int(center_y - h / 2)  # Calculate top-left y-coordinate
                boxes.append([x, y, w, h])  # Store bounding box coordinates
                confidences.append(float(confidence))  # Store confidence score
                class_ids.append(class_id)  # Store class ID

    # Apply non-max suppression to remove overlapping boxes
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)  
    # Suppress overlapping boxes based on confidence thresholds

    # Define font for displaying labels
    font = cv2.FONT_HERSHEY_PLAIN

    # Draw bounding boxes and labels on the frame
    for i in range(len(boxes)):
        if i in indexes:  # Only consider boxes that are not suppressed
            x, y, w, h = boxes[i]  # Extract box coordinates
            label = str(classes[class_ids[i]])  # Get the class label
            color = (255, 0, 0)  # Set color for the bounding box
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)  # Draw the bounding box
            cv2.putText(frame, label, (x, y + 30), font, 3, color, 3)  # Put the label text on the frame

    # Display the processed frame
    cv2.imshow("Video", frame)  # Show the frame in a window

    # Exit the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close all OpenCV windows
cap.release()  # Release the video capture object
cv2.destroyAllWindows()  # Close all OpenCV windows
