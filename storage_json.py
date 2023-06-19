from istorage import IStorage
import json


class StorageJson(IStorage):
    def __init__(self, file_path):
        self.file_path = file_path

    def load_data(self):
        """
        Load data from a JSON file.
        :return: dict: The loaded data as a dictionary.
        """
        with open(self.file_path, "r") as fileobj:
            data = json.load(fileobj)
            return data

    def list_movies(self):
        """
        List all the movies and their ratings
        """
        data = self.load_data()
        print(f"{len(data)} movies in total")
        for keys, value in data.items():
            print(f"{keys}: {value['Rating']}")

    def add_movie(self, title, year, rating, poster):
        """
       Add a new movie to the movie repository
        """
        data = self.load_data()

        data[title] = {"Rating": rating, "Year": year, "Poster": poster}

        with open(self.file_path, "w") as fileobj:
            json.dump(data, fileobj)

        print(f"Movie {title} successfully added")

    def delete_movie(self, title):
        """
        Delete a movie from the movie repository
        """
        data = self.load_data()

        del data[title]
        print(f"Movie {title} successfully deleted")

        with open(self.file_path, "w") as fileobj:
            json.dump(data, fileobj)

    def update_movie(self, title, notes):
        """
        Updates the notes of a movie in the movie repository
        """
        data = self.load_data()

        data[title]["Notes"] = notes
        print("Movie successfully updated")

        with open("data.json", "w") as fileobj:
            json.dump(data, fileobj)



