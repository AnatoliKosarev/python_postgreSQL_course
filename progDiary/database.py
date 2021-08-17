import sqlite3

connection = sqlite3.connect("data.db")
connection.row_factory = sqlite3.Row  # returns cursor in the form of a dictionary (runs slower then tuple by default)


def create_table():
    with connection:  # context manager commits queries and closes connection automatically
        connection.execute("CREATE TABLE IF NOT EXISTS entries(content TEXT, date TEXT);")
        # connection.commit()  # if used without context manager
        # connection.close()  # if used without context manager


def add_entry(entry_content: str, entry_date: str):
    with connection:
        connection.execute("INSERT INTO entries VALUES (?, ?);", (entry_content, entry_date))  # to avoid SQL injections f-string not used


def get_entry():  # no context manager used because function doesn't change db data, so no commit or rollback needed
    cursor = connection.execute("SELECT * FROM entries;")
    return cursor  # returns cursor which gives a new row in the form of a tuple when used in a loop


def search_for_entry(entry_date: str):
    cursor = connection.execute("SELECT * FROM entries WHERE date = ?;", (entry_date,))
    return cursor
