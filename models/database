"""Database connection module"""
import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG

def get_db_connection():
    """Create and return database connection"""
    try:
        connection = mysql.connector.connect(
            host=DB_CONFIG['host'],
            database=DB_CONFIG['database'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None
