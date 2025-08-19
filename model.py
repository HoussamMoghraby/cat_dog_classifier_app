import os
import logging
import cv2
import numpy as np
from PIL import Image
from urllib.request import urlretrieve
from ultralytics import YOLO
import base64

class ObjectDetector:
    # COCO dataset class names that YOLOv8 can detect
    CLASS_NAMES = {
        0: 'person', 1: 'bicycle', 2: 'car', 3: 'motorcycle', 4: 'airplane',
        5: 'bus', 6: 'train', 7: 'truck', 8: 'boat', 9: 'traffic light',
        10: 'fire hydrant', 11: 'stop sign', 12: 'parking meter', 13: 'bench',
        14: 'bird', 15: 'cat', 16: 'dog', 17: 'horse', 18: 'sheep',
        19: 'cow', 20: 'elephant', 21: 'bear', 22: 'zebra', 23: 'giraffe',
        24: 'backpack', 25: 'umbrella', 26: 'handbag', 27: 'tie', 28: 'suitcase',
        29: 'frisbee', 30: 'skis', 31: 'snowboard', 32: 'sports ball', 33: 'kite',
        34: 'baseball bat', 35: 'baseball glove', 36: 'skateboard', 37: 'surfboard',
        38: 'tennis racket', 39: 'bottle', 40: 'wine glass', 41: 'cup', 42: 'fork',
        43: 'knife', 44: 'spoon', 45: 'bowl', 46: 'banana', 47: 'apple', 48: 'sandwich',
        49: 'orange', 50: 'broccoli', 51: 'carrot', 52: 'hot dog', 53: 'pizza',
        54: 'donut', 55: 'cake', 56: 'chair', 57: 'couch', 58: 'potted plant',
        59: 'bed', 60: 'dining table', 61: 'toilet', 62: 'tv', 63: 'laptop',
        64: 'mouse', 65: 'remote', 66: 'keyboard', 67: 'cell phone', 68: 'microwave',
        69: 'oven', 70: 'toaster', 71: 'sink', 72: 'refrigerator', 73: 'book',
        74: 'clock', 75: 'vase', 76: 'scissors', 77: 'teddy bear', 78: 'hair drier',
        79: 'toothbrush'
    }
    
    # We're interested in cats (class 15) and dogs (class 16)
    TARGET_CLASSES = {15: 'cat', 16: 'dog'}
    
    def __init__(self, model_path):
        logging.info("ObjectDetector class initialized")
        self.model = YOLO(model_path)
        logging.info("YOLO model loaded successfully!")

    def detect(self, image_path):
        """
        Detect objects in the image and highlight cats and dogs
        Returns: (annotated_image_base64, detection_results)
        """
        logging.info(f"Processing image: {image_path}")
        
        # Run YOLOv8 inference
        results = self.model(image_path, conf=0.25)  # confidence threshold 0.25
        
        # Process results
        result = results[0]  # first image
        original_img = cv2.imread(image_path)
        annotated_img = original_img.copy()
        
        # Track detected cats and dogs
        detected_objects = []
        
        # Go through each detection
        for box in result.boxes:
            class_id = int(box.cls[0].item())
            confidence = box.conf[0].item()
            
            # Get coordinates (convert from normalized to pixel values)
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            
            # Check if this is a cat or dog
            if class_id in self.TARGET_CLASSES:
                class_name = self.TARGET_CLASSES[class_id]
                color = (0, 255, 0) if class_name == 'cat' else (0, 0, 255)  # Green for cats, Red for dogs
                
                # Draw rectangle and label
                cv2.rectangle(annotated_img, (x1, y1), (x2, y2), color, 2)
                label = f"{class_name.upper()}: {confidence:.2f}"
                cv2.putText(annotated_img, label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                
                detected_objects.append({
                    "class": class_name,
                    "confidence": confidence,
                    "box": [x1, y1, x2, y2]
                })
            else:
                # Draw light gray boxes for other detected objects
                cv2.rectangle(annotated_img, (x1, y1), (x2, y2), (200, 200, 200), 1)
                if class_id in self.CLASS_NAMES:
                    cv2.putText(annotated_img, self.CLASS_NAMES[class_id], (x1, y1-5), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.4, (150, 150, 150), 1)
        
        # Convert the annotated image to base64 for displaying in HTML
        _, buffer = cv2.imencode('.jpg', annotated_img)
        img_base64 = base64.b64encode(buffer).decode('utf-8')
        
        # Format detection results
        if not detected_objects:
            result_text = "No cats or dogs detected in this image."
        else:
            cats = len([obj for obj in detected_objects if obj["class"] == "cat"])
            dogs = len([obj for obj in detected_objects if obj["class"] == "dog"])
            result_text = f"Detected: {cats} cat(s) and {dogs} dog(s)"
            
        return img_base64, result_text, detected_objects
    
    def download_url(self, url, filename):
        """Download a file from URL to filename."""
        urlretrieve(url, filename)
        return filename

def main():
    model = ObjectDetector('yolov8n.pt')
    img_path = 'input.jpg'
    
    # Download a test image
    urlretrieve("https://cdn.britannica.com/60/8160-050-08CCEABC/German-shepherd.jpg", img_path)
    
    # Process the image
    _, result_text, detections = model.detect(img_path)
    logging.info(f"Detection results: {result_text}")
    logging.info(f"Detailed detections: {detections}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()