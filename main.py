# === CLI logic for managing the library system ===

from library import Library, Book  # Import main classes
from db_connection import Connection
from colorama import Fore, init
init(autoreset=True)

# Display help menu
def show_help(commands):
    print(Fore.BLUE + "\n===== Library Management System =====")
    print(Fore.BLUE + "Available commands:")
    for cmd, desc in commands.items():
        print(Fore.BLUE + f"  {cmd:<10} - {desc}")
    print(Fore.BLUE + "=====================================\n")

def main():
    # Check database connection before starting
    print(Fore.YELLOW + "\nChecking database connection...")
    con = Connection().get_connection()
    if con is None:
        print(Fore.YELLOW + "\nCannot start application without database connection!")
        print(Fore.YELLOW + "Please ensure:")
        print(Fore.YELLOW + "   • MySQL server is running")
        print(Fore.YELLOW + "   • .env file exists with correct DB credentials")
        print(Fore.YELLOW + "   • Database exists and is accessible\n")
        return  # Exit main function
    else:
        print(Fore.GREEN + "\nDatabase connected successfully!")
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
                                print(Fore.RED + "Enter a valid year")
                        except ValueError:
                            print(Fore.RED + "Year must be a number")
                    else:
                        print(Fore.RED + 'Usage: add "Title" "Author" year')
                except ValueError:
                    print(Fore.RED + 'Usage: add "Title" "Author" year')
                    print(Fore.RED + 'Make sure to use quotes around title and author')

            elif command == "show":
                if lib.books:
                    lib.show_books()
                else:
                    print(Fore.RED + "Library is empty.")

            elif command == "state":
                lib.stats_book()

            elif command.startswith("edit "):
                # Extract the search term from the command
                edit_term = command[5:]  # Remove "edit " part
                if edit_term:
                    lib.edit_book(edit_term)
                else:
                    print(Fore.RED + "Usage: edit <term>")

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
                    print(Fore.RED + "Usage: search <term>")

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
                    print(Fore.RED + "Usage: remove <term>")

            # elif command == "remove":
            #     title = input("Enter title to remove: ").strip()
            #     if title:
            #         lib.remove_book(title)
            #     else:
            #         print("Remove canceled.")

            elif command == "help":
                show_help(commands)

            elif command == "help add":
                print(Fore.BLUE + "\n=== ADD COMMAND ===")
                print(Fore.BLUE + 'Usage: add "Title" "Author" year')
                print(Fore.BLUE + "===================\n")

            elif command == "help remove":
                print(Fore.BLUE + "\n=== REMOVE COMMAND ===")
                print(Fore.BLUE + "Usage: remove BookTitle")
                print(Fore.BLUE + "======================\n")

            elif command == "help search":
                print(Fore.BLUE + "\n=== SEARCH COMMAND ===")
                print(Fore.BLUE + "Usage: search term")
                print(Fore.BLUE + "======================\n")

            elif command == "help edit":
                print(Fore.BLUE + "\n=== EDIT COMMAND ===")
                print(Fore.BLUE + "Usage: edit BookTitle")
                print(Fore.BLUE + "Then follow prompts to change title/author/year")
                print(Fore.BLUE + "====================\n")

            elif command == "clear":
                import os
                os.system('cls' if os.name == 'nt' else 'clear')

            elif command == "exit" or command == "x":
                print(Fore.CYAN + "\nExiting...")
                break

            else:
                print(Fore.RED + "\nUnknown command! Check 'help'")
    except KeyboardInterrupt:
        print(Fore.CYAN + "\nExiting...")


# Run only if this file is main.py
if __name__ == "__main__":
    main()
