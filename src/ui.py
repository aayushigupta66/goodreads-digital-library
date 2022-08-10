from bson import ObjectId
from src.scraper import *
from src.parser import *
from bson.json_util import dumps, loads

starting_url = ""

db = client.goodReads.data


def start_command_line():
    """
    Function to start the command line interface with a choice of functions to pick.
    """
    # initial prompt
    print("Enter one of the following keywords to configure the Digital Library:")
    print("Scrape Goodreads")
    print("Update Library")
    print("Export Collection")
    print("API Calls")
    command = input('Keyword: ')

    # redirect to appropriate function and rerun prompt otherwise
    if command == "Scrape Goodreads":
        run_scrape()
    elif command == "Update Library":
        run_update()
    elif command == "Export Collection":
        run_export()
    elif command == "API Calls":
        run_api_calls()
    else:
        print("Invalid keyword. Please select from the given choices.")
        start_command_line()


def run_scrape():
    """
    Method to scrape the Goodreads website using the Book and Author objects from the scraper.py file.
    """
    global starting_url

    # run prompts
    url_prompt()
    scrape_num_prompt()

    # create initial book to start the scraper
    Book(starting_url)


def url_prompt():
    """
    Create the user prompt for the starting url and check if the URL is valid.
    """
    global starting_url

    # starting url input for scraper to run
    starting_url = input('Enter starting URL: ')

    # check if the starting url directs to the Goodreads website
    # and print error if url is invalid and restart prompt
    if not starting_url.startswith("https://www.goodreads.com/book/show/"):
        print("URL is not valid. Please try again.")
        url_prompt()


def scrape_num_prompt():
    """
        Create the user prompt for the minimum number of books and authors to scrape and
        check if the input values are valid.
    """
    # input minimum number of books and authors to scrape
    min_book = int(input('Enter minimum number of books to scrape: '))
    min_author = int(input('Enter minimum number of authors to scrape: '))

    # print error if values are invalid and restart prompt
    if min_book > 200 or min_author > 50:
        print("Parameters not valid. Must be less than 200 books and 50 authors. Please try again.")
        scrape_num_prompt()

    # set the parameters in the scraper file
    set_parameters(min_book, min_author)


def run_update():
    """
    Method to read from JSON files to create new books / authors or update existing books / authors.
    """
    # input file path
    file_name = input("Enter file name: ")

    # insert data
    try:
        with open(file_name) as f:
            data = loads(f.read())
    except:
        print("Invalid JSON file. Please try again.")
        exit(1)

    for doc in data:
        doc_id = doc['_id']
        if db.count_documents({'_id': ObjectId(doc_id)}) != 0:
            # id exists, update the library
            try:
                db.replace_one(doc, doc)
            except:
                print("Could not update library. Please try again.")
                exit(1)
        else:
            # id does not exist insert to library
            try:
                db.insert_one(doc)
            except:
                print("Could not insert object. Please try again.")
                exit(1)


def run_export():
    """
    Method to export existing books / authors into JSON files.
    """
    # retrieve data
    cursor = db.find()
    list_cur = list(cursor)
    json_data = dumps(list_cur, indent=2)

    # write to data.json file
    with open('../data.json', 'w') as file:
        file.write(json_data)


def run_api_calls():
    """
    Function to start the API Call interface with a choice of functions to pick.
    """
    # select call prompt
    print("Enter one of the following keywords to specify the API endpoint or enter 'BACK' to return to the main menu:")
    print("GET")
    print("PUT")
    print("POST")
    print("DELETE")
    keyword = input('Keyword: ')

    # redirect to appropriate function and rerun prompt otherwise
    if keyword == "GET":
        run_get()
    elif keyword == "PUT":
        run_put()
    elif keyword == "POST":
        run_post()
    elif keyword == "DELETE":
        run_delete()
    elif keyword == "BACK":
        start_command_line()
    else:
        print("Invalid keyword. Please select from the given choices.")
        run_api_calls()


def run_get():
    """
    Function to start the GET endpoint interface with a choice of functions to pick:
    get book / author information or perform a search.
    """
    # select get prompt
    print("Enter one of the following keywords to specify if you want to get book / author information or perform a "
          "search or enter 'BACK' to return to the previous menu:")
    print("Get Book")
    print("Get Author")
    print("Perform Search")
    print("BACK")
    keyword = input('Keyword: ')

    if keyword == "Get Book":
        print(run_get_book())
        run_get()
    elif keyword == "Get Author":
        print(run_get_author())
        run_get()
    elif keyword == "Perform Search":
        print(run_search())
        run_get()
    elif keyword == "BACK":
        run_api_calls()
    else:
        print("Invalid keyword. Please select from the given choices.")
        run_get()


def run_get_book():
    """
    Method to get book information based on given ID.
    :return: book information in json format
    """
    book_id = input("Enter Book ID: ")
    cur = db_books.find({'book_id': book_id})

    # create an empty list for our results
    results = []
    for doc in cur:
        results.append(dumps(doc, indent=2))

    if len(results) == 0:
        return "ID not found."
    else:
        return results


def run_get_author():
    """
    Method to get author information based on given ID.
    :return: author information in json format
    """
    author_id = input("Enter Author ID: ")
    cur = db_authors.find({'id': author_id})

    # create an empty list for our results
    results = []
    for doc in cur:
        results.append(dumps(doc, indent=2))

    if len(results) == 0:
        return "ID not found."
    else:
        return results


