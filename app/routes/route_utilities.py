# Import abort to stop execution and return error responses
# Import make_response to create custom HTTP responses
from flask import abort, make_response

# Import db to query the database
from ..db import db

# UTILITY FUNCTION: Validate model ID and retrieve model from database
# This is a generic/reusable function that works with ANY model class (Book, Author, etc.)
# Used by routes to avoid code duplication when validating IDs
# Parameters:
#   cls = the model class (e.g., Book, Author)
#   model_id = the ID from the URL (comes as a string)
# Returns: Model instance if found, or aborts with 400/404 error
def validate_model(cls, model_id):
    # STEP 1: Validate that model_id is a valid integer
    try:
        # Try to convert model_id from string to integer
        # model_id comes from URL as string (e.g., "1", "abc", "12.5")
        # Example: "/books/1" → model_id = "1" (string)
        # Example: "/books/cat" → model_id = "cat" (string)
        model_id = int(model_id)
    except:
        # If conversion fails (e.g., "abc", "cat", "12.5"), this block runs
        # cls.__name__ gets the class name as a string (e.g., "Book", "Author")
        # This makes the error message dynamic and reusable for any model
        response = {"message": f"{cls.__name__} {model_id} invalid"}
        
        # abort() stops execution and returns 400 Bad Request error
        # 400 = client error (invalid input format)
        # make_response() creates HTTP response with our message and status code
        abort(make_response(response , 400))

    # STEP 2: Query the database to find the model with this ID
    # db.select(cls) builds a SQL query: SELECT * FROM <table_name>
    # cls is the model class (Book, Author, etc.)
    # .where(cls.id == model_id) adds WHERE id = model_id
    # Example: SELECT * FROM book WHERE id = 1
    query = db.select(cls).where(cls.id == model_id)
    
    # Execute the query and get a single result (or None if not found)
    # scalar() returns one object or None (unlike scalars() which returns multiple)
    model = db.session.scalar(query)
    
    # STEP 3: Check if model was found in database
    if not model:
        # Model doesn't exist in database - create error message
        # cls.__name__ gets the class name (e.g., "Book" → "Book 3 not found")
        response = {"message": f"{cls.__name__} {model_id} not found"}
        
        # abort() stops execution and returns 404 Not Found error
        # 404 = resource doesn't exist
        # make_response() creates HTTP response with our message and status code
        abort(make_response(response, 404))
    
    # STEP 4: Model is valid and exists - return it
    # This model object will be used by the calling route function
    # Example: Returns a Book object that can be updated, deleted, or returned as JSON
    return model
