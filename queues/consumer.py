import csv
import time
import os
import portalocker

DB_FILE = "jobs_queue.csv"

def process_jobs():
    print("Consumer uruchomiony. Oczekiwanie na zadania...")
    
    while True: 
        if not os.path.isfile(DB_FILE):
            time.sleep(5)
            continue

        job_to_do = None
        all_rows = []

        
        with open(DB_FILE, "r+", newline="", encoding="utf-8") as f:
            portalocker.lock(f, portalocker.LockFlags.EXCLUSIVE)
            
            reader = list(csv.reader(f))
            if not reader:
                portalocker.unlock(f)
                time.sleep(5)
                continue
            
            header = reader[0]
            rows = reader[1:]
            
            for row in rows:
                if job_to_do is None and row[2] == "pending":
                    row[2] = "in_progress"
                    job_to_do = row
                all_rows.append(row)
            
            if job_to_do:
                f.seek(0)
                f.truncate()
                writer = csv.writer(f)
                writer.writerow(header)
                writer.writerows(all_rows)
            
            portalocker.unlock(f)

        # 2. Wykonywanie pracy poza zablokowanym plikiem
        if job_to_do:
            print(f" Rozpoczęto: {job_to_do[1]} (ID: {job_to_do[0]})")
            time.sleep(30) # Symulacja pracy 30s
            
            # 3. Zmiana statusu na 'done'
            update_job_status(job_to_do[0], "done")
            print(f" Zakończono: {job_to_do[0]}")
        else:
            time.sleep(5) # Odczekanie 5s przed kolejnym sprawdzeniem

def update_job_status(job_id, new_status):
    with open(DB_FILE, "r+", newline="", encoding="utf-8") as f:
        portalocker.lock(f, portalocker.LockFlags.EXCLUSIVE)
        reader = list(csv.reader(f))
        f.seek(0)
        f.truncate()
        writer = csv.writer(f)
        for row in reader:
            if row[0] == job_id:
                row[2] = new_status # Zmiana statusu na done
            writer.writerow(row)
        portalocker.unlock(f)

if __name__ == "__main__":
    process_jobs()