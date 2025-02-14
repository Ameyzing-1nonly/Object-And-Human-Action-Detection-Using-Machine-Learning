import cv2
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
from collections import deque
from threading import Thread
import time

# Load pre-trained I3D model
print("Loading model...")
model = hub.load("https://tfhub.dev/deepmind/i3d-kinetics-400/1")
print("Model loaded successfully!")

# Load Kinetics-400 Labels
try:
    with open("kinetics_labels.txt", "r") as f:
        kinetics_labels = [line.strip() for line in f.readlines()]
    print("Kinetics-400 labels loaded successfully!")
except FileNotFoundError:
    print("Error: kinetics_labels.txt not found!")
    exit(1)

# Open webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 30)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

if not cap.isOpened():
    print("Error: Could not access the webcam.")
    exit(1)

# Buffer for action recognition
FPS = cap.get(cv2.CAP_PROP_FPS) or 30
FRAME_COUNT = int(FPS * 1.5)
frame_buffer = deque(maxlen=FRAME_COUNT)
predictions_buffer = deque(maxlen=5)

frame = None
def read_frame():
    global frame
    while True:
        ret, frame = cap.read()
        if not ret:
            break

Thread(target=read_frame, daemon=True).start()

def preprocess_frame(frame):
    frame = cv2.resize(frame, (224, 224))
    frame = (frame / 127.5) - 1
    return frame

cv2.namedWindow("Live Action Recognition", cv2.WINDOW_NORMAL)
last_prediction_time = time.time()

while True:
    if frame is None:
        continue

    if time.time() - last_prediction_time < 1 / FPS:
        continue

    last_prediction_time = time.time()
    processed_frame = preprocess_frame(frame)
    frame_buffer.append(processed_frame)

    if len(frame_buffer) == FRAME_COUNT:
        print("Making prediction...")
        input_clip = np.expand_dims(np.array(frame_buffer), axis=0)
        input_tensor = tf.convert_to_tensor(input_clip, dtype=tf.float32)

        prediction = model.signatures["default"](input_tensor)
        prediction_index = np.argmax(prediction["default"])

        action = kinetics_labels[prediction_index] if prediction_index < len(kinetics_labels) else "Unknown"
        predictions_buffer.append(action)
        most_common_action = max(set(predictions_buffer), key=predictions_buffer.count)

        print(f"Predicted action: {most_common_action}")
        cv2.putText(frame, f"Action: {most_common_action}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

    cv2.imshow("Live Action Recognition", frame)

    # ✅ Detect if 'q' is pressed OR window is closed manually
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q') or cv2.getWindowProperty("Live Action Recognition", cv2.WND_PROP_VISIBLE) < 1:
        print("User exited or closed window.")
        break

cap.release()
cv2.destroyAllWindows()
print("Live analysis stopped.")
