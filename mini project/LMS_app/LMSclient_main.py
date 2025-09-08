import repository
from mail_sender import send_gmail
from LMS_model import Book
import json
import os
from scraper import scrape
from BookCal import BookCal

def menu_providers():
    message = '''
The menu choices are
1 - Create Book
2 - Read All Books 
3 - Read By Id 
4 - Update 
5 - Delete 
6 - Exit / Logout
Your choice:'''
    choice = int(input(message))
    if choice == 1:
        title = input('Title: ')
        copies = input('Copies: ')
        price = input('Price: ')
        bookDict = Book(title=title, copies=copies, price=price)
        book = repository.create_new_book(bookDict)
        # mail sending after employee created
        from datetime import datetime
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        result = send_gmail("rsudha1610@gmail.com",
                f"Book Created at {now_str}",
                f"name: {bookDict.title}")
        print(f'Book created successfully.\n {repository.read_book_id(book)}')
    elif choice == 2:
        Books = repository.read_all()
        print('Books: ')
        for book in Books:
            print(book)
    elif choice == 3:
        id = int(input('Book id: '))
        book = repository.read_book_id(id)
        if book == None:
            print('book not found')
        else:
            print(book)
    elif choice == 4:
        id = int(input('Book id: '))
        old_book = repository.read_book_id(id)
        if old_book == None:
            print('book Not Found.')
        else:
            print(old_book)
            # copies = input('Copies: ')
            user_input = input(f"Want to update the Title({old_book.title}): (T|F) ").strip().lower()
            if user_input != "f":
                new_title = input("Title: ")
            else:
                new_title = old_book.title
            user_input = input(f"Want to update the Price({old_book.price}): (T|F) ").strip().lower()
            if user_input != "f":
                new_price = input("Price: ")
            else:
                new_price = old_book.price
            user_input = input(f"Want to update the Copies({old_book.copies}): (T|F) ").strip().lower()
            if user_input != "f":
                new_copies = input("Copies: ")
            else:
                new_copies = old_book.copies
            new_product_dict = Book(id=id,title=new_title, copies=new_copies, price=new_price)
            savedbook = repository.update_book_by_id(new_product_dict)
            print(f'Book Updated successfully.\n {repository.read_book_id(savedbook)}')
    elif choice == 5:
        id = int(input('Book id: '))
        old_book = repository.read_book_id(id)
        if old_book == None:
            print('book Not Found.')
        else:
            print(old_book)
            if input('Are you sure to delete(y/n)?') == 'y':
                repository.delete_book_by_id(id)
                print(f'Book with id : {id}.\nDeleted Successfully')
    # elif choice == 6:
    #     calculator = BookCal()
    #     total_value = calculator.calculate_total_stock_value()
    #     print("Total stock value : ", total_value)
    return choice

def menu_provider():
    print('>>>>>>Welcome to Book Management App<<<<<<<<<<<<<<<<<<<<')
    choice = menu_providers()
    while choice != 6:
        choice = menu_providers()
    print('Thank you for using app')