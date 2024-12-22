import torch
import cv2

# Load custom-trained YOLOv5 model
# Replace 'path/to/your/custom/weights.pt' with the actual path
model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt', force_reload=True)

cap = cv2.VideoCapture(0)

while True:
    ret, img = cap.read()
    if not ret:
        break

    # Perform detection on the image
    result = model(img)
    print('result:', result)

    # Convert detected result to pandas DataFrame
    data_frame = result.pandas().xyxy[0]
    print('data_frame:')
    print(data_frame)

    # Draw bounding boxes and labels
    for index, row in data_frame.iterrows():
        # Coordinates of the bounding box
        x1, y1, x2, y2 = int(row['xmin']), int(row['ymin']), int(row['xmax']), int(row['ymax'])

        # Label name and confidence score
        label = row['name']
        conf = row['confidence']
        text = f"{label} {conf:.2f}"

        # Draw rectangle and text on the image
        cv2.rectangle(img, (x1, y1), (x2, y2), (255, 255, 0), 2)
        cv2.putText(img, text, (x1, y1 - 5), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 2)

    # Show the image
    cv2.imshow('IMAGE', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
