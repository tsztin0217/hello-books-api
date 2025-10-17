from flask import Flask
from .routes.book_routes import books_bp
# from .routes.hello_world_routes import hello_world_bp

def create_app():
    app = Flask(__name__)

    # Register blueprints
    # app.register_blueprint(hello_world_bp)
    app.register_blueprint(books_bp)

    return app