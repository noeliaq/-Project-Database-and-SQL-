"""
Module 3 Project: Library Management System
models.py — SQLAlchemy models and database setup

Your job: Implement the models marked with # TODO.
All models must use SQLAlchemy 2.0 syntax: Mapped and mapped_column.
"""
import datetime
from sqlalchemy import create_engine, String, Integer, ForeignKey, Table, Column, Date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session
from datetime import date
from typing import Optional


engine = create_engine("sqlite:///library.db", echo=False)


class Base(DeclarativeBase):
    pass


# Association table for Book <-> Author (many-to-many)
# TODO: Define the book_authors association table
book_authors = Table(
    "book_authors",
    Base.metadata,
    Column("book_id",   Integer, ForeignKey("books.id"),   primary_key=True),
    Column("author_id", Integer, ForeignKey("authors.id"), primary_key=True),
)


# TODO: Implement the Author model
# Attributes: id (PK), name (required), bio (optional)
# Relationship: books (many-to-many via book_authors)
class Author(Base):
    __tablename__ = "authors"
    # TODO: define columns and relationship
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    bio: Mapped[Optional[str]] = mapped_column (String(200))

    books: Mapped[list["Book"]] = relationship(
        secondary=book_authors, back_populates="authors"
    )

    def __repr__(self):
        return f"<Author(name = '{self.name}')>"

# TODO: Implement the Member model
# Attributes: id (PK), name (required), email (unique, required), membership_date (date)
# Relationship: borrowings (one-to-many)
class Member(Base):
    __tablename__ = "members"
    # TODO: define columns and relationship
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column (String(100), nullable=False)
    email: Mapped[str] = mapped_column (String(200),nullable= False, unique=True)
    membership_date:Mapped[datetime.date] = mapped_column (nullable= False)

    borrowings: Mapped[list["Borrowing"]] = relationship(back_populates="members")

    def __repr__(self):
        return f"<Member (name = '{self.name}')>"

# TODO: Implement the Book model
# Attributes: id (PK), title (required), isbn (unique, required),
#             year_published (optional, integer), available_copies (integer, default 1)
# Relationships: authors (many-to-many via book_authors), borrowings (one-to-many)
class Book(Base):
    __tablename__ = "books"
    # TODO: define columns and relationships
    id: Mapped[int] = mapped_column(primary_key= True)
    title: Mapped[str] = mapped_column (String(100), nullable= False)
    isbn: Mapped [int] = mapped_column (unique= True, nullable= False)
    year_published: Mapped[Optional[int]] = mapped_column (Integer)
    available_copies: Mapped[int] = mapped_column (Integer, default= 1)

    authors: Mapped[list ["Author"]] = relationship(
    secondary=book_authors, back_populates= "books"
    )
    borrowings: Mapped[list["Borrowing"]] = relationship ("Borrowing", back_populates="books")

    def __repr__(self):
        return f"<Book (id={self.id},(title = {self.title}>"
# TODO: Implement the Borrowing model
# Attributes: id (PK), book_id (FK -> books.id), member_id (FK -> members.id),
#             checkout_date (date), return_date (date, nullable — NULL means not yet returned)
# Relationships: book, member
class Borrowing(Base):
    __tablename__ = "borrowings"
    # TODO: define columns and relationships
    id: Mapped [int] = mapped_column(primary_key= True)
    book_id: Mapped[int] = mapped_column(ForeignKey ("books.id"))
    member_id: Mapped[int] = mapped_column(ForeignKey ("members.id"))
    checkout_date: Mapped[datetime.date]
    return_date: Mapped[datetime.date | None]
    
    books: Mapped["Book"] = relationship ("Book", back_populates="borrowings")
    members: Mapped["Member"] = relationship ("Member", back_populates= "borrowings")

    def __repr__(self):
        return f"<Borrowing (id = '{self.id}'>"
    
def init_db():
    """Create all tables in the database. Call once before using any other functions."""
    #TODO: 
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    
  
print("tables created")