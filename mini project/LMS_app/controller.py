from flask import Flask, request, jsonify  
from mail_sender import send_gmail
from model import Book
import repo
import logging
from StockCalculator import StockCalculator
import json
import os
from scraper import scrape

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

app = Flask(__name__)

@app.route("/books", methods=['GET'])
def read_all_books():
    book_objects = repo.read_all()
    books = []
    for book_obj in book_objects:
        book = {'id': book_obj.id, 'title': book_obj.title, 'price': book_obj.price, 'copies': book_obj.copies}
        books.append(book)
    return jsonify(books)

@app.route("/books", methods=['POST'])
def create_book():
    book = request.get_json()
    id = repo.create_new_book(Book(title=book['title'], price=book['price'], copies=book['copies']))
    book_c = repo.read_book_id(id)
    savedBook = {'id':book_c.id, 'title':book_c.title, 'price': book_c.price, 'copies': book_c.copies}
    # mail sending after employee created
    from datetime import datetime
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    result = send_gmail("rsudha1610@gmail.com",
            f"Book Created at {now_str}",
            f"name: {book['title']}")
    return jsonify(savedBook)

@app.route("/books/<id>", methods=['GET'])
def read_book_by_id(id):
    id = int(id)
    book_obj = repo.read_book_id(id)
    book = {'id': book_obj.id, 'title': book_obj.title, 'price': book_obj.price, 'copies': book_obj.copies}
    return jsonify(book)

@app.route("/books/<id>", methods=['PUT'])
def update_book(id):
    id = int(id)
    book_data = request.get_json()
    repo.update_book_by_id(repo.Book(id=id, title=book_data['title'], price=book_data['price'], copies=book_data['copies']))
    book_obj = repo.read_book_id(id)
    saved_book = {'id': book_obj.id, 'title': book_obj.title, 'price': book_obj.price, 'copies': book_obj.copies}
    return jsonify(saved_book)

@app.route("/books/<id>", methods=['DELETE'])
def delete_book_by_id(id):
    id = int(id)
    repo.delete_book_by_id(id)
    return jsonify({"message": f"Book with ID {id} has been deleted from the library."}), 200

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

@app.route('/books/scraped/<int:pages>', methods=['POST'])
def scrape_books_endpoint(pages):
    # delete_json_file()
    scrape(pages)  # Ensure this function is defined elsewhere in your code
    json_file_path = "./lms_app/scraped_books.json"
    
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
