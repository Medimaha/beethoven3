import requests
from bs4 import BeautifulSoup
import json
import os

# Base URL of the website
base_url = 'https://books.toscrape.com/catalogue/page-{}.html'

# List to store book details
books = []

# Function to extract data from a single page
def extract_data_from_page(soup, page):
    for book in soup.find_all('article', class_='product_pod'):
        title = book.h3.a['title']
        price = book.find('p', class_='price_color').text
        availability = book.find('p', class_='instock availability').text.strip()
        
        book_data = {
            'page': page,
            'Title': title,
            'Price': price,
            'Availability': availability,
            'copies': 18
        }
        
        books.append(book_data)

# Function to scrape a specified number of pages
def scrape_books(num_pages=10):
    for page in range(1, num_pages + 1):  # Scraping the specified number of pages
        url = base_url.format(page)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        extract_data_from_page(soup, page)
        print(f"Extracted data from page {page}")
    return books  # Return the list of books

def scrape(pages):
    global books
    books = []
    print(books)
    delete_json_file()
    books = scrape_books(pages)  # Get the list of books
    print(len(books))
    # Save the data to a JSON file
    with open("./lms_app/scraped_books.json", 'w', encoding='utf-8') as json_file:
        json.dump(books, json_file, ensure_ascii=False, indent=4)

    print("Data saved to scraped_books.json")

# Example usage
if __name__ == "__main__":
    pages = 4  # Specify the number of pages to scrape
    scrape(pages)

def delete_json_file():
    file_path = "./lms_app/scraped_books.json"
    """Delete the specified JSON file."""
    try:
        os.remove(file_path)
        print(f"{file_path} has been deleted.")
    except FileNotFoundError:
        print(f"The file {file_path} does not exist.")
    except PermissionError:
        print(f"Permission denied: unable to delete {file_path}.")
    except Exception as e:
        print(f"An error occurred: {e}")
