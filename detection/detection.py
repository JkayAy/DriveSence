'''
1. detection.py (YOLOv8 Vehicle Detection Script)
This script handles vehicle detection using YOLOv8, calls the OCR function from ocr.py to recognize license plates, and sends the violation data to the backend API.
'''
import cv2
import requests
from ultralytics import YOLO
from ocr import recognize_license_plate  # Import OCR function
import time

# Load YOLOv8 model
model = YOLO('bestmodels/bestv9t.pt')  # Use the desired YOLOv8 model

# Function to process the video stream
def process_video(video_source='sample_video.mp4'):
#def process_video(video_source=0):
    cap = cv2.VideoCapture(video_source)  # 0 for webcam or video file path

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Perform vehicle detection
        results = model(frame)
        detections = results[0].boxes  # Get detected boxes

        for detection in detections:
            box = detection.xyxy[0]  # Bounding box coordinates
            conf = detection.conf  # Confidence score
            cls = int(detection.cls)  # Class ID

            if cls == 2:  # Class '2' is typically for 'car' in the COCO dataset
                # Draw bounding box
                x1, y1, x2, y2 = map(int, box)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

                # Crop the detected vehicle for license plate recognition
                vehicle_image = frame[y1:y2, x1:x2]
                license_plate_text = recognize_license_plate(vehicle_image)

                if license_plate_text:
                    print(f'Detected License Plate: {license_plate_text}')
                    # Placeholder for speed detection (can be enhanced later)
                    speed = 80  # Replace with actual speed detection logic
                    record_violation(license_plate_text, speed)

        cv2.imshow('Vehicle Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Function to record violations to the backend
def record_violation(license_plate, speed):
    violation_data = {
        'license_plate': license_plate,
        'speed': speed
    }
    try:
        response = requests.post('http://localhost:5000/record_violation', json=violation_data)
        if response.status_code == 200:
            print('Violation recorded successfully.')
        else:
            print(f'Failed to record violation: {response.text}')
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    process_video()  # Start processing the video
