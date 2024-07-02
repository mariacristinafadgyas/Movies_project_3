from abc import ABC, abstractmethod


class IStorage(ABC):
    """Storage interface that contains the definitions of the methods"""
    @abstractmethod
    def list_movies(self):
        """Abstract method for displaying the (movie) database """
        pass

    @abstractmethod
    def add_movie(self, title, year, rating, poster):
        """Abstract method to add an item (movie) to a database"""
        pass

    @abstractmethod
    def delete_movie(self, title):
        """Abstract method to delete an item (movie) from a database"""
        pass

    @abstractmethod
    def update_movie(self, title, rating):
        """Abstract method to update an item (movie) in a database"""
        pass
