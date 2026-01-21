from worker.tasks import process_image_task

task = process_image_task.delay("test.jpg", "test_out.jpg")
print(f"Task sent! ID: {task.id}")