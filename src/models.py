class Book:
    def __init__(self, title, author, isbn):
        self._title = title
        self.author = author
        self._isbn = isbn
        self._is_borrowed = False

    @property
    def is_borrowed(self):
        return self._is_borrowed
    
    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, new_title):
        if not isinstance(new_title, str) or not new_title:
            raise ValueError("Check to ensure you enter the correct title")
        new_title = new_title.strip()
        if not new_title:
            raise ValueError("Check to ensure you enter the correct title")
        self._title = new_title


    @property
    def isbn(self):
        return self._isbn
    


    def borrow(self):
        if self._is_borrowed:
            raise ValueError(f"{self.title} already borrowed")
        self._is_borrowed = True

    def return_book(self):
        self._is_borrowed = False

    def __repr__(self):
        return f"Book('{self.title}','{self.author}', '{self.isbn}')"

class Member:
    def __init__(self, name, member_id):
        self.name = name
        self.member_id = member_id
        self.borrowed_books = []

    def __repr__(self):
        return f"Member('{self.name}' books held {len(self.borrowed_books)})"

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




