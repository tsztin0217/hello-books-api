# manage creating database and migration objects

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .models.base import Base

# create an instance of SQLAlchemy called db
# and pass it to the Base class as the constructor argument
# will use it when we need to interact with the database
# to perform operations like creating and updating records
db = SQLAlchemy(model_class=Base)

# make an instance of Migrate called migrate
# will use it to update the database tables when we make changes
# to our model class's attributes
migrate = Migrate()