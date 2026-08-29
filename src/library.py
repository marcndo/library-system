from src.member import Member
from src.book import Book
from src.repositories import BookRepository, MemberRepository


class Library:
    def __init__(self, book_repo:BookRepository, member_repo:MemberRepository):
        self.book_repo = book_repo
        self.member_repo = member_repo

    def add_book(self, book: Book):
        self.book_repo.add_book(book)

    def add_member(self, member: Member):
        self.member_repo.add_member(member)

    def lend_book(self,*,member_id, isbn):
        book = self.book_repo.get_by_isbn(isbn)
        member = self.member_repo.get_by_member_id(member_id)
        if not member:
            raise ValueError("Member not registered")
        if not book:
            raise ValueError("Book not available")
        book.borrow()
        self.book_repo.update_book(book, member_id=member_id)
