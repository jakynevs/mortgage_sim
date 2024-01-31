from db_setup import create_connection
from flask import Flask, jsonify, request
import re

# Create instance of Flask class
app = Flask(__name__)

# Function to validate dni input
def valid_dni(dni):
    
    # Check is 9 digits and a sting:
    if len(dni) != 9 or type(dni) != str:
        return False
    
    # Official table numbers corresponding from 0 > 22 
    official_number_table = "TRWAGMYFPDXBNJZSQVHLCKE"

    # Logic to deal with foreginer NIE's that start with a letter
    first_digit = dni[0]

    if first_digit.upper() == "X":
        dni = "0" + dni[1:]
    if first_digit.upper() == "Y":
        dni = "1" + dni[1:]
    if first_digit.upper() == "Z":
        dni = "2" + dni[1:]
    
    # Get number part of dni
    number = int(dni[:-1])

    # Get last letter of dni
    letter = dni[-1].upper()

    # Check if letter meets official guidelines
    return letter == official_number_table[number % 23]

# Function to validate name input
def valid_name(name):
    if not isinstance(name, str) or len(name) > 100:
        return False
    else:
        return True

# Function to validate email input
def valid_email(email):
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if not re.fullmatch(email_regex, email):
        return False
    else:
        return True

# Function to validate requested_capital input
def valid_requested_capital(requested_capital):
    if not isinstance(requested_capital, (int, float)) or requested_capital <= 0:
        return False
    else:
        return True

# Function to retrieve client from DB using dni
def get_client_by_dni(dni):
    try:
        conn = create_connection()  
        cursor = conn.cursor()     

        # SQL command to retrieve client:
        cursor.execute("SELECT * FROM Client WHERE dni=?", (dni,))
        client = cursor.fetchone()
        return client
    
    except Exception as e:
        # Log exception:
        print(f"An error occurred: {e}")
        return None
    
    finally:
        conn.close()

# ENDPOINTS:

# POST request to add new client 
@app.route('/client', methods=['POST'])
def add_client():
    
    expected_fields = {'name', 'dni', 'email', 'requested_capital'}
    data = request.json
    
    # Make sure there is a request body:
    if not data:
        return jsonify({"error": "Empty request body"}), 400

    # Check for unexpected fields:
    unexpected_fields = set(data.keys()) - expected_fields
    if unexpected_fields:
        return jsonify({"error": f"Unexpected fields: {unexpected_fields}"}), 400

    # Breakdown of client data
    name = data.get('name')
    dni = data.get('dni')
    email = data.get('email')
    requested_capital = data.get('requested_capital')
    
    # DNI validation:
    if not dni or not valid_dni(dni):
        return jsonify({"error": "Invalid or missing dni"}), 400
    
    # Check if there is already someone with this dni in db:
    if get_client_by_dni(dni):
        return jsonify({"error": "Client with this dni already exists"}), 400

    # Name validation:
    if not name or not valid_name(name):
        return jsonify({"error": "Invalid or missing name"}), 400

    # Email validation:
    if not email or not valid_email(email):
        return jsonify({"error": "Invalid or missing email"}), 400
    
    # Requested capital validation:
    if not requested_capital:
        return jsonify({"error": "requested_capital missing"}), 400
    if not valid_requested_capital(requested_capital):
        return jsonify({"error": "requested_capital must be a positive number"}), 400
    
    #Insert data to DB
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Client (name, dni, email, requested_capital) VALUES (?, ?, ?, ?)',
                    (name, dni, email, requested_capital))
        conn.commit()
    
    except Exception as e:
        # Log exception:
        print(f"An error occurred: {e}")
        return jsonify({'error': 'Database operation failed'}), 500

    finally:
        conn.close()

    return jsonify({'message': 'Client added successfully'}), 201
    

# GET request to retrieve individual client
@app.route('/client/<dni>', methods=['GET'])
def get_client(dni):
    
    # Validation of DNI
    if not valid_dni(dni):
        return jsonify({"error": "Invalid dni"}), 400
    
    client = get_client_by_dni(dni)
    
    if client:
        return jsonify(client)
    else:
        return jsonify({'error': 'Client not found'}), 404
 
# DELETE request to delete individual client
@app.route('/client/<dni>', methods=['DELETE'])
def delete_client(dni):   
    
    # Validation of DNI
    if not valid_dni(dni):
        return jsonify({"error": "Invalid dni"}), 400
    
    client = get_client_by_dni(dni)
    
    conn = create_connection()  
    cursor = conn.cursor()    

    if client:
        
        try:
            # Delete from DB
            cursor.execute("DELETE FROM Client WHERE dni=?", (dni,))
            conn.commit()
        
        except Exception as e:
            # Log exception:
            print(f"An error occurred: {e}")
            return jsonify({'error': 'Database operation failed'}), 500

        finally:
            conn.close()

        client = get_client_by_dni(dni)

        # Confirmation that client has been deleted
        if not client:
            return jsonify({'message': 'Resource deleted successfully'}), 200
        
        # Error handling if still a matching client with given DNI
        else:
            return jsonify({'error': 'Deletion failed'}), 500
    
    else:
        return jsonify({'error': 'Client not found'}), 404

