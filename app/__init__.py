# Import Flask class to create the web application
from flask import Flask

# Import db (database instance) and migrate (for database migrations)
from .db import db, migrate

# Import book model so SQLAlchemy knows about the Book table
from .models import book

# Import the books blueprint containing all book-related routes
from .routes.book_routes import books_bp
# Old hello world routes (commented out)
# from .routes.hello_world_routes import hello_world_bp

# Application factory function - creates and configures the Flask app
def create_app():
    # Create a new Flask application instance
    # __name__ tells Flask where to find resources (templates, static files)
    app = Flask(__name__)

    # Configure SQLAlchemy settings
    # SQLALCHEMY_TRACK_MODIFICATIONS: Disable feature that signals app on every db change
    # Setting to False saves memory and improves performance
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # DATABASE_URI: Connection string to tell SQLAlchemy where the database is
    # Format: postgresql+psycopg2://username:password@host:port/database_name
    # postgresql+psycopg2 = database type and driver
    # postgres:postgres = username:password for database
    # localhost:5432 = database server location (local computer, default PostgreSQL port)
    # hello_books_development = name of the database to use
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:postgres@localhost:5432/hello_books_development'

    # Initialize the database with this Flask app
    # Connects SQLAlchemy to the Flask app
    db.init_app(app)
    
    # Initialize Flask-Migrate with this app and database
    # Enables database migration commands (flask db migrate, flask db upgrade, etc.)
    migrate.init_app(app, db)

    # Register blueprints - plug in route modules to the main app
    # Commented out hello world routes
    # app.register_blueprint(hello_world_bp)
    
    # Register the books blueprint - makes all /books routes available
    app.register_blueprint(books_bp)

    # Return the fully configured Flask application
    return app