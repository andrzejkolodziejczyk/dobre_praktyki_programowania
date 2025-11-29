import csv
from pathlib import Path
from fastapi import APIRouter
from models import Movie, Link, Rating, Tag

router = APIRouter()

@router.get('/movies')
def get_movies():
    movies = []
    rows = read_csv_file('movies.csv')
    
    for row in rows:
        movie = Movie(
            movieId=row['movieId'],
            title=row['title'],
            genres=row['genres']
        )
        movies.append(movie.__dict__)
    
    return movies


@router.get('/links')
def get_links():
    links = []
    rows = read_csv_file('links.csv')
    
    for row in rows:
        link = Link(
            movieId=row['movieId'],
            imdbId=row['imdbId'],
            tmdbId=row['tmdbId']
        )
        links.append(link.__dict__)
    
    return links


@router.get('/ratings')
def get_ratings():
    ratings = []
    rows = read_csv_file('ratings.csv')
    
    for row in rows:
        rating = Rating(
            userId=row['userId'],
            movieId=row['movieId'],
            rating=row['rating'],
            timestamp=row['timestamp']
        )
        ratings.append(rating.__dict__)
    
    return ratings


@router.get('/tags')
def get_tags():
    tags = []
    rows = read_csv_file('tags.csv')
    
    for row in rows:
        tag = Tag(
            userId=row['userId'],
            movieId=row['movieId'],
            tag=row['tag'],
            timestamp=row['timestamp']
        )
        tags.append(tag.__dict__)
    
    return tags

def read_csv_file(filename: str):
    """Read a CSV file and return its contents as a list of dictionaries."""
    csv_path = Path(__file__).parent.parent / 'db' / filename
    
    data = []
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    
    return data
