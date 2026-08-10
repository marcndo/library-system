class Book:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.is_borrowed = False

    def borrow(self):
        if self.is_borrowed:
            raise ValueError(f"{self.title} already borrowed")
        self.is_borrowed = True

    def is_return(self):
        self.is_borrowed = False

    def __repr__(self):
        return f"Book('{self.title}','{self.author}', '{self.isbn}')"

class Member:
    def __init__(self, name, member_id):
        self.name = name
        self.member_id = member_id
        self.borrowed_books = []

    def __repr__(self):
        return f"Member('{self.name}' books held {len(self.borrowed_books)})"

