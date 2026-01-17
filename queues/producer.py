from init_db import SessionLocal, Job, init_db

def add_jobs(count=1):
    init_db()
    session = SessionLocal()
    try:
        for i in range(1, count + 1):
            new_job = Job(task_name=f"Rozmowa telefoniczna nr {i}", status="pending")
            session.add(new_job)
        session.commit()
        print(f"Pomyślnie dodano {count} zadań do bazy.")
    except Exception as e:
        session.rollback()
        print(f"Błąd: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    add_jobs(1)