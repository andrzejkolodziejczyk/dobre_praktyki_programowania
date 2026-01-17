import sys
from pathlib import Path
import csv


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Movie, Link, Rating, Tag, User


# Database configuration
DB_NAME = "movies.db"

DATABASE_URL = f"sqlite:///{DB_NAME}"


def init_database():
    
    engine = create_engine(
        DATABASE_URL,
        echo=False, 
        connect_args={"check_same_thread": False}
    )
    
    Base.metadata.create_all(engine)
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    return engine, SessionLocal


def get_engine():
    engine = create_engine(
        DATABASE_URL,
        echo=False,
        connect_args={"check_same_thread": False}
    )
    return engine


def get_session():
    engine = get_engine()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()

def read_csv_file(filename: str):
    csv_path = Path(__file__).parent / filename
    
    data = []
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    
    return data


def load_csv_data_to_db(engine, session_factory):
    session = session_factory()
    
    try:
        movies_data = read_csv_file("../db/movies.csv")
        links_data = read_csv_file("../db/links.csv")
        ratings_data = read_csv_file("../db/ratings.csv")
        tags_data = read_csv_file("../db/tags.csv")

        movies = [
            Movie(
                movieId=row["movieId"],
                title=row["title"],
                genres=row["genres"]
            )
            for row in movies_data
        ]
        session.add_all(movies)
        
        links = [
            Link(
                movieId=row["movieId"],
                imdbId=row["imdbId"],
                tmdbId=row["tmdbId"]
            )
            for row in links_data
        ]
        session.add_all(links)

        ratings = [
            Rating(
                userId=row["userId"],
                movieId=row["movieId"],
                rating=row["rating"],
                timestamp=row["timestamp"]
            )
            for row in ratings_data
        ]
        session.add_all(ratings)

        tags = [
            Tag(
                userId=row["userId"],
                movieId=row["movieId"],
                tag=row["tag"],
                timestamp=row["timestamp"]
            )
            for row in tags_data
        ]
        session.add_all(tags)

        users = [
            User(
                username="admin",
                password_hash="$2b$12$KIXQJY5Z6Yh1Fh8H7G6kUuJ8jFh8H7G6kUuJ8jFh8H7G6kUuJ8jFh8H7G6kUu",  # bcrypt hash for "adminpass"
                roles="ROLE_ADMIN"
            )
        ]
        session.add_all(users)
        
        session.commit()
        
    except Exception as e:
        session.rollback()
        print(f"\n✗ Error loading data: {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    engine, SessionLocal = init_database()
    load_csv_data_to_db(engine, SessionLocal)
    print(f"Db initialized succesfully, file: {DB_NAME}")
