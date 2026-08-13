from src.member import Member
from src.book import Book

class Library:
    def __init__(self):
        self.books = {}
        self.members = {}

    def add_book(self, book: Book):
        self.books[book.isbn] = book

    def add_member(self, member: Member):
        self.members[member.member_id] = member

    def lend_book(self,*,member_id, isbn):
        book = self.books.get(isbn)
        member = self.members.get(member_id)
        if not member:
            raise ValueError("Member not registered")
        if not book:
            raise ValueError("Book not available")
        book.borrow()
        member.borrowed_books.append(book)