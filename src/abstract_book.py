from abc import ABC, abstractmethod

class AbstractBook(ABC):

    @abstractmethod
    def borrow(self):
        pass

    @abstractmethod
    def return_book(self):
        pass