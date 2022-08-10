import datetime
import uuid
from dataclasses import dataclass


@dataclass
class BaseModel:
    id: uuid.UUID
    created_at: datetime.datetime | None
    updated_at: datetime.datetime | None


@dataclass
class FilmWork(BaseModel):
    title: str | None
    description: str | None
    creation_date: str | None
    file_path: str | None
    type: str | None
    rating: float | None


@dataclass
class Genre(BaseModel):
    name: str | None
    description: str | None


@dataclass
class GenreFilmWork:
    id: uuid.UUID
    film_work_id: uuid.UUID | None
    genre_id: uuid.UUID | None
    created_at: datetime.datetime | None


@dataclass
class Person(BaseModel):
    full_name: str | None


@dataclass
class PersonFilmWork:
    id: uuid.UUID
    film_work_id: uuid.UUID | None
    person_id: uuid.UUID | None
    role: str | None
    created_at: datetime.datetime | None
