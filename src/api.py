import os
import time
import json
import redis
import uuid
from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from licencePlateDetector import recognizePlate

app = FastAPI(title="LPR Pipeline API")


QUEUE_NAME = "image_processing_queue"
RESULTS_KEY = "processed_results"
QUEUE_DIR = "queued_images"

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
os.makedirs(QUEUE_DIR, exist_ok=True)

@app.post("/process")
async def processImage(file: UploadFile = File(...)):

    contents = await file.read()
    
    result = recognizePlate(contents)
    
    return {"message": "Image processed successfully", "data": result}



@app.post("/queue")
async def queue_image(file: UploadFile = File(...)):
    id = str(uuid.uuid4())
    
    extension = os.path.splitext(file.filename)[1]
    filePath = os.path.join(QUEUE_DIR, f"{id}{extension}")
    
    with open(filePath, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    jobData = {
        "id": id,
        "path": os.path.abspath(filePath),
        "name": file.filename
    }
    
    r.lpush(QUEUE_NAME, json.dumps(jobData))
    
    return {"status": "queued", "job_id": id, "path_saved": filePath}



@app.get("/results")
async def get_results():
    allResults = r.hgetall(RESULTS_KEY)
    parsedResults = {key: json.loads(value) for key, value in allResults.items()}
    return parsedResults


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)