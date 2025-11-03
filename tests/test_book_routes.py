import pytest
# Test function to verify GET /books returns empty list when no books exist
# Takes 'client' parameter - pytest automatically provides the client fixture from conftest.py
def test_get_all_books_with_no_records(client):
    # ACT PHASE: Perform the action we want to test
    # Make a GET request to /books endpoint using the test client
    # This simulates a user visiting http://localhost:5000/books
    response = client.get("/books")
    
    # Extract the JSON data from the response
    # Converts the JSON response body to a Python object (list/dict)
    response_body = response.get_json()

    # ASSERT PHASE: Verify the results match our expectations
    # Check that the HTTP status code is 200 (OK)
    # 200 means the request was successful
    assert response.status_code == 200

    # Check that the response body is an empty list
    # When no books exist in database, should return []
    assert response_body == []

# Test function to verify GET /books/<id> returns a specific book
# Takes 'client' and 'two_saved_books' fixtures
# two_saved_books fixture creates 2 books in the database before test runs
def test_get_one_book(client, two_saved_books):
    # ACT PHASE: Request one specific book by ID
    # Makes GET request to /books/1 to get the first book
    response = client.get("/books/1")
    
    # Extract the JSON response body
    # Should contain data for the book with ID 1
    response_body = response.get_json()

    # ASSERT PHASE: Verify the response matches expected book
    # Check that status code is 200 (OK - book found)
    assert response.status_code == 200
    
    # Check that response contains the correct book data
    # Should match the first book from two_saved_books fixture
    assert response_body == {
        "id": 1,                        # Database auto-generated ID
        "title": "Ocean Book",          # Title from fixture
        "description": "watr 4evr"      # Description from fixture
    }

# Test function to verify POST /books creates a new book
# Takes 'client' fixture - database is empty at start (no arrange needed)
def test_create_one_book(client):
    # ACT PHASE: Send POST request to create a new book
    # Make POST request to /books endpoint
    # json parameter sends data as JSON in request body
    # This is what a client would send to create a book
    response = client.post("/books", json={
        "title": "New Book",         # Book title to create
        "description": "The Best!"   # Book description to create
    })
    
    # Extract the JSON response body
    # Should contain the created book with auto-generated ID
    response_body = response.get_json()

    # ASSERT PHASE: Verify the book was created successfully
    # Check that status code is 201 (Created - resource successfully created)
    # 201 is the standard HTTP code for successful POST/creation
    assert response.status_code == 201
    
    # Check that response contains the newly created book data
    # Should include all the data we sent, plus an auto-generated ID
    assert response_body == {
        "id": 1,                      # Database auto-generated ID (first book = 1)
        "title": "New Book",          # Title matches what we sent
        "description": "The Best!"    # Description matches what we sent
    }

def test_create_one_book_no_title(client):
    # Arrange
    test_data = {"description": "The Best!"}

    # Act
    response = client.post("/books", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {'message': 'Invalid request: missing title'}

def test_create_one_book_no_description(client):
    # Arrange
    test_data = {"title": "New Book"}

    # Act
    response = client.post("/books", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {'message': 'Invalid request: missing description'}

def test_create_one_book_with_extra_keys(client):
    # Arrange
    test_data = {
        "extra": "some stuff",
        "title": "New Book",
        "description": "The Best!",
        "another": "last value"
    }

    # Act
    response = client.post("/books", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == {
        "id": 1,
        "title": "New Book",
        "description": "The Best!"
    }

def test_update_book(client, two_saved_books):
    # Arrange
    test_data = {
        "title": "New Book",
        "description": "The Best!"
    }

    # Act
    response = client.put("/books/1", json=test_data)

    # Assert
    assert response.status_code == 204
    assert response.content_length is None

def test_update_book_with_extra_keys(client, two_saved_books):
    # Arrange
    test_data = {
        "extra": "some stuff",
        "title": "New Book",
        "description": "The Best!",
        "another": "last value"
    }

    # Act
    response = client.put("/books/1", json=test_data)

    # Assert
    assert response.status_code == 204
    assert response.content_length is None

def test_update_book_missing_record(client, two_saved_books):
    # Arrange
    test_data = {
        "title": "New Book",
        "description": "The Best!"
    }

    # Act
    response = client.put("/books/3", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"message": "Book 3 not found"}

def test_update_book_invalid_id(client, two_saved_books):
    # Arrange
    test_data = {
        "title": "New Book",
        "description": "The Best!"
    }

    # Act
    response = client.put("/books/cat", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"message": "Book cat invalid"}

def test_delete_book(client, two_saved_books):
    # Act
    response = client.delete("/books/1")

    # Assert
    assert response.status_code == 204
    assert response.content_length is None

def test_delete_book_missing_record(client, two_saved_books):
    # Act
    response = client.delete("/books/3")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"message": "Book 3 not found"}

def test_delete_book_invalid_id(client, two_saved_books):
    # Act
    response = client.delete("/books/cat")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"message": "Book cat invalid"}
