from src.member import Member
from src.book import Book
from src.repositories import BookRepository, MemberRepository
from src.logger import get_logger

logger = get_logger(__name__)

class Library:
    def __init__(self, book_repo:BookRepository, member_repo:MemberRepository):
        self.book_repo = book_repo
        self.member_repo = member_repo

    def add_book(self, book: Book):
        self.book_repo.add_book(book)
        logger.info(f"Book added: {book.title} (ISBN:{book.isbn})")

    def add_member(self, member: Member):
        self.member_repo.add_member(member)

    def lend_book(self,*,member_id, isbn):
        book = self.book_repo.get_by_isbn(isbn)
        member = self.member_repo.get_by_member_id(member_id)
        if not member:
            logger.warning(f"Lend failed: member {member_id} not registered")
            raise ValueError("Member not registered")
        if not book:
            logger.warning(f"Lend failed: book with ISBN {isbn} not available")
            raise ValueError("Book not available")
        try:
            book.borrow()
        except ValueError as e:
            logger.warning(f"Lend failed: {e}")
            raise 
        self.book_repo.update_book(book, member_id=member_id)
        logger.info(f"Book lent: {book.title} (ISBN: {book.isbn}) to member {member_id}")
