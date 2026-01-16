import time
import json
import redis
from licencePlateDetector import recognizePlate

QUEUE_NAME = "image_processing_queue"
RESULTS_KEY = "processed_results"

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def runConsumer():
    print(f"Consumer started. Waiting for jobs in '{QUEUE_NAME}'...")
    
    while True:
        _, job = r.brpop(QUEUE_NAME)
        jobData = json.loads(job)
        
        id = jobData['id']
        print(f"Processing job {id} for file {jobData['name']}...")
        
        result = {
            "id": id,
            "data": recognizePlate(jobData['path']),
            "processed_at": time.time()
        }
        
        r.hset(RESULTS_KEY, id, json.dumps(result))
        print(f"Job {id} finished and saved.")

runConsumer()