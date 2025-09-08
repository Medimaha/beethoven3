import sqlite3
from model import Book
import logging
from concurrent.futures import ThreadPoolExecutor
from typing import List

"""
    Establish a connection to the SQLite database.

    This function creates and returns a connection object to the SQLite database
    specified by the database file name 'app_db.db'.

    Returns:
        sqlite3.Connection: A connection object to the SQLite database.

    Raises:
        sqlite3.Error: If there is an error connecting to the database.
    """
def connect():
    con = sqlite3.connect('app_db.db')
    return con


    """
    Create the library table in the database if it does not already exist.

    This function executes a SQL command to create a table named 'library' with the following columns:
    - id: An auto-incrementing primary key.
    - title: The title of the book (string, not null).
    - price: The price of the book (integer, not null).
    - copies: The number of copies available in stock (integer, not null).

    Returns:
        None

    Raises:
        Exception: If there is an error connecting to the database or executing the SQL command.
    """
    sql = """CREATE TABLE IF NOT EXISTS library(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title VARCHAR(255) NOT NULL,
        price INTEGER NOT NULL,
        copies INTEGER NOT NULL
    )"""
def libraryTablesCreate():
    sql = """CREATE TABLE IF NOT EXISTS library(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title VARCHAR(255) NOT NULL,
        price INTEGER NOT NULL,
        copies INTEGER NOT NULL
    )"""

    try:
        with connect() as con:
            con.execute(sql)
            print("Library table created or already exists.")
    except Exception as e:
        print(f"An error occurred while creating the table: {e}")


    """
    Insert a new book into the library database.

    This function takes a Book object as input, inserts its details into the 'library' table,
    and returns the unique identifier of the newly created book.

    Args:
        book (Book): A Book object containing the following attributes:
            - title (str): The title of the book.
            - price (float): The price of the book.
            - copies (int): The number of copies available in stock.

    Returns:
        int: The unique identifier (ID) of the newly created book, or None if the operation fails.

    Raises:
        Exception: If there is an error connecting to the database, executing the query, or committing the transaction.
    """
def createBook(book):
    sql = """INSERT INTO library(title, price, copies)
            VALUES(?, ?, ?)"""
    params = (book.title, book.price, book.copies)

    try:
        with connect() as con:
            cur = con.cursor()
            cur.execute(sql, params)
            id = cur.lastrowid
            con.commit()
            return id
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
    
    """
    Retrieve all books from the library database.

    This function connects to the database, executes a SQL query to select all records
    from the 'library' table, and returns a list of Book objects representing each book.

    Returns:
        list: A list of Book objects, each containing the following attributes:
            - id (int): The unique identifier for the book.
            - title (str): The title of the book.
            - price (float): The price of the book.
            - copies (int): The number of copies available in stock.

    Raises:
        Exception: If there is an error connecting to the database or executing the query.
    """
def readAllBooks():
    sql = """SELECT * FROM library"""
    params = tuple()
    con = connect()
    cur = con.cursor()
    response = cur.execute(sql,params)
    result = response.fetchall() 
    con.close()

    books = []
    for row in result:
        books.append(Book(id=row[0], title=row[1], price=row[2], copies=row[3]))
    return books 

    """
    Retrieve all books from the library database.

    This function connects to the database, executes a SQL query to select all records
    from the 'library' table, and returns a list of Book objects representing each book.

    Returns:
        list: A list of Book objects, each containing the following attributes:
            - id (int): The unique identifier for the book.
            - title (str): The title of the book.
            - price (float): The price of the book.
            - copies (int): The number of copies available in stock.

    Raises:
        Exception: If there is an error connecting to the database or executing the query.
    """
def readAllBooksList():
    sql = """SELECT * FROM library"""
    params = tuple()
    con = connect()
    cur = con.cursor()
    response = cur.execute(sql,params)
    result = response.fetchall() 
    con.close()

    books = []
    for row in result:
        books.append(Book(id=row[0], title=row[1], price=row[2], copies=row[3]))
    return books 

    """
    Update the details of an existing book in the library database.

    This function takes a Book object as input and updates its details in the 'library' table
    based on the book's ID.

    Args:
        book (Book): A Book object containing the following attributes:
            - id (int): The unique identifier of the book.
            - title (str): The new title of the book.
            - price (float): The new price of the book.
            - copies (int): The new number of copies available in stock.

    Returns:
        int: The number of rows affected by the update operation, or None if the operation fails.

    Raises:
        Exception: If there is an error connecting to the database, executing the query, or committing the transaction.
    """
def updateBook(book):
    
    sql = """UPDATE library SET title = ?, price = ?, copies = ? WHERE id = ?"""
    params = (book.title, book.price, book.copies, book.id,)

    try:
        with connect() as con:  # Automatically closes the connection
            cur = con.cursor()
            cur.execute(sql, params)
            con.commit()
            return cur.rowcount  # Returns the number of rows affected
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

    """
        Delete a book from the library database by its ID.

        This function removes the book with the specified ID from the 'library' table.

        Args:
            book_id (int): The unique identifier of the book to be deleted.

        Returns:
            int: The number of rows affected by the delete operation, or None if the operation fails.

        Raises:
            Exception: If there is an error connecting to the database, executing the query, or committing the transaction.
    """
def deleteBook(book_id):
    sql = """DELETE FROM library WHERE id = ?"""

    try:
        with connect() as con:  # Automatically closes the connection
            cur = con.cursor()
            cur.execute(sql, (book_id,))
            con.commit()
            return cur.rowcount  # Returns the number of rows affected
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

    """
        Retrieve a book from the library database by its ID.

        This function fetches the details of a book with the specified ID from the 'library' table
        and returns a Book object.

        Args:
            id (int): The unique identifier of the book to be retrieved.

        Returns:
            Book: A Book object containing the book's details, or None if no book is found with the given ID.

        Raises:
            Exception: If there is an error connecting to the database or executing the query.
    """
def readBookById(id):
    sql = """SELECT * FROM library WHERE (id=?)"""
    params = (id,)
    con = connect()
    cur = con.cursor()
    response = cur.execute(sql,params)
    result = response.fetchone() #row=[id,title,...]
    con.close()

    if result != None:
        book = Book(id=result[0],title=result[1],price=result[2],copies=result[3])
    else:
        book = None 
    return book



def seed_data():
    book_data = [
        {"title": "Book One", "price": 10.99, "copies": 5},
        {"title": "Book Two", "price": 15.50, "copies": 3},
        {"title": "Book Three", "price": 7.25, "copies": 10},
        {"title": "Book Four", "price": 12.00, "copies": 2},
        {"title": "Book Five", "price": 8.99, "copies": 4},
        {"title": "Book Six", "price": 14.75, "copies": 1},
        {"title": "Book Seven", "price": 9.50, "copies": 6},
        {"title": "Book Eight", "price": 11.25, "copies": 8},
        {"title": "Book Nine", "price": 13.00, "copies": 7},
        {"title": "Book Ten", "price": 6.50, "copies": 9},
       
       
    ]

    for book in book_data:
        createBook(Book(title=book['title'], price=book['price'], copies=book['copies']))