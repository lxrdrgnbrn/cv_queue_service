from worker.celery_app import celery_app
from worker.model import ObjectDetector
import os

detector = None

@celery_app.task(name="process_image")
def process_image_task(image_path, output_path):
    global detector
    if detector is None:
        print("Loading model inside worker...")
        detector = ObjectDetector()
    try:
        if not os.path.exists(image_path):
            return {"error": f"file {image_path} not found"}
        
        stats = detector.predict(image_path, output_path)
        
        return {
            "status": "success",
            "input": image_path,
            "output": output_path,
            "objects": stats
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}