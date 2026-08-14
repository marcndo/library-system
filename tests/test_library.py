import pytest
from src import Book, Member, Library

@pytest.fixture
def library():
    return Library()

@pytest.fixture
def sample_book():
    return Book("Discrete Mathematics", "John Lehman", "0001")

@pytest.fixture
def sample_member():
    return Member("Jack","M0001")

def test_add_book_stores_it(library, sample_book):
    library.add_book(sample_book)
    assert sample_book.isbn in library.books

def test_add_member_stores_it(library,sample_member):
    library.add_member(sample_member)
    assert sample_member.member_id in library.members

def test_lend_book_marks_book_borrowed(library, sample_book, sample_member):
    library.add_book(sample_book)
    library.add_member(sample_member)
    library.lend_book(isbn=sample_book.isbn, member_id=sample_member.member_id)
    assert sample_book.is_borrowed is True

def test_lend_book_adds_book_to_member_list(library, sample_book, sample_member):
    library.add_book(sample_book)
    library.add_member(sample_member)
    library.lend_book(isbn=sample_book.isbn, member_id=sample_member.member_id)
    assert sample_book in sample_member.borrowed_books

def test_lend_book_with_unknown_isbn_raises_error(library, sample_member, sample_book):
    library.add_member(sample_member)
    with pytest.raises(ValueError):
        library.lend_book(isbn=sample_book.isbn, member_id=sample_member.member_id)

def test_lend_book_with_unkwone_member_id_raises_error(library, sample_book, sample_member):
    library.add_book(sample_book)
    with pytest.raises(ValueError):
        library.lend_book(isbn=sample_book.isbn, member_id=sample_member.member_id)

def test_lend_book_twice_raises_error(library, sample_book, sample_member):
    library.add_book(sample_book)
    library.add_member(sample_member)
    library.lend_book(isbn=sample_book.isbn, member_id=sample_member.member_id)
    with pytest.raises(ValueError):
        library.lend_book(isbn=sample_book.isbn, member_id=sample_member.member_id)

    

