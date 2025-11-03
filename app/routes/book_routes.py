# Import Blueprint to create a modular set of routes
# Import abort to stop execution and return error responses
# Import make_response to create custom HTTP responses
# Import request to access incoming HTTP request data
from flask import Blueprint, abort, make_response, request, Response

# Import the Book model class to create new book instances
from app.models.book import Book

# Import db to interact with the database (add, commit, query, etc.)
from ..db import db

# Old import when using in-memory list (now using database instead)
# from app.models.book import books

# Create a Blueprint named "books" with URL prefix "/books"
# All routes in this blueprint will start with /books
books_bp = Blueprint("books_dp", __name__, url_prefix="/books")

# Decorator: Register this function to handle POST requests to /books
@books_bp.post("")
def create_book():
    # Get the JSON data from the incoming request body
    request_body = request.get_json()

    try:
        new_book = Book.from_dict(request_body)
    except KeyError as error:
        response = {"message": f"Invalid request: missing {error.args[0]}"}
        abort(make_response(response, 400))
    
    # Add the new book to the database session (staging area)
    db.session.add(new_book)
    
    # Commit the changes to save the book to the database permanently
    db.session.commit()

    # Create a response dictionary with the new book's data
    # response = {
    #     "id": new_book.id,              # Auto-generated database ID
    #     "title": new_book.title,        # The book's title
    #     "description": new_book.description,  # The book's description
    # }
    response = new_book.to_dict()

    # Return the response with status code 201 (Created)
    return response, 201

# Decorator: Register this function to handle GET requests to /books
# Supports optional query parameters for filtering
# Example: GET /books?title=Harry&description=magic
@books_bp.get("")
def get_all_books():
    # STEP 1: Start building the SQL query to select all books
    # This is the base query that will be modified based on query parameters
    query = db.select(Book)

    # STEP 2: Check for 'title' query parameter and filter if present
    # request.args.get("title") retrieves the value from URL query string
    # Example URL: /books?title=Harry → title_param = "Harry"
    # Example URL: /books → title_param = None (parameter not provided)
    # get() returns None if parameter doesn't exist (won't raise error)
    title_param = request.args.get("title")
    
    # If title_param exists (user provided ?title=something in URL)
    if title_param:
        # Add a WHERE clause to filter books by title
        # ilike() = case-insensitive LIKE search (works in PostgreSQL)
        # % is wildcard - matches any characters
        # Example: "%Harry%" matches "Harry Potter", "The Harry", "harry"
        query = query.where(Book.title.ilike(f"%{title_param}%"))
    
    # STEP 3: Check for 'description' query parameter and filter if present
    # request.args.get("description") retrieves description from query string
    # Example URL: /books?description=magic → description_param = "magic"
    # Can combine with title: /books?title=Harry&description=wizard
    description_param = request.args.get("description")
    
    # If description_param exists (user provided ?description=something)
    if description_param:
        # Add another WHERE clause to filter by description
        # This combines with title filter if both are provided (AND logic)
        # ilike() is case-insensitive pattern matching
        query = query.where(Book.description.ilike(f"%{description_param}%"))
    
    # STEP 4: Add ORDER BY clause to sort results by ID
    # This happens after all filters are applied
    # Results will be sorted in ascending order (1, 2, 3, ...)
    query = query.order_by(Book.id)
    
    
    # Execute the query and get the results as Book objects
    # scalars() returns the actual Book objects (not raw database rows)
    books = db.session.scalars(query)
    # We could also write the line above as:
    # books = db.session.execute(query).scalars()

    # Create an empty list to hold the book data in dictionary format
    books_response = []
    
    # # Loop through each Book object returned from the database
    # for book in books:
    #     # Convert each Book object into a dictionary and add it to the list
    #     books_response.append(
    #         {
    #             "id": book.id,              # The book's database ID
    #             "title": book.title,        # The book's title
    #             "description": book.description  # The book's description
    #         }
    #     )

    for book in books:
        books_response.append(book.to_dict())
    
    # Return the list of book dictionaries as JSON (Flask auto-converts)
    # Status code defaults to 200 (OK) if not specified
    return books_response

# Decorator: Register this function to handle GET requests to /books/<book_id>
# <book_id> is a URL parameter - captures the ID from the URL
# Example: GET /books/1 → book_id = "1" (as string)
@books_bp.get("/<book_id>")
def get_one_book(book_id):
    # Call validate_book to check if book_id is valid and book exists
    # If validation fails, validate_book will abort with 400 or 404 error
    # If successful, returns the Book object from database
    book = validate_model(Book, book_id)

    # Build and return a dictionary with the book's data
    # Flask automatically converts this dictionary to JSON
    # Status code defaults to 200 (OK)
    # return {
    #     "id": book.id,                      # The book's database ID
    #     "title": book.title,                # The book's title
    #     "description": book.description,    # The book's description
    # }
    return book.to_dict()

