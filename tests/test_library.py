import pytest
from src import Book, Member, Library
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from src.db_models import Base
from src.repositories import BookRepository, MemberRepository

@pytest.fixture
def library():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session = Session(engine)
    book_repo = BookRepository(session)
    member_repo = MemberRepository(session)
    return Library(book_repo, member_repo)

@pytest.fixture
def sample_book():
    return Book("Discrete Mathematics", "John Lehman", "0001")

@pytest.fixture
def sample_member():
    return Member("Jack","M0001")

def test_add_book_stores_it(library, sample_book):
    library.add_book(sample_book)
    found = library.book_repo.get_by_isbn(sample_book.isbn)
    assert found is not None
    assert found.title == sample_book.title

def test_add_member_stores_it(library,sample_member):
    library.add_member(sample_member)
    found = library.member_repo.get_by_member_id(sample_member.member_id)
    assert found.name is not None
    assert found.name == sample_member.name

def test_lend_book_marks_book_borrowed(library, sample_book, sample_member):
    library.add_book(sample_book)
    library.add_member(sample_member)
    library.lend_book(isbn=sample_book.isbn, member_id=sample_member.member_id)
    updated_book = library.book_repo.get_by_isbn(sample_book.isbn)
    assert updated_book.is_borrowed is True

def test_lend_book_adds_book_to_member_list(library, sample_book, sample_member):
    library.add_book(sample_book)
    library.add_member(sample_member)
    library.lend_book(isbn=sample_book.isbn, member_id=sample_member.member_id)
    updated_book = library.book_repo.get_by_isbn(sample_book.isbn)

    assert updated_book.is_borrowed is True

def test_lend_book_with_unknown_isbn_raises_error(library, sample_member, sample_book):
    library.add_member(sample_member)
    with pytest.raises(ValueError):
        library.lend_book(isbn=sample_book.isbn, member_id=sample_member.member_id)

def test_lend_book_with_unknown_member_id_raises_error(library, sample_book, sample_member):
    library.add_book(sample_book)
    with pytest.raises(ValueError):
        library.lend_book(isbn=sample_book.isbn, member_id=sample_member.member_id)

def test_lend_book_twice_raises_error(library, sample_book, sample_member):
    library.add_book(sample_book)
    library.add_member(sample_member)
    library.lend_book(isbn=sample_book.isbn, member_id=sample_member.member_id)
    with pytest.raises(ValueError):
        library.lend_book(isbn=sample_book.isbn, member_id=sample_member.member_id)

    

