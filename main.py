from storage_json import StorageJson
from movie_app import MovieApp


def main():
    storage = StorageJson('movies.json')
    movie_app = MovieApp(storage)
    movie_app.display_welcome_message()
    movie_app.run()


if __name__ == "__main__":
    main()
