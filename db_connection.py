import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()

class Connection:
    def __init__(self):
        pass


    @staticmethod
    def get_connection():
        try:
            connection = mysql.connector.connect(
                host=os.getenv("DB_HOST"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASS"),
                database=os.getenv("DB_NAME")
            )

            if connection.is_connected():
                return connection

        except Error as e:
            return None
