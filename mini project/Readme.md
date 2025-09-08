# Library Management System(LMS)
### **Problem Statement**: 
     Design a multi-module API application for Book {id, title, price, copies} with CRUD operations in SQLite. The client app should send an email immediately when a new book is added. Implement multi-threaded/processed/coroutines total stock value calculation in batches of 10 books, and include a web scraping module to fetch book prices from online bookstores. Ensure logging, exception handling, and PEP 8 compliance.


```
    GET - http://localhost:5000/books             // to get all the books
    GET - http://localhost:5000/books/<id>        // to get a particular id based on id
    POST - http://localhost:5000/books            // to add a new book (title, price, copies)
    PUT - http://localhost:5000/books/<id>        // to update the existed book
    DELETE - http://localhost:5000/books/<id>     // to delete the book by using its id
    GET - http://localhost:5000/books/stock-value // to get the stock value
    GET - http://localhost:5000/books/scraped/1   // scrape the books how many pages need to 

```