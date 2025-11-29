import sys
from fastapi import APIRouter

sys.path.append("../db")

from models import Movie, Link, Rating, Tag
from init_db import get_session

router = APIRouter()


@router.get('/movies')
def get_movies():
    session = get_session()
    try:
        movies = session.query(Movie).all()
        return movies
    finally:
        session.close()


@router.get('/links')
def get_links():
    session = get_session()
    try:
        links = session.query(Link).all()
        return links
    finally:
        session.close()


@router.get('/ratings')
def get_ratings():
    session = get_session()
    try:
        ratings = session.query(Rating).all()
        return ratings
    finally:
        session.close()


@router.get('/tags')
def get_tags():
    session = get_session()
    try:
        tags = session.query(Tag).all()
        return  tags
    finally:
        session.close()
