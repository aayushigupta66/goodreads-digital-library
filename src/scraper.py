from bs4 import BeautifulSoup
from urllib.request import urlopen
import pymongo
import os
from dotenv import load_dotenv

# global variables keeping track of the book / author urls and counts
book_count = 0
author_count = 0
books = set()
authors = set()

# global variables for the minimum number of books and authors the program needs to scrape
min_books = 0
min_authors = 0

# loading environment variables -- password
load_dotenv()
PASSWORD = os.getenv("PASSWORD")

# connecting to PyMongo and MongoDB
client = pymongo.MongoClient("mongodb+srv://aayushi3:" + PASSWORD +
                             "@cluster0.zzei0.mongodb.net/goodReads?retryWrites=true&w=majority")
db_books = client.goodReads.books
db_authors = client.goodReads.authors


def db_insert_book(obj):
    """
    Insert the book object into the database.
    :param obj: author or book object
    """
    my_dict = vars(obj)
    try:
        db_books.insert_one(my_dict)
    except:
        print('An error occurred object was not stored to db.')


def db_insert_author(obj):
    """
    Insert the author object into the database.
    :param obj: author or book object
    """
    my_dict = vars(obj)
    try:
        db_authors.insert_one(my_dict)
    except:
        print('An error occurred object was not stored to db.')


def check_status():
    """
    Check the number of books and authors added to the database and
    end the program if both requirements are fulfilled.
    """
    try:
        # assertion to make sure the loop isn't endless
        assert book_count <= min_books or author_count <= min_authors
    except:
        # exit signal
        print("Scraping complete.")
        exit(1)


def check_none(obj):
    """
    Check if the item passed through is of type None and return an object that is writable accordingly.
    :param obj: object to be checked
    :return: string "NA" if the param is None and obj otherwise
    """
    if obj is None:
        return "NA"
    else:
        return obj


def set_parameters(book_num, author_num):
    """
    Setter for the minimum number of books and authors to be scraped.
    :param book_num: minimum number of books scraped
    :param author_num: minimum number of authors scraped
    """
    global min_books
    global min_authors

    min_books = book_num
    min_authors = author_num


class Book:
    def __init__(self, book_url):
        """
        Constructor for creating the Book object.
        :param book_url: starting book url
        """
        # update book count and check if program requirements are fulfilled
        global book_count
        book_count += 1
        print("book " + str(book_count))
        check_status()

        # start scraping with book url and beautiful soup functions
        self.book_url = book_url
        print(book_url)
        books.add(book_url)
        html_doc = urlopen(self.book_url)
        soup = BeautifulSoup(html_doc, 'html.parser')

        # set variables for the object with the class's functions
        self.title = self.get_title(soup)
        self.book_id = self.get_book_id()
        self.ISBN = self.get_isbn(soup)
        self.author_url = self.get_author_url(soup)
        self.author = self.get_author(soup)
        self.rating = self.get_rating(soup)
        self.rating_count = self.get_rating_count(soup)
        self.review_count = self.get_review_count(soup)
        self.image_url = self.get_image_url(soup)
        self.similar_books = self.get_similar_books(soup)

        # once the variables are set, insert the object to the database
        db_insert_book(self)

        # scrape to the next author and book objects
        self.scrape_author()
        self.scrape_similar_books()

    def get_title(self, soup):
        """
        Get the title of the book with the bookTitle id.
        :param soup: beautiful soup var to help with scraping
        :return: title of the book
        """
        return check_none(soup.find("h1", id="bookTitle").string.strip())

    def get_book_id(self):
        """
        Get the id of the book from the book url.
        :return: book's id from Goodreads
        """
        prefix = "https://www.goodreads.com/book/show/"
        id_builder = self.book_url[len(prefix):]
        return id_builder.split("-")[0]

    def get_isbn(self, soup):
        """
        Get the ISBN of the book from the meta tag.
        :param soup: beautiful soup var to help with scraping
        :return: book's ISBN
        """
        return check_none(soup.find("meta", property="books:isbn")["content"])

    def get_author_url(self, soup):
        """
        Get the author's url on the Goodread website from the meta tag.
        :param soup: beautiful soup var to help with scraping
        :return: author's url
        """
        return check_none(soup.find("meta", property="books:author")["content"])

    def get_author(self, soup):
        """
        Get the author's full name from the bookAuthorProfile__name class.
        :param soup: beautiful soup var to help with scraping
        :return: author's full name
        """
        div_tag = soup.find("div", class_="bookAuthorProfile__name")
        if div_tag is not None:
            a_tag = div_tag.find("a").string
            return check_none(a_tag.strip())
        else:
            return "NA"

    def get_rating(self, soup):
        """
        Get the rating of the book from the Goodread's website from the itemprop value.
        :param soup: beautiful soup var to help with scraping
        :return: rating of the book
        """
        return check_none(soup.find(itemprop="ratingValue").string.strip())

    def get_rating_count(self, soup):
        """
        Get the rating count of the book from the Goodread's website from the itemprop value.
        :param soup: beautiful soup var to help with scraping
        :return: rating count of the book
        """
        return check_none(soup.find(itemprop="ratingCount")["content"])

    def get_review_count(self, soup):
        """
        Get the review count of the book from the Goodread's website from the itemprop value.
        :param soup: beautiful soup var to help with scraping
        :return: review count of the book
        """
        return check_none(soup.find(itemprop="reviewCount")["content"])

    def get_image_url(self, soup):
        """
        Get the book cover's image url from the id="coverImage" param.
        :param soup: beautiful soup var to help with scraping
        :return: book cover image url
        """
        if soup.find(id="coverImage") is None:
            return "NA"
        else:
            return check_none(soup.find(id="coverImage")["src"])

    def get_similar_books(self, soup):
        """
        Get similar book urls from the "See similar books..." link on the Goodreads website.
        :param soup: beautiful soup var to help with scraping
        :return: similar book urls
        """
        # get links leading to similar books list
        similar_links = soup.find_all("a", class_="actionLink right seeMoreLink")
        if similar_links is None:
            return []
        similar_url = ""

        # pick out similar url
        for link in similar_links:
            if link["href"].startswith("https://www.goodreads.com/book/similar/"):
                similar_url = link["href"]
                break
        if similar_url == "":
            return []

        # use similar html to add links to book_list
        similar_html = urlopen(similar_url)
        similar_soup = BeautifulSoup(similar_html, 'html.parser')
        book_list = []
        for tag in similar_soup.find_all("a", class_="gr-h3 gr-h3--serif gr-h3--noMargin"):
            book_list.append("https://www.goodreads.com" + tag["href"])
        if len(book_list) > 0:
            book_list.pop(0)
        return book_list

    def scrape_author(self):
        """
        Creates an author object with the given author url to further scrape the website.
        """
        if self.author_url not in authors:
            Author(self.author_url)

    def scrape_similar_books(self):
        """
        Creates multiple book objects with the given similar_books urls to further scrape the website.
        """
        for url in self.similar_books:
            if url not in books:
                Book(url)


