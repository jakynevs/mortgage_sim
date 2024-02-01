import json
import pytest
from app import app  

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_update_client(client):
    # Define a test client data
    test_data = {
        "name": "Sofia Gómez",
        "dni": "23456789D",
        "email": "sofia.gomez@example.com",
        "requested_capital": 10000
    }

    test_dni = "23456789D"

    # Send a UPDATE request to the '/client' endpoint
    response = client.put(f'/client/{test_dni}', data=json.dumps(test_data), content_type='application/json')

    # Check if the response is as expected
    assert response.status_code == 200
    assert b"Client successfully updated" in response.data 

def test_update_client_empty_body(client):
    # Define a test client data
    test_data = {}

    test_dni = "23456789D"

    # Send a UPDATE request to the '/client' endpoint
    response = client.put(f'/client/{test_dni}', data=json.dumps(test_data), content_type='application/json')

    # Check if the response is as expected
    assert response.status_code == 400
    assert b"Empty request body" in response.data 

def test_update_client_unexpected_fields(client):
    # Define a test client data
    test_data = {
        "name": "Sofia Gómez",
        "dni": "23456789D",
        "extra_field": 1222,
        "email": "sofia.gomez@example.com",
        "requested_capital": 10000
    }

    test_dni = "23456789D"

    # Send a UPDATE request to the '/client' endpoint
    response = client.put(f'/client/{test_dni}', data=json.dumps(test_data), content_type='application/json')

    # Check if the response is as expected
    assert response.status_code == 400
    assert b"Unexpected fields:" in response.data 

def test_update_client_client_not_found(client):
    # Define a test client data
    test_data = {
        "name": "Sofia Gómez",
        "dni": "23456789D",
        "email": "sofia.gomez@example.com",
        "requested_capital": 10000
    }

    test_dni = "24681257A"

    # Send a UPDATE request to the '/client' endpoint
    response = client.put(f'/client/{test_dni}', data=json.dumps(test_data), content_type='application/json')

    # Check if the response is as expected
    assert response.status_code == 404
    assert b"Client not found" in response.data 
