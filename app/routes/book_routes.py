from flask import Blueprint, abort, make_response
# from app.models.book import books
books_bp = Blueprint("books", __name__, url_prefix="/books")

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