class Author:
    def __init__(self, author_url):
        """
        Constructor for creating the Author object.
        :param author_url: starting author url
        """
        # update author count and check if program requirements are fulfilled
        global author_count
        author_count += 1
        print("author " + str(author_count))
        check_status()

        # start scraping with author url and beautiful soup functions
        self.author_url = author_url
        print(author_url)
        authors.add(author_url)
        html_doc = urlopen(self.author_url)
        soup = BeautifulSoup(html_doc, 'html.parser')

        # set variables for the object with the class's functions
        self.name = self.get_name(soup)
        self.id = self.get_id()
        self.rating = self.get_rating(soup)
        self.rating_count = self.get_rating_count(soup)
        self.review_count = self.get_review_count(soup)
        self.image_url = self.get_image_url(soup)
        self.related_authors = self.get_related_authors()
        self.author_books = self.get_author_books(soup)

        # once the variables are set, insert the object to the database
        db_insert_author(self)

        # scrape to the next author and book objects
        self.scrape_author_books()
        self.scrape_related_authors()

    def get_name(self, soup):
        """
        Get the author's name using the itemprop="name" property.
        :param soup: beautiful soup var to help with scraping
        :return: author's name
        """
        return check_none(soup.find(itemprop="name").string)

    def get_id(self):
        """
        Get id of the author form the author url.
        :return: author's id from Goodreads
        """
        prefix = "https://www.goodreads.com/author/show/"
        id_builder = self.author_url[len(prefix):]
        return id_builder.split(".")[0]

    def get_rating(self, soup):
        """
        Get the rating of the author from the Goodread's website from the itemprop value.
        :param soup: beautiful soup var to help with scraping
        :return: rating of the author
        """
        return check_none(soup.find(itemprop="ratingValue").string)

    def get_rating_count(self, soup):
        """
        Get the rating count of the author from the Goodread's website from the itemprop value.
        :param soup: beautiful soup var to help with scraping
        :return: rating count of the author
        """
        return check_none(soup.find(itemprop="ratingCount")["content"])

    def get_review_count(self, soup):
        """
        Get the review count of the author from the Goodread's website from the itemprop value.
        :param soup: beautiful soup var to help with scraping
        :return: review count of the author
        """
        return check_none(soup.find(itemprop="reviewCount")["content"])

    def get_image_url(self, soup):
        """
        Get the author's profile image url from the meta data for itemprop="image".
        :param soup: beautiful soup var to help with scraping
        :return: author profile image url
        """
        return check_none(soup.find("meta", itemprop="image")["content"])

    def get_related_authors(self):
        """
        Get related author urls from the "Similar authors" link on the Goodreads website.
        :return: related author urls
        """
        # create the similar url and create another soup
        similar_url = self.author_url.replace("show", "similar")
        similar_html = urlopen(similar_url)
        soup = BeautifulSoup(similar_html, 'html.parser')

        # add to author list from the responsiveAuthor__media class
        author_list = []
        for tag in soup.find_all("div", class_="responsiveAuthor__media"):
            author_list.append(tag.find("a")["href"])
        if len(author_list) > 0:
            author_list.pop(0)
        return author_list

    def get_author_books(self, soup):
        """
        Get the author's book urls provided on the Goodreads website.
        :param soup: beautiful soup var to help with scraping
        :return: book urls
        """
        book_list = []
        for tag in soup.find_all("a", class_="bookTitle"):
            if tag["href"].startswith("/book/show/"):
                book_url = "https://www.goodreads.com" + tag["href"]
                book_list.append(book_url)
        return book_list

    def scrape_related_authors(self):
        """
        Creates author objects with the given related author urls to further scrape the website.
        """
        for url in self.related_authors:
            if url not in authors:
                Author(url)

    def scrape_author_books(self):
        """
        Creates book objects with the given author book urls to further scrape the website.
        """
        for url in self.author_books:
            if url not in books:
                Book(url)
