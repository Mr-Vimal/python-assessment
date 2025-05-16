import os  # Import the os module for file path operations
import datetime  # Import datetime module to work with date and time

# Change the working directory to the directory where the script is located
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def read_books():
    """
    Reads all book records from 'library.txt' file.
    Returns a list of books, where each book is a list of its fields.
    """
    books = []  # Initialize an empty list to store all books

    try:
        # Open the file 'library.txt' in read mode
        with open("library.txt", "r") as file:
            # Read the file line by line
            for line in file:
                # Remove any leading/trailing whitespace and split the line into parts based on '|'
                parts = line.strip().split("|")

                # Check if the line has exactly 7 fields (including return time)
                if len(parts) == 7:
                    books.append(parts)  # Add the book data (list) to the books list
    except FileNotFoundError:
        # If the file does not exist, ignore the error and return empty list
        pass

    return books  # Return the list of books


def write_books(books):
    """
    Writes all books from the list back into 'library.txt'.
    Each book is written as a '|' separated string.
    """
    # Open 'library.txt' in write mode to overwrite existing content
    with open("library.txt", "w") as file:
        # Iterate over each book entry in the books list
        for book in books:
            # Join the fields of the book list into a single string separated by '|'
            line = "|".join(book)

            # Write the line to the file, adding a newline character
            file.write(line + "\n")


def view_books():
    """
    Display all books with details including their status, added time,
    borrowed time, and return time.
    """
    books = read_books()  # Read books from file

    if not books:
        # If no books found, notify the user
        print("\nNo books found in the library.")
        return  # Exit the function early

    # Print header for the books list
    print("\nAll Books:")
    print("ID\tTitle\t\t\tAuthor\t\t\tStatus\t\tAdded Time\t\tBorrowed Time\t\tReturn Time")
    print("-" * 140)  # Separator line

    # Loop through all books to print their details
    for book in books:
        # Unpack book fields into variables
        id_, title, author, status, added_time, borrowed_time, return_time = book

        # Format and print book details in aligned columns
        print(f"{id_}\t{title[:15]:<20}{author[:20]:<25}{status:<15}\t{added_time:<20}\t{borrowed_time:<20}\t{return_time}")


def borrow_book():
    """
    Allows the user to borrow a book by searching by ID or Title.
    Updates the book status to 'Borrowed' and sets the borrowed time.
    """
    search = input("Enter Book ID or Title to borrow: ").strip()  # Get user input for book search

    books = read_books()  # Load books from file
    found = False  # Flag to track if a book was found matching the search

    # Loop through each book to find a matching ID or title
    for book in books:
        # Match either book ID or title (case-insensitive)
        if book[0] == search or book[1].lower() == search.lower():
            found = True  # Mark that the book was found
            # Check if the book is available to borrow
            if book[3].lower() == "available":
                book[3] = "Borrowed"  # Update status to 'Borrowed'
                # Set the borrowed time to current timestamp
                book[5] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                book[6] = "None"  # Clear any previous return time
                print(f"Book '{book[1]}' borrowed successfully at {book[5]}.")  # Confirm borrowing
            else:
                # If already borrowed, display the time it was borrowed
                print(f"Book '{book[1]}' is already borrowed (at {book[5]}).")
            break  # Exit loop after finding the book

    if not found:
        # If no matching book was found, notify the user
        print("Book not found by given ID or Title.")

    write_books(books)  # Save updated book list to file


def return_book():
    """
    Allows user to return a borrowed book by entering its ID.
    Updates book status to 'Available' and records return time.
    """
    book_id = input("Enter Book ID to return: ").strip()  # Get book ID from user

    books = read_books()  # Load books from file
    found = False  # Flag to track if book was found

    for book in books:
        if book[0] == book_id:
            found = True  # Book found
            if book[3].lower() == "borrowed":
                book[3] = "Available"  # Mark book as available again
                # Record current time as return time
                book[6] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print("Book returned successfully.")
            else:
                # If book wasn't borrowed, inform user
                print("Book is already available.")
            break  # Exit loop after processing the book

    if not found:
        # If no book matched the ID
        print("Book ID not found.")

    write_books(books)  # Save updated book list


def add_book():
    """
    Allows user to add a new book by entering title and author.
    Automatically assigns new book ID and sets added time.
    """
    books = read_books()  # Load current books

    # Generate new book ID by incrementing the highest existing ID
    if books:
        last_id = max(int(book[0]) for book in books)  # Find max existing ID
        new_id = str(last_id + 1)  # Increment by 1
    else:
        new_id = "100"  # Start ID numbering from 100 if no books exist

    # Prompt user for book title and author
    title = input("Enter Book Title: ").strip()
    author = input("Enter Author Name: ").strip()

    # Validate inputs (title and author must not be empty)
    if not title or not author:
        print("All fields (Title and Author) are required.")
        return  # Exit function if validation fails

    # Record current timestamp as added time
    added_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    borrowed_time = "None"  # Initially not borrowed
    return_time = "None"    # No return time yet

    # Append new book record to books list
    books.append([new_id, title, author, "Available", added_time, borrowed_time, return_time])

    write_books(books)  # Save to file
    print(f"Book added successfully with ID: {new_id} at {added_time}")


# Main program loop - displays menu and processes user input repeatedly
while True:
    print("\n--- Book Library Management System ---")
    print("1. View Available Books")
    print("2. Borrow a Book")
    print("3. Return a Book")
    print("4. Add a New Book")
    print("5. Exit")

    choice = input("Enter your choice (1-5): ").strip()  # Get menu selection from user

    # Process menu choice by calling the corresponding function
    if choice == "1":
        view_books()         # Show all books with details
    elif choice == "2":
        borrow_book()        # Borrow a book by ID or Title
    elif choice == "3":
        return_book()        # Return a book by ID
    elif choice == "4":
        add_book()           # Add a new book record
    elif choice == "5":
        print("Thank you! Goodbye.")  # Exit message
        break  # Exit the while loop and end the program
    else:
        # Handle invalid menu inputs
        print("Invalid choice. Try again.")
