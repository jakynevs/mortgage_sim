from db_setup import create_connection
from flask import Flask, jsonify, request
# import sqlite3

app = Flask(__name__)

# POST request to add new client 
@app.route('/client', methods=['POST'])
def add_client():
    # Breakdown of client data
    data = request.json
    name = data.get('name')
    dni = data.get('dni')
    email = data.get('email')
    requested_capital = data.get('requested_capital')

    # validate dni
    # handle null values
    
    #Insert data to DB
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Client (name, dni, email, requested_capital) VALUES (?, ?, ?, ?)',
                   (name, dni, email, requested_capital))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Client added successfully'}), 201
    
# GET, PUT and DELETE requests for individual client
@app.route('/client/<dni>', methods=['GET', 'PUT', 'DELETE'])
def get_client(dni):
    if request.method == "GET":
        conn = create_connection()  
        cursor = conn.cursor()     
        cursor.execute("SELECT * FROM Client WHERE dni=?", (dni,))
    
        client = cursor.fetchone()
        conn.close() # Need to close?

        return jsonify( client)
    
    if request.method == "DELETE":
        conn = create_connection()  
        cursor = conn.cursor()    
        cursor.execute("SELECT * FROM Client WHERE dni=?", (dni,))
        client = cursor.fetchone()

        if client:
            cursor.execute("DELETE FROM Client WHERE dni=?", (dni,))
            conn.commit()

            cursor.execute("SELECT * FROM Client WHERE dni=?", (dni,))
            client = cursor.fetchone()

            if not client:
                conn.close()
                return jsonify({'message': 'Resource deleted successfully'}), 200
            
            else:
                conn.close()
                return jsonify({'error': 'Deletion failed'}), 500
        
        else:
        # Client does not exist
            conn.close()
            return jsonify({'error': 'Client not found'}), 404

    if request.method == "PUT": #Check Idempotency: A PUT request is idempotent, meaning that making the same request multiple times should produce the same result. Ensure your implementation adheres to this principle.
        data = request.json
        name = data.get("name")
        email = data.get("email")
        requested_capital = data.get("requested_capital")

        conn = create_connection()  
        cursor = conn.cursor()    

        cursor.execute("SELECT * FROM Client WHERE dni=?", (dni,))
        client = cursor.fetchone()

        if client:
            cursor.execute(''' 
                UPDATE Client
                SET name = ? ,
                email = ? ,
                requested_capital = ?
                WHERE dni = ?
                ''', (name, email, requested_capital, dni,))
            
            conn.commit()

            # Confirm successful update
            cursor.execute("SELECT * FROM Client WHERE dni=?", (dni,))
            updated_client = cursor.fetchone()

            if updated_client:
                return jsonify({'message': 'Client successfully updated'}), 200
            else:
                return jsonify({'error': 'Update failed'}), 500


        else: 
            conn.close()
            return jsonify({'error': 'Client not found'}), 404
    
    
    # if client:
    #     client_data = {key: client[key] for key in client.keys()} 
    #     return jsonify(client_data)
    # else:
    #     return jsonify({'error': 'Client not found'}), 404

@app.route('/client/mortgage_sim/<dni>', methods=['POST'])
def get_mortgage_sim(dni):
    # Info to retrieve mortgage simulation of a given client
    data = request.json
    
    conn = create_connection()  
    cursor = conn.cursor()     
    cursor.execute("SELECT * FROM Client WHERE dni=?", (dni,))
    client = cursor.fetchone()

    client_id = client[0]  # Find client_id from data 
    
    # Mortgage calculation inputs:
    requested_capital = client[-1]  # Last element of the tuple
    tae = data.get("tae")
    repayment_term = data.get("repayment_term")
    i = tae / 100 / 12 # Monthly interest rate
    n = repayment_term * 12 # Repayment term in months

    # Mortgage calculation
    # Return to 2 decimal places
    monthly_instalment = requested_capital * i / (1 - (1 + i) ** (-n))
    total = monthly_instalment * n

    # Add data to DB
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO MortgageSimulation (client_id, tae, repayment_term, monthly_instalment, total) VALUES (?, ?, ?, ?, ?)',
                   (client_id, tae, repayment_term, monthly_instalment, total))
    
    conn.commit()
    conn.close()
    
    return jsonify({
        'monthly_instalment': round(monthly_instalment, 2),
        "total": round(total, 2)
        }), 200

if __name__ == '__main__':
    app.run(debug=True)  # Start the Flask app
