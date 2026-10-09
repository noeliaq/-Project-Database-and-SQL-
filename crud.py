"""
Module 3 Project: Library Management System
crud.py — Create, Read, Update, Delete operations

Your job: Implement every function below.
Import your models and engine from models.py.
"""
import datetime
from models import engine, Book, Author, Member, Borrowing
from sqlalchemy.orm import Session
from datetime import date, timedelta
from sqlalchemy import select, func

# ──────────────────────────────────────────
# CREATE
# ──────────────────────────────────────────

def add_book(title: str, isbn: str, year_published: int = None,
             available_copies: int = 1, author_ids: list[int] = None):
    """Add a new book to the database. Returns the created Book object."""
    # TODO: open a Session, create a Book, add + commit, return it
    with Session(engine) as session:
        book = Book(title = title, isbn = isbn, year_published = year_published, available_copies = available_copies)
        if author_ids:
            authors = session.query(Author).filter(Author.id.in_(author_ids)).all()
            book.authors.extend(authors)
        session.add(book)
        session.commit()
        session.refresh(book) #populates the auto generated id 
        print(f" Created: {book} (id={book.id})")
        return book

def add_author(name: str, bio: str = None):
    """Add a new author. Returns the created Author object."""
    # TODO: implement
    with Session(engine) as session:
        author = Author(name = name, bio = bio)
        session.add(author)
        session.commit()
        session.refresh(author)
        print(f" Created: {author} (id={author.id})")
        return author


def add_member(name: str, email: str):
    """
    Register a new member with today's date as membership_date.
    Returns the created Member object.
    """
    # TODO: implement
    with Session(engine) as session:
        member = Member(
            name = name, 
            email = email,
            membership_date=date.today())
        session.add(member)
        session.commit()
        session.refresh(member)
        print(f" Created: {member} (id = {member.id})")
        return member

def checkout_book(book_id: int, member_id: int):
    """
    Check out a book to a member.
    Decrements available_copies by 1 and sets checkout_date to today.
    Raises ValueError if available_copies == 0.
    Returns the created Borrowing object.
    """
    # TODO: implement
    with Session(engine) as session:
        book = session.get(Book, book_id)
        if not book:
            raise ValueError(f"Book with {book_id} not found")
        member = session.get(Member, member_id)
        if not member:
            raise ValueError(f"Member with {member_id} not found")
        
        if book.available_copies <= 0:
            raise ValueError (f"The book with {book.id} is not available.")
        
        book.available_copies -=1

        borrowing = Borrowing(
            book_id =book.id, 
            member_id = member.id,
            checkout_date = datetime.date.today(),
            return_date = None,
)
        session.add( borrowing)
        session.commit()
        session.refresh(borrowing)
        return borrowing
# ──────────────────────────────────────────
# READ
# ──────────────────────────────────────────

def list_books():
    """Return a list of all Book objects."""
    # TODO: implement
    print("list")
    with Session(engine) as session:
        return session.query(Book).all()


def search_books_by_title(title: str):
    """Return books whose title contains the given string (case-insensitive)."""
    with Session(engine) as session:

        return session.query(Book).filter(Book.title.ilike(f"%{title}%")).all()


def find_books_by_author(author_name: str):
    """Return all books associated with an author whose name contains author_name."""
    # TODO: implement
    with Session(engine) as session:
        return (session.query(Book).join(Author).filter(Author.name.ilike(f"% {author_name}%")).all()
        )

def list_member_borrowings(member_id: int):
    """Return all active (unreturned) Borrowing objects for the given member."""
    # TODO: implement
    with Session(engine) as session:
        return(
            session.query(Borrowing)
            .filter(
                Borrowing.member_id == member_id,
                Borrowing.return_date.is_(None)
            ).all()
        )


def list_overdue_books(days: int = 14):
    """
    Return Borrowing objects where return_date is NULL and
        9/25                    14      today is 10/05
    checkout_date is more than `days` days ago.
    """
    # TODO: implement                           #duration of time 
    cut_off = datetime.date.today() - datetime.timedelta(days = days)
    with Session(engine) as session:
          return (
            session.query(Borrowing)
            .filter(
                Borrowing.return_date.is_(None), 
                Borrowing.checkout_date < cut_off) 
        
            .all()
          )
# ──────────────────────────────────────────
# UPDATE
# ──────────────────────────────────────────

def return_book(borrowing_id: int):
    """
    Mark a borrowing as returned.
    Sets return_date to today and increments book.available_copies by 1.
    Raises ValueError if the borrowing is not found or already returned.
    """
    # TODO: implement
    with Session(engine) as session:
        borrow = session.get(Borrowing, borrowing_id)
        if not borrow: 
            raise ValueError (f"Borrow book with {borrowing_id} Not found")
        elif borrow.return_date is not None: # book is already returned
            raise ValueError (f"Book already returned ")
    
        borrow.return_date = datetime.date.today()
        borrow.books.available_copies += 1
        session.commit()
        session.refresh(borrow)
    
        print(f"Book returned {borrow}")

        return borrow

def update_member_email(member_id: int, new_email: str):
    """Update the email address for a member. Returns the updated Member object."""
    # TODO: implement
    with Session(engine) as session:
        member = session.get(Member, member_id)
        if not member:
            raise ValueError (f"Member with {member_id} not found")
        old_email = member.email
        member.email = new_email  #update the database field

        session.commit()
        session.refresh(member) #refresh the member id 

        print (f"The old email was {old_email} and new email is {new_email} for member with ID {member_id}")

        return member
# ──────────────────────────────────────────
# DELETE
# ──────────────────────────────────────────

def delete_book(book_id: int):
    """
    Delete a book from the database.
    Raises ValueError if the book has any active (unreturned) borrowings.
    """
    # TODO: implement
    with Session(engine) as session:
        book = session.get(Book, book_id), filter
        if not book:
            raise ValueError (f"Book with {book_id} Not found")
        
        #check if there are unreturned borrowings for this specific book
        unreturned_borrowings = ( 
            session.query(Borrowing)
                .filter (
                    Borrowing.book_id == book_id,
                    Borrowing.return_date.is_(None)
                )
                .first()
        )
        if unreturned_borrowings:
            raise ValueError (f"Book {book_id} ({book.title}) cannot be deleted as it has not been returned.")
        #delete the book
        title = book.title
        session.delete(book)
        session.commit()

        print (f" book deleted {title}")
            


def delete_member(member_id: int):
    """
    Delete a member from the database.
    Raises ValueError if the member has any active (unreturned) borrowings.
    """
    # TODO: implement
    with Session(engine) as session:
        member = session.get(Member, member_id)
        if not member:
            raise ValueError (f" Member ID {member_id} not found")
        
        unreturned_borrowing = (session.query(Borrowing)
            .filter (
                Borrowing.member_id == member_id,
                Borrowing.return_date.is_(None) # Null book is not returned yet
            )
            .first()
        )
        if unreturned_borrowing:
            raise ValueError (f"cannot delete member {member_id} as it still has unreturned books")
        
       
        session.delete(member)
        session.commit()

        print (f" Member {member_id} deleted")
        