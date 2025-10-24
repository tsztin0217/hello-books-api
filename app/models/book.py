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
