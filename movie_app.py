import random
import requests
from storage_json import StorageJson

API_KEY = 79153533


class MovieApp:
    def __init__(self, storage):
        self.storage = storage

    def _command_list_movies(self):
        """
        Handle the command to list all movies.
        :return:
        """
        self.storage.list_movies()
        self._wait_response()

    def _command_add_movie(self):
        """
        Handle the command to add a movie
        :return:
        """
        new_movie = input("Enter new movie name:")
        api_url = f'http://www.omdbapi.com/?apikey={API_KEY}&t={new_movie}'
        data = self.storage.load_data()

        if new_movie.lower() in map(str.lower, data.keys()):
            print(f'{new_movie} already exists')
            self._wait_response()
            return

        try:
            response = requests.get(api_url)
            api_data = response.json()
            title = api_data["Title"]
            year = api_data["Year"]
            rating = api_data["imdbRating"]
            poster = api_data["Poster"]

            self.storage.add_movie(title, year, rating, poster)

        except Exception as e:
            print(e)
        self._wait_response()

    def _command_delete_movie(self):
        """
        Handle the command to delete the movie
        :return:
        """
        data = self.storage.load_data()
        delete = input("Enter movie to remove: ")
        if delete.lower() not in map(str.lower, data.keys()):
            print(f"{delete} doesn't exist")
            self._wait_response()

        else:
            movie_to_delete = None
            for key in data.keys():
                if delete.lower() in key.lower():
                    movie_to_delete = key
                    break
            self.storage.delete_movie(movie_to_delete)
            self._wait_response()

    def _command_update_movie(self):
        """
        Handle the command to update notes of a movie
        :return:
        """
        data = self.storage.load_data()
        update = input("Enter movie name: ")
        if update.lower() not in map(str.lower, data.keys()):
            print(f"{update} doesn't exist")
            self._wait_response()
        else:
            new_notes = input("Enter movie notes: ")
            movie_to_update = None
            for key in data.keys():
                if update.lower() in key.lower():
                    movie_to_update = key
                    break
            self.storage.update_movie(movie_to_update, new_notes)
            self._wait_response()

    # @staticmethod
    def update_html_file(self):
        """
        Takes a movie object and returns a serialized string in
        HTML format that can be used to display movies on a web page.
        """
        data = self.storage.load_data()
        output = " "
        for keys, values in data.items():
            output += '<li>'
            output += '<div class="movie">'
            output += f'<img class="movie-poster" src="{values["Poster"]}"/>'
            output += f'<div class="movie-title">{keys}</div>'
            output += f'<div class="movie-year">{values["Year"]}</div>'
            output += "</div>"
            output += "</li>"
        return output

    def generate_website(self):
        """Generate the movie application website. Reads the index template file,
         replaces placeholders with generated content.
        :return:
        """
        with open("static/index_template.html", "r") as fileobj:
            new_data = fileobj.read()
            output = self.update_html_file()
            new_title = "Anish's Movie Application"
            new_file = new_data.replace("__TEMPLATE_TITLE__", new_title).replace("__TEMPLATE_MOVIE_GRID__", output)

        with open("static/html_file.html", "w") as fileobj:
            fileobj.write(new_file)

        print("Successfully generated the website.")
        self._wait_response()

    @staticmethod
    def _wait_response():
        input("Press enter to continue:")

    def _stats(self):
        """
        Calculate and print statistics based on movie ratings.
        """
        data = self.storage.load_data()
        list_of_rating = []
        for movie, details in data.items():
            list_of_rating.append(float(details["Rating"]))
        values_list = list_of_rating
        values_len = len(values_list)

        # average rating
        values_sum = sum(values_list)
        average = values_sum / values_len
        print(f"Average rating: {average}")

        # median rating
        sorted_values = sorted(values_list)
        if values_len % 2 == 0:
            median = (sorted_values[values_len // 2 - 1] + sorted_values[values_len // 2]) / 2
        else:
            median = sorted_values[values_len // 2]
        print(f"Median rating: {median}")

        # best movie
        best_movie = max(values_list)
        for key, value in data.items():
            if float(value["Rating"]) == best_movie:
                print(f"Best movie: {key}, {value['Rating']}")

        # worst movie
        worst_movie = min(values_list)
        for key, value in data.items():
            if float(value["Rating"]) == worst_movie:
                print(f"Worst movie: {key}, {value['Rating']}")

        self._wait_response()

    def _random_movie(self):
        """
        Prints a random movie from the movie's object.
        """
        data = self.storage.load_data()
        random_key = random.choice(list(data.keys()))
        print(f"Your movie for tonight: {random_key}, it's rated {data[random_key]['Rating']}")
        self._wait_response()

    def _search_movie(self):
        """
        Search for movie by a given part of the movie name.
        """
        data = self.storage.load_data()
        search = input("Enter part of movie name:")
        found_movie = []

        for key in data.keys():
            if search.lower() in key.lower():
                found_movie.append(key)

        if found_movie:
            for movie in found_movie:
                print(f"{movie}, {data[movie]['Rating']} ")
        else:
            print(f"Movie {search} does not exist.")
        self._wait_response()

    def _movies_sort(self):
        """
        Sort movies in descending order by their rating.
        """
        data = self.storage.load_data()
        sorted_movies = sorted(data.items(), key=lambda x: x[1]["Rating"], reverse=True)
        for movie, details in sorted_movies:
            print(f"{movie}, {details['Rating']}")
        self._wait_response()

    def run(self):
        while True:
            user_input = input("""
********** My Movies Database **********

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
9. Generate Website

Enter choice (0-9): """)

            if user_input == "0":
                print("Bye!")
                return
            elif user_input == "1":
                self._command_list_movies()
            elif user_input == "2":
                self._command_add_movie()
            elif user_input == "3":
                self._command_delete_movie()
            elif user_input == "4":
                self._command_update_movie()
            elif user_input == "5":
                self._stats()
            elif user_input == "6":
                self._random_movie()
            elif user_input == "7":
                self._search_movie()
            elif user_input == "8":
                self._movies_sort()
            elif user_input == "9":
                self.generate_website()

