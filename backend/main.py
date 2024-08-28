from flask import request, jsonify
from config import app, db
from models import Contact
from sqlalchemy.exc import IntegrityError

# Get request to get all existing contacts in the database
@app.route("/contacts", methods=["GET"])
def get_all_contacts():
    contacts = Contact.query.all()  # Query all contacts from the database
    json_contacts = list(map(lambda x: x.to_json(), contacts))  # Convert each contact to JSON
    return jsonify({"contacts": json_contacts})  # Return the list of contacts as JSON

# Post request to create a new contact in the database
@app.route("/create_contact", methods=["POST"])
def create_contact():
    first_name = request.json.get("firstName")  # Get first name from request JSON
    last_name = request.json.get("lastName")  # Get last name from request JSON
    phone_number = request.json.get("phoneNumber")  # Get phone number from request JSON
    email = request.json.get("email")  # Get email from request JSON

    # Check if all required fields are provided
    if not first_name or not last_name or not phone_number or not email:
        return jsonify({"message": "You must include a first name, last name, phone number and email"}), 400

    # Create a new Contact object
    new_contact = Contact(first_name=first_name, last_name=last_name, phone_number=phone_number, email=email)
    try:
        db.session.add(new_contact)  # Add the new contact to the session
        db.session.commit()  # Commit the session to save the contact
    except IntegrityError as e:
        db.session.rollback()  # Rollback the session if there's an error
        if "UNIQUE constraint failed: contact.email" in str(e):
            return jsonify({"message": "Email already exists"}), 400  # Return a custom message for unique constraint failure
        else:
            return jsonify({"message": str(e)}), 400  # Return a general error message
    except Exception as e:
        db.session.rollback()  # Rollback the session if there's a different error
        return jsonify({"message": str(e)}), 400  # Return a general error message
    
    return jsonify({"message": "User created!"}), 201  # Return success message if contact is created

# Patch request to update an existing contact by user_id
@app.route("/update_contact/<int:user_id>", methods=["PATCH"])
def update_contact(user_id):
    contact = Contact.query.get(user_id)  # Find the contact by user_id
    if not contact:
        return jsonify({"message": "Contact not found"}), 404  # Return error if contact is not found
    
    data = request.json  # Get the data from the request JSON
    # Update contact details, use existing values if not provided
    contact.first_name = data.get("firstName", contact.first_name)
    contact.last_name = data.get("lastName", contact.last_name)
    contact.phone_number = data.get("phoneNumber", contact.phone_number)
    contact.email = data.get("email", contact.email)

    db.session.commit()  # Commit the session to save the updated contact
    return jsonify({"message": "Contact updated!"}), 200  # Return success message if contact is updated

# Delete request to delete an existing contact by user_id
@app.route("/delete_contact/<int:user_id>", methods=["DELETE"])
def delete_contact(user_id):
    contact = Contact.query.get(user_id)  # Find the contact by user_id
    if not contact:
        return jsonify({"message": "Contact not found"}), 404  # Return error if contact is not found
    
    db.session.delete(contact)  # Delete the contact from the session
    db.session.commit()  # Commit the session to finalize the deletion
    return jsonify({"message": "Contact deleted!"}), 200  # Return success message if contact is deleted

# Main block to set up the database and run the application
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create all tables in the database if they don't exist

    app.run(debug=True)  # Run the Flask application with debug mode enabled