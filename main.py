from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from src.repositories import BookRepository, MemberRepository
from src.library import Library
from pydantic import BaseModel
from src.book import Book

app = FastAPI()
engine = create_engine("sqlite:///library.db")

@app.get("/")
def read_root():
    return {"message": "Library System API"}

@app.get("/books")
def get_books():
    with Session(engine) as session:
        book_repo = BookRepository(session)
        books = book_repo.get_all()
        return [{"title":b.title, "author":b.author, "isbn":b.isbn, "is_borrowed":b.is_borrowed} for b in books]


class BookCreateRequest(BaseModel):
    title: str
    author: str
    isbn: str

@app.post("/books")
def create_books(request: BookCreateRequest):
    with Session(engine) as session:
        book_repo = BookRepository(session)
        book = Book(request.title, request.author, request.isbn)
        book_repo.add_book(book)
        session.commit()
        return {"title":book.title, "author":book.author, "isbn":book.isbn}
