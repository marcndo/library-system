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


def test_setting_valid_title_update():
    book = Book("Discrete Mathematics","John Lehman", "0001")
    book.title = "Mathematics for Computer Science"
    assert book.title == "Mathematics for Computer Science"

def test_setting_empty_title_raises_error():
    book = Book("Discrete Mathematics","John Lehman", "0001")
    with pytest.raises(ValueError):
        book.title = ""

def test_setting_whitespace_title_raises_error():
    book = Book("Discrete Mathematics","John Lehman", "0001")
    with pytest.raises(ValueError):
        book.title = " "

def test_non_string_title_raise_error():
    book = Book("Discrete Mathematics","John Lehman", "0001")
    with pytest.raises(ValueError):
        book.title = 34








