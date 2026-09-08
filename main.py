from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from src.repositories import BookRepository, MemberRepository, UserRepository
from src.library import Library
from pydantic import BaseModel
from src.book import Book
from src.user import User
from fastapi import Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError


app = FastAPI()
engine = create_engine("sqlite:///library.db")


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc:ValueError):
    return JSONResponse(
        status_code = 422,
        content = {"detail": str(exc)},
    )

@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc:IntegrityError):
    return JSONResponse(
        status_code=409,
        content = {"detail": "A resource with this value already exists."},
    )

class BookCreateRequest(BaseModel):
    title: str
    author: str
    isbn: str

class BookLendRequest(BaseModel):
    member_id: str
    isbn: str

class UserCreateRequest(BaseModel):
    user_name:str
    password: str


@app.get("/")
def read_root():
    return {"message": "Library System API"}

@app.get("/books")
def get_books():
    with Session(engine) as session:
        book_repo = BookRepository(session)
        books = book_repo.get_all()
        return [{"title":b.title, "author":b.author, "isbn":b.isbn, "is_borrowed":b.is_borrowed} for b in books]

@app.post("/books")
def create_books(request: BookCreateRequest):
    with Session(engine) as session:
        book_repo = BookRepository(session)
        book = Book(request.title, request.author, request.isbn)
        book_repo.add_book(book)
        session.commit()
        return {"title":book.title, "author":book.author, "isbn":book.isbn}


@app.post("/lend")
def lend_book(request: BookLendRequest):
    with Session(engine) as session:
        book_repo = BookRepository(session)
        member_repo = MemberRepository(session)
        library = Library(book_repo, member_repo)
        member_id = request.member_id
        book_isbn = request.isbn
        library.lend_book(isbn=book_isbn, member_id=member_id)
        session.commit()
        return {"message":f"book {book_isbn} successfully borrowed by {member_id}"}

@app.get("/books/{isbn}")
def get_book(isbn: str):
    with Session(engine) as session:
        book_repo = BookRepository(session)
        book = book_repo.get_by_isbn(isbn)
        if book is None:
            raise ValueError(f"No book with isbn {isbn} found.")
        return {"title":book.title, "author":book.author, "isbn":book.isbn, "borrowed":book.is_borrowed}

@app.post("/register")
def create_user(request:UserCreateRequest):
    with Session(engine) as session:
        user_repo = UserRepository(session)
        user = User.create(request.user_name, request.password)
        user_repo.add_user(user)
        session.commit()
    return {"user_name":user.user_name}



