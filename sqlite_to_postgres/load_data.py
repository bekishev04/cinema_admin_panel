import dataclasses
import sqlite3

import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extensions import cursor as _cursor
from psycopg2.extras import DictCursor, execute_values

from config.settings import DATABASES
from sqlite_to_postgres import sqlite_models


TABLES = {
    "film_work": sqlite_models.FilmWork,
    "genre": sqlite_models.Genre,
    "genre_film_work": sqlite_models.GenreFilmWork,
    "person": sqlite_models.Person,
    "person_film_work": sqlite_models.PersonFilmWork,
}


def get_fields(model) -> str:
    fields = [field.name for field in dataclasses.fields(model)]
    return ", ".join(fields)


def get_values_in_key_order(data_row, keys):
    _data = {}
    for k in keys:
        _data[k] = dataclasses.asdict(data_row)[k]
    return tuple(_data.values())


def prepare_data(data, model):
    prepare_data = []
    model_fields = model.__dataclass_fields__.keys()
    for row in data:
        prepare_data.append(get_values_in_key_order(row, model_fields))
    return prepare_data


def load_from_sqlite(cursor: sqlite3.Cursor, table, n: int = 10_000):
    """Load data from sqlite with paginate"""

    i = 0
    fields = get_fields(TABLES[table])

    while True:

        cursor.execute(f"SELECT {fields} FROM {table} LIMIT {n} OFFSET {i};")

        i += n

        rows = cursor.fetchall()
        if rows:
            yield rows
        else:
            break


def save_data(table: str, data, pg_cursor: _cursor):
    model = TABLES[table]
    fields = get_fields(model)

    for rows in data:
        vals = prepare_data(rows, model)

        execute_values(
            pg_cursor,
            f"""
            INSERT INTO content.{table} ({fields})
            VALUES
            %s
            ON CONFLICT (id) DO NOTHING
            """,
            vals,
        )


def load_and_save_data(sqlite_con: sqlite3.Connection, pg_con: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""

    pg_cursor = pg_con.cursor()

    # create database
    sql = open("sql.ddl", "r").read()
    pg_cursor.execute(sql)

    for table in TABLES:

        # первый аргумент курсор, второй данные, мапим их в нужный нам dataclass
        sqlite_con.row_factory = lambda x, y: TABLES[table](*y)
        sqlite_cursor = sqlite_con.cursor()

        data = load_from_sqlite(
            sqlite_cursor,
            table,
        )
        save_data(table, data, pg_cursor)


if __name__ == "__main__":
    databases = DATABASES["default"]
    dsl = {
        "dbname": databases["NAME"],
        "user": databases["USER"],
        "password": databases["PASSWORD"],
        "host": databases["HOST"],
        "port": databases["PORT"],
    }
    with sqlite3.connect("db.sqlite") as sqlite_con, psycopg2.connect(
        **dsl, cursor_factory=DictCursor
    ) as pg_con:
        load_and_save_data(sqlite_con, pg_con)
