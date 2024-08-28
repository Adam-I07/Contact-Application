from flask import Flask  # Import the Flask class to create a Flask application
from flask_sqlalchemy import SQLAlchemy  # Import SQLAlchemy to handle database operations
from flask_cors import CORS  # Import CORS to enable Cross-Origin Resource Sharing

app = Flask(__name__)  # Create an instance of the Flask application
CORS(app)  # Enable CORS on the Flask app to allow requests from other domains

# Configure the Flask app to use SQLite as the database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydatabase.db"

# Disable the modification tracking feature of SQLAlchemy to save resources
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)  # Create a SQLAlchemy instance and link it to the Flask app
