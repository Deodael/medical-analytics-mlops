from fastapi.testclient import TestClient
from src.main import app

# Initialize a virtual client to test endpoints without spinning up a live server
client = TestClient(app)

def test_health_check_endpoint():
    """Ensure the root health status indicator responds successfully."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "status": "online",
        "framework": "FastAPI",
        "environment": "Production"
    }

def test_prediction_pipeline_logic():
    """Verify that incoming feature arrays yield accurate scoring matrix outputs."""
    response = client.post(
        "/predict",
        params={"age": 45, "bmi": 28.5, "cholesterol": 190}
    )
    assert response.status_code == 200
    data = response.json()
    assert "prediction_output" in data
    # Matrix math validation check: (45 * 0.4) + (28.5 * 0.5) + (190 * 0.1) = 51.25
    assert data["risk_score_metric"] == 51.25
    assert data["prediction_output"] == "High Risk"
