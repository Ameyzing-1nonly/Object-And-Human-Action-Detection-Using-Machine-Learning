import numpy as np
import cv2

import sys

if len(sys.argv) < 2:
    print("Error: No image file provided.")
    sys.exit(1)

image_path = sys.argv[1]  # Get image path from command line argument
print(f"Processing image: {image_path}")

prototxt_path = r"C:\Users\User\Downloads\Object Detection\models\MobileNetSSD_deploy.prototxt.txt"
model_path = r"C:\Users\User\Downloads\Object Detection\models\MobileNetSSD_deploy.caffemodel"


min_confidence = 0.1

classes = ["background","aeroplane","bicycle","bird","boat","bottle","bus","car","cat","chair","cow","diningtable","dog","horse","motorbike","person","pottedplant","sheep","sofa","train","tvmonitor"]

np.random.seed(543210)
colors = np.random.uniform(0, 255, size=(len(classes), 3))

net = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)

image = cv2.imread(image_path)
if image is None:
    print(f"Error: Could not load image {image_path}")
    exit(1)

height, width = image.shape[0], image.shape[1]

blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007, (300, 300), 130)

net.setInput(blob)
detected_objects = net.forward()

for i in range(detected_objects.shape[2]):
    
    confidence = detected_objects[0][0][i][2]
    
    if confidence > min_confidence:
        
        class_index = int(detected_objects[0, 0, i, 1])
        
        upper_left_x = int(detected_objects[0, 0, i, 3] * width)
        upper_left_y = int(detected_objects[0, 0, i, 4] * height)
        lower_right_x = int(detected_objects[0, 0, i, 5] * width)
        lower_right_y = int(detected_objects[0, 0, i, 6] * height)
        
        prediction_text = f"{classes[class_index]}: {confidence:.2f}%"
        cv2.rectangle(image, (upper_left_x, upper_left_y), (lower_right_x, lower_right_y), colors[class_index], 3)
        cv2.putText(image, prediction_text, (upper_left_x, 
                    upper_left_y - 15 if upper_left_y > 30 else upper_left_y + 15), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, colors[class_index], 2)

cv2.imshow("Detected Objects", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
