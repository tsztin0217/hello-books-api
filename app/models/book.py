# OLD IMPLEMENTATION: Plain Python class (no database)
# This was used before we added database functionality
# class Book:
#     def __init__(self, id, title, description):
#         self.id = id
#         self.title = title
#         self.description = description


# OLD IMPLEMENTATION: In-memory list of books (data lost when server restarts)
# books = [
#     Book(1, "Fictional Book", "A fantasy novel set in an imaginary world."),
#     Book(2, "Wheel of Time", "A fantasy novel set in an imaginary world."),
#     Book(3, "Fictional Book Title", "A fantasy novel set in an imaginary world.")
# ]

# Import Mapped and mapped_column for type hints and column definitions
# These help define database columns with Python type annotations
from sqlalchemy.orm import Mapped, mapped_column

# Import db (database instance) to create database models
from ..db import db

# Define the Book model class
# Inherits from db.Model, which makes it a database table
class Book(db.Model):
    # Define the 'id' column
    # Mapped[int] = type hint (this column stores integers)
    # primary_key=True = this is the unique identifier for each row
    # autoincrement=True = database automatically generates IDs (1, 2, 3...)
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    # Define the 'title' column
    # Mapped[str] = type hint (this column stores strings/text)
    # No additional options = this is a required field
    title: Mapped[str]
    
    # Define the 'description' column
    # Mapped[str] = type hint (this column stores strings/text)
    # No additional options = this is a required field
    description: Mapped[str]

    # CLASS METHOD: Create a Book instance from a dictionary
    # @classmethod decorator means this method belongs to the class itself, not an instance
    # Used in POST /books route to convert incoming JSON data into a Book object
    @classmethod
    def from_dict(cls, book_data):
        # cls = the Book class itself (not an instance)
        # book_data = dictionary with "title" and "description" keys
        # Example: {"title": "New Book", "description": "Great story"}
        
        # Create a new Book instance using data from the dictionary
        # cls() calls Book() constructor
        # Extracts "title" from book_data dictionary using ["title"]
        # Extracts "description" from book_data dictionary using ["description"]
        # If either key is missing, raises KeyError (caught in route)
        new_book = cls(title=book_data["title"],
                        description=book_data["description"])
        
        # Return the newly created Book object
        # This Book object can then be added to the database
        return new_book
    
    # INSTANCE METHOD: Convert a Book instance to a dictionary
    # Used in GET routes to convert Book objects into JSON-serializable dictionaries
    # self = the specific Book instance we're converting
    def to_dict(self):
        # Create an empty dictionary to hold the book data
        book_as_dict = {}
        
        # Add the book's id to the dictionary
        # self.id = this book's database ID (e.g., 1, 2, 3)
        book_as_dict["id"] = self.id
        
        # Add the book's title to the dictionary
        # self.title = this book's title string (e.g., "Ocean Book")
        book_as_dict["title"] = self.title
        
        # Add the book's description to the dictionary
        # self.description = this book's description string (e.g., "watr 4evr")
        book_as_dict["description"] = self.description

        # Return the dictionary
        # Flask will automatically convert this to JSON in the response
        # Example output: {"id": 1, "title": "Ocean Book", "description": "watr 4evr"}
        return book_as_dict