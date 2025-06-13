from db_connection import Connection

class Book:
    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year

    def __str__(self):
        return f"'{self.title}' by {self.author} ({self.year})"
    
    def __repr__(self):
        return f"Book(title='{self.title}', author='{self.author}', year='{self.year}')"

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "year": self.year
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(data["title"], data["author"], data["year"])
    
    def save_to_db(self):
        conn = Connection.get_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            query = "INSERT INTO books (title, author, year) VALUES (?, ?, ?)"
            cursor.execute(query, (self.title, self.author, self.year))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error saving to DB: {e}")
            return False
        finally:
            conn.close()