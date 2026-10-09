"""
Module 3 Project: Library Management System
seed.py — Populate the database with sample data for testing.

Run after implementing your models and CRUD functions:
    python seed.py

Sample data is loaded from sample_data.json.
"""

import json
from models import init_db
from crud import add_author, add_book, add_member, checkout_book, return_book


def seed():
    """Load sample data from sample_data.json and insert it into the database."""
    init_db()

    with open("sample_data.json") as f:
        data = json.load(f)

    # TODO: Loop through data["authors"] and call add_author() for each entry
    authors_by_name ={}
    for author_data in data.get("authors", []):
        author = add_author(
            name = author_data ["name"], 
            bio= author_data.get("bio"))
        authors_by_name[author.name] = author.id

    # TODO: Loop through data["books"] and call add_book() for each entry
     #       Tip: you'll need to look up author IDs to link them to books
    books_by_isbn= {}
    for books_data in data.get("books", []):
        author_ids = [
            authors_by_name[name]
            for name in books_data.get("authors", [])
            if name in authors_by_name
        ]
        book = add_book(
         title = books_data ["title"], 
         isbn= books_data ["isbn"], 
         year_published= books_data.get("year_published"), 
         available_copies=books_data["available_copies"],
         author_ids=author_ids
        )
        books_by_isbn[book.isbn] = book.id

    # TODO: Loop through data["members"] and call add_member() for each entry
    members_by_email = {}
    for members_data in data.get("members", []):
        member = add_member(
            name=members_data["name"], 
            email=members_data["email"])
        members_by_email[member.email] = member.id

    # TODO: Loop through data["borrowings"] and call checkout_book() for each entry
    #       Tip: look up book and member IDs by isbn / email
    for item in data.get("borrowings", []):
        book_id = books_by_isbn.get(item["book_isbn"])
        member_id = members_by_email.get(item["member_email"])

        if not book_id or not member_id:
            print ("Book or Member not found ")
            continue
        borrowing = checkout_book(book_id=book_id, member_id=member_id)
           
    # TODO: For borrowings that have a return_date, call return_book() to mark them returned
        if item.get ("return_date"):
         return_book (borrowing.id)

    print("Seed complete!")


if __name__ == "__main__":
    seed()

