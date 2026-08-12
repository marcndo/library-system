# Artifacts


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