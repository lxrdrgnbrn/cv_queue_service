from worker.celery_app import celery_app
from worker.model import ObjectDetector
from worker.monitoring import TASKS_PROCESSED, OBJECTS_DETECTED, PROCESSING_TIME
import os
import time

detector = None

@celery_app.task(name="process_image")
def process_image_task(image_path, output_path):
    global detector
    if detector is None:
        print("Loading model inside worker...")
        detector = ObjectDetector()
    
    start_time = time.time()
    
    try:
        if not os.path.exists(image_path):
            return {"error": f"file {image_path} not found"}
        
        # Инференс
        detected_objects = detector.predict(image_path, output_path)
        
        # --- МЕТРИКИ ---
        TASKS_PROCESSED.inc() 
        
        for obj_name in detected_objects:
            OBJECTS_DETECTED.labels(class_name=obj_name).inc()
            
        duration = time.time() - start_time
        PROCESSING_TIME.observe(duration)
        # ----------------
        
        return {
            "status": "success",
            "objects": detected_objects,
            "duration": duration
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}