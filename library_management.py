import os
import datetime

# Ensure we're in the script directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def read_books():
    books = []  # Initialize an empty list to hold book entries

    try:
        # Try opening the library.txt file in read mode
        with open("library.txt", "r") as file:
            for line in file:
                # Strip whitespace and split line into 6 parts using '|'
                parts = line.strip().split("|")

                # Only accept lines with 6 fields (valid book entry)
                if len(parts) == 6:
                    books.append(parts)  # Add the parsed book to the list
    except FileNotFoundError:
        # If the file doesn't exist yet, just return an empty list
        pass

    return books  # Return the list of books


def write_books(books):
    # Open the file in write mode (this clears the existing contents)
    with open("library.txt", "w") as file:
        for book in books:
            # Convert the list of book fields into a string with '|' separators
            line = "|".join(book)

            # Write the line to the file with a newline character
            file.write(line + "\n")


def view_books():
    books = read_books()  # Load books from the file

    # If no books found, show a message and stop
    if not books:
        print("\nNo books found in the library.")
        return

    # Print the table header
    print("\nAll Books:")
    print("ID\tTitle\t\t\tAuthor\t\t\tStatus\t\t\tAdded Time\t\tBorrowed Time")
    print("-" * 120)

    # Loop through each book and print its details in columns
    for book in books:
        id_, title, author, status, added_time, borrowed_time = book  # Unpack book fields
        print(f"{id_}\t{title[:15]:<20}{author[:20]:<25}{status:<15}\t\t{added_time:<25}{borrowed_time}")



def borrow_book():
    # Ask the user to input Book ID or Title
    search = input("Enter Book ID or Title to borrow: ").strip()

    books = read_books()  # Load books from file
    found = False  # Flag to check if a matching book is found

    for book in books:
        # Check if ID or title matches the input
        if book[0] == search or book[1].lower() == search.lower():
            found = True
            if book[3].lower() == "available":
                # If book is available, update its status and set borrowed time
                book[3] = "Borrowed"
                book[5] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"Book '{book[1]}' borrowed successfully at {book[5]}.")
            else:
                # If already borrowed, notify the user with time
                print(f"Book '{book[1]}' is already borrowed (at {book[5]}).")
            break  # Exit the loop after finding the book

    if not found:
        print("Book not found by given ID or Title.")  # If no match, show error

    write_books(books)  # Save the updated book list


def return_book():
    # Ask user to input the ID of the book to return
    book_id = input("Enter Book ID to return: ")

    books = read_books()  # Load books
    found = False  # Track if book is found

    for book in books:
        if book[0] == book_id:
            found = True
            if book[3].lower() == "borrowed":
                # If book is borrowed, mark it as available and clear borrowed time
                book[3] = "Available"
                book[5] = ""
                print("Book returned successfully.")
            else:
                # If it's not borrowed, inform the user
                print("Book is already available.")
    if not found:
        print("Book ID not found.")  # If no match found

    write_books(books)  # Save updated book data


def add_book():
    books = read_books()  # Load current books

    # Determine new book ID: get highest existing ID and increment
    if books:
        last_id = max(int(book[0]) for book in books)
        new_id = str(last_id + 1)
    else:
        new_id = "100"  # Start from 100 if no books

    # Ask user to input book title and author
    title = input("Enter Book Title: ").strip()
    author = input("Enter Author Name: ").strip()

    # Validate input: both fields must be non-empty
    if not title or not author:
        print("All fields (Title and Author) are required.")
        return

    # Record current time for 'added time', and set borrowed time as "None"
    added_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    borrowed_time = "None"

    # Add the new book to the list
    books.append([new_id, title, author, "Available", added_time, borrowed_time])

    write_books(books)  # Save to file
    print(f"Book added successfully with ID: {new_id} at {added_time}")


# Run the main menu in a loop until user exits
while True:
    # Display the main menu
    print("\n--- Book Library Management System ---")
    print("1. View Available Books")
    print("2. Borrow a Book")
    print("3. Return a Book")
    print("4. Add a New Book")
    print("5. Exit")

    # Get user input for menu choice
    choice = input("Enter your choice (1-5): ")

    # Execute appropriate function based on user's choice
    if choice == "1":
        view_books()         # View all books (both available & borrowed)
    elif choice == "2":
        borrow_book()        # Borrow a book by ID or title
    elif choice == "3":
        return_book()        # Return a borrowed book by ID
    elif choice == "4":
        add_book()           # Add a new book to the library
    elif choice == "5":
        print("Thank you! Goodbye.")  # Exit the program
        break
    else:
        print("Invalid choice. Try again.")  # Handle invalid menu input

