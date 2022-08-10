import flask
from flask import request, jsonify
from flask_cors import CORS
from src.scraper import *
from src.parser import *
from bson.json_util import dumps

# create Flask application object
app = flask.Flask(__name__)
app.config["DEBUG"] = True
CORS(app)


# curl http://127.0.0.1:5000/api/book?id=36116546
@app.route('/api/book', methods=['GET'])
def api_get_book():
    """
    Get book information for given ID.
    :return: appropriate response and status code
    """
    query_parameters = request.args

    # create an empty list for our results
    results = []

    if 'id' in query_parameters:
        book_id = query_parameters['id']
        cur = db_books.find({'book_id': book_id})

        for doc in cur:
            results.append(dumps(doc, indent=2))

        if len(results) == 0:
            # set page not found status response code
            status_code = 404
            response = {"error": "ID not found."}
            return response, status_code

        response = jsonify(results)

        # set OK success status response code
        status_code = 200
        return response, status_code

    else:
        response = {"error": "Invalid parameters."}
        # set Bad Request status response code
        status_code = 400
        return response, status_code


@app.route('/api/author', methods=['GET'])
def api_get_author():
    """
    Get author information for given ID.
    :return: appropriate response and status code
    """
    query_parameters = request.args

    # create an empty list for our results
    results = []

    if 'id' in query_parameters:
        author_id = query_parameters['id']
        cur = db_authors.find({'id': author_id})

        for doc in cur:
            results.append(dumps(doc, indent=2))

        if len(results) == 0:
            response = {"error": "ID not found."}
            # set page not found status response code
            status_code = 404
            return response, status_code

        response = jsonify(results)

        # set OK success status response code
        status_code = 200
        return response, status_code

    else:
        response = {"error": "ID not found."}
        # set Bad Request status response code
        status_code = 400
        return response, status_code


# curl http://127.0.0.1:5000/api/search?q=book.book_id:27
@app.route('/api/search', methods=['GET'])
def api_get_search():
    """
    Get search results based on specified query string.
    :return: appropriate response and status code
    """
    query_parameters = request.args

    # create an empty list for our results
    results = []

    if 'q' in query_parameters:
        query = query_parameters['q']
        updated_query = parse_query(query)

        if updated_query == "Invalid search query.":
            response = {"error": "Invalid search query."}
            # set Bad Request status response code
            status_code = 400
            return response, status_code

        cur = db_books.find(updated_query)

        for doc in cur:
            results.append(dumps(doc, indent=2))

        response = jsonify(results)

        # set OK success status response code
        status_code = 200
        return response, status_code

    else:
        response = {"error": "Invalid parameters."}
        # set Bad Request status response code
        status_code = 400
        return response, status_code


# curl -H 'Content-Type: application/json' -X PUT -d '{"ISBN": "1234567890"}' http://127.0.0.1:5000/api/book?id=2767052
@app.route('/api/book', methods=['PUT'])
def api_put_book():
    """
    Put, or update book specified by the ID.
    :return: appropriate response and status code
    """
    query_parameters = request.args
    json_input = request.json

    # create an empty list for our results
    results = []

    if 'id' in query_parameters:
        book_id = query_parameters['id']
        doc = db_books.find_one_and_update({'book_id': book_id}, {"$set": json_input})

        results.append(dumps(doc, indent=2))
        response = jsonify(results)

        # set OK success status response code
        status_code = 200
        return response, status_code
    else:
        response = {"error": "Invalid parameters."}
        # set Bad Request status response code
        status_code = 400
        return response, status_code


@app.route('/api/author', methods=['PUT'])
def api_put_author():
    """
    Put, or update author specified by the ID.
    :return: appropriate response and status code
    """
    query_parameters = request.args
    json_input = request.json

    # create an empty list for our results
    results = []

    if 'id' in query_parameters:
        author_id = query_parameters['id']
        doc = db_authors.find_one_and_update({'id': author_id}, {"$set": json_input})

        results.append(dumps(doc, indent=2))
        response = jsonify(results)

        # set OK success status response code
        status_code = 200
        return response, status_code
    else:
        response = {"error": "Invalid parameters."}
        # set Bad Request status response code
        status_code = 400
        return response, status_code


# curl -H 'Content-Type: application/json' -X POST -d '{"ISBN": "1234567890"}' http://127.0.0.1:5000/api/book
@app.route('/api/book', methods=['POST'])
def api_post_book():
    """
    Leverage POST requests to ADD A book to the backend (database).
    :return: appropriate response and status code
    """
    json_input = request.json

    try:
        db_books.insert_one(json_input)
        response = {"success": "Successfully posted book."}
        # set OK success status response code
        status_code = 200
        return response, status_code
    except:
        response = {"error": "Unable to add to database."}
        # set Bad Request status response code
        status_code = 400
        return response, status_code


