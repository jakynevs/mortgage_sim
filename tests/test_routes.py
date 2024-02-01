import json
import pytest
from db_setup import create_connection
from app import app  

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def delete_test_client(client_dni):
    # Assuming you have a function to create a DB connection
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Client WHERE dni=?", (client_dni,))
    conn.commit()
    conn.close()

def test_add_client(client):
    # Define a test client data
    test_data = {
        "name": "John Doe",
        "dni": "67654321M",
        "email": "john@example.com",
        "requested_capital": 10000
    }

    # Send a POST request to the '/client' endpoint
    response = client.post('/client', data=json.dumps(test_data), content_type='application/json')
    
    # Delete client so test can be ran again
    delete_test_client(test_data["dni"])

    # Check if the response is as expected
    assert response.status_code == 201 
    assert b"Client added successfully" in response.data 

def test_add_client_already_exists(client):
    # Define a test client data
    test_data = {
        "name": "John Doe",
        "dni": "12345678Z",
        "email": "john@example.com",
        "requested_capital": 10000
    }

    # Send a POST request to the '/client' endpoint
    response = client.post('/client', data=json.dumps(test_data), content_type='application/json')
    
    # Check if the response is as expected
    assert response.status_code == 400 
    assert b"Client with this dni already exists" in response.data 

def test_add_client_invalid_dni(client):
    # Define a test client data
    test_data = {
        "name": "John Doe",
        "dni": "244567Z",
        "email": "john@example.com",
        "requested_capital": 10000
    }

    # Send a POST request to the '/client' endpoint
    response = client.post('/client', data=json.dumps(test_data), content_type='application/json')
    
    # Check if the response is as expected
    assert response.status_code == 400 
    assert b"Invalid or missing dni" in response.data 

def test_add_client_missing_email(client):
    # Define a test client data
    test_data = {
        "name": "John Doe",
        "dni": "12244896H",
        "requested_capital": 10000
    }

    # Send a POST request to the '/client' endpoint
    response = client.post('/client', data=json.dumps(test_data), content_type='application/json')
    
    # Check if the response is as expected
    assert response.status_code == 400 
    assert b"Invalid or missing email" in response.data 

def test_add_client_additional_field(client):
    # Define a test client data
    test_data = {
        "name": "John Doe",
        "dni": "12345678Z",
        "extra": "data",
        "requested_capital": 10000
    }

    # Send a POST request to the '/client' endpoint
    response = client.post('/client', data=json.dumps(test_data), content_type='application/json')
    
    # Check if the response is as expected
    assert response.status_code == 400 
    assert b"Unexpected fields" in response.data 


