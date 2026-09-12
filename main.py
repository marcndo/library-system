from fastapi import FastAPI,Depends, HTTPException, status
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
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm,  OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError

import jwt

app = FastAPI()
engine = create_engine("sqlite:///library.db")

SECRET_KEY ="6bb3500c8d8dbdf35e7b4a5a8d4a995cdb6c9bd8a2efca7db2f181c6458ebefc"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception

    with Session(engine) as session:
        user_repo = UserRepository(session)
        user = user_repo.get_user_by_name(username)
        if user is None:
            raise credentials_exception
        return user

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
def lend_book(request: BookLendRequest,current_user: User = Depends(get_current_user)):
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


def create_access_token(user_name: str):
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode = {"sub": user_name, "exp": expire}
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    with Session(engine) as session:
        user_repo = UserRepository(session)
        user_name = form_data.username
        user = user_repo.get_user_by_name(user_name)
        if user is None  or not user.verify_password(form_data.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = create_access_token(form_data.username)
        return {"access_token": access_token,"token_type":"bearer"}









