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
    
    client = cursor.fetchall()
    conn.close() # Need to close?
    
    return jsonify(client)
    
    # if client:
    #     client_data = {key: client[key] for key in client.keys()} 
    #     return jsonify(client_data)
    # else:
    #     return jsonify({'error': 'Client not found'}), 404

@app.route('/client/mortgage_sim/<client_id>', methods=['GET'])
def get_mortgage_sim():
    # Info to retrieve mortgage simulation of a given client
    
    pass

# @app.route('/client/<client_id>', methods=['PUT'])
# def get_client():
#     # Info to retrieve client
    
#     pass

if __name__ == '__main__':
    app.run(debug=True)  # Start the Flask app
