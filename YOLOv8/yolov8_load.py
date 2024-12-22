from pathlib import Path  # To handle file paths
from ultralytics import YOLO  # YOLOv8 for object detection
import cv2  # OpenCV for accessing the webcam
import supervision as sv  # Supervision library for enhanced visualization

# Set the path to the best.pt model file
model_path = 'path_to_best.pt'  # Replace with the actual path to your best.pt file

# Load the YOLOv8 model
model = YOLO(model_path)  # Load custom YOLOv8 model

# Define a box annotator using supervision
box_annotator = sv.BoxAnnotator(
    thickness=2,  # Thickness of the box
    text_thickness=1,  # Thickness of the label text
    text_scale=0.5,  # Scale of the label text
)

# Open the webcam
cap = cv2.VideoCapture(0)  # Initialize the webcam (0 is the default camera)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Loop to read frames from the webcam
while True:
    ret, frame = cap.read()  # Read a frame from the webcam
    if not ret:
        print("Error: Failed to capture frame from webcam.")
        break

    # Run inference on the frame
    results = model(frame)  # Perform inference using YOLOv8

    # Extract detection results
    detections = sv.Detections.from_yolov8(results[0])  # Convert YOLOv8 results to Supervision detections

    # Annotate the frame with detections
    labels = [
        f"{model.model.names[class_id]} {confidence:.2f}"  # Label format: Class Name and Confidence
        for _, confidence, class_id, _ in detections
    ]
    annotated_frame = box_annotator.annotate(
        scene=frame,  # Original frame
        detections=detections,  # Detections from YOLOv8
        labels=labels,  # Labels for each detection
    )

    # Display the annotated frame
    cv2.imshow('YOLOv8 Detection with Supervision', annotated_frame)

    # Break the loop on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close OpenCV windows
cap.release()  # Release the webcam resource
cv2.destroyAllWindows()  # Close all OpenCV windows
