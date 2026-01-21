from fastapi import FastAPI, UploadFile, File
import shutil
import os
import uuid
from worker.tasks import process_image_task

app = FastAPI()

UPLOAD_DIR = "data/uploads"
RESULT_DIR = "data/results"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(RESULT_DIR, exist_ok=True)

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "cv_service"}
    

@app.post("/upload")
async def upload_image(file: UploadFile=File(...)):
    filename = f"{uuid.uuid4()}.jpg"
    input_path = os.path.join(UPLOAD_DIR, filename)
    output_path = os.path.join(RESULT_DIR, filename)
    
    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    task = process_image_task.delay(input_path, output_path)
    
    return{
        "task_id": task.id,
        "status": "processing",
        "input_path": input_path
    }

