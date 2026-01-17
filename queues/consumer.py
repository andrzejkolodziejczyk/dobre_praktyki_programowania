import time
from init_db import SessionLocal, Job

def process_jobs():
    print("Consumer uruchomiony. Oczekiwanie na pracę...")
    
    while True:
        session = SessionLocal()
        try:
            job = session.query(Job).filter(Job.status == "pending").first()

            if job:
                job.status = "in_progress"
                job_id = job.id
                task_name = job.task_name
                session.commit()
                
                print(f"[{job_id}] Przetwarzanie: {task_name}...")
                
                time.sleep(30)
                

                job.status = "done"
                session.commit()
                print(f"[{job_id}] Zakończono sukcesem.")
            else:
                session.close()
                time.sleep(5) # Czekaj jeśli nie ma pracy
        except Exception as e:
            session.rollback()
            print(f"Wystąpił błąd: {e}")
            time.sleep(5)
        finally:
            session.close()

if __name__ == "__main__":
    process_jobs()