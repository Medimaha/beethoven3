from flask import Flask, request, jsonify  
from .mail_send import send_gmail
from .model import Book
# from lms_app.calculate_stockv2 import run_stock_value_calculation
import repo
import logging
from .StockCalculator import StockCalculator
import json
import os
from .scrape import scrape

import threading
from time import sleep


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
# repo.libraryTablesCreate()

'''
    Retrieve all books from the library.

    This endpoint returns a list of all books in the library database.

    Returns:
        Response: A JSON array of book objects, each containing:
            - id (int): The unique identifier of the book.
            - title (str): The title of the book.
            - price (float): The price of the book.
            - copies (int): The number of copies available in stock.
'''

@app.route("/books", methods=['GET'])
def read_all_books():
    book_objects = repo.readAllBooks()
    books = []
    for book_obj in book_objects:
        book = {'id': book_obj.id, 'title': book_obj.title, 'price': book_obj.price, 'copies': book_obj.copies}
        books.append(book)
    return jsonify(books)


    """
    Create a new book in the library.

    This endpoint accepts a JSON object containing the details of the book to be created,
    adds it to the library database, and sends a notification email.

    Request Body:
        JSON object containing:
            - title (str): The title of the book.
            - price (float): The price of the book.
            - copies (int): The number of copies available in stock.

    Returns:
        Response: A JSON object representing the created book, containing:
            - id (int): The unique identifier of the created book.
            - title (str): The title of the book.
            - price (float): The price of the book.
            - copies (int): The number of copies available in stock.
    """
@app.route("/books", methods=['POST'])
def create_book():
    book = request.get_json()
    id = repo.createBook(Book(title=book['title'], price=book['price'], copies=book['copies']))
    book_c = repo.readBookById(id)
    savedBook = {'id':book_c.id, 'title':book_c.title, 'price': book_c.price, 'copies': book_c.copies}
    # mail sending after employee created
    from datetime import datetime
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    result = send_gmail("inahpm7@gmail.com",
            f"Book Created at {now_str}",
            f"name: {book['title']}")
    return jsonify(savedBook)
    # return jsonify(id)


    """
    Retrieve a book by its ID.

    This endpoint returns the details of a specific book identified by its ID.

    Args:
        id (int): The unique identifier of the book to be retrieved.

    Returns:
        Response: A JSON object representing the book, containing:
            - id (int): The unique identifier of the book.
            - title (str): The title of the book.
            - price (float): The price of the book.
            - copies (int): The number of copies available in stock.
    """
@app.route("/books/<id>", methods=['GET'])
def read_book_by_id(id):
    id = int(id)
    book_obj = repo.readBookById(id)
    book = {'id': book_obj.id, 'title': book_obj.title, 'price': book_obj.price, 'copies': book_obj.copies}
    return jsonify(book)


    """
    Update the details of an existing book.

    This endpoint updates the details of a book identified by its ID.

    Args:
        id (int): The unique identifier of the book to be updated.
        Request Body:
            JSON object containing:
                - title (str): The new title of the book.
                - price (float): The new price of the book.
                - copies (int): The new number of copies available in stock.

    Returns:
        Response: A JSON object representing the updated book, containing:
            - id (int): The unique identifier of the book.
            - title (str): The title of the book.
            - price (float): The price of the book.
            - copies (int): The number of copies available in stock.
    """
@app.route("/books/<id>", methods=['PUT'])
def update_book(id):
    id = int(id)
    book_data = request.get_json()
    repo.updateBook(repo.Book(id=id, title=book_data['title'], price=book_data['price'], copies=book_data['copies']))
    book_obj = repo.readBookById(id)
    saved_book = {'id': book_obj.id, 'title': book_obj.title, 'price': book_obj.price, 'copies': book_obj.copies}
    return jsonify(saved_book)


    """
    Delete a book by its ID.

    This endpoint removes a book from the library database identified by its ID.

    Args:
        id (int): The unique identifier of the book to be deleted.

    Returns:
        Response: A JSON object containing a message indicating the result of the deletion.
            Example:
                {"message": "Book with ID 5 has been deleted from the library."}
    """
@app.route("/books/<id>", methods=['DELETE'])
def delete_book_by_id(id):
    id = int(id)
    repo.deleteBook(id)
    return jsonify({"message": f"Book with ID {id} has been deleted from the library."}), 200

    """
    Send an email.

    This endpoint sends an email to the specified recipient with the provided subject and body.

    Request Body:
        JSON object containing:
            - to_address (str): The recipient's email address.
            - subject (str): The subject of the email.
            - body (str): The body content of the email.

    Returns:
        Response: A JSON object indicating the result of the email sending operation.
            - On success: {"message": "Email sent successfully!"}
            - On failure: {"error": "Failed to send email."}

    Raises:
        ValueError: If any of the required fields (to_address, subject, body) are missing.
    """
@app.route("/send-email", methods=['POST'])
def send_email():
    email_data = request.get_json()
    
    to_address = email_data.get('to_address')
    subject = email_data.get('subject')
    body = email_data.get('body')

    if not to_address or not subject or not body:
        return jsonify({"error": "Missing required fields: to_address, subject, body"}), 400

    success = send_gmail(to_address, subject, body)

    if success:
        return jsonify({"message": "Email sent successfully!"}), 200
    else:
        return jsonify({"error": "Failed to send email."}), 500


    """
    Endpoint to get the total stock value of all books.

    Returns:
        Response: A JSON object containing the total stock value.
    """
total_value = 0

def calculate_stock_value(batch_size=10):
    global total_value
    try:
        books = read_all_books()
        print(len(books))
        total_value = 0
        for i in range(0, len(books), batch_size):
            print(f"{i}")
            batch = books[i:i + batch_size]
            batch_value = sum(book['price'] * book['copies'] for book in batch)
            total_value += batch_value
            
            logging.info(f"Processed batch {i // batch_size + 1}: Total value = {batch_value:.2f}")
            sleep(1)  # Simulate processing time
            
        logging.info(f"Total stock value: {total_value:.2f}")
        
    except Exception as e:
        logging.error(f"Error calculating stock value: {e}")
        total_value = 0  # Reset total_value on error

# Function to run the stock value calculation in a separate thread
def run_stock_value_calculation():
    thread = threading.Thread(target=calculate_stock_value)
    thread.start()
    thread.join()

@app.route("/books/stock-value", methods=['GET'])
def get_stock_value():
    try:
        calculator = StockCalculator()
        total_value = calculator.calculate_total_stock_value()
        return jsonify({'total_stock_value': total_value})
    except Exception as e:
        logging.error(f"Error calculating stock value: {str(e)}")
        return jsonify({'error': str(e)}), 500




@app.route('/books/scrapen/<int:pages>', methods=['POST'])
def scrape_books_endpoint(pages):
    
    scrape(pages)  # Ensure this function is defined elsewhere in your code
    json_file_path = "./app/scraped_books.json"
    
    try:
        if not os.path.exists(json_file_path):
            logging.error(f"Scraped JSON file not found: {json_file_path}")
            return jsonify({'error': 'Scraped JSON file not found'}), 404
        
        with open(json_file_path, 'r', encoding='utf-8') as file:
            scraped_data = json.load(file)
        
        logging.info("Successfully retrieved scraped books data")
        return jsonify(scraped_data), 200
    
    except json.JSONDecodeError as e:
        logging.error(f"Invalid JSON format in {json_file_path}: {str(e)}")
        return jsonify({'error': 'Invalid JSON format'}), 500
    
    except Exception as e:
        logging.error(f"Error reading scraped books: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/books/scraped', methods=['GET'])
def get_scraped_books():
    try:
        json_file_path = "./lms_app/scraped_books.json"
        if not os.path.exists(json_file_path):
            logging.error(f"Scraped JSON file not found: {json_file_path}")
            return jsonify({'error': 'Scraped JSON file not found'}), 404
        
        with open(json_file_path, 'r', encoding='utf-8') as file:
            scraped_data = json.load(file)
        
        logging.info("Successfully retrieved scraped books data")
        return jsonify(scraped_data), 200
    
    except json.JSONDecodeError as e:
        logging.error(f"Invalid JSON format in {json_file_path}: {str(e)}")
        return jsonify({'error': 'Invalid JSON format'}), 500
    
    except Exception as e:
        logging.error(f"Error reading scraped books: {str(e)}")
        return jsonify({'error': str(e)}), 500

def controller():
    app.run(debug=True)
