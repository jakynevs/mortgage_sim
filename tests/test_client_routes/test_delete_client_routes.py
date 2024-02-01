import json
import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def add_test_client(client):

    # Define a test client data
    test_data = {
        "name": "John Doe",
        "dni": "67654321M",
        "email": "john@example.com",
        "requested_capital": 10000,
    }

    # Send a POST request to the '/client' endpoint
    client.post("/client", data=json.dumps(test_data), content_type="application/json")


def test_delete_client(client):

    add_test_client(client)

    test_dni = "67654321M"

    response = client.delete(f"/client/{test_dni}")

    # Check if the response is as expected
    assert response.status_code == 200
    assert b"Client deleted successfully" in response.data


def test_delete_client_not_found(client):

    test_dni = "24681257A"

    response = client.delete(f"/client/{test_dni}")

    # Check if the response is as expected
    assert response.status_code == 404
    assert b"Client not found" in response.data
