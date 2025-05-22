import os
import json

# json file
BOOKS_FILE = "books.json"

class Book:
    # This sets up a new book with title, author, and year
    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year

    # When you print the book, this is what shows up (clean and readable)
    def __str__(self):
        return f"'{self.title} by {self.author} in {self.year}'"
    
    # Turn the book into a dictionary so we can save it later (like to JSON)
    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "year": self.year
        }

    # Take a dictionary and turn it back into a Book object
    @classmethod
    def from_dict(cls, data):
        return cls(data["title"], data["author"], data["year"])


class Library:


    # Start with an empty library (no books yet)
    def __init__(self):
        self.books = []
        self.load_from_file(BOOKS_FILE)

    # Add a book to the list
    def add_book(self, book):
        self.books.append(book)
        self.save_to_file(BOOKS_FILE)
        print(f"{book} has been added successfully!")

    # Show all the books in the library
    def show_books(self):
        print("Here are the books in the library: \n")
        c = 0
        for book in self.books:
            c = c + 1
            print(f"{c} - {book}")

    # Remove a book by name (not case-sensitive)
    def remove_book(self, name_book):
        for book in self.books:
            if name_book.lower() == book.title.lower():
                # this for check if remove or not
                check = input(f"Are you sure you want to remove '{name_book}' ? (Y/N) : ") 
                if check.lower() == 'y':
                    self.books.remove(book)
                    self.save_to_file(BOOKS_FILE)
                    print(f"'{name_book}' removed successfully!")
                else:
                    print('You canceled the remove')
                return
        print(f"Oops, no book called '{name_book}' found here.")


    # Search for a book by title name
    def search_book(self, name_book):
        found = False  # check if we found any matching book
        c = 0  # Counter

        for book in self.books:
            if name_book.lower() in book.title.lower():
                if not found:
                    print("Matching books:")  # Only print this once, when we find the first match
                    found = True
                c += 1
                print(f"{c} - {book}")

        if not found:
            print(f"Book name '{name_book}' not found here.")



    # Editing the books
    def edit_book(self, name_book):
        for book in self.books:
            if name_book.lower() == book.title.lower():
                while True:
                    check = input(f"What do you want to change from '{name_book}' ? : (Title / author / year) ").strip().lower()
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
                            book.title = new_title
                            break

                elif check == "author":
                    while True:
                        new_author = input('Enter the new author: ')
                        if new_author == book.author:
                            print("You didn't change anything! Try again.")
                        else:
                            book.author = new_author
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

                        book.year = new_year
                        break


                self.save_to_file(BOOKS_FILE)
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


    # Save all the books to a JSON file
    def save_to_file(self, filename):
        # First, convert every book to a dictionary
        data = [book.to_dict() for book in self.books]
        
        # Then write that list into a file as JSON
        with open(filename, 'w') as f:
            json.dump(data, f)

    # Load books from a JSON file into the library
    def load_from_file(self, filename):
        # Only do it if the file exists (to avoid crashing)
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                data = json.load(f)
                self.books = [Book.from_dict(d) for d in data]
        else:
            print("File not found")
