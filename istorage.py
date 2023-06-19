from abc import ABC, abstractmethod


class IStorage(ABC):
    """
    Abstract base class serves as an interface for movie app
    """
    @abstractmethod
    def list_movies(self):
        pass

    @abstractmethod
    def add_movie(self, title, year, rating, poster):
        pass

    @abstractmethod
    def delete_movie(self, title):
        pass

    @abstractmethod
    def update_movie(self, title, notes):
        pass
