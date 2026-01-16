import os
import time
import json
import redis
import uuid
from fastapi import FastAPI, UploadFile, File, BackgroundTasks

app = FastAPI(title="LPR Pipeline API")


QUEUE_NAME = "image_processing_queue"
RESULTS_KEY = "processed_results"
QUEUE_DIR = "queued_images"

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
os.makedirs(QUEUE_DIR, exist_ok=True)

@app.post("/process")
async def processImage(file: UploadFile = File(...)):

    contents = await file.read()
    
    mockResult = {
        "filename": file.filename,
        "plateNumber": "KRA12345",  
    }
    
    return {"message": "Image processed successfully", "data": mockResult}



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



#consumer
def run_consumer():
    print(f"Consumer started. Waiting for jobs in '{QUEUE_NAME}'...")
    
    while True:
        _, job = r.brpop(QUEUE_NAME)
        jobData = json.loads(job)
        
        id = jobData['id']
        print(f"Processing job {id} for file {jobData['name']}...")
        
        time.sleep(2)
        result = {
            "id": id,
            "plate": "KR77777",
            "processed_at": time.time()
        }
        
        r.hset(RESULTS_KEY, id, json.dumps(result))
        print(f"Job {id} finished and saved.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    run_consumer()