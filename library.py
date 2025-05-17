class Book:
    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year

    def __str__(self):
        return f"{self.title} by {self.author}, {self.year}"

class Library:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def show_books(self):
        for book in self.books:
            print(book)

    def remove_books(self, name_book):
        for book in self.books:
            if name_book.lower() in book.title.lower():
                self.books.remove(book)
                print(f"'{name_book}' removed successfully!")
                return
        print(f"Book '{name_book}' not found.")

    def search_book(self, name_book):
        for book in self.books:
            if name_book.lower() in book.title.lower():
                print(f"Found book:\n {book}")
                return
        print(f" Book '{name_book}' not found.")


# try the class

lib = Library()

book1 = Book("Moaad", "M", 1949)
book2 = Book("The Alchemist", "Paulo Coelho", 1988)

lib.add_book(book1)
lib.add_book(book2)
lib.show_books()
lib.search_book('moaad')