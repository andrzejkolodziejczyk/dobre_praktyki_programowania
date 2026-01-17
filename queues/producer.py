import csv
import uuid
import portalocker
import os

DB_FILE = "jobs_queue.csv"

def add_job(task_name):
    file_exists = os.path.isfile(DB_FILE)
    
    with open(DB_FILE, "a", newline="", encoding="utf-8") as f:
        portalocker.lock(f, portalocker.LockFlags.EXCLUSIVE)
        
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["id", "task", "status"])
        
        job_id = str(uuid.uuid4())[:8]
        writer.writerow([job_id, task_name, "pending"]) 
        
        print(f"Dodano zadanie: {task_name} (ID: {job_id})")

if __name__ == "__main__":
    add_job("Rozmowa telefoniczna")