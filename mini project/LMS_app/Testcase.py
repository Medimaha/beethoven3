import unittest
from unittest.mock import patch, MagicMock
from dataclasses import dataclass

import repository

@dataclass
class Book:
    id: int
    title: str
    price: float
    copies: int

class TestLibraryManager(unittest.TestCase):
    @patch('repository.sqlite3.connect')
    def test_connect_success(self, mock_sqlite_connect):
        mock_conn = MagicMock()
        mock_sqlite_connect.return_value = mock_conn

        result = repository.connector()

        # Assert
        mock_sqlite_connect.assert_called_once_with('app_db.db')
        self.assertEqual(result, mock_conn)


    @patch('repository.connect')
    def test_update_book_success(self, mock_connect):
        book = Book(id=1, title="Updated Book", price=29.99, copies=5)
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.rowcount = 1

        result = repository.updateBook(book)

        mock_cursor.execute.assert_called_once_with(
            "UPDATE library SET title = ?, price = ?, copies = ? WHERE id = ?",
            ("Updated Book", 29.99, 5, 1)
        )
        mock_conn.commit.assert_called_once()
        self.assertEqual(result, 1)

if __name__ == '__main__':
    unittest.main()