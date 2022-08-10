# Goodreads Digital Library

Building a Digital Library.

## Design

Split the code into two files that handles the web scraping and command line interface.

1. `scraper` - Contains the `Book` and `Author` class that gathers information of different Authors and Books from 
   Goodreads. The file also runs the scraper with BeautifulSoup4 given a starting URL and stores the results in a 
   PyMongo database.
   
2. `ui` - Contains the command line interface of the program, allowing users to pick the starting URL, select an 
   arbitrary number of books and authors to scrape, and other read and write functionalities.
   
## Database

Used mongoDB and PyMongo to store the data from web scraping the Goodreads website. The program stores 
the data into the database while scraping.

## Testing

Conducted testing by configuring the IntelliJ IDEA for unit testing with jUnit. Tested every public method by using
`assert()` functions.

