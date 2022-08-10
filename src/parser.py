def parse_query(query):
    """
    Main function to parse the query passed through the API call.
    :param query: original query
    :return: parsed query
    """
    query_vars = query.split(".")

    query_object = query_vars[0]
    query_field = query_vars[1].split(":")[0]
    query_content = query_vars[1].split(":")[1]

    if query_object == "book":
        book_vars = {"book_url", "title", "book_id", "ISBN", "author_url", "author", "rating", "rating_count",
                     "review_count", "image_url", "similar_books"}

        # error is reported if object or the field does not exist
        if query_field in book_vars:
            return parse_logical_operator(query_content, query_field)
        else:
            return "Invalid search query."

    elif query_object == "author":
        author_vars = {"author_url", "name", "id", "rating", "rating_count", "review_count", "image_url",
                       "related_authors", "author_books"}

        # error is reported if object or the field does not exist
        if query_field in author_vars:
            return parse_logical_operator(query_content, query_field)
        else:
            return "Invalid search query."

    else:
        return "Invalid search query."


def parse_logical_operator(query_content, query_field):
    """
    Helper method for differentiating between logical operators such as AND, OR, and regular statements.
    :param query_content: qualification content
    :param query_field: field being searched for
    :return: parsed query
    """
    if "AND" in query_content:
        var1 = query_content.split(" AND ")[0]
        var2 = query_content.split(" AND ")[1]
        return {"$and": [{query_field: parse_other_operators(var1)},
                         {query_field: parse_other_operators(var2)}]}
    elif "OR" in query_content:
        var1 = query_content.split(" OR ")[0]
        var2 = query_content.split(" OR ")[1]
        return {"$or": [{query_field: parse_other_operators(var1)},
                        {query_field: parse_other_operators(var2)}]}
    else:
        return {query_field: parse_other_operators(query_content)}


def parse_other_operators(var):
    """
    Helper methods for differentiating between operators such as NOT, >, <, and "".
    :param var: query content that needs to be parsed
    :return: parsed query
    """
    if "NOT" in var:
        not_var = var.split("NOT ")[1]
        # checking for exact match indicator - ""
        if '"' in not_var:
            return {"$not": {"$eq": not_var.split('"')[1]}}
        else:
            return {"$not": {"$regex": ".*" + not_var + ".*"}}
    elif ">" in var:
        greater_var = var.split("> ")[1]
        return {"$gt": greater_var}
    elif "<" in var:
        less_var = var.split("< ")[1]
        return {"$lt": less_var}
    elif '"' in var:
        return {"$eq": var.split('"')[1]}
    else:
        return {"$regex": ".*" + var + ".*"}
