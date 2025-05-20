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
    def remove_books(self, name_book):
        for book in self.books:
            if name_book.lower() in book.title.lower():
                self.books.remove(book)
                self.save_to_file(BOOKS_FILE)
                print(f"'{name_book}' removed successfully!")
                return
        print(f"Oops, no book called '{name_book}' found here.")

    # Search for a book by name (also not case-sensitive)
    def search_book(self, name_book):
        for book in self.books:
            if name_book.lower() in book.title.lower():
                print(f"Found this book for you:\n{book}")
                return
        print(f"Book name '{name_book}' not found here.")
    # Editing the books in a simple way :)
    def edit_book(self, name_book):
        for book in self.books:
            if name_book.lower() in book.title.lower():
                new_title = input('Enter the new title : ')
                new_author = input('Enter the new author : ')
                new_year = input('Enter the new year : ')
                b = Book(new_title, new_author, new_year)
                self.books.append(b)
                self.save_to_file(BOOKS_FILE)
                self.load_from_file(BOOKS_FILE)
                print(f"\nBook with title {name_book} change to \n {b} \n Edited successfully!\n")
            else:
                print(f"Book name '{name_book}' not found here.")

    def stats_book(self):
        count_books = len(self.books) # number of books
        print(f"The number of books : {count_books}")
        
        min_year = self.books[0].year # the first book year

        for book in self.books:
            if int(book.year) < int(min_year): 
                min_year = book.year # the min year after for loop

        print(f"The oldest book was published in: {min_year}")

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
