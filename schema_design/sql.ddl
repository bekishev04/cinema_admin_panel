CREATE SCHEMA IF NOT EXISTS content;


CREATE TABLE IF NOT EXISTS content.film_work
(
    id            TEXT
        primary key,
    title         TEXT not null,
    description   TEXT,
    creation_date DATE,
    file_path     TEXT,
    rating        FLOAT,
    type          TEXT not null,
    created_at    timestamp with time zone,
    updated_at    timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.genre
(
    id          TEXT
        primary key,
    name        TEXT not null,
    description TEXT,
    created_at  timestamp with time zone,
    updated_at  timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.genre_film_work
(
    id           TEXT
        primary key,
    film_work_id TEXT not null,
    genre_id     TEXT not null,
    created_at   timestamp with time zone
);

create unique index film_work_genre
    on genre_film_work (film_work_id, genre_id);

CREATE TABLE IF NOT EXISTS content.person
(
    id         text
        primary key,
    full_name  text not null,
    created_at timestamp with time zone,
    updated_at timestam with time zone
);

CREATE TABLE IF NOT EXISTS content.person_film_work
(
    id           TEXT
        primary key,
    film_work_id TEXT not null,
    person_id    TEXT not null,
    role         TEXT not null,
    created_at   timestamp with time zone
);

create unique index film_work_person_role
    on person_film_work (film_work_id, person_id, role);



