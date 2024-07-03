from storage_json import StorageJson
from storage_csv import StorageCsv
from movie_app import MovieApp


def main():
    """Execution of the app and selection of the desired storage type"""
    # storage = StorageJson('movies_data.json')
    storage = StorageCsv('movies_data.csv')
    movie_app = MovieApp(storage)
    movie_app.display_welcome_message()
    movie_app.run()


if __name__ == "__main__":
    main()
