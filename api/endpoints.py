import sys
import jwt
import bcrypt
from fastapi import APIRouter, HTTPException, Path, Depends, Header
from typing import List, Optional
from pydantic import BaseModel
from jwt_manager import verify_token, verify_admin, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_HOURS
from models import Movie, Link, Rating, Tag, User
from init_db import get_session
from datetime import datetime, timedelta

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

class UserCreate(BaseModel):
    username: str
    password: str
    roles: Optional[List[str]] = ["REG_USER"]

class LoginData(BaseModel):
    username: str
    password: str

def get_object_or_404(session, model, obj_id):
    obj = session.query(model).filter(model.id == obj_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail=f"{model.__name__} not found")
    return obj

# ==========================================
# MOVIES CRUD
# ==========================================

@router.get('/movies')
def get_movies(current_user: dict = Depends(verify_token)):
    session = get_session()
    try:
        movies = session.query(Movie).all()
        return movies
    finally:
        session.close()


@router.post('/movies')
def create_movie(data: MovieCreate, current_user: dict = Depends(verify_token)):
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
def read_movie(id: int = Path(...), current_user: dict = Depends(verify_token)):
    session = get_session()
    try:
        return get_object_or_404(session, Movie, id)
    finally:
        session.close()

@router.put('/movies/{id}')
def update_movie(id: int, data: MovieCreate, current_user: dict = Depends(verify_token)):
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
def delete_movie(id: int, current_user: dict = Depends(verify_token)):
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
def get_links(current_user: dict = Depends(verify_token)):
    session = get_session()
    try:
        links = session.query(Link).all()
        return links
    finally:
        session.close()

@router.post('/links')
def create_link(data: LinkCreate, current_user: dict = Depends(verify_token)):
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
def read_link(id: int, current_user: dict = Depends(verify_token)):
    session = get_session()
    try:
        return get_object_or_404(session, Link, id)
    finally:
        session.close()

@router.put('/links/{id}')
def update_link(id: int, data: LinkCreate, current_user: dict = Depends(verify_token)):
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
def delete_link(id: int, current_user: dict = Depends(verify_token)):
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
def get_ratings(current_user: dict = Depends(verify_token)):
    session = get_session()
    try:
        ratings = session.query(Rating).all()
        return ratings
    finally:
        session.close()

@router.post('/ratings')
def create_rating(data: RatingCreate, current_user: dict = Depends(verify_token)):
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
def read_rating(id: int, current_user: dict = Depends(verify_token)):
    session = get_session()
    try:
        return get_object_or_404(session, Rating, id)
    finally:
        session.close()

@router.put('/ratings/{id}')
def update_rating(id: int, data: RatingCreate, current_user: dict = Depends(verify_token)):
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
def delete_rating(id: int, current_user: dict = Depends(verify_token)):
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
def get_tags(current_user: dict = Depends(verify_token)):
    session = get_session()
    try:
        tags = session.query(Tag).all()
        return  tags
    finally:
        session.close()

@router.post('/tags')
def create_tag(data: TagCreate, current_user: dict = Depends(verify_token)):
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
def read_tag(id: int, current_user: dict = Depends(verify_token)):
    session = get_session()
    try:
        return get_object_or_404(session, Tag, id)
    finally:
        session.close()

@router.put('/tags/{id}')
def update_tag(id: int, data: TagCreate, current_user: dict = Depends(verify_token)):
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
def delete_tag(id: int, current_user: dict = Depends(verify_token)):
    session = get_session()
    try:
        tag = get_object_or_404(session, Tag, id)
        session.delete(tag)
        session.commit()
        return {"detail": "Tag deleted"}
    finally:
        session.close()

# ==========================================
# USERS CRUD
# ==========================================

@router.post("/users")
def create_user(
    user: UserCreate, 
    authorization: str = Header(None)
):
    session = get_session()
    # Check if trying to create admin user
    if "ROLE_ADMIN" in user.roles:
        # Admin role requires authentication and ROLE_ADMIN permission
        if not authorization:
            raise HTTPException(status_code=401, detail="Authorization required to create admin user")
        
        try:
            scheme, token = authorization.split()
            if scheme.lower() != "bearer":
                raise HTTPException(status_code=401, detail="Invalid authentication scheme")
        except ValueError:
            raise HTTPException(status_code=401, detail="Invalid authorization header format")
        
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            if "ROLE_ADMIN" not in payload.get("roles", []):
                raise HTTPException(status_code=403, detail="Admin access required to create admin user")
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")
    
    # Check if user already exists
    existing_user = session.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    # Hash password
    password_hash = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    
    # Create new user
    db_user = User(
        username=user.username,
        password_hash=password_hash.decode('utf-8'),
        roles=user.roles
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

# ==================== AUTH ====================

@router.post("/login", )
def login(data: LoginData):
    # Check if user exists
    session = get_session()
    user = session.query(User).filter(User.username == data.username).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Verify password
    if not bcrypt.checkpw(data.password.encode('utf-8'), user.password_hash.encode('utf-8')):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Generate JWT token
    payload = {
        "sub": user.username,
        "user_id": user.id,
        "roles": user.roles,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    
    return {"access_token": token, "token_type": "bearer"}

@router.get("/user_details")
def get_user_details(current_user: dict = Depends(verify_token)):
    return {
        "username": current_user.get("sub"),
        "user_id": current_user.get("user_id"),
        "roles": current_user.get("roles"),
        "token_issued_at": current_user.get("iat"),
        "token_expires_at": current_user.get("exp")}