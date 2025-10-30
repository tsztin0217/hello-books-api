# Import pytest for testing framework and fixtures
import pytest

# Import create_app to create our Flask application
from app import create_app

# Import db to interact with the database (create/drop tables)
from app.db import db

# Import request_finished signal to hook into Flask request lifecycle
from flask.signals import request_finished

# Import dotenv to load environment variables from .env file
from dotenv import load_dotenv

# Import os to access environment variables
import os

# Load environment variables from .env file into the environment
# This makes variables like SQLALCHEMY_TEST_DATABASE_URI available
load_dotenv()

# Fixture that creates and configures a Flask app for testing
# Other fixtures and tests can use this by requesting 'app' parameter
@pytest.fixture
def app():
    # Create a configuration dictionary for the test app
    test_config = {
        # TESTING mode enables test-specific behavior (better error messages, etc.)
        "TESTING": True,
        
        # Use a separate test database (not your development database!)
        # Gets the database URI from environment variables
        "SQLALCHEMY_DATABASE_URI": os.environ.get('SQLALCHEMY_TEST_DATABASE_URI')
    }
    
    # Create the Flask app with our test configuration
    # Passes test_config to override default settings
    app = create_app(test_config)

    # Register a signal handler that runs after each request finishes
    # connect_via(app) makes it only apply to this test app
    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        # Remove the database session after each request
        # Prevents data from bleeding between tests
        db.session.remove()

    # SETUP PHASE: Create app context and database tables
    # app_context() makes the app the "active" app for database operations
    with app.app_context():
        # Create all database tables based on your models (Book, etc.)
        # This gives tests a fresh database to work with
        db.create_all()
        
        # YIELD: Pause here and give the app to the test
        # Test runs while fixture is paused
        yield app

    # CLEANUP PHASE: Runs after the test finishes
    # Create app context again for cleanup operations
    with app.app_context():
        # Drop (delete) all database tables
        # Ensures tests don't leave data behind
        db.drop_all()


# Fixture that creates a test client for making HTTP requests
# Depends on 'app' fixture (pytest automatically calls app() first)
@pytest.fixture
def client(app):
    # Create and return a test client from the app
    # This client can make requests like: client.get('/books')
    # Without actually running a server
    return app.test_client()