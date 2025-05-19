# === CLI logic for managing the library system ===

from library import Library, Book  # Import main classes

lib = Library()
lib.load_from_file("books.json")  # Load saved books from file


# Validate year input from user (must be numeric or empty)
def get_valid_year():
    while True:
        try:
            year = input("Year : ").strip()
            if not year:
                return None
            return int(year)
        except ValueError:
            print("Please enter a valid year (numeric value).")

# === Main command loop ===
while True:
    # Available user commands
    commands = {
        "add": "Add a new book",
        "show": "Display all books",
        "search": "Search for books",
        "remove": "Remove a book",
        "exit": "Exit the program",
        "help": "Show this help menu"
    }

    # Display help menu
    def show_help():
        print("\n===== Library Management System =====")
        print("Available commands:")
        for cmd, desc in commands.items():
            print(f"  {cmd:<8} - {desc}")
        print("=====================================\n")

    # Read user command
    command = input("\nEnter command (or 'help' for options): ").strip().lower()

    # === Command handlers ===
    if command == "add":
        title = input("Title: ").strip()
        author = input("Author: ").strip()
        year = get_valid_year()
        if title and author:
            b = Book(title, author, year)
            lib.add_book(b)
            lib.save_to_file("books.json")  # Save after adding
        else:
            print("Book not added. All fields must be provided.")

    elif command == "show":
        if lib.books:
            lib.show_books()
        else:
            print("Library is empty.")

    elif command == "search":
        title = input("Enter title to search: ").strip()
        if title:
            lib.search_book(title)
        else:
            print("Search canceled.")

    elif command == "remove":
        title = input("Enter title to remove: ").strip()
        if title:
            lib.remove_books(title)
            lib.save_to_file("books.json")  # Save after removal
        else:
            print("Remove canceled.")

    elif command == "help":
        show_help()

    elif command == "exit":
        print("Bye!")
        break

    else:
        print("\nUnknown command! Check 'help'")
