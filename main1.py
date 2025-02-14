import numpy as np
import cv2

prototxt_path = r"C:\Users\User\Downloads\Object Detection\models\MobileNetSSD_deploy.prototxt.txt"
model_path = r"C:\Users\User\Downloads\Object Detection\models\MobileNetSSD_deploy.caffemodel"

min_confidence = 0.1
classes = ["background", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair",
           "cow", "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]

np.random.seed(543210)
colors = np.random.uniform(0, 255, size=(len(classes), 3))

net = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit(1)

cv2.namedWindow("Detected Objects", cv2.WINDOW_NORMAL)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Couldn't read from webcam.")
        break

    height, width = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007, (300, 300), 130)
    net.setInput(blob)
    detected_objects = net.forward()

    for i in range(detected_objects.shape[2]):
        confidence = detected_objects[0][0][i][2]
        if confidence > min_confidence:
            class_index = int(detected_objects[0, 0, i, 1])
            x1, y1 = int(detected_objects[0, 0, i, 3] * width), int(detected_objects[0, 0, i, 4] * height)
            x2, y2 = int(detected_objects[0, 0, i, 5] * width), int(detected_objects[0, 0, i, 6] * height)
            
            label = f"{classes[class_index]}: {confidence:.2f}%"
            cv2.rectangle(frame, (x1, y1), (x2, y2), colors[class_index], 3)
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, colors[class_index], 2)

    cv2.imshow("Detected Objects", frame)

    # ✅ Detect if 'q' is pressed OR window is closed manually
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q') or cv2.getWindowProperty("Detected Objects", cv2.WND_PROP_VISIBLE) < 1:
        print("User exited or closed window.")
        break

cap.release()
cv2.destroyAllWindows()
print("Live Object Detection stopped.")
