from config import db  # Import the database instance from the configuration file

class Contact(db.Model):
    # Define the Contact class as a model for the database, inheriting from db.Model
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for each contact, serves as the primary key
    first_name = db.Column(db.String(80), unique=False, nullable=False)  # First name of the contact, required
    last_name = db.Column(db.String(80), unique=False, nullable=False)  # Last name of the contact, required
    phone_number = db.Column(db.String(40), unique=False, nullable=False)  # Phone number of the contact, required
    email = db.Column(db.String(120), unique=True, nullable=False)  # Email of the contact, required and must be unique

    def to_json(self):
        # Method to convert a Contact object to a JSON-serializable dictionary
        return {
            "id": self.id,  # Include the contact's id
            "firstName": self.first_name,  # Include the contact's first name
            "lastName": self.last_name,  # Include the contact's last name
            "phoneNumber": self.phone_number,  # Include the contact's phone number
            "email": self.email  # Include the contact's email
        }