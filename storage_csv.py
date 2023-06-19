from istorage import IStorage


class StorageCsv(IStorage):
    def __init__(self, file_path):
        self.file_path = file_path

    def load_data(self):
        """
        Load movie data from a CSV file and return it as a dictionary
        :return:
        """
        with open(self.file_path, "r") as fileobj:
            data = fileobj.readlines()
            movie_dict = {}
            for movie in data[1:]:
                split_movie = movie.strip().split(",")
                if len(split_movie) == 4:
                    title, rating, year, poster = split_movie
                    movie_dict.update({title: {"Rating": float(rating), "Year": int(year), "Poster": poster}})
                else:
                    title, rating, year, poster, note = split_movie
                    movie_dict.update({title: {"Rating": float(rating), "Year": int(year),"Poster": poster, "Note": note}})
            return movie_dict

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
        with open(self.file_path, "r") as fileobj:
            data = fileobj.read()

        with open(self.file_path, "w") as fileobj:
            fileobj.write(f"{data.strip()}\n{title},{rating},{year},{poster}")
            print("Movie added successfully")

    def delete_movie(self, title):
        """
        Delete a movie from the movie repository
        """
        with open(self.file_path, "r") as fileobj:
            data = fileobj.readlines()
        new_data = ""
        for line in data:
            if title not in line:
                new_data += line
        with open(self.file_path, "w") as fileobj:
            fileobj.write(new_data)
            print("Movie deleted successfully")

    def update_movie(self, title, notes):
        """
       Updates the notes of a movie in the movie repository
        """
        with open(self.file_path, "r") as fileobj:
            data = fileobj.readlines()

        updated_lines = []
        for lines in data:
            row = lines.strip().split(",")
            if row[0] == title:
                if len(row) > 4:
                    row[4] = notes
                else:
                    row.append(notes)
            updated_line = ",".join(row)
            updated_lines.append(updated_line)
        print("Movie successfully updated")

        with open(self.file_path, "w") as fileobj:
            fileobj.write("\n".join(updated_lines))

