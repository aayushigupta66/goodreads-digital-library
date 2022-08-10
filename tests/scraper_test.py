import io
import unittest
import unittest.mock
from src import scraper


class TestDigitalLibrary(unittest.TestCase):

    def test_set_book_min(self):
        scraper.set_parameters(200, 5)
        self.assertEqual(200, scraper.min_books)

    def test_set_author_min(self):
        scraper.set_parameters(200, 5)
        self.assertEqual(5, scraper.min_authors)

    def test_check_none(self):
        obj = None
        self.assertEqual("NA", scraper.check_none(obj))

    def test_check_not_none(self):
        obj = [1, 2, 3]
        self.assertEqual(obj, scraper.check_none(obj))

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def assert_stdout(self, mock_stdout):
        scraper.db_insert([1, 2, 3])
        self.assertEqual(mock_stdout.getvalue(), 'An error occurred object was not stored to db.')


if __name__ == '__main__':
    unittest.main()
