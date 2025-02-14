import cv2
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
from collections import deque
from ultralytics import YOLO  # Import YOLO model for object detection
import sys
import os

# ✅ Check if a video file is provided
if len(sys.argv) < 2:
    print("Error: No video file provided.")
    sys.exit(1)

video_path = sys.argv[1]  # Get video path from command line argument

# ✅ Check if the file exists
if not os.path.exists(video_path):
    print(f"Error: Video file not found at {video_path}")
    sys.exit(1)

print(f"Processing video: {video_path}")

# ✅ Load pre-trained I3D model for action recognition
print("Loading action recognition model...")
action_model = hub.load("https://tfhub.dev/deepmind/i3d-kinetics-400/1")
print("Action recognition model loaded successfully!")

# ✅ Load YOLOv8 model for object detection
print("Loading object detection model...")
object_model = YOLO("yolov8n.pt")  # Load YOLOv8 (Nano version for speed)
print("Object detection model loaded successfully!")

# ✅ Load Kinetics-400 Labels
try:
    with open("kinetics_labels.txt", "r") as f:
        kinetics_labels = [line.strip() for line in f.readlines()]
    print("Kinetics-400 labels loaded successfully!")
except FileNotFoundError:
    print("Error: kinetics_labels.txt not found!")
    sys.exit(1)

# ✅ Buffer for action recognition
FRAME_COUNT = 32  # Number of frames for action recognition
frame_buffer = deque(maxlen=FRAME_COUNT)

def preprocess_frame(frame):
    """Resize and normalize the frame for I3D model."""
    frame = cv2.resize(frame, (224, 224))
    frame = (frame / 127.5) - 1  # Normalize to [-1, 1]
    return frame

def draw_bounding_boxes(frame, results):
    """Draw bounding boxes for detected objects."""
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            confidence = box.conf[0]
            class_id = int(box.cls[0])
            label = f"{object_model.names[class_id]} {confidence:.2f}"

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Green box
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 
                        0.5, (0, 255, 0), 2)
    return frame

def analyze_video(video_path):
    print(f"Opening video: {video_path}")
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"Error: Could not open video file {video_path}")
        return

    cv2.namedWindow("Action Recognition & Object Detection", cv2.WINDOW_NORMAL)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("End of video or error reading frame.")
            break

        processed_frame = preprocess_frame(frame)
        frame_buffer.append(processed_frame)

        # ✅ Object detection using YOLO
        results = object_model(frame)  
        frame = draw_bounding_boxes(frame, results)  

        # ✅ Action recognition
        if len(frame_buffer) == FRAME_COUNT:
            input_clip = np.expand_dims(np.array(frame_buffer), axis=0)
            prediction = action_model.signatures["default"](tf.constant(input_clip, dtype=tf.float32))
            prediction_index = np.argmax(prediction["default"])

            if prediction_index < len(kinetics_labels):
                action = kinetics_labels[prediction_index]
            else:
                action = "Unknown"

            # ✅ Draw action text
            cv2.putText(frame, f"Action: {action}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                        0.8, (0, 255, 255), 2)

        resized_frame = cv2.resize(frame, (1280, 720))
        cv2.imshow("Action Recognition & Object Detection", resized_frame)

        # ✅ Properly detect exit (q key OR closing the window)
        key = cv2.waitKey(1) & 0xFF  
        if key == ord('q') or cv2.getWindowProperty("Action Recognition & Object Detection", cv2.WND_PROP_VISIBLE) < 1:
            print("User exited or closed window.")
            break

    cap.release()
    cv2.destroyAllWindows()
    print("Video analysis completed.")

# ✅ Run the video analysis
analyze_video(video_path)
