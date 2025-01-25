import pytest
import requests
from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.services.data_enrichment_service import DataEnrichmentService

# Create a FastAPI app instance for testing
app = FastAPI()

# Create an instance of the DataEnrichmentService
data_enrichment_service = DataEnrichmentService()

@app.get("/test/enrich_user/{user_id}")
def enrich_user(user_id: str):
    return data_enrichment_service.enrich_user_data(user_id)

@app.get("/test/enrich_transaction/{transaction_id}")
def enrich_transaction(transaction_id: str):
    return data_enrichment_service.enrich_transaction_data(transaction_id)

# Create a test client
client = TestClient(app)

def test_enrich_user_data_integration(mocker):
    """Integration test for enriching user data."""
    user_id = "12345"
    mock_response = {"id": user_id, "name": "John Doe", "email": "john@example.com"}

    # Mock the external API call
    mocker.patch("requests.get", return_value=Mock(status_code=200, json=lambda: mock_response))

    response = client.get(f"/test/enrich_user/{user_id}")
    assert response.status_code == 200
    assert response.json() == mock_response

def test_enrich_user_data_http_error(mocker):
    """Integration test for handling HTTP error when enriching user data."""
    user_id = "12345"

    # Mock the external API call to return a 404 error
    mocker.patch("requests.get", return_value=Mock(status_code=404))

    response = client.get(f"/test/enrich_user/{user_id}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Failed to fetch user data"}

def test_enrich_transaction_data_integration(mocker):
    """Integration test for enriching transaction data."""
    transaction_id = "67890"
    mock_response = {"id": transaction_id, "amount": 100, "status": "completed"}

    # Mock the external API call
    mocker.patch("requests.get", return_value=Mock(status_code=200, json=lambda: mock_response))

    response = client.get(f"/test/enrich_transaction/{transaction_id}")
    assert response.status_code == 200
    assert response.json() == mock_response

def test_enrich_transaction_data_http_error(mocker):
    """Integration test for handling HTTP error when enriching transaction data."""
    transaction_id = "67890"

    # Mock the external API call to return a 404 error
    mocker.patch("requests.get", return_value=Mock(status_code=404))

    response = client.get(f"/test/enrich_transaction/{transaction_id}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Failed to fetch transaction data"}
