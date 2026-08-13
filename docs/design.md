# Artifacts

## CRC cards

Class: Book
-------------------------------------------------
Responsibilities               | Collaborators
- borrow itself                | (none - self-contained)
- return itself                | (none - self-contained)
- validate/change its title    | (none - self-contained)
- expose its isbn (read-only)  | (none - self-contained)
Note: Book implements the AbstractBook contract (is-a), not a collaboration.

Class: Member
-------------------------------------------------
Responsibilities               | Collaborators
- stores borrowed books        |  (none - self-contained)



Class: Library
-------------------------------------------------
Responsibilities           | Collaborators
- add books to iself       | Book
- add memeber to itself    | Member
- lend out books to members| Book, Member


Class: Ebook
-------------------------------------------------
Responsibilities           | Collaborators
- return itself            | (none - self-contained)
- borrow itself            | (none - self-contained)
- expose isbn read-only|   | (none - self-contained)
- validate/change its title| (none - self-contained)
Note: Ebook implements the AbstractBook contract (is-a), not a collaboration.


Class: AbstractBook
-------------------------------------------------
Responsibilities                     | Collaborators
- declare that borrow must exist     | none
- declare that return book must exist| none
Note: Book and Ebook implement this contract (is-a) AbstractBook has no collaborators, only implementers.

## UML class

AbstractBook abstract
---------------
(no attributes)
---------------
+ borrow()
+ return_book()

Book
---------------
+ title: str
+ isbn: str
+ is_borrowed : bool
+ author: str
---------------
+ borrow(): bool
+ return_book(): bool
Book inherits from AbstractBook

Member
---------------
+ name: str
+ member_id: str
+ borrowed_books: list
---------------
- no private method
+ no public method

Ebook
---------------
+ title: str
+ isbn: str
+ is_borrowed : bool
+ author: str
+ file_size_mb
---------------
+ borrow(): bool
+ return_book(): bool
NB.Ebook inherits from AbstractBook


Labrary
---------------
+ books: dict
+ members: dict
---------------
+ add_book(): none
+ add_member(): none
+ lend_book(): none
NB:Library aggregates Book and Member (has-many, but they can exist independently)
calls methods on books and members


