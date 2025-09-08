import sqlite3
from model import Book
import logging
from concurrent.futures import ThreadPoolExecutor
from typing import List

def connect():
    con = sqlite3.connect('lms_app_db.db')
    return con

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

def create_new_book(book):
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

def read_all():
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

def update_book_by_id(book):
    # print(book)
    sql = """UPDATE library SET title = ?, price = ?, copies = ? WHERE id = ?"""
    params = (book.title, book.price, book.copies, book.id,)

    try:
        with connect() as con:  # Automatically closes the connection
            cur = con.cursor()
            cur.execute(sql, params)
            con.commit()
            # return cur.rowcount  # Returns the number of rows affected
            return book.id
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def delete_book_by_id(book_id):
    sql = """DELETE FROM library WHERE id = ?"""

    try:
        with connect() as con:  # Automatically closes the connection
            cur = con.cursor()
            cur.execute(sql, (book_id,))
            con.commit()
            # return cur.rowcount  # Returns the number of rows affected
            return book_id
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def read_book_id(id):
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



def initial_data():
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
        {"title": "Book Eleven", "price": 20.00, "copies": 2},
        {"title": "Book Twelve", "price": 5.75, "copies": 12}
    ]

    for book in book_data:
        create_new_book(Book(title=book['title'], price=book['price'], copies=book['copies']))