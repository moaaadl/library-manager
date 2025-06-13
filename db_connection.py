import sqlite3
from colorama import Fore, init
init(autoreset=True)

class Connection:
    DB_NAME = "library.db"
    
    @staticmethod
    def get_connection():
        try:
            conn = sqlite3.connect(Connection.DB_NAME)
            return conn
        except sqlite3.Error as e:
            print(Fore.RED + f"Database connection error: {e}")
            return None
    
    @staticmethod
    def init_database():
        conn = Connection.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS books (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        author TEXT NOT NULL,
                        year TEXT NOT NULL
                    )
                ''')
                
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        email TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL
                    )
                ''')
                
                conn.commit()
                print(Fore.GREEN + "Database initialized successfully!")
                
            except sqlite3.Error as e:
                print(Fore.RED + f"Error initializing database: {e}")
            finally:
                conn.close()