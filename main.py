# === CLI logic for managing the library system ===

from library import Library, Book  # Import main classes

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

# Display help menu
def show_help(commands):
    print("\n===== Library Management System =====")
    print("Available commands:")
    for cmd, desc in commands.items():
        print(f"  {cmd:<8} - {desc}")
    print("=====================================\n")

def main():
    lib = Library()
    lib.load_from_file("books.json")

    commands = {
        "add": "Add a new book",
        "show": "Display all books",
        "search": "Search for books",
        "remove": "Remove a book",
        "edit": "Edit a book",
        "state": "Functions to show stats",
        "exit or x": "Exit the program",
        "help": "Show help menu"
    }

    try:
        while True:
            command = input("\nEnter command (or 'help' for options): ").strip().lower()

            if command == "add":
                title = input("Title: ").strip()
                author = input("Author: ").strip()
                year = get_valid_year()
                if title and author:
                    b = Book(title, author, year)
                    lib.add_book(b)
                else:
                    print("Book not added. All fields must be provided.")

            elif command == "show":
                if lib.books:
                    lib.show_books()
                else:
                    print("Library is empty.")

            elif command == "state":
                lib.stats_book()

            elif command == "edit":
                title = input("Enter title to edit: ").strip()
                if title: 
                    lib.edit_book(title)
                else:
                    print("Edit canceled.")

            elif command == "search":
                title = input("Enter title to search: ").strip()
                if title:
                    lib.search_book(title)
                else:
                    print("Search canceled.")

            elif command == "remove":
                title = input("Enter title to remove: ").strip()
                if title:
                    lib.remove_book(title)
                else:
                    print("Remove canceled.")

            elif command == "help":
                show_help(commands)

            elif command == "exit" or command == "x":
                print("Bye!")
                break

            else:
                print("\nUnknown command! Check 'help'")
    except KeyboardInterrupt:
        print("\nBye!")


# Run only if this file is the entry point
if __name__ == "__main__":
    main()
