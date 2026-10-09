"""
Module 3 Project: Library Management System
main.py — Command-line interface

Your job: Implement each menu handler function below.
The main menu loop is already provided — just fill in the handlers.
"""

from models import init_db
from crud import (
    add_book, add_author, add_member, checkout_book, return_book,
    list_books, search_books_by_title, find_books_by_author,
    list_member_borrowings, list_overdue_books,
)


def handle_add_book():
    """Prompt for book details and add to the database."""
    # TODO: Use input() to collect title, isbn, year_published, available_copies
    
    title = input("Title: ").strip()
    isbn = input ("ISBN: ").strip()

    try:
        year_published = int(input("Year Published: ").strip())
        available_copies = int(input ("Available Copies: ").strip())
    
    except ValueError:
        print ("Year published and available copies must be numbers ")
        return
    
    # TODO: Call add_book() and print a confirmation message
    book =add_book(title, isbn, year_published, available_copies)
    print (f"Book {book.title} (ISBN: {book.isbn}) has been added ")


def handle_add_member():
    """Prompt for member details and register in the database."""
    # TODO: Use input() to collect name and email
    name = input ("Name: ").strip()
    email = input ("Email: ").strip()
    # TODO: Call add_member() and print a confirmation message
    member = add_member(name, email)
    print (f"Member: {member.name} (ID: {member.id}) has been registered")


def handle_search_books():
    """Prompt for a search term and display matching books."""
    # TODO: Prompt for a title keyword, call search_books_by_title(), print results
    title = input("Enter title keyword: ").strip().strip("\"'")
    if not title:
        print("No search term entered.")
        return

    books = search_books_by_title(title)
    if not books:
        print(f"No books found with '{title}'")
        return

    print(f"\nBooks Found: {len(books)}")
    for b in books:
        print(f"- ID: {b.id} | Title: {b.title} | ISBN: {b.isbn} | Copies: {b.available_copies}")

def handle_checkout():
    """Prompt for book ID and member ID, then check out the book."""
    # TODO: Show available books (call list_books())
    available_books = list_books()
    for book in available_books:
        print (f"ID {book.id} | Title '{book.title}' | Copies: {available_books}")

    # TODO: Prompt for book_id and member_id
    try:
        book_id = (int(input("Enter Book ID ")))
        member_id =(int(input("Enter Member ID ")))
    
    except ValueError:
        print(f"IDs must be only numbers")
        return

    # TODO: Call checkout_book() and handle ValueError (book not available)
    try:
        borrowing = checkout_book(book_id, member_id)

        print (f"Sucess! Check out book ID {borrowing.book_id} to member ID {borrowing.member_id}" )
    
    except ValueError as e:
        print (f"Error: {e}")


def handle_return():
    """Prompt for a borrowing ID and return the book."""
    # TODO: Prompt for borrowing_id, call return_book(), print confirmation
    try:
        borrowing_id = (int(input("Enter borrowing ID: ")))
    except ValueError:
        print ("Enter only numbers")
        return
    try:
        returned_record = return_book (borrowing_id)

        print (f"The book (borrowing # {returned_record.id} has been returned")

    except ValueError as e:
        print (f" Cannot be returned, Borrowing ID #{borrowing_id}: {e}")


def handle_member_borrowings():
    """Display all active borrowings for a member."""
    # TODO: Prompt for member_id, call list_member_borrowings(), print results
    
    try:

        member_id = int(input (f"Enter Member ID "))
    except ValueError:
        print ("Error: Member ID must be a number")
        return
    
    borrowings = list_member_borrowings(member_id)

    if not borrowings:
        print ("No active memmber borrowing found")
        return

    print (f"Active Borrowings for member {member_id}")
    for b in borrowings:
        print(f"Borrowing {b.id} | checked out: {b.checkout_date}")


def handle_overdue():
    """Display all overdue borrowings."""
    # TODO: Call list_overdue_books() and print results
    days = 14

    overdue_borrowings = list_overdue_books(days) 
    if not overdue_borrowings:
        print ("There are no overdue books")
        return

    print (f"Book(s) are over due for more than {days}")

    for b in overdue_borrowings:
        print (f"Book ID:{b.book_id} | Member ID:{b.member_id} | Checkout Data: {b.checkout_date}")


def main():
    init_db()

    while True:
        print("\n📚 Library Management System")
        print("1. Add a book")
        print("2. Add a member")
        print("3. Search books")
        print("4. Check out a book")
        print("5. Return a book")
        print("6. View member's borrowings")
        print("7. View overdue books")
        print("8. Exit")

        choice = input("\nChoose an option (1-8): ").strip()

        if choice == "1":
            handle_add_book()
        elif choice == "2":
            handle_add_member()
        elif choice == "3":
            handle_search_books()
        elif choice == "4":
            handle_checkout()
        elif choice == "5":
            handle_return()
        elif choice == "6":
            handle_member_borrowings()
        elif choice == "7":
            handle_overdue()
        elif choice == "8":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1-8.")


if __name__ == "__main__":
    main()
