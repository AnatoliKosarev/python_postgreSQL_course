import datetime
import database

menu = """Please select one of the following options:
1) Add new movie.
2) View upcoming movies.
3) View all movies.
4) Watch a movie.
5) View watched movies.
6) Create a new user.
7) Find a movie by title.
8) Exit.

Your selection: """

welcome = "Welcome to the watchlist app!"

print(welcome)
database.create_tables()


def prompt_add_movie():
    title = input("Movie title: ")
    release_date = input("Release date (dd-mm-YYYY): ")
    parsed_date = datetime.datetime.strptime(release_date, "%d-%m-%Y")
    timestamp = parsed_date.timestamp()
    database.add_movie(title, timestamp)


def print_movie_list(heading, movies):
    print(f"--{heading} movies--")
    for _id, title, release_date in movies:
        movie_date = datetime.datetime.fromtimestamp(release_date)
        human_date = movie_date.strftime("%d %b %Y")
        print(f"{_id}: {title} on {human_date}")
    print("----\n")


def prompt_watch_movie():
    watcher_name = input("Enter your name: ")
    movie_id = int(input("Enter movie id you've watched: "))
    database.watch_movie(watcher_name, movie_id)


def prompt_create_user():
    username = input("Enter your username: ")
    database.create_user(username)


def prompt_show_watched_movies():
    watcher_name = input("Enter your name: ")
    movies = database.get_watched_movies(watcher_name)
    if movies:
        print_movie_list(f"{watcher_name}'s watched", movies)
    else:
        print(f"{watcher_name}'s watched movie list is empty.")


def prompt_movie_search():
    title = input("Enter movie title: ")
    movies = database.get_query_movies(title)
    if movies:
        print_movie_list("Searched", movies)
    else:
        print("No movies where found.")


while (user_selection := input(menu)) != "8":
    if user_selection == "1":
        prompt_add_movie()
    elif user_selection == "2":
        movies = database.get_movies(upcoming=True)
        if movies:
            print_movie_list("Upcoming", movies)
        else:
            print("No upcoming movies yet.")
    elif user_selection == "3":
        movies = database.get_movies()
        print_movie_list("All", movies)
    elif user_selection == "4":
        prompt_watch_movie()
    elif user_selection == "5":
        prompt_show_watched_movies()
    elif user_selection == "6":
        prompt_create_user()
    elif user_selection == "7":
        prompt_movie_search()
    else:
        print("Invalid input, please try again!")