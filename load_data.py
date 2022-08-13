import dataclasses
import sqlite3

import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extensions import cursor as _cursor
from psycopg2.extras import DictCursor, execute_values

from config.settings import DATABASES
from sqlite_to_postgres.utils_models import ListModels, ConverterModels


def load_from_sqlite(cursor: sqlite3.Cursor, model, n: int = 10_000):
    """Load data from sqlite with paginate"""

    fields = ConverterModels.get_fields(model)

    # cursor.execute(f"SELECT {fields} FROM {model.table} LIMIT {n} OFFSET {i};")
    cursor.execute(f"SELECT {fields} FROM {model.table}")

    rows = cursor.fetchmany(n)
    return rows


def save_data(model, rows, pg_cursor: _cursor):
    fields = ConverterModels.get_fields(model)

    vals = ConverterModels.prepare_data(rows)

    execute_values(
        pg_cursor,
        f"""
        INSERT INTO content.{model.table} ({fields})
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
    sql = open("schema_design/sql.ddl", "r").read()
    pg_cursor.execute(sql)

    for model in list(ListModels):

        # первый аргумент курсор, второй данные, мапим их в нужный нам dataclass
        sqlite_con.row_factory = lambda x, y: model(*y)
        sqlite_cursor = sqlite_con.cursor()

        data = load_from_sqlite(
            sqlite_cursor,
            model,
        )
        save_data(model, data, pg_cursor)


if __name__ == "__main__":
    databases = DATABASES["default"]
    dsl = {
        "dbname": databases["NAME"],
        "user": databases["USER"],
        "password": databases["PASSWORD"],
        "host": databases["HOST"],
        "port": databases["PORT"],
    }
    try:
        with sqlite3.connect(
            "sqlite_to_postgres/db.sqlite"
        ) as sqlite_con, psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_con:
            load_and_save_data(sqlite_con, pg_con)
    finally:
        sqlite_con.close()
        pg_con.close()
