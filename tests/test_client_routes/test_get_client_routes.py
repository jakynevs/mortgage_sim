import pytest
from app import app  

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_client(client):

    test_dni = "12345666W"

    # Send a GET request to the '/client/<dni>' endpoint
    response = client.get(f'/client/{test_dni}')

    # Get dni from JSON response
    response_dni = response.json['data'][2]

    # Check if the response is as expected
    assert response.status_code == 200
    assert response_dni == test_dni 

def test_get_client_not_found(client):

    test_dni = "24681257A"

    # Send a GET request to the '/client/<dni>' endpoint
    response = client.get(f'/client/{test_dni}')

    # Check if the response is as expected
    assert response.status_code == 404
    assert b"Client not found" in response.data 

def test_get_client_invalid_dni(client):

    test_dni = "24681357D"

    # Send a GET request to the '/client/<dni>' endpoint
    response = client.get(f'/client/{test_dni}')

    # Check if the response is as expected
    assert response.status_code == 400
    assert b"Invalid dni" in response.data 

