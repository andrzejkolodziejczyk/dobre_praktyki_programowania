import sys
from fastapi import APIRouter, HTTPException, Path
from typing import List, Optional
from pydantic import BaseModel

from models import Movie, Link, Rating, Tag
from init_db import get_session

router = APIRouter()

#Create models for endpoints

class MovieCreate(BaseModel):
    movieId: str
    title: str
    genres: Optional[str] = None

    class Config:
        from_attributes = True

class LinkCreate(BaseModel):
    movieId: str  
    imdbId: Optional[str] = None
    tmdbId: Optional[str] = None

    class Config:
        from_attributes = True

class RatingCreate(BaseModel):
    id: str
    userId: str
    movieId: str
    rating: float 
    timestamp: int  

    class Config:
        from_attributes = True

class TagCreate(BaseModel):
    userId: str
    movieId: str
    tag: str
    timestamp: int 

    class Config:
        from_attributes = True

def get_object_or_404(session, model, obj_id):
    obj = session.query(model).filter(model.id == obj_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail=f"{model.__name__} not found")
    return obj

# ==========================================
# MOVIES CRUD
# ==========================================

@router.get('/movies')
def get_movies():
    session = get_session()
    try:
        movies = session.query(Movie).all()
        return movies
    finally:
        session.close()


@router.post('/movies')
def create_movie(data: MovieCreate):
    session = get_session()
    try:
        new_movie = Movie(**data.model_dump())
        session.add(new_movie)
        session.commit()
        session.refresh(new_movie)
        return new_movie
    finally:
        session.close()

@router.get('/movies/{id}')
def read_movie(id: int = Path(...)):
    session = get_session()
    try:
        return get_object_or_404(session, Movie, id)
    finally:
        session.close()

@router.put('/movies/{id}')
def update_movie(id: int, data: MovieCreate):
    session = get_session()
    try:
        movie = get_object_or_404(session, Movie, id)
        for key, value in data.items():
            setattr(movie, key, value)
        session.commit()
        return movie
    finally:
        session.close()

@router.delete('/movies/{id}')
def delete_movie(id: int):
    session = get_session()
    try:
        movie = get_object_or_404(session, Movie, id)
        session.delete(movie)
        session.commit()
        return {"detail": "Movie deleted"}
    finally:
        session.close()

# ==========================================
# LINKS CRUD
# ==========================================

@router.get('/links')
def get_links():
    session = get_session()
    try:
        links = session.query(Link).all()
        return links
    finally:
        session.close()

@router.post('/links')
def create_link(data: LinkCreate):
    session = get_session()
    try:
        new_link = Link(**data.model_dump())
        session.add(new_link)
        session.commit()
        session.refresh(new_link)
        return new_link
    finally:
        session.close()

@router.get('/links/{id}')
def read_link(id: int):
    session = get_session()
    try:
        return get_object_or_404(session, Link, id)
    finally:
        session.close()

@router.put('/links/{id}')
def update_link(id: int, data: LinkCreate):
    session = get_session()
    try:
        link = get_object_or_404(session, Link, id)
        for key, value in data.items():
            setattr(link, key, value)
        session.commit()
        return link
    finally:
        session.close()

@router.delete('/links/{id}')
def delete_link(id: int):
    session = get_session()
    try:
        link = get_object_or_404(session, Link, id)
        session.delete(link)
        session.commit()
        return {"detail": "Link deleted"}
    finally:
        session.close()

# ==========================================
# RATINGS CRUD
# ==========================================

@router.get('/ratings')
def get_ratings():
    session = get_session()
    try:
        ratings = session.query(Rating).all()
        return ratings
    finally:
        session.close()

@router.post('/ratings')
def create_rating(data: RatingCreate):
    session = get_session()
    try:
        new_rating = Rating(**data)
        session.add(new_rating)
        session.commit()
        session.refresh(new_rating)
        return new_rating
    finally:
        session.close()

@router.get('/ratings/{id}')
def read_rating(id: int):
    session = get_session()
    try:
        return get_object_or_404(session, Rating, id)
    finally:
        session.close()

@router.put('/ratings/{id}')
def update_rating(id: int, data: RatingCreate):
    session = get_session()
    try:
        rating = get_object_or_404(session, Rating, id)
        for key, value in data.items():
            setattr(rating, key, value)
        session.commit()
        return rating
    finally:
        session.close()

@router.delete('/ratings/{id}')
def delete_rating(id: int):
    session = get_session()
    try:
        rating = get_object_or_404(session, Rating, id)
        session.delete(rating)
        session.commit()
        return {"detail": "Rating deleted"}
    finally:
        session.close()

# ==========================================
# TAGS CRUD
# ==========================================

@router.get('/tags')
def get_tags():
    session = get_session()
    try:
        tags = session.query(Tag).all()
        return  tags
    finally:
        session.close()

@router.post('/tags')
def create_tag(data: TagCreate):
    session = get_session()
    try:
        new_tag = Tag(**data)
        session.add(new_tag)
        session.commit()
        session.refresh(new_tag)
        return new_tag
    finally:
        session.close()

@router.get('/tags/{id}')
def read_tag(id: int):
    session = get_session()
    try:
        return get_object_or_404(session, Tag, id)
    finally:
        session.close()

@router.put('/tags/{id}')
def update_tag(id: int, data: TagCreate):
    session = get_session()
    try:
        tag = get_object_or_404(session, Tag, id)
        for key, value in data.items():
            setattr(tag, key, value)
        session.commit()
        return tag
    finally:
        session.close()

@router.delete('/tags/{id}')
def delete_tag(id: int):
    session = get_session()
    try:
        tag = get_object_or_404(session, Tag, id)
        session.delete(tag)
        session.commit()
        return {"detail": "Tag deleted"}
    finally:
        session.close()

