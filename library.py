from db_connection import Connection


class Book:
    # This sets up a new book with title, author, and year
    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year

    # When you print the book, this is what shows up (clean and readable)
    def __str__(self):
        return f"'{self.title} by {self.author} in {self.year}'"
    
    # When you inspect the book in a list or debug, this is what shows up
    def __repr__(self):
        return f"Book(title='{self.title}', author='{self.author}', year='{self.year}')"


    # This turns the book into a simple dictionary (so we can save it easily)
    def to_dict(self):
        book_data = {
            "title": self.title,
            "author": self.author,
            "year": self.year
        }
        return book_data
    

    # This takes a dictionary and makes a Book from it
    @classmethod
    def from_dict(cls, data):
        title = data["title"]
        author = data["author"]
        year = data["year"]
        return cls(title, author, year)
    

    def save_to_db(self):
        db = Connection.get_connection()
        if not db:
            return False
        try:
            cursor = db.cursor()
            query = "INSERT INTO books (title, author, year) VALUES (%s, %s, %s)"
            value = (self.title, self.author, self.year)
            cursor.execute(query, value) 
            db.commit()
        except Exception as e:
            print(f"Error saving to DB: {e}")
        finally:
            db.close()



class Library:

    # Start with an empty library (no books yet)
    def __init__(self):
        self.books = []
        self.load_from_db()

    # Add a book to the list
    def add_book(self, book):
        titles = [b.title.lower() for b in self.books]
        if book.title.lower() not in titles:
            check = input(f"Are you sure you want to save '{book.title}'? (Y/N) ").strip().lower()
            if check == "y":
                self.books.append(book)
                book.save_to_db()
                print(f"{book} has been added successfully!")
            else:
                print("Add canceled.")
        else:
            print(f"Book {book.title} is on library!")

    # Show all the books in the library
    def show_books(self):
        print("Here are the books in the library: \n")
        c = 0
        for book in self.books:
            c = c + 1
            print(f"{c} - {book}")

    # Remove a book by name (not case-sensitive)
    def remove_book(self, name_book):
        db = Connection.get_connection()
        for book in self.books:
            if name_book.lower() == book.title.lower():
                # this for check if remove or not
                check = input(f"Are you sure you want to remove '{name_book}' ? (Y/N) : ") 
                if check.lower() == 'y':
                    self.books.remove(book)
                    print(f"'{name_book}' removed successfully!") # remove from array 

                    # remove from db
                    try:
                        cursor = db.cursor()
                        query = "DELETE FROM books WHERE title = %s AND author = %s AND year = %s"
                        value = (book.title, book.author, book.year)
                        cursor.execute(query, value) 
                        db.commit()
                    except Exception as e:
                        print(f"Error saving to DB: {e}")
                    finally:
                        db.close()
                else:
                    print('You canceled the remove')
                return
        print(f"Oops, no book called '{name_book}' found here.")


    # Search for a book by title name only in self.books not DB
    def search_book(self, name_book):
        found = False  # check if we found any matching book
        c = 0 

        for book in self.books:
            if name_book.lower() in book.title.lower() or name_book.lower() in book.author.lower():
                if not found:
                    print(f"Matching books : '{name_book}':")
                    found = True
                c += 1
                print(f"{c} - {book}")
            

        if not found:
            print(f"Book name '{name_book}' not found here.")



    # Editing the books from the self.books and DB
    def edit_book(self, name_book):
        db = Connection().get_connection()
        cursor = db.cursor()
        for book in self.books:
            if name_book.lower() == book.title.lower():
                while True:
                    check = input(f"What do you want to change from '{name_book}' ? : (Title / author / year) : ").strip().lower()
                    if check not in ['title', 'author', 'year']:
                        print("Please select Title, Author, or Year")
                        continue 
                    else:
                        break  # out

                if check == "title":
                    while True:
                        new_title = input('Enter the new title: ')
                        if new_title == book.title:
                            print("You didn't change anything! Try again.")
                        else:
                            try:
                                query = "UPDATE books SET title = %s WHERE title = %s AND author = %s AND year = %s"
                                values = (new_title, book.title, book.author, book.year)
                                cursor.execute(query, values) 
                                db.commit()
                                book.title = new_title
                            except Exception as e:
                                print(f"Error saving to DB: {e}")
                            break

                elif check == "author":
                    while True:
                        new_author = input('Enter the new author: ')
                        if new_author == book.author:
                            print("You didn't change anything! Try again.")
                        else:
                            try:
                                query = "UPDATE books SET author = %s WHERE title = %s AND author = %s AND year = %s"
                                values = (new_author, book.title, book.author, book.year)
                                cursor.execute(query, values) 
                                db.commit()
                                book.author = new_author
                            except Exception as e:
                                print(f"Error saving to DB: {e}")
                            break

                elif check == "year":
                    while True:
                        new_year = input('Enter the new year: ')
                        if not new_year.isdigit():
                            print("Year must be a number! Try again.")
                            continue

                        if new_year == book.year:
                            print("You didn't change anything! Try again.")
                            continue

                        try:
                            query = "UPDATE books SET year = %s WHERE title = %s AND author = %s AND year = %s"
                            values = (new_year, book.title, book.author, book.year)
                            cursor.execute(query, values) 
                            db.commit()
                            book.year = new_year
                        except Exception as e:
                            print(f"Error saving to DB: {e}")
                        break

                cursor.close()
                db.close()
                print(f"\nBook with title '{name_book}' changed to \n{book}\nEdited successfully!\n")
                return

        print(f"Book name '{name_book}' not found here.")


    def stats_book(self):
        if not self.books: # if is no books
            print("No books to analyze.")
            return

        count_books = len(self.books)
        print(f"The number of books : {count_books}")

        oldest = self.books[0]
        for book in self.books:
            if int(book.year) < int(oldest.year):
                oldest = book

        print(f"The oldest book was published in: '{oldest.year}' by '{oldest.author}'")


    def load_from_db(self):
        db = Connection.get_connection()
        try:
            cursor = db.cursor()
            cursor.execute("SELECT title, author, year FROM books")
            results = cursor.fetchall()
            self.books = []
            for row in results:
                book = Book(row[0], row[1], row[2])
                self.books.append(book)
        except Exception as e:
            print(f"Error loading from DB: {e}")
        finally:
            db.close()
