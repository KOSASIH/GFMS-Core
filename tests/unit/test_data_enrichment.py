import pytest
from unittest.mock import patch, Mock
from fastapi import HTTPException
from src.services.data_enrichment_service import DataEnrichmentService

@pytest.fixture
def data_enrichment_service():
    """Fixture to create an instance of DataEnrichmentService."""
    return DataEnrichmentService()

def test_enrich_user_data_success(data_enrichment_service):
    """Test successful enrichment of user data."""
    user_id = "12345"
    mock_response = {"id": user_id, "name": "John Doe", "email": "john@example.com"}

    with patch("requests.get") as mock_get:
        mock_get.return_value = Mock(status_code=200, json=lambda: mock_response)
        
        result = data_enrichment_service.enrich_user_data(user_id)
        assert result == mock_response
        mock_get.assert_called_once_with("https://api.example.com/userinfo?id=12345")

def test_enrich_user_data_http_error(data_enrichment_service):
    """Test handling of HTTP error when enriching user data."""
    user_id = "12345"

    with patch("requests.get") as mock_get:
        mock_get.return_value = Mock(status_code=404)
        
        with pytest.raises(HTTPException) as excinfo:
            data_enrichment_service.enrich_user_data(user_id)
        
        assert excinfo.value.status_code == 404
        assert "Failed to fetch user data" in str(excinfo.value.detail)

def test_enrich_user_data_exception(data_enrichment_service):
    """Test handling of general exceptions when enriching user data."""
    user_id = "12345"

    with patch("requests.get") as mock_get:
        mock_get.side_effect = Exception("Network error")
        
        with pytest.raises(HTTPException) as excinfo:
            data_enrichment_service.enrich_user_data(user_id)
        
        assert excinfo.value.status_code == 500
        assert "Internal Server Error" in str(excinfo.value.detail)

def test_enrich_transaction_data_success(data_enrichment_service):
    """Test successful enrichment of transaction data."""
    transaction_id = "67890"
    mock_response = {"id": transaction_id, "amount": 100, "status": "completed"}

    with patch("requests.get") as mock_get:
        mock_get.return_value = Mock(status_code=200, json=lambda: mock_response)
        
        result = data_enrichment_service.enrich_transaction_data(transaction_id)
        assert result == mock_response
        mock_get.assert_called_once_with("https://api.example.com/transaction?id=67890")

def test_enrich_transaction_data_http_error(data_enrichment_service):
    """Test handling of HTTP error when enriching transaction data."""
    transaction_id = "67890"

    with patch("requests.get") as mock_get:
        mock_get.return_value = Mock(status_code=404)
        
        with pytest.raises(HTTPException) as excinfo:
            data_enrichment_service.enrich_transaction_data(transaction_id)
        
        assert excinfo.value.status_code == 404
        assert "Failed to fetch transaction data" in str(excinfo.value.detail)

def test_enrich_transaction_data_exception(data_enrichment_service):
    """Test handling of general exceptions when enriching transaction data."""
    transaction_id = "67890"

    with patch("requests.get") as mock_get:
        mock_get.side_effect = Exception("Network error")
        
        with pytest.raises(HTTPException) as excinfo:
            data_enrichment_service.enrich_transaction_data(transaction_id)
        
        assert excinfo.value.status_code == 500
        assert "Internal Server Error" in str(excinfo.value.detail)
