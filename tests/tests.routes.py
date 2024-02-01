import json
import pytest
from app import app  

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_add_client(client):
    # Define a test client data
    test_data = {
        "name": "John Doe",
        "dni": "87654321X",
        "email": "john@example.com",
        "requested_capital": 10000
    }

    # Send a POST request to the '/client' endpoint
    response = client.post('/client', data=json.dumps(test_data), content_type='application/json')
    
    # Check if the response is as expected
    assert response.status_code == 201 
    assert b"Client added successfully" in response.data 

def test_add_client_invalid_dni(client):
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
    assert b"Invalid or missing dni" in response.data 

def test_add_client_missing_email(client):
    # Define a test client data
    test_data = {
        "name": "John Doe",
        "dni": "12345678Z",
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


