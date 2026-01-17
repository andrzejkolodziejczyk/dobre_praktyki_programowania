from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from typing import Optional
from datetime import datetime


Base = declarative_base()


class Movie(Base):
    __tablename__ = "movies"
    
    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    genres = Column(String)
    
    def __init__(self, movieId: str, title: str, genres: str):
        self.id = movieId
        self.title = title
        self.genres = genres


class Link(Base):
    __tablename__ = "links"
    
    id = Column(String, ForeignKey("movies.id"), primary_key=True)
    imdbId = Column(String)
    tmdbId = Column(String)
    
    def __init__(self, movieId: str, imdbId: str, tmdbId: str):
        self.id = movieId
        self.imdbId = imdbId
        self.tmdbId = tmdbId


class Rating(Base):
    __tablename__ = "ratings"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    userId = Column(String, nullable=False)
    movieId = Column(String, ForeignKey("movies.id"), nullable=False)
    rating = Column(Float, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    
    def __init__(self, userId: str, movieId: str, rating: str, timestamp: str):
        self.userId = userId
        self.movieId = movieId
        self.rating = float(rating)
        self.timestamp = datetime.fromtimestamp(int(timestamp))


class Tag(Base):
    __tablename__ = "tags"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    userId = Column(String, nullable=False)
    movieId = Column(String, ForeignKey("movies.id"), nullable=False)
    tag = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    
    def __init__(self, userId: str, movieId: str, tag: str, timestamp: str):
        self.userId = userId
        self.movieId = movieId
        self.tag = tag
        self.timestamp = datetime.fromtimestamp(int(timestamp))


