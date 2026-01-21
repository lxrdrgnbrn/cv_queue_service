from worker.model import ObjectDetector

detector = ObjectDetector()
stats = detector.predict("test.jpg", "result.jpg")
print(stats)