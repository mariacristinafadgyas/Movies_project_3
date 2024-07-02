import random
import matplotlib.pyplot as plt
import difflib
import country_converter as coco
import sys


class MovieApp:
    """This class support multiple methods"""

    def __init__(self, storage):
        self._storage = storage

    def _command_list_movies(self):
        """Displays the movies structure"""
        movies = self._storage.list_movies()
        return movies

    def _command_add_movie(self):
        """Adds a movie to the movies structure"""
        self._storage.add_movie()
        self._storage.list_movies()

    def _command_delete_movie(self):
        """Deletes a movie from the movies structure"""
        self._storage.delete_movie()
        self._storage.list_movies()

    def _command_update_movie(self):
        """Updates the movies structure"""
        self._storage.update_movie()
        self._storage.list_movies()

    def _command_movie_stats(self):
        """Displays the movies statistics"""
        movies_database = self._storage.read_data()
        ratings_sum = 0
        ratings_list = []
        for movie in movies_database:
            ratings_sum += movie['rating']
            ratings_list.append(movie['rating'])
        average_rating = ratings_sum / len(movies_database)
        print("\u001b[38;5;129;1mAverage rating: \u001b[0m", round(average_rating, 2))

        ratings_list.sort()
        length_of_values_list = len(ratings_list)
        if length_of_values_list % 2 == 0:
            median_rating = (ratings_list[length_of_values_list // 2 - 1] + ratings_list[
                length_of_values_list // 2]) / 2
        else:
            median_rating = ratings_list[length_of_values_list // 2]
        print("\u001b[38;5;129;1mMedian rating: \u001b[0m", median_rating)

        best_movie = max(movies_database, key=lambda x: x['rating'])
        print(f"\u001b[38;5;220;1mBest movie: \u001b[36m{best_movie['title']}, {best_movie['rating']}, "
              f"{best_movie['year_of_release']}\u001b[0m")

        worst_movie = min(movies_database, key=lambda x: x['rating'])
        print(f"\u001b[38;5;220;1mWorst movie: \u001b[36m{worst_movie['title']}, {worst_movie['rating']}, "
              f"{worst_movie['year_of_release']}\u001b[0m")

        return average_rating, median_rating, best_movie['title'], worst_movie['title']

    def _command_random_movie(self):
        """Displays a random movie to the screen"""
        movies_database = self._storage.read_data()
        sel_random_movie = random.choice(movies_database)
        print(f"\u001b[36mYour movie for tonight: \u001b[38;5;202;1m{sel_random_movie['title']},"
              f"\u001b[0m \u001b[36mit's rated \u001b[38;5;220;1m{sel_random_movie['rating']}\u001b[0m")
        return sel_random_movie

    def _command_search_movie(self):
        """Searches a movie using fuzzy search"""
        movies_database = self._storage.read_data()
        matches = []
        similarity_cutoff = 0.5
        search_key = input("\u001b[35mEnter part of movie name: ")
        for movie in movies_database:
            ratio = difflib.SequenceMatcher(None, search_key, movie['title']).ratio()
            if ratio >= similarity_cutoff:
                matches.append((movie['title'], movie['rating']))
        if not matches:
            print("\u001b[31m\u001b[1mNo matches found.\u001b[0m")
        # print(matches)
        for movie, rating in matches:
            print(f"\u001b[38;5;208;1m{movie}, {rating}\u001b[0m")
        return matches

    def _command_sort_by_rating(self):
        """Sorts the movies by rating"""
        movies_database = self._storage.read_data()
        sorted_movies = sorted(movies_database, key=lambda d: d['rating'], reverse=True)
        for movie in sorted_movies:
            print(f"\u001b[36m{movie['title']}: \u001b[38;5;220;1m{movie['rating']}\u001b[0m")
        return sorted_movies

    def _command_rating_histogram(self):
        """Saves to file the movies histogram"""
        movies_database = self._storage.read_data()
        ratings = []
        for movie in movies_database:
            ratings.append(movie['rating'])
        plt.figure(figsize=(10, 5))
        plt.hist(ratings, color='pink', width=0.4)
        plt.show()
        plt.savefig('Ratings_chart.png')

    def _generate_website(self):
        """Receives the output string of the previous function and the path of the HTML
             template as parameters and generates the HTML file"""

        def get_country_flag(movie_country):
            """Retrieves country codes"""
            if "," in movie_country:
                first_country = movie_country.split(',')[0].strip()
            else:
                first_country = movie_country.strip()

            iso2_country_code = coco.convert(names=first_country, to='ISO2')  # Conversion to ISO2 code

            return iso2_country_code

        def serialize_movie(movie_obj):
            """Receives a movie object as parameter and returns a string containing
            the desired data for a single movie"""
            output = ''
            output += '<li>'
            output += '<div class="movie">'
            output += (f'<a href="https://www.imdb.com/title/{movie_obj["imdbID"]}/">'
                       f'<img class="movie-poster" src={movie_obj["poster"]}/></a>')
            output += f'<div class="movie-title">{movie_obj["title"]}</div>'
            output += f'<div class="movie-year">{movie_obj["year_of_release"]}</div>'
            output += f'<div class="movie-rating">Rating: {movie_obj["rating"]}</div>'
            output += (f'<img class="movie-country" src="https://flagsapi.com/'
                       f'{get_country_flag(movie_obj["country"])}/shiny/32.png" >')
            output += f'<div class="movie-note">{movie_obj["note"]}</div>'
            output += '</div>'
            output += '</li>'
            return output

        def serialize_movies():
            """Receives a list of dictionaries containing movies data as parameter and returns
            a string containing the desired data for the whole list of movies"""
            movies_database = self._storage.read_data()
            output = ''
            for movie in movies_database:
                output += serialize_movie(movie)
            return output

        replaced_output = ""
        with open("index_template.html", "r") as fileobj:
            template = fileobj.read()

        if "__TEMPLATE_TITLE__" in template:
            replaced_output = template.replace("__TEMPLATE_TITLE__", "My Favorite Movie App")

        if "__TEMPLATE_MOVIE_GRID__" in template:
            replaced_output = replaced_output.replace("__TEMPLATE_MOVIE_GRID__", serialize_movies())

        with open("index.html", "w") as file_output:
            file_output.write(replaced_output)

        print("\u001b[36mWebsite was generated successfully.\u001b[0m")

    @staticmethod
    def display_welcome_message():
        print('''\u001b[38;5;54;1m ********** My Movies Database **********

        Menu:
        0. Exit
        1. List movies
        2. Add movie
        3. Delete movie
        4. Update movie
        5. Stats
        6. Random movie
        7. Search movie
        8. Movies sorted by rating
        9. Create Rating Histogram
        10. Generate Website
        \u001b[0m''')

    def run(self):
        """Displays the welcome message and asks the user to select an option"""
        while True:
            try:
                user_choice = int(input("\u001b[35mEnter choice (0-10): \u001b[0m"))
                if isinstance(user_choice, int):
                    break
            except ValueError:
                print("\u001b[38;5;196;1mPlease enter a number between 0 and 10.\u001b[0m")
        if user_choice == 0:
            print("\u001b[38;5;87;1mBye!\u001b[0m")
            sys.exit()
        elif user_choice == 1:
            self._command_list_movies()
        elif user_choice == 2:
            self._command_add_movie()
        elif user_choice == 3:
            self._command_delete_movie()
        elif user_choice == 4:
            self._command_update_movie()
        elif user_choice == 5:
            self._command_movie_stats()
        elif user_choice == 6:
            self._command_random_movie()
        elif user_choice == 7:
            self._command_search_movie()
        elif user_choice == 8:
            self._command_sort_by_rating()
        elif user_choice == 9:
            self._command_rating_histogram()
        elif user_choice == 10:
            self._generate_website()
        else:
            print("\u001b[31m\u001b[1mPlease select a number between 0 and 10.\u001b[0m")

        print()
        input("\u001b[33mPress Enter to continue...")

        while True:
            print()
            search_again = input('\u001b[35mDo you want to select another option (Y/N)?\u001b[0m')
            if search_again == 'Y' or search_again == 'y':
                self.display_welcome_message()
                self.run()
            elif search_again == 'N' or search_again == 'n':
                sys.exit()
            else:
                print('\u001b[31m\u001b[1mSelect Y for Yes or, N for No\u001b[0m')
