from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_predict_low_risk():
    # Send a known low-risk baseline health profile
    payload = {"age": 22, "bmi": 21.0, "cholesterol": 160}
    response = client.post("/predict", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert "prediction_output" in data
    assert data["prediction_output"] == "Low Risk Profile"
    assert "inference_confidence_percentage" in data
    assert data["inference_confidence_percentage"] >= 0.0

def test_predict_high_risk():
    # Send a known high-risk baseline health profile
    payload = {"age": 65, "bmi": 34.2, "cholesterol": 260}
    response = client.post("/predict", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert "prediction_output" in data
    assert data["prediction_output"] == "High Risk Profile"
    assert "inference_confidence_percentage" in data

def test_invalid_data_types():
    # Test the FastAPI automatic Pydantic validation guardrails
    payload = {"age": "not-a-number", "bmi": 24.5, "cholesterol": 180}
    response = client.post("/predict", json=payload)
    assert response.status_code == 422  # Unprocessable Entity
