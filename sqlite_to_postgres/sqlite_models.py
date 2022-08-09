import datetime
import uuid
from dataclasses import dataclass, field


@dataclass
class BaseModel:
    id: uuid.UUID
    created_at: datetime.datetime
    updated_at: datetime.datetime


@dataclass
class FilmWork(BaseModel):
    title: str
    description: str
    creation_model: str
    file_path: str
    type: str
    rating: float


@dataclass
class Genre(BaseModel):
    name: str
    description: str


@dataclass
class GenreFilmWork:
    id: uuid.UUID
    film_work_id: uuid.UUID
    genre_id: uuid.UUID
    created_at: datetime.datetime


@dataclass
class Person(BaseModel):
    full_name: str


@dataclass
class PersonFilmWork:
    id: uuid.UUID
    film_work_id: uuid.UUID
    person_id: uuid.UUID
    role: str
    created_at: datetime.datetime
