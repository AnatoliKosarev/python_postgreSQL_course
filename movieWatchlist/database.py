import sqlite3
import datetime

CREATE_MOVIE_TABLE = """CREATE TABLE IF NOT EXISTS movies (
    id INTEGER PRIMARY KEY,
    title TEXT,
    release_timestamp REAL
);
"""

CREATE_USERS_TABLE = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT);"

CREATE_WATCHED_TABLE = """CREATE TABLE IF NOT EXISTS watched (
    user_id INTEGER,
    movie_id INTEGER,
    FOREIGN KEY(user_id) REFERENCES users(id)
    FOREIGN KEY(movie_id) REFERENCES movies(id)
);
"""
CREATE_RELEASE_INDEX = "CREATE INDEX IF NOT EXISTS idx_release_timestamp ON movies (release_timestamp);"
INSERT_MOVIES = "INSERT INTO movies (title, release_timestamp) VALUES (?, ?);"
GET_USER_ID = "SELECT id FROM users WHERE username = ?;"
INSERT_WATCHED_MOVIE = "INSERT INTO watched (user_id, movie_id) VALUES (?, ?);"
INSERT_USER = "INSERT INTO users (username) VALUES (?);"
DELETE_MOVIE = "DELETE FROM movies WHERE title = ?;"
SELECT_ALL_MOVIES = "SELECT * FROM movies;"
SELECT_UPCOMING_MOVIES = "SELECT * FROM movies WHERE release_timestamp > ?;"
SELECT_WATCHED_MOVIES = """SELECT movies.* 
    FROM movies
    JOIN watched ON movies.id = watched.movie_id
    JOIN users ON watched.user_id = users.id 
    WHERE users.username = ?;"""
SEARCH_FOR_A_MOVIE = "SELECT * FROM movies WHERE title LIKE ?;"

connection = sqlite3.connect("data.db")


def create_tables():
    with connection:
        connection.execute(CREATE_MOVIE_TABLE)
        connection.execute(CREATE_USERS_TABLE)
        connection.execute(CREATE_WATCHED_TABLE)
        connection.execute(CREATE_RELEASE_INDEX)  # to speed up search by release_timestamp


def create_user(username: str):
    with connection:
        connection.execute(INSERT_USER, (username,))


def add_movie(title: str, release_timestamp: float):
    with connection:
        connection.execute(INSERT_MOVIES, (title, release_timestamp))


def get_movies(upcoming=False):
    with connection:
        cursor = connection.cursor()
        if upcoming:
            today_timestamp = datetime.datetime.today().timestamp()
            cursor.execute(SELECT_UPCOMING_MOVIES, (today_timestamp,))
        else:
            cursor.execute(SELECT_ALL_MOVIES)
        return cursor.fetchall()


def watch_movie(watcher_name: str, movie_id: int):
    with connection:
        cursor = connection.cursor()
        cursor.execute(GET_USER_ID, (watcher_name,))
        user_id = cursor.fetchone()[0]
        connection.execute(INSERT_WATCHED_MOVIE, (user_id, movie_id))


def get_watched_movies(watcher_name: str):
    with connection:
        cursor = connection.cursor()
        cursor.execute(SELECT_WATCHED_MOVIES, (watcher_name,))
        return cursor.fetchall()


def get_query_movies(title: str):
    with connection:
        cursor = connection.cursor()
        cursor.execute(SEARCH_FOR_A_MOVIE, (f"%{title}%",))
        return cursor.fetchall()


