from istorage import IStorage
import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('API_KEY')

REQUEST_URL = "http://www.omdbapi.com/?apikey=" + API_KEY + "&t="


class StorageJson(IStorage):
    """Implements the IStorage interface and saves the data in a JSON file"""

    def __init__(self, file_path):
        self.file_path = file_path

    def read_data(self):
        """Reads  the movies database"""
        try:
            with open(self.file_path, "r") as fileobj:
                movies_database = json.loads(fileobj.read())
            return movies_database
        except FileNotFoundError:
            with open(self.file_path, mode="w") as file:
                file.write("")
            return []
        except json.JSONDecodeError: # To handle cases where the file contents are not valid JSON.
            return []
        except Exception as e:
            print(f"\u001b[38;5;197;1mAn error occurred: {e}\u001b[0m")
            return []

    def sync_database(self, movies_database):
        """Synchronizes the movies database"""
        updated_database = json.dumps(movies_database)
        with open(self.file_path, 'w') as fileobj:
            fileobj.write(updated_database)

    def list_movies(self):
        """Displays the movies in the database"""
        movies_database = self.read_data()
        print()
        print(f"\u001b[38;5;208;1m{len(movies_database)} movies in total\u001b[0m")
        for movie in movies_database:
            print(f"\u001b[38;5;38;1m{movie['title']}: \u001b[38;5;160;1m{movie['rating']}\u001b[0m, released in \u001b["
                f"38;5;28;1m{movie['year_of_release']}\u001b[0m")

    def add_movie(self):
        """Adds a new movie to the movies' database.
        Loads the information from the JSON file, adds the movie,
        and synchronizes the database.
        """

        movies_database = self.read_data()
        while True:
            try:
                title = input("\u001b[35mPlease enter a new movie: \u001b[0m")
                search_rq_url = REQUEST_URL + title
                movie_info = requests.get(search_rq_url)
                res_movie_info = movie_info.json()
                add_title = res_movie_info["Title"]

                movie_exists = False
                for movie in movies_database:
                    if add_title.lower() == movie['title'].lower():
                        movie_exists = True
                        print(f"\u001b[38;5;197;1mMovie {add_title} already exist!\u001b[0m")
                        break
                if not movie_exists:
                    break
            except ConnectionError:
                print("\u001b[38;5;197;1mPlease check your internet connection!\u001b[0m")
            except KeyError:
                print("\u001b[38;5;197;1mPlease provide an actual film name!\u001b[0m")

        rating_str = res_movie_info["Ratings"][0]["Value"]
        add_rating = float(rating_str.split('/')[0])
        add_year = res_movie_info["Year"]
        add_poster = res_movie_info["Poster"]
        add_movie_imdb_id = res_movie_info["imdbID"]
        add_country = res_movie_info["Country"]

        new_movie = {
            "title": add_title,
            "rating": add_rating,
            "year_of_release": add_year,
            "poster": add_poster,
            "note": "",
            "imdbID": add_movie_imdb_id,
            "country": add_country
        }

        movies_database.append(new_movie)
        print(f"\u001b[36mMovie {add_title} successfully added")
        print()

        self.sync_database(movies_database)
        return movies_database


    def delete_movie(self):
        """Deletes a movie from the movies' database.
           Loads the information from the JSON file, deletes the movie,
           and synchronizes the database."""
        movies_database = self.read_data()
        movie_to_be_deleted = input("\u001b[35mPlease select a movie to be deleted: \u001b[0m")
        movie_found = False
        for i in range(len(movies_database)):
            if movies_database[i]['title'].lower() == movie_to_be_deleted.lower():
                del movies_database[i]
                print(
                    f"\u001b[36mThe movie \u001b[38;5;160m{movie_to_be_deleted.capitalize()}\u001b[0m \u001b[36m "
                    f"successfully deleted.\u001b[0m")
                movie_found = True
                break
        if not movie_found:
            print("\u001b[38;5;197;1mError! The movie is not part of the database!\u001b[0m")
        self.sync_database(movies_database)
        return movies_database

    def update_movie(self):
        """Updates the movies database"""
        movies_database = self. read_data()
        movie_to_be_updated = input("\u001b[35mPlease select a movie to be updated: \u001b[0m")

        movie_found = False
        for i in range(len(movies_database)):
            if movies_database[i]['title'].lower() == movie_to_be_updated.lower():
                movies_database[i]['note'] = input("\u001b[38;5;49;1mPlease enter movie note 🙄: \u001b[0m")
                print(f"\u001b[38;5;181;1mThe movie \u001b[38;5;213;1m"
                      f"{movie_to_be_updated}\u001b[38;5;181;1m was successfully updated.\u001b[0m")
                movie_found = True
                break
        if not movie_found:
            print("\u001b[38;5;197;1mError! The movie you are trying to update is not part of the database!\u001b[0m")
        self.sync_database(movies_database)
        return movies_database

# storage = StorageJson('movies.json')
# storage.list_movies()
# storage.add_movie()
# storage.delete_movie("The Guilty")
# storage.update_movie("The Shawshank Redemption")
