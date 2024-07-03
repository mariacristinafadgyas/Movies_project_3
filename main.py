from storage_json import StorageJson
from storage_csv import StorageCsv
from movie_app import MovieApp
import sys


def main():
    """Execution of the app and selection of the desired storage type"""

    arg1 = sys.argv[1]
    if ".json" in arg1 and len(arg1) > 4:
        storage = StorageJson(arg1)
    elif ".csv" in arg1 and len(arg1) > 4:
        storage = StorageCsv(arg1)
    else:
        print("\u001b[38;5;197;1mPlease insert a file name with the"
              " extension: \u001b[38;5;78;1m.json\u001b[0m "
              "\u001b[38;5;197;1mor\u001b[0m \u001b[38;5;78;1m.csv"
              "!\u001b[0m")

    movie_app = MovieApp(storage)
    movie_app.display_welcome_message()
    movie_app.run()


if __name__ == "__main__":
    main()
