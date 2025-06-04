# === CLI logic for managing the library system ===

from library import Library, Book  # Import main classes
from db_connection import Connection

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
        "clear": "Clear the content",
        "help add": "Show how to add books",
        "help remove": "Show how to remove books", 
        "help search": "Show how to search books",
        "help edit": "Show how to edit books"
    }

    try:
        while True:
            command = input("\nEnter command (or 'help' for options): ").strip().lower()

            if command.startswith("add "):
                args = command[4:].strip()
                try:
                    import shlex
                    parts = shlex.split(args)
                    
                    if len(parts) == 3:
                        title, author, year_str = parts
                        try:
                            year = int(year_str)
                            if 1800 <= year <= 2025:
                                b = Book(title, author, year)
                                lib.add_book(b)
                            else:
                                print("Enter a valid year")
                        except ValueError:
                            print("Year must be a number")
                    else:
                        print('Usage: add "Title" "Author" year')
                except ValueError:
                    print('Usage: add "Title" "Author" year')
                    print('Make sure to use quotes around title and author')

            elif command == "show":
                if lib.books:
                    lib.show_books()
                else:
                    print("Library is empty.")

            elif command == "state":
                lib.stats_book()

            elif command.startswith("edit "):
                # Extract the search term from the command
                edit_term = command[5:]  # Remove "edit " part
                if edit_term:
                    lib.edit_book(edit_term)
                else:
                    print("Usage: edit <term>")

            # elif command == "edit":
            #     title = input("Enter title to edit: ").strip()
            #     if title: 
            #         lib.edit_book(title)
            #     else:
            #         print("Edit canceled.")

            elif command.startswith("search "):
                # Extract the search term from the command
                search_term = command[7:]  # Remove "search " part
                if search_term:
                    lib.search_book(search_term)
                else:
                    print("Usage: search <term>")

            # elif command == "search":
            #     search_term = input("Enter search term: ").strip()
            #     if search_term:
            #         lib.search_book(search_term)

            elif command.startswith("remove "):
                # Extract the search term from the command
                remove_term = command[7:]  # Remove "search " part
                if remove_term:
                    lib.remove_book(remove_term)
                else:
                    print("Usage: remove <term>")

            # elif command == "remove":
            #     title = input("Enter title to remove: ").strip()
            #     if title:
            #         lib.remove_book(title)
            #     else:
            #         print("Remove canceled.")

            elif command == "help":
                show_help(commands)

            elif command == "help add":
                print("\n=== ADD COMMAND ===")
                print('Usage: add "Title" "Author" year')
                print("===================\n")

            elif command == "help remove":
                print("\n=== REMOVE COMMAND ===")
                print("Usage: remove BookTitle")
                print("======================\n")

            elif command == "help search":
                print("\n=== SEARCH COMMAND ===")
                print("Usage: search term")
                print("======================\n")

            elif command == "help edit":
                print("\n=== EDIT COMMAND ===")
                print("Usage: edit BookTitle")
                print("Then follow prompts to change title/author/year")
                print("====================\n")

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


# Run only if this file is main.py
if __name__ == "__main__":
    main()
