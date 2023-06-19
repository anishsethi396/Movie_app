from storage_json import StorageJson
from movie_app import MovieApp
from storage_csv import StorageCsv

storage1 = StorageJson('data.json')
storage2 = StorageCsv('data.csv')

movies = MovieApp(storage1)
movies.run()
