import os
import datetime

# Ensure we're in the script directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def read_books():
    books = []
    try:
        with open("library.txt", "r") as file:
            for line in file:
                parts = line.strip().split("|")
                if len(parts) == 6:
                    books.append(parts)
    except FileNotFoundError:
        pass
    return books

def write_books(books):
    with open("library.txt", "w") as file:
        for book in books:
            line = "|".join(book)
            file.write(line + "\n")

def view_books():
    books = read_books()

    if not books:
        print("\nNo books found in the library.")
        return

    print("\nAll Books:")
    print("ID\tTitle\t\t\tAuthor\t\t\tStatus\t\t\tAdded Time\t\tBorrowed Time")
    print("-" * 120)
    for book in books:
        id_, title, author, status, added_time, borrowed_time = book
        print(f"{id_}\t{title[:15]:<20}{author[:20]:<25}{status:<15}\t\t{added_time:<25}{borrowed_time}")


def borrow_book():
    search = input("Enter Book ID or Title to borrow: ").strip()
    books = read_books()
    found = False

    for book in books:
        if book[0] == search or book[1].lower() == search.lower():
            found = True
            if book[3].lower() == "available":
                book[3] = "Borrowed"
                book[5] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"Book '{book[1]}' borrowed successfully at {book[5]}.")
            else:
                print(f"Book '{book[1]}' is already borrowed (at {book[5]}).")
            break

    if not found:
        print("Book not found by given ID or Title.")

    write_books(books)

def return_book():
    book_id = input("Enter Book ID to return: ")
    books = read_books()
    found = False
    for book in books:
        if book[0] == book_id:
            found = True
            if book[3].lower() == "borrowed":
                book[3] = "Available"
                book[5] = ""
                print("Book returned successfully.")
            else:
                print("Book is already available.")
    if not found:
        print("Book ID not found.")
    write_books(books)

def add_book():
    books = read_books()

    if books:
        last_id = max(int(book[0]) for book in books)
        new_id = str(last_id + 1)
    else:
        new_id = "100"

    title = input("Enter Book Title: ").strip()
    author = input("Enter Author Name: ").strip()

    if not title or not author:
        print("All fields (Title and Author) are required.")
        return

    added_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    borrowed_time = "None"

    books.append([new_id, title, author, "Available", added_time, borrowed_time])
    write_books(books)
    print(f"Book added successfully with ID: {new_id} at {added_time}")

# Main Menu
while True:
    print("\n--- Book Library Management System ---")
    print("1. View Available Books")
    print("2. Borrow a Book")
    print("3. Return a Book")
    print("4. Add a New Book")
    print("5. Exit")

    choice = input("Enter your choice (1-5): ")

    if choice == "1":
        view_books()
    elif choice == "2":
        borrow_book()
    elif choice == "3":
        return_book()
    elif choice == "4":
        add_book()
    elif choice == "5":
        print("Thank you! Goodbye.")
        break
    else:
        print("Invalid choice. Try again.")