# Helper function to validate book_id and retrieve the book from database
# Used by get_one_book and update_book to avoid code duplication
# Returns: Book object if found, or aborts with error if invalid/not found
def validate_model(cls, model_id):
    # STEP 1: Validate that book_id is a valid integer
    try:
        # Try to convert book_id from string to integer
        # book_id comes from URL as string (e.g., "1", "abc", "12.5")
        model_id = int(model_id)
    except:
        # If conversion fails (e.g., "abc", "hello"), this block runs
        # Create an error message dictionary
        response = {"message": f"{cls.__name__} {model_id} invalid"}
        # abort() stops execution and returns 400 Bad Request error
        # make_response() creates HTTP response with our message and status code
        abort(make_response(response , 400))

    # STEP 2: Query the database to find the book with this ID
    # Build a SQL query: SELECT * FROM book WHERE id = book_id
    query = db.select(cls).where(cls.id == model_id)
    
    # Execute the query and get a single result (or None if not found)
    # scalar() returns one Book object or None (unlike scalars() which returns multiple)
    book = db.session.scalar(query)
    
    # STEP 3: Check if book was found in database
    if not book:
        # Book doesn't exist - create error message
        response = {"message": f"{cls.__name__} {model_id} not found"}
        # abort() stops execution and returns 404 Not Found error
        abort(make_response(response, 404))

    # STEP 4: Book is valid and exists - return it
    # This Book object will be used by the calling function
    return book

# Decorator: Register this function to handle PUT requests to /books/<book_id>
# PUT is used to update/replace an existing resource
# Example: PUT /books/1 with JSON body → updates book with ID 1
@books_bp.put("/<book_id>")
def update_book(book_id):
    # STEP 1: Validate the book_id and get the existing book from database
    # If book doesn't exist or ID is invalid, validate_book will abort with error
    # If successful, we get the Book object that we want to update
    book = validate_model(Book, book_id)
    
    # STEP 2: Get the JSON data from the request body
    # This contains the new title and description from the client
    # Example: {"title": "New Title", "description": "New Description"}
    request_body = request.get_json()

    # STEP 3: Update the book's attributes with new values from request
    # Extract "title" from request JSON and assign to book.title
    book.title = request_body["title"]
    
    # Extract "description" from request JSON and assign to book.description
    book.description = request_body["description"]
    
    # STEP 4: Save the changes to the database
    # commit() writes the updated book data to PostgreSQL
    # No need to call db.session.add() because book already exists in session
    db.session.commit()

    # STEP 5: Return empty response with 204 No Content status
    # 204 means "success, but no data to return"
    # This is standard for PUT/UPDATE operations
    # mimetype tells client to expect JSON format (even though body is empty)
    return Response(status=204, mimetype="application/json")

@books_bp.delete("/<book_id>")
def delete_book(book_id):
    # STEP 1: Validate the book_id and get the existing book from database
    book = validate_model(Book, book_id)

    # STEP 2: Delete the book from the database session
    db.session.delete(book)

    # STEP 3: Commit the changes to permanently remove the book
    db.session.commit()

    # STEP 4: Return empty response with 204 No Content status
    return Response(status=204, mimetype="application/json")


# @books_bp.get("")
# def get_all_books():
#     books_response = []
#     for book in books:
#         books_response.append(
#             {
#                 "id": book.id,
#                 "title": book.title,
#                 "description": book.description
#             }
#         )
#     return {"books": books_response}

# @books_bp.get("/<book_id>")
# def get_one_book(book_id):
#     book = validate_book(book_id)

#     return {
#         "id": book.id,
#         "title": book.title,
#         "description": book.description
#     }

# def validate_book(book_id):
#     # PART 1: Check if book_id is a valid number
#     try:
#         book_id = int(book_id)
#     except ValueError:
#         response = {"message": f"book {book_id} invalid"}
#         abort(make_response(response, 400))  # ← abort #1 is INSIDE except
#         # If this abort runs, function STOPS here
    
#     # PART 2: Search for the book (only runs if Part 1 succeeded)
#     for book in books:
#         if book.id == book_id:
#             return book  # Found it! Return and exit
    
#     # PART 3: If we reach here, book wasn't found
#     response = {"message": f"book {book_id} not found"}
#     abort(make_response(response, 404))  # ← abort #2 is OUTSIDE, at the end
