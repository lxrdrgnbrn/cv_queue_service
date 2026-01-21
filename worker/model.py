from ultralytics import YOLO
import cv2
import numpy as np

class ObjectDetector:
    def __init__(self, model_name='yolov8n.pt'):
        self.model = YOLO(model_name)
        pass
    
    def predict(self, image_path, output_path):
        results = self.model(image_path)
        result = results[0]
        
        ploted_image = result.plot()
        cv2.imwrite(output_path, ploted_image)
        
        
        class_ids = result.boxes.cls.tolist()
        
        objects = [result.names[int(cls_id)] for cls_id in class_ids]
        return objects
    