import pytest
import sys
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from app import app
from init_db import get_session
from models import Base, Movie, Link, Rating, Tag

# Test database
TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL, echo=False)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    def override_get_session():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_session] = override_get_session
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

# ==================== FIXTURES ====================

@pytest.fixture
def sample_movies(db_session):
    movies = [
        Movie(movieId=1, title="Test Movie 1", genres="Action"),
        Movie(movieId=2, title="Test Movie 2", genres="Comedy"),
        Movie(movieId=3, title="Test Movie 3", genres="Drama"),
    ]
    for movie in movies:
        db_session.add(movie)
    db_session.commit()
    return movies

@pytest.fixture
def sample_links(db_session):
    links = [
        Link(movieId=1, imdbId="tt0111161", tmdbId="278"),
        Link(movieId=2, imdbId="tt0068646", tmdbId="238"),
        Link(movieId=3, imdbId="tt0468569", tmdbId="155"),
    ]
    for link in links:
        db_session.add(link)
    db_session.commit()
    return links

@pytest.fixture
def sample_ratings(db_session):
    ratings = [
        Rating(userId=1, movieId=1, rating=3.0, timestamp=1234567890),
        Rating(userId=2, movieId=1, rating=4.5, timestamp=1234567891),
        Rating(userId=1, movieId=2, rating=5.0, timestamp=1234567892),
    ]
    for rating in ratings:
        db_session.add(rating)
    db_session.commit()
    return ratings

@pytest.fixture
def sample_tags(db_session):
    tags = [
        Tag(userId=1, movieId=1, tag="awesome", timestamp=1234567890),
        Tag(userId=2, movieId=1, tag="must watch", timestamp=1234567891),
        Tag(userId=1, movieId=2, tag="boring", timestamp=1234567892),
    ]
    for tag in tags:
        db_session.add(tag)
    db_session.commit()
    return tags