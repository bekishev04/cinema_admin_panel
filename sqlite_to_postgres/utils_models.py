from __future__ import annotations

import dataclasses
import enum

from sqlite_to_postgres import sqlite_models


class StrEnum(str, enum.Enum):
    """Custom Enum Str"""

    table: str

    def __new__(cls, value: str, table: str) -> StrEnum:
        obj = str.__new__(cls, value)
        obj._value_ = value

        obj.table = table

        return obj


class ListModels(StrEnum):
    """Enum List Sqlite Models"""

    FilmWork = sqlite_models.FilmWork, "film_work"
    Genre = sqlite_models.Genre, "genre"
    GenreFilmWork = sqlite_models.GenreFilmWork, "genre_film_work"
    Person = sqlite_models.Person, "person"
    PersonFilmWork = sqlite_models.PersonFilmWork, "person_film_work"

    def __call__(self, *args, **kwargs):
        return self.value(*args, **kwargs)


class ConverterModels:
    @classmethod
    def get_fields(cls, model) -> str:
        fields = model.value.__dataclass_fields__.keys()
        return ", ".join(fields)

    @classmethod
    def prepare_data(cls, rows):
        prepare_data = []
        for row in rows:
            prepare_data.append(dataclasses.astuple(row))
        return prepare_data