def run_search():
    """
    Method to get search results based on specified query string.
    :return: search results in json format
    """
    query = input("Enter search query: ")
    updated_query = parse_query(query)

    if updated_query == "Invalid search query.":
        return "Invalid search query."
    else:
        cur = db_books.find(updated_query)

        # create an empty list for our results
        results = []
        for doc in cur:
            results.append(dumps(doc, indent=2))

        return results


def run_put():
    """
    Function to start the PUT endpoint interface with a choice of functions to pick:
    update book / author information.
    """
    # select put prompt
    print("Enter one of the following keywords to specify if you want to update book / author information "
          "or enter 'BACK' to return to the previous menu:")
    print("Put Book")
    print("Put Author")
    print("BACK")
    keyword = input('Keyword: ')

    if keyword == "Put Book":
        print(run_put_book())
        run_put()
    elif keyword == "Put Author":
        print(run_put_author())
        run_put()
    elif keyword == "BACK":
        run_api_calls()
    else:
        print("Invalid keyword. Please select from the given choices.")
        run_put()


def run_put_book():
    """
    Method to put, or update book specified by the ID.
    :return: book information in json format
    """
    book_id = input("Enter Book ID: ")
    str_input = input("Enter json input: ")
    json_input = loads(str_input)

    # create an empty list for our results
    results = []
    doc = db_books.find_one_and_update({'book_id': book_id}, {"$set": json_input})

    if doc is None:
        return "No such ID is found."

    results.append(dumps(doc, indent=2))
    return results


def run_put_author():
    """
    Method to put, or update author specified by the ID.
    :return: author information in json format
    """
    author_id = input("Enter Author ID: ")
    str_input = input("Enter json input: ")
    json_input = loads(str_input)

    # create an empty list for our results
    results = []
    doc = db_authors.find_one_and_update({'id': author_id}, {"$set": json_input})

    if doc is None:
        return "No such ID is found."

    results.append(dumps(doc, indent=2))
    return results


def run_post():
    """
    Function to start the POST endpoint interface with a choice of functions to pick:
    create or scrape new books / authors.
    """
    # select post prompt
    print("Enter one of the following keywords to specify if you want to create or scrape new books / authors "
          "or enter 'BACK' to return to the previous menu:")
    print("Post Book")
    print("Post Author")
    print("Post Books")
    print("Post Authors")
    print("New Scrape")
    print("BACK")
    keyword = input('Keyword: ')

    if keyword == "Post Book":
        print(run_post_book())
        run_post()
    elif keyword == "Post Books":
        print(run_post_books())
        run_post()
    elif keyword == "Post Author":
        print(run_post_author())
        run_post()
    elif keyword == "Post Authors":
        print(run_post_authors())
        run_post()
    elif keyword == "New Scrape":
        print(run_scrape())
        run_post()
    elif keyword == "BACK":
        run_api_calls()
    else:
        print("Invalid keyword. Please select from the given choices.")
        run_post()


def run_post_book():
    """
    Method that leverages POST requests to ADD A book to the backend (database).
    :return: reports if post is successful or not
    """
    str_input = input("Enter json input: ")
    json_input = loads(str_input)

    try:
        db_books.insert_one(json_input)
        return "Successfully added to database."
    except:
        return "Unable to add to database."


def run_post_author():
    """
    Method that leverages POST requests to ADD AN author to the backend (database).
    :return: reports if post is successful or not
    """
    str_input = input("Enter json input: ")
    json_input = loads(str_input)

    try:
        db_authors.insert_one(json_input)
        return "Successfully added to database."
    except:
        return "Unable to add to database."


def run_post_books():
    """
    Method that leverages POST requests to ADD SEVERAL books to the backend (database).
    :return: reports if post is successful or not
    """
    str_input = input("Enter json input: ")
    json_input = loads(str_input)

    try:
        db_books.insert_many(json_input)
        return "Successfully added to database."
    except:
        return "Unable to add to database."


def run_post_authors():
    """
    Method that leverages POST requests to ADD SEVERAL authors to the backend (database).
    :return: reports if post is successful or not
    """
    str_input = input("Enter json input: ")
    json_input = loads(str_input)

    try:
        db_authors.insert_many(json_input)
        return "Successfully added to database."
    except:
        return "Unable to add to database."


def run_delete():
    """
    Function to start the DELETE endpoint interface with a choice of functions to pick:
    delete book / author.
    """
    # select post prompt
    print("Enter one of the following keywords to specify if you want to delete book / author "
          "or enter 'BACK' to return to the previous menu:")
    print("Delete Book")
    print("Delete Author")
    print("BACK")
    keyword = input('Keyword: ')

    if keyword == "Delete Book":
        print(run_delete_book())
        run_delete()
    elif keyword == "Delete Author":
        print(run_delete_author())
        run_delete()
    elif keyword == "BACK":
        run_api_calls()
    else:
        print("Invalid keyword. Please select from the given choices.")
        run_delete()


def run_delete_book():
    """
    Method to delete book specified by the ID.
    :return: reports if delete is successful or not
    """
    book_id = input("Enter Book ID: ")

    try:
        db_books.delete_one({'book_id': book_id})
        return "Successfully deleted book."
    except:
        return "Invalid parameters."


def run_delete_author():
    """
    Method to delete author specified by the ID.
    :return: reports if delete is successful or not
    """
    author_id = input("Enter Author ID: ")

    try:
        db_authors.delete_one({'id': author_id})
        return "Successfully deleted author."
    except:
        return "Invalid parameters."


if __name__ == '__main__':
    # run ui
    start_command_line()
