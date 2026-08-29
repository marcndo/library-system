from sqlalchemy import select
from src.db_models import BookORM, MemberORM
from src.book import Book
from src.member import Member




class BookRepository:
    def __init__(self, session):
        self.session = session

    def get_by_isbn(self, isbn):
        stmt = select(BookORM).where(BookORM.isbn==isbn)
        orm_book =  self.session.scalars(stmt).first()
        if not orm_book:
            return 
        return self._to_domain(orm_book)

    def _to_domain(self,orm_book:BookORM):
        book = Book(orm_book.title, orm_book.author, orm_book.isbn)
        if orm_book.is_borrowed:
            book.borrow()
        return book


    
    def add_book(self, book: Book):
        orm_book = self._to_orm(book)
        self.session.add(orm_book)
        self.session.flush()

    def _to_orm(self, book:Book):
        return BookORM(
            title = book.title,
            author = book.author,
            isbn = book.isbn,
            is_borrowed = book.is_borrowed,
        )


    def get_all(self):
        books = []
        for orm_book in  self.session.scalars(select(BookORM)).all():
            books.append(self._to_domain(orm_book))
        return books

class MemberRepository:
    def __init__(self, session):
        self.session = session

    def get_by_member_id(self, member_id):
        stmt = select(MemberORM).where(MemberORM.member_id==member_id)
        orm_member = self.session.scalars(stmt).first()
        if not orm_member:
            return
        return self._to_domain(orm_member)

    def _to_domain(self, member:MemberORM):
        member = Member(member.name, member.member_id)
        return member



    def add_member(self, member: Member):
        orm_member = self._to_orm(member)
        self.session.add(orm_member)
        self.session.flush()


    def _to_orm(self, member:Member):
        return MemberORM(
            name = member.name,
            member_id = member.member_id,
        )


    def get_all(self):
        members = []
        for orm_member in self.session.scalars(select(MemberORM)).all():
            members.append(self._to_domain(orm_member))
        return members

