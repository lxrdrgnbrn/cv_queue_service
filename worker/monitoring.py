from prometheus_client import Counter, Histogram

TASKS_PROCESSED = Counter(
    'cv_tasks_processed_total', 
    'Total processed images'
)

OBJECTS_DETECTED = Counter(
    'cv_objects_detected_total', 
    'Detected objects count', 
    ['class_name']
)

PROCESSING_TIME = Histogram(
    'cv_processing_seconds', 
    'Time spent processing image',
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0]
)