from models.book import Book  # Fixed: removed 'models.' since book.py is in root directory
from db_connection import Connection
from colorama import Fore, init
init(autoreset=True)


class Library:

    def __init__(self):
        self.books = []
        self.load_from_db()



    def add_book(self, book):
        titles = [b.title.lower() for b in self.books]
        if book.title.lower() not in titles:
            check = input(Fore.RED + f"Are you sure you want to save '{book.title}'? (Y/N): ").strip().lower()
            if check == "y":
                if book.save_to_db():
                    self.books.append(book)
                    print(Fore.GREEN + f"{book} has been added successfully!")
                else:
                    print(Fore.RED + "Failed to save book to database.")
            else:
                print(Fore.RED + "Add canceled.")
        else:
            print(Fore.YELLOW + f"Book '{book.title}' already exists in library!")



    def show_books(self):
        if not self.books:
            print(Fore.YELLOW + "No books in the library.")
            return
            
        print(Fore.BLUE + "Here are the books in the library:\n")
        for i, book in enumerate(self.books, 1):
            print(f"{i} - {book}")



    def remove_book(self, name_book):
        for book in self.books:
            if name_book.lower() == book.title.lower():
                check = input(Fore.RED + f"Are you sure you want to remove '{name_book}'? (Y/N): ").strip().lower()
                
                if check == 'y':
                    conn = Connection.get_connection()
                    if conn:
                        try:
                            cursor = conn.cursor()
                            query = "DELETE FROM books WHERE title = ? AND author = ? AND year = ?"
                            values = (book.title, book.author, book.year)
                            cursor.execute(query, values)
                            conn.commit()
                            
                            self.books.remove(book)
                            print(Fore.GREEN + f"'{name_book}' removed successfully!")
                            
                        except Exception as e:
                            print(f"Error deleting from DB: {e}")
                        finally:
                            conn.close()
                    else:
                        print(Fore.RED + "Could not connect to database!")
                else:
                    print(Fore.RED + 'Remove operation canceled.')
                return
        
        print(Fore.RED + f"Book '{name_book}' not found.")

    def search_book(self, name_book):
        matches = [] 
        
        for book in self.books:
            if name_book.lower() in book.title.lower() or name_book.lower() in book.author.lower():
                matches.append(book)
        
        if matches:
            print(f"Found {len(matches)} matching book(s) for '{name_book}':")
            for i, book in enumerate(matches, 1):
                print(f"{i} - {book}")
        else:
            print(Fore.RED + f"No books found matching '{name_book}'.")



    def edit_book(self, name_book):
        for book in self.books:
            if name_book.lower() == book.title.lower():
                while True:
                    check = input(f"What do you want to change in '{name_book}'? (title/author/year): ").strip().lower()
                    if check in ['title', 'author', 'year']:
                        break
                    print(Fore.RED + "Please select: title, author, or year")

                new_value = input(Fore.BLUE + f'Enter the new {check}: ').strip()
                
                if check == 'year' and not new_value.isdigit():
                    print(Fore.RED + "Year must be a number!")
                    return
                
                current_value = getattr(book, check)
                if new_value == current_value:
                    print(Fore.RED + "No changes made - same value entered.")
                    return

                # Update database
                conn = Connection.get_connection()
                if conn:
                    try:
                        cursor = conn.cursor()
                        query = f"UPDATE books SET {check} = ? WHERE title = ? AND author = ? AND year = ?"
                        values = (new_value, book.title, book.author, book.year)
                        cursor.execute(query, values)
                        conn.commit()
                        
                        setattr(book, check, new_value)
                        print(Fore.GREEN + f"Book updated successfully!\nNew details: {book}")
                        
                    except Exception as e:
                        print(f"Error updating database: {e}")
                    finally:
                        cursor.close()
                        conn.close()
                return
        
        print(Fore.RED + f"Book '{name_book}' not found.")

    def stats_book(self):
        if not self.books:
            print(Fore.YELLOW + "No books to analyze.")
            return

        print(Fore.CYAN + f"Total number of books: {len(self.books)}")
        
        oldest = min(self.books, key=lambda b: int(b.year))
        print(Fore.CYAN + f"Oldest book: '{oldest.title}' by {oldest.author} ({oldest.year})")
        
        newest = max(self.books, key=lambda b: int(b.year))
        print(Fore.CYAN + f"Newest book: '{newest.title}' by {newest.author} ({newest.year})")

    def load_from_db(self):
        conn = Connection.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='books'")
                if cursor.fetchone():
                    cursor.execute("SELECT title, author, year FROM books")
                    results = cursor.fetchall()
                    self.books = []
                    for row in results:
                        book = Book(row[0], row[1], row[2])
                        self.books.append(book)
                    print(Fore.BLUE + f"Loaded {len(self.books)} books from database.")
                else:
                    self.books = []
                    print("Books table not found. Starting with empty library.")
            except Exception as e:
                print(f"Error loading from database: {e}")
                self.books = []
            finally:
                conn.close()
        else:
            print("Could not connect to database.")
            self.books = []