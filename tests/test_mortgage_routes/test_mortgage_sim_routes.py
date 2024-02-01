import json
import pytest
from db.db_setup import create_connection
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def add_test_client_with_requested_capital(client, requested_capital):
    test_client_data = {
        "name": "Test Client",
        "dni": "36489612C",
        "email": "testclient@example.com",
        "requested_capital": requested_capital,
    }
    response = client.post(
        "/client", data=json.dumps(test_client_data), content_type="application/json"
    )

    assert response.status_code == 201
    return test_client_data["dni"]


# Delete funtion of client. To be run after being added.
def delete_test_client(client_dni):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Client WHERE dni=?", (client_dni,))
    conn.commit()
    conn.close()


def calculate_expected_monthly_instalment(tae, repayment_term, requested_capital):
    # Calculation logic
    annual_interest_rate = tae / 100
    monthly_interest_rate = annual_interest_rate / 12
    num_payments = repayment_term * 12

    monthly_instalment = (
        requested_capital
        * monthly_interest_rate
        / (1 - (1 + monthly_interest_rate) ** (-num_payments))
    )
    total = monthly_instalment * num_payments
    return monthly_instalment, total


def test_mortgage_sim(client):

    requested_capital = 25000
    test_dni = add_test_client_with_requested_capital(client, requested_capital)

    # Define a test client data
    test_data = {"tae": 2.5, "repayment_term": 20}

    # Send a POST request to the '/client/mortgage/<dni>' endpoint
    response = client.post(
        f"/client/mortgage_sim/{test_dni}",
        data=json.dumps(test_data),
        content_type="application/json",
    )

    delete_test_client(test_dni)

    # Parse the JSON response body into a dictionary
    response_json = response.get_json()

    # Check if the response is as expected
    assert response.status_code == 200
    assert "monthly_instalment" in response_json
    assert "total" in response_json

    # Assertion for the calculated monthly instalment
    expected_monthly_instalment, total = calculate_expected_monthly_instalment(
        test_data["tae"], test_data["repayment_term"], requested_capital
    )
    assert round(response_json["monthly_instalment"], 2) == round(
        expected_monthly_instalment, 2
    )
    assert round(response_json["total"], 2) == round(total, 2)


def test_mortgage_sim_empty_request_body(client):

    requested_capital = 25000
    test_dni = add_test_client_with_requested_capital(client, requested_capital)

    # Define a test client data
    test_data = {}

    # Send a POST request to the '/client/mortgage/<dni>' endpoint
    response = client.post(
        f"/client/mortgage_sim/{test_dni}",
        data=json.dumps(test_data),
        content_type="application/json",
    )

    delete_test_client(test_dni)

    # Parse the JSON response body into a dictionary
    response_json = response.get_json()

    # Check if the response is as expected
    assert response.status_code == 400
    assert b"Empty request body" in response.data


def test_mortgage_sim_invalid_tae(client):

    requested_capital = 25000
    test_dni = add_test_client_with_requested_capital(client, requested_capital)

    # Define a test client data
    test_data = {"tae": 250, "repayment_term": 20}

    # Send a POST request to the '/client/mortgage/<dni>' endpoint
    response = client.post(
        f"/client/mortgage_sim/{test_dni}",
        data=json.dumps(test_data),
        content_type="application/json",
    )

    delete_test_client(test_dni)

    # Parse the JSON response body into a dictionary
    response_json = response.get_json()

    # Check if the response is as expected
    assert response.status_code == 400
    assert b"tae must be a positive number and less than 100" in response.data
