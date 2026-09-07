from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class BookORM(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    isbn = Column(String, unique=True, nullable=False)
    is_borrowed = Column(Boolean, default=False)
    member_id = Column(Integer, ForeignKey("members.id"),nullable=True)
    borrowed_by = relationship("MemberORM", back_populates="borrowed_books")

    def __repr__(self):
        return f"BookORM('{self.title},'{self.isbn}')"

class MemberORM(Base):
    __tablename__ = "members"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    member_id = Column(String, unique=True, nullable=False)
    borrowed_books = relationship("BookORM", back_populates="borrowed_by")

    def __repr__(self):
        return f"MemberORM('{self.name}' member_id = {self.member_id})"

class UserORM(Base):
        __tablename__ = "users"
        id = Column(Integer, primary_key=True)
        user_name = Column(String, unique=True)
        hashed_password = Column(String, nullable=False)

        def __repr__(self):
            return f"UserORM('{self.user_name}')"
    

