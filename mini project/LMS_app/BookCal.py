import threading
from queue import Queue
import repository
import logging

class BookCal:
    def __init__(self):
        self.queue = Queue()
        self.total_value = 0
        self.lock = threading.Lock()

    def calculate_batch(self):
        while not self.queue.empty():
            books = self.queue.get()
            batch_value = sum(book.price * book.copies for book in books)
            with self.lock:
                self.total_value += batch_value
            self.queue.task_done()

    def calculate_total_stock_value(self):
        try:
            books = repository.readAllBooks()
            batch_size = 10
            threads = []

            # Split books into batches
            for i in range(0, len(books), batch_size):
                self.queue.put(books[i:i + batch_size])

            # Start threads
            for _ in range(min(4, self.queue.qsize())):
                t = threading.Thread(target=self.calculate_batch)
                t.start()
                threads.append(t)

            # Wait for all threads to complete
            for t in threads:
                t.join()

            logging.info(f"Total stock value calculated: {self.total_value}")
            return self.total_value
        except Exception as e:
            logging.error(f"Error calculating stock value: {str(e)}")
            raise