import os
import psycopg2
import datetime

from dotenv import load_dotenv

load_dotenv()

CREATE_MOVIE_TABLE = """CREATE TABLE IF NOT EXISTS movies (
    id SERIAL PRIMARY KEY,
    title TEXT,
    release_timestamp REAL
);
"""

CREATE_USERS_TABLE = "CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, username TEXT);"

CREATE_WATCHED_TABLE = """CREATE TABLE IF NOT EXISTS watched (
    user_id INTEGER,
    movie_id INTEGER,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(movie_id) REFERENCES movies(id)
);
"""
CREATE_RELEASE_INDEX = "CREATE INDEX IF NOT EXISTS idx_release_timestamp ON movies (release_timestamp);"
INSERT_MOVIES = "INSERT INTO movies (title, release_timestamp) VALUES (%s, %s);"
GET_USER_ID = "SELECT id FROM users WHERE username = %s;"
INSERT_WATCHED_MOVIE = "INSERT INTO watched (user_id, movie_id) VALUES (%s, %s);"
INSERT_USER = "INSERT INTO users (username) VALUES (%s);"
DELETE_MOVIE = "DELETE FROM movies WHERE title = %s;"
SELECT_ALL_MOVIES = "SELECT * FROM movies;"
SELECT_UPCOMING_MOVIES = "SELECT * FROM movies WHERE release_timestamp > %s;"
SELECT_WATCHED_MOVIES = """SELECT movies.* 
    FROM movies
    JOIN watched ON movies.id = watched.movie_id
    JOIN users ON watched.user_id = users.id 
    WHERE users.username = %s;"""
SEARCH_FOR_A_MOVIE = "SELECT * FROM movies WHERE title LIKE %s;"

connection = psycopg2.connect(os.environ["DATABASE_URL"])


def create_tables():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_MOVIE_TABLE)
            cursor.execute(CREATE_USERS_TABLE)
            cursor.execute(CREATE_WATCHED_TABLE)
            cursor.execute(CREATE_RELEASE_INDEX)  # to speed up search by release_timestamp


def create_user(username: str):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_USER, (username,))


def add_movie(title: str, release_timestamp: float):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_MOVIES, (title, release_timestamp))


def get_movies(upcoming=False):
    with connection:
        with connection.cursor() as cursor:
            if upcoming:
                today_timestamp = datetime.datetime.today().timestamp()
                cursor.execute(SELECT_UPCOMING_MOVIES, (today_timestamp,))
            else:
                cursor.execute(SELECT_ALL_MOVIES)
            return cursor.fetchall()


def watch_movie(watcher_name: str, movie_id: int):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(GET_USER_ID, (watcher_name,))
            user_id = cursor.fetchone()[0]
            cursor.execute(INSERT_WATCHED_MOVIE, (user_id, movie_id))


def get_watched_movies(watcher_name: str):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_WATCHED_MOVIES, (watcher_name,))
            return cursor.fetchall()


def get_query_movies(title: str):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SEARCH_FOR_A_MOVIE, (f"%{title}%",))
            return cursor.fetchall()