# PUT request to update individual client
@app.route('/client/<dni>', methods=['PUT'])
def update_client(dni):

    # Validation of dni in url
    if not valid_dni(dni):
        return jsonify({"error": "Invalid dni"}), 400

    expected_fields = {'name', 'dni', 'email', 'requested_capital'}
    data = request.json
    
    # Make sure there is a request body:
    if not data:
        return jsonify({"error": "Empty request body"}), 400
    
    # Check for unexpected fields:
    unexpected_fields = set(data.keys()) - expected_fields
    if unexpected_fields:
        return jsonify({"error": f"Unexpected fields: {unexpected_fields}"}), 400
        
    # Breakdown of client data in request body
    name = data.get("name")
    email = data.get("email")
    requested_capital = data.get("requested_capital")

    # Handling of new dni:
    if data.get("dni") and dni != data.get("dni"):
        new_dni = data.get("dni")
        
        # new_dni validation:
        if not valid_dni(new_dni):
            return jsonify({"error": "Invalid dni"}), 400
        
        # Check that new_dni isn't duplicate:
        if get_client_by_dni(new_dni):
            return jsonify({"error": "Client with this dni already exists"}), 400
    
    else:
        new_dni = dni
        
    # Name validation:
    if not name or not valid_name(name):
        return jsonify({"error": "Invalid or missing name"}), 400

    # Email validation:
    if not email or not valid_email(email):
        return jsonify({"error": "Invalid or missing email"}), 400
    
    # Requested capital validation:
    if not requested_capital:
        return jsonify({"error": "requested_capital missing"}), 400
    if not valid_requested_capital(requested_capital):
        return jsonify({"error": "requested_capital must be a positive number"}), 400
    
    client = get_client_by_dni(dni)
    
    if client:
        try:
            conn = create_connection()  
            cursor = conn.cursor()    

            # SQL to update client in DB
            cursor.execute(''' 
                UPDATE Client
                SET name = ? ,
                dni = ?
                email = ? ,
                requested_capital = ?
                WHERE dni = ?
                ''', (name, new_dni, email, requested_capital, dni,))
            
            conn.commit()
        
        except Exception as e:
            # Log exception:
            print(f"An error occurred: {e}")
            return jsonify({'error': 'Database operation failed'}), 500

        finally:
            conn.close()

        # Confirm successful update
        updated_client = get_client_by_dni(new_dni)

        if updated_client:
            return jsonify({'message': 'Client successfully updated'}), 200
        else:
            return jsonify({'error': 'Update failed'}), 500

    else: 
        return jsonify({'error': 'Client not found'}), 404

# POST request for Mortgage Simulation
@app.route('/client/mortgage_sim/<dni>', methods=['POST'])
def get_mortgage_sim(dni):
    
    # Validation of DNI in url
    if not valid_dni(dni):
        return jsonify({"error": "Invalid or missing DNI"}), 400
    
    expected_fields = {'tae', 'repayment_term'}
    data = request.json
    
    # Make sure there is a request body:
    if not data:
        return jsonify({"error": "Empty request body"}), 400
    
    # Check for unexpected fields:
    unexpected_fields = set(data.keys()) - expected_fields
    if unexpected_fields:
        return jsonify({"error": f"Unexpected fields: {unexpected_fields}"}), 400
    
    # Find client and client_id 
    client = get_client_by_dni(dni)
    client_id = client[0]  
    
    if client:

        # Breakdown of TAE and repayment term from request body
        tae = data.get("tae")
        repayment_term = data.get("repayment_term")

        # TAE validation:
        if tae is None:
            return jsonify({"error": "tae missing"}), 400
        if not isinstance(tae, (int, float)) or tae <= 0 or tae > 100:
            return jsonify({"error": "tae must be a positive number and less than 100"}), 400

        # Repayment term validation:
        if repayment_term is None:
            return jsonify({"error": "repayment_term missing"}), 400
        if not isinstance(repayment_term, (int)) or repayment_term <= 0 or repayment_term > 40:
            return jsonify({"error": "repayment_term must be a positive number and less than 40 years"}), 400

        # Retrieve requested capital from client info.
        requested_capital = client[-1]  

        # Monthly interest rate
        i = tae / 100 / 12 
        # Repayment term in months
        n = repayment_term * 12 

        # Mortgage calculations
        monthly_instalment = requested_capital * i / (1 - (1 + i) ** (-n))
        total = monthly_instalment * n

        # Add data to DB
        try:
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute('INSERT INTO MortgageSimulation (client_id, tae, repayment_term, monthly_instalment, total) VALUES (?, ?, ?, ?, ?)',
                        (client_id, tae, repayment_term, monthly_instalment, total))
            
            conn.commit()

        except Exception as e:
            # Log exception:
            print(f"An error occurred: {e}")
            return jsonify({'error': 'Database operation failed'}), 500
        
        finally:
            conn.close()
    else:
        return jsonify({'error': 'Client not found'}), 404
    
    # Return outputs to 2 decimal places
    return jsonify({
        'monthly_instalment': round(monthly_instalment, 2),
        "total": round(total, 2)
        }), 200

# Start Flask application
if __name__ == '__main__':
    app.run(debug=True)  
