from src.ui import *
from src.parser import *
from json_vars import *
import unittest.mock
from unittest.mock import patch


class TestDigitalLibrary(unittest.TestCase):

    # TEST GET API CALL

    book_id = '13335037'
    invalid_book_id = '1234'
    author_id = '15872'
    invalid_author_id = '1234'
    search_query = 'book.book_id:13335037'
    search_query_invalid = 'object.field:content'

    @patch('builtins.input', return_value=book_id)
    def test_get_book_valid(self, mock_input):
        result = run_get_book()
        self.assertEqual(result, get_book_json)

    @patch('builtins.input', return_value=author_id)
    def test_get_author_valid(self, mock_input):
        result = run_get_author()
        self.assertEqual(result, get_author_json)

    @patch('builtins.input', return_value=invalid_book_id)
    def test_get_book_invalid(self, mock_input):
        result = run_get_book()
        self.assertEqual(result, "ID not found.")

    @patch('builtins.input', return_value=invalid_author_id)
    def test_get_author_invalid(self, mock_input):
        result = run_get_author()
        self.assertEqual(result, "ID not found.")

    @patch('builtins.input', return_value=search_query)
    def test_perform_search(self, mock_input):
        result = run_search()
        self.assertEqual(result, get_book_json)

    @patch('builtins.input', return_value=search_query_invalid)
    def test_perform_search_invalid(self, mock_input):
        result = run_search()
        self.assertEqual(result, "Invalid search query.")

    # TEST PUT API CALL

    put_isbn = '{"ISBN": "1234567890"}'
    put_rating = '{"rating": "5.0"}'

    @patch('builtins.input', side_effect=[book_id, put_isbn])
    def test_put_book(self, mock_input):
        result = run_put_book()
        self.assertEqual(result, put_book_json)

    @patch('builtins.input', side_effect=[invalid_book_id, put_isbn])
    def test_put_book_invalid(self, mock_input):
        result = run_put_book()
        self.assertEqual(result, "No such ID is found.")

    @patch('builtins.input', side_effect=[author_id, put_rating])
    def test_put_author(self, mock_input):
        result = run_put_author()
        self.assertEqual(result, put_author_json)

    @patch('builtins.input', side_effect=[invalid_author_id, put_isbn])
    def test_put_author_invalid(self, mock_input):
        result = run_put_author()
        self.assertEqual(result, "No such ID is found.")

    # TEST POST API CALL

    @patch('builtins.input', return_value=post_book_json)
    def test_post_book(self, mock_input):
        result = run_post_book()
        self.assertEqual(result, "Successfully added to database.")

    @patch('builtins.input', return_value=post_books_json)
    def test_post_books(self, mock_input):
        result = run_post_books()
        self.assertEqual(result, "Successfully added to database.")

    @patch('builtins.input', return_value=post_author_json)
    def test_post_author(self, mock_input):
        result = run_post_author()
        self.assertEqual(result, "Successfully added to database.")

    @patch('builtins.input', return_value=post_authors_json)
    def test_post_authors(self, mock_input):
        result = run_post_authors()
        self.assertEqual(result, "Successfully added to database.")


    # TEST DELETE API CALL

    @patch('builtins.input', return_value=invalid_book_id)
    def test_delete_book(self, mock_input):
        result = run_delete_book()
        self.assertEqual(result, "Successfully deleted book.")

    @patch('builtins.input', return_value=invalid_author_id)
    def test_delete_author(self, mock_input):
        result = run_delete_author()
        self.assertEqual(result, "Successfully deleted author.")

    # TEST PARSER

    def test_parse_invalid_query(self):
        result = parse_query('object.field:content')
        self.assertEqual(result, "Invalid search query.")

    def test_parse_valid_query(self):
        result = parse_query('book.book_id:13335037')
        self.assertEqual(result, {'book_id': {'$regex': '.*13335037.*'}})

    def test_parse_logical_operator(self):
        result = parse_logical_operator('13335037', 'book_id')
        self.assertEqual(result, {'book_id': {'$regex': '.*13335037.*'}})

    def test_parse_other_operator(self):
        result = parse_other_operators('NOT 123')
        self.assertEqual(result, {'$not': {'$regex': '.*123.*'}})


if __name__ == '__main__':
    unittest.main()
