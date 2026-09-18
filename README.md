
# Library System

A backend-driven library management application for managing
books, members, and borrowing transactions.

## Problem Statement

Small libraries may manage books, members, and borrowing records manually. As the number of books and members grows, keeping track of which books are available, which are currently borrowed, and who has borrowed them can become difficult to manage accurately.
This project addresses that problem by providing a centralized system for managing books, members, and borrowing transactions.

## Solution
A web-based library management application that centralizes book, member, and borrowing management. The system provides authenticated access to library operations, persists data through a relational database, and exposes the core functionality through a FastAPI backend and web interface.

## Key features
* **Member Management** - Register and manage library members.
* **Book Management** - Add and manage books in the library.
* **Book Lending** - Lend books to registered members while tracking their lending status.
* **Librarian Authentication** - Authenticate librarians to control access to the library management system.


## Architecture
## System Architecture

The application follows a layered architecture that separates the user interface, API layer, application logic, data access, and persistence.

```text
                    ┌──────────────────────┐
                    │      Frontend        │
                    │   HTML/CSS/JavaScript│
                    └──────────┬───────────┘
                               │ HTTP
                               ▼
                    ┌──────────────────────┐
                    │       FastAPI        │
                    │      REST API        │
                    └──────────┬───────────┘
                               │
                 ┌─────────────┴─────────────┐
                 │                           │
                 ▼                           ▼
        ┌─────────────────┐        ┌─────────────────┐
        │ Application     │        │ Authentication  │
        │ Logic / Domain  │        │ JWT + pwdlib    │
        └────────┬────────┘        └─────────────────┘
                 │
                 ▼
        ┌─────────────────┐
        │   Repository    │
        │     Layer       │
        └────────┬────────┘
                 │ SQLAlchemy
                 ▼
        ┌─────────────────┐
        │     SQLite      │
        │    Database     │
        └─────────────────┘
```

The frontend communicates with the FastAPI backend through HTTP requests. The backend handles API requests and application logic, while the repository layer manages database operations through SQLAlchemy. JWT-based authentication and password hashing are used to protect authenticated operations.

## Why this project exists

This was built as a deliberate practice project to internalize OOP
fundamentals and professional project structure before building larger,
database-backed backend systems. See [docs/design.md](docs/design.md)
for the full design reasoning (CRC cards, responsibility decisions).

## Features

- Book and Ebook classes sharing a common AbstractBook contract
- Library coordinates lending, tracking availability across books and members
- Encapsulated state (e.g. a book can't be double-borrowed, or have its
  title corrupted by invalid input)
- 17 passing tests covering both success and failure paths


## Data Model

The system uses three primary database models:

* **Book** - Stores book information including title, author, ISBN, and borrowing status.
* **Member** - Stores registered library members and their unique member IDs.
* **User** - Stores librarian credentials used for authentication.

### Relationships

A member can borrow multiple books, while a book can be borrowed by at most one member at a time. The relationship is represented through the `member_id` foreign key on the `books` table.

```text
┌──────────────────┐
│      users       │
├──────────────────┤
│ id               │
│ user_name        │
│ hashed_password  │
└──────────────────┘
        │
        │ authenticates
        ▼
   ┌──────────┐
   │Librarian │
   └──────────┘


┌──────────────────┐          ┌──────────────────┐
│     members      │          │      books       │
├──────────────────┤          ├──────────────────┤
│ id               │◄─────────│ member_id (FK)   │
│ name             │   1   N  │ id               │
│ member_id        │          │ title            │
└──────────────────┘          │ author           │
                              │ isbn             │
                              │ is_borrowed      │
                              └──────────────────┘
```

The database layer is implemented using SQLAlchemy ORM with SQLite as the persistence layer.


## API Overview

The application exposes a REST API for managing books, lending operations, and librarian authentication.

| Method | Endpoint        | Description                                            | Authentication |
| ------ | --------------- | ------------------------------------------------------ | -------------- |
| `GET`  | `/books`        | Retrieve all books                                     | No             |
| `POST` | `/books`        | Add a new book                                         | No             |
| `GET`  | `/books/{isbn}` | Retrieve a book by ISBN                                | No             |
| `POST` | `/lend`         | Lend a book to a member                                | JWT required   |
| `POST` | `/register`     | Register a librarian account                           | No             |
| `POST` | `/token`        | Authenticate a librarian and obtain a JWT access token | No             |

### Example Workflow

```text
Register librarian
       │
       ▼
  POST /register
       │
       ▼
  POST /token
       │
       ▼
   JWT token
       │
       ▼
   POST /lend
       │
       ▼
  Book borrowed
```

Interactive API documentation is available through FastAPI's generated documentation.

## Authentication & Authorization

The application uses username/password authentication with JWT bearer tokens to protect lending operations.

### Authentication Flow

```text
Librarian
    │
    │ Register credentials
    ▼
POST /register
    │
    ▼
User account created
    │
    │ Login
    ▼
POST /token
    │
    ▼
JWT access token
    │
    │ Bearer token
    ▼
POST /lend
    │
    ▼
get_current_user()
    │
    ▼
Lending operation
```

### Implementation

* **User registration** — `POST /register` creates a librarian account.
* **Password protection** — User credentials are stored using a hashed-password field rather than storing the plaintext password.
* **Login** — `POST /token` validates the supplied username and password.
* **JWT authentication** — Successful authentication returns a JWT access token using the Bearer token scheme.
* **Protected lending endpoint** — `POST /lend` requires an authenticated user through FastAPI's dependency injection.
* **Invalid credentials** — Failed authentication returns `401 Unauthorized`.

The authentication flow separates credential verification from protected library operations, allowing lending functionality to be accessed only by authenticated users.

## Validation & Error Handling

The application validates incoming API requests through Pydantic request models and enforces additional data integrity constraints at the database and application levels.

### Request Validation

API request bodies are defined using Pydantic models, including:

* `BookCreateRequest` for adding books.
* `BookLendRequest` for lending operations.
* `UserCreateRequest` for librarian registration.

This ensures that incoming request data conforms to the expected structure before it reaches the application logic.

### Data Integrity

The database also enforces constraints on important fields:

* Book ISBNs are unique.
* Member IDs are unique.
* Required fields such as book title, author, ISBN, member name, and hashed password cannot be null.
* A book's `member_id` may be null when the book is not currently associated with a member.

### Authentication Errors

Authentication failures are explicitly handled by the login endpoint. When the supplied username or password is invalid, the API returns:

```text
401 Unauthorized
```

with an appropriate authentication response.

### Business-Rule Validation

The library domain logic also handles invalid lending operations, including cases such as:

* Attempting to lend a book that is already borrowed.
* Attempting to lend an unregistered book.
* Attempting to lend a book to an unregistered member.

These behaviors are covered by automated tests to verify that invalid lending operations are handled correctly.


## Testing

The project uses **Pytest** for automated testing of the core library functionality and business rules.

The test suite covers books, ebooks, and library operations:

```text
tests/
├── test_book.py
├── test_ebook.py
└── test_library.py
```

### Tested Behaviors

The tests verify important application behaviors, including:

* Creating and configuring books correctly.
* Setting and updating book lending status.
* Lending a book successfully.
* Preventing a book from being borrowed when it is already borrowed.
* Rejecting lending attempts for unregistered books.
* Rejecting lending attempts for unregistered members.

This provides coverage for both expected application behavior and invalid lending scenarios.

### Running the Tests

Run the complete test suite with:

```bash
python3 -m pytest
```

The test suite helps ensure that changes to the library domain logic do not unintentionally break existing behavior.


## Tech Stack

| Category             | Technology                 |
| -------------------- | -------------------------- |
| **Language**         | Python                     |
| **API Framework**    | FastAPI                    |
| **ORM**              | SQLAlchemy                 |
| **Database**         | SQLite                     |
| **Data Validation**  | Pydantic                   |
| **Authentication**   | JWT / OAuth2 Bearer Tokens |
| **Password Hashing** | pwdlib                     |
| **Testing**          | Pytest                     |
| **Frontend**         | HTML, CSS, JavaScript      |
| **Containerization** | Docker                     |
| **Deployment**       | Render                     |