@app.route('/api/books', methods=['POST'])
def api_post_books():
    """
    Leverage POST requests to ADD SEVERAL books to the backend (database).
    :return: appropriate response and status code
    """
    json_input = request.json

    try:
        db_books.insert_many(json_input)
        response = {"success": "Successfully posted books."}
        # set OK success status response code
        status_code = 200
        return response, status_code
    except:
        response = {"error": "Unable to add to database."}
        # set Bad Request status response code
        status_code = 400
        return response, status_code


@app.route('/api/author', methods=['POST'])
def api_post_author():
    """
    Leverage POST requests to ADD AN author to the backend (database).
    :return: appropriate response and status code
    """
    json_input = request.json

    try:
        db_books.insert_one(json_input)
        response = {"success": "Successfully posted author."}
        # set OK success status response code
        status_code = 200
        return response, status_code
    except:
        response = {"error": "Unable to add to database."}
        # set Bad Request status response code
        status_code = 400
        return response, status_code


@app.route('/api/authors', methods=['POST'])
def api_post_authors():
    """
    Leverage POST requests to ADD SEVERAL authors to the backend (database).
    :return: appropriate response and status code
    """
    json_input = request.json

    try:
        db_books.insert_many(json_input)
        response = {"success": "Successfully posted authors."}
        # set OK success status response code
        status_code = 200
        return response, status_code
    except:
        response = {"error": "Unable to add to database."}
        # set Bad Request status response code
        status_code = 400
        return response, status_code


@app.route('/api/scrape', methods=['POST'])
def api_post_scrape():
    """
    Scrape either authors or books and save the results in the database.
    :return: appropriate response and status code
    """
    post_input = request.data

    set_parameters(1, 1)
    Book("https://www.goodreads.com/book/show/" + post_input.decode("utf-8"))

    response = {"success": "Successfully scraped."}
    # set OK success status response code
    status_code = 200
    return response, status_code


# curl -X DELETE http://127.0.0.1:5000/api/book?id=18144031
@app.route('/api/book', methods=['DELETE'])
def api_delete_book():
    """
    Delete book specified by the ID.
    :return: appropriate response and status code
    """
    query_parameters = request.args

    if 'id' in query_parameters:
        book_id = query_parameters['id']
        doc = db_books.delete_one({'book_id': book_id})

        response = {"success": "Successfully deleted book."}
        # set OK success status response code
        status_code = 200
        return response, status_code
    else:
        response = {"error": "Invalid parameters."}
        # set Bad Request status response code
        status_code = 400
        return response, status_code


@app.route('/api/author', methods=['DELETE'])
def api_delete_author():
    """
    Delete author specified by the ID.
    :return: appropriate response and status code
    """
    query_parameters = request.args

    if 'id' in query_parameters:
        author_id = query_parameters['id']
        doc = db_authors.delete_one({'id': author_id})

        response = {"success": "Successfully deleted author."}
        # set OK success status response code
        status_code = 200
        return response, status_code
    else:
        response = {"error": "Invalid parameters."}
        # set Bad Request status response code
        status_code = 400
        return response, status_code


@app.route('/vis/top-books', methods=['GET'])
def api_top_books():
    """
    Gets the ranking of top k highest rated books.
    :return: appropriate response and status code
    """
    query_parameters = request.args

    # create an empty list for our results
    results = []

    if 'k' in query_parameters:
        k = int(query_parameters['k'])
        cur = db_books.find().sort('rating', -1)

        counter = 0
        for doc in cur:
            if counter == k:
                break
            results.append(dumps(doc, indent=2))
            counter += 1

        response = jsonify(results)

        # set OK success status response code
        status_code = 200
        return response, status_code
    else:
        response = {"error": "Invalid parameters."}
        # set Bad Request status response code
        status_code = 400
        return response, status_code


@app.route('/vis/top-authors', methods=['GET'])
def api_top_authors():
    """
    Gets the ranking of top k highest rated authors.
    :return: appropriate response and status code
    """
    query_parameters = request.args

    # create an empty list for our results
    results = []

    if 'k' in query_parameters:
        k = int(query_parameters['k'])
        cur = db_authors.find().sort('rating', -1)

        counter = 0
        for doc in cur:
            if counter == k:
                break
            results.append(dumps(doc, indent=2))
            counter += 1

        response = jsonify(results)

        # set OK success status response code
        status_code = 200
        return response, status_code
    else:
        response = {"error": "Invalid parameters."}
        # set Bad Request status response code
        status_code = 400
        return response, status_code


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
