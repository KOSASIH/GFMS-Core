import pytest
from fastapi.testclient import TestClient
from src.ai_service import app  # Adjust the import based on your project structure
import joblib
import numpy as np

# Mock the model loading
class MockModel:
    def predict(self, features):
        # Mock prediction logic (for example, return the sum of features)
        return [np.sum(features)]

# Replace the actual model with the mock model
def mock_load_model():
    return MockModel()

# Test client for FastAPI
client = TestClient(app)

# Fixture to replace the model loading in the AI service
@pytest.fixture(autouse=True)
def override_model_loading(monkeypatch):
    monkeypatch.setattr("src.ai_service.joblib.load", mock_load_model)

def test_get_insight():
    # Test the AI service prediction endpoint
    response = client.post("/ai/predict", json={"features": [1.0, 2.0, 3.0]})
    assert response.status_code == 200
    assert response.json() == {"prediction": [6.0]}  # Expecting the sum of features

def test_get_insight_invalid_input():
    # Test the AI service prediction endpoint with invalid input
    response = client.post("/ai/predict", json={"features": "invalid_input"})
    assert response.status_code == 422  # Unprocessable Entity

def test_get_insight_empty_features():
    # Test the AI service prediction endpoint with empty features
    response = client.post("/ai/predict", json={"features": []})
    assert response.status_code == 422  # Unprocessable Entity

def test_get_insight_large_input():
    # Test the AI service prediction endpoint with a large input
    response = client.post("/ai/predict", json={"features": [1.0] * 1000})
    assert response.status_code == 200
    assert response.json() == {"prediction": [1000.0]}  # Expecting the sum of features
