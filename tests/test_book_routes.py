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