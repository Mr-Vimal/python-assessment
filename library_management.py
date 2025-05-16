# Functions to read and write books from the file

def read_books():
    books = []
    try:
        file = open("library.txt", "r")
        for line in file:
            parts = line.strip().split("|")
            if len(parts) == 4:
                books.append(parts)
        file.close()
    except:
        pass
    return books

def write_books(books):
    file = open("library.txt", "w")
    for book in books:
        line = "|".join(book)
        file.write(line + "\n")
    file.close()

#  View Available Books
def view_books():
    books = read_books()
    print("\nAvailable Books:")
    print("ID\tTitle\t\t\tAuthor")
    for book in books:
        if book[3].lower() == "available":
            print(book[0] + "\t" + book[1][:20] + "\t" + book[2])

# Borrow a Book
def borrow_book():
    book_id = input("Enter Book ID to borrow: ")
    books = read_books()
    found = False
    for book in books:
        if book[0] == book_id:
            found = True
            if book[3].lower() == "available":
                book[3] = "Borrowed"
                print("Book borrowed successfully.")
            else:
                print("Book is already borrowed.")
    if not found:
        print("Book ID not found.")
    write_books(books)

# Return a Book
def return_book():
    book_id = input("Enter Book ID to return: ")
    books = read_books()
    found = False
    for book in books:
        if book[0] == book_id:
            found = True
            if book[3].lower() == "borrowed":
                book[3] = "Available"
                print("Book returned successfully.")
            else:
                print("Book is already available.")
    if not found:
        print("Book ID not found.")
    write_books(books)

#Add a New Book
def add_book():
    book_id = input("Enter new Book ID: ")
    title = input("Enter Book Title: ")
    author = input("Enter Author Name: ")
    
    books = read_books()
    for book in books:
        if book[0] == book_id:
            print("Book ID already exists.")
            return
    
    books.append([book_id, title, author, "Available"])
    write_books(books)
    print("Book added successfully.")

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
