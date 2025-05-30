# === CLI logic for managing the library system ===

from library import Library, Book  # Import main classes
from db_connection import Connection

# Validate year input from user (must be numeric or empty)
def get_valid_year():
    while True:
        try:
            year = input("Year : ").strip()
            if not year:
                print("Error: Year is missing.")
                continue
            intYear = int(year)
            if intYear < 1800 or intYear > 2025:
                print("Enter a valid year.")
                continue
            return intYear
        except ValueError:
            print("Please enter a valid year (numeric value).")

# Display help menu
def show_help(commands):
    print("\n===== Library Management System =====")
    print("Available commands:")
    for cmd, desc in commands.items():
        print(f"  {cmd:<10} - {desc}")
    print("=====================================\n")

def main():
    # Check database connection before starting
    print("\nChecking database connection...")
    con = Connection().get_connection()
    if con is None:
        print("\nCannot start application without database connection!")
        print("Please ensure:")
        print("   • MySQL server is running")
        print("   • .env file exists with correct DB credentials")
        print("   • Database exists and is accessible\n")
        return  # Exit main function
    else:
        print("\nDatabase connected successfully!")
        con.close()

    lib = Library()
    
    commands = {
        "add": "Add a new book",
        "show": "Display all books",
        "search": "Search for books",
        "remove": "Remove a book",
        "edit": "Edit a book",
        "state": "Show stats",
        "exit or x": "Exit the program",
        "clear" : "Clear the content",
        "help": "Show help menu"
    }

    try:
        while True:
            command = input("\nEnter command (or 'help' for options): ").strip().lower()

            if command == "add":
                print("\nAll fields must be provided!\n")
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

            elif command == "clear":
                import os
                os.system('cls' if os.name == 'nt' else 'clear')

            elif command == "exit" or command == "x":
                print("\nExiting...")
                break

            else:
                print("\nUnknown command! Check 'help'")
    except KeyboardInterrupt:
        print("\nExiting...")


# Run only if this file is the entry point
if __name__ == "__main__":
    main()
