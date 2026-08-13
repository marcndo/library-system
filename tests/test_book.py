import pytest
from src import Book

def test_borrow_marks_book_borrowed():
    book = Book("Discrete Mathematics","John Lehman", "0001")
    book.borrow()
    assert book.is_borrowed == True, "Book should be marked as borrowed"


def test_borrow_twice_raise_error():
    book = Book("Discrete Mathematics","John Lehman", "0001")
    book.borrow()
    with pytest.raises(ValueError):
        book.borrow()
