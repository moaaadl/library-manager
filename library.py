import os
import json

class Book:
    # Constructor: set up the book with title, author, and year
    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year

    # When you print a Book object, this is what shows up — nice and neat
    def __str__(self):
        return f"'{self.title} by {self.author}, {self.year}'"
    
    # This turns the book into a dictionary — perfect for saving to JSON later
    def to_dict(self):
        # Just pack all the info in a dict so we can save or send it easily
        return {
            "title": self.title,
            "author": self.author,
            "year": self.year
        }

    # This is like a factory method: gives you a Book object from a dictionary
    @classmethod
    def from_dict(cls, data):
        # 'cls' means the Book class itself — so we're making a new Book here
        # Just pull out the info from the dict and call the constructor
        return cls(data["title"], data["author"], data["year"])


class Library:
    # Constructor: start with an empty list of books
    def __init__(self):
        self.books = []

    # Add a book object to the library collection
    def add_book(self, book):
        self.books.append(book)
        print(f"{book} has been added successfully!")

    # Show all books in the library, one by one
    def show_books(self):
        print("Here are the books in the library:")
        for book in self.books:
            print(book)

    # Remove a book by name (case-insensitive)
    def remove_books(self, name_book):
        for book in self.books:
            if name_book.lower() in book.title.lower():
                self.books.remove(book)
                print(f"'{name_book}' removed successfully! ✂️")
                return
        print(f"Oops, no book called '{name_book}' found here.")

    # Search for a book by name (case-insensitive)
    def search_book(self, name_book):
        for book in self.books:
            if name_book.lower() in book.title.lower():
                print(f"Found this book for you:\n{book}")
                return
        print(f"No luck finding '{name_book}' here.")

    # Save all books to a JSON file
    def save_to_file(self, filename):
        # Convert each Book object to a dictionary
        data = [book.to_dict() for book in self.books]
        
        # Open the file in write mode and save the list of book dicts as JSON
        with open(filename, 'w') as f:
            json.dump(data, f)

    # Load books from a JSON file into the Library's books list
    def load_from_file(self, filename):
        # Check if the file exists to avoid errors
        if os.path.exists(filename):
            # Open the file in read mode
            with open(filename, 'r') as f:
                # Load JSON data (a list of dictionaries)
                data = json.load(f)
                
                # Convert each dictionary back into a Book object and update the books list
                self.books = [Book.from_dict(d) for d in data]
        else:
            print("File not found")


        




# Let's try it out:

lib = Library()


# Load from file — brings books back from JSON
lib.load_from_file("books.json")

# Show again — books are back baby!
lib.show_books()
