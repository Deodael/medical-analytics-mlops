from fastapi import FastAPI
import pandas as pd

app = FastAPI(
    title="Medical Analytics Production Engine",
    description="Enterprise MLOps pipeline serving health analytics forecasts.",
    version="1.0.0"
)

@app.get("/")
def health_check():
    """Production health check endpoint."""
    return {
        "status": "online",
        "framework": "FastAPI",
        "environment": "Production"
    }

@app.post("/predict")
def predict(age: int, bmi: float, cholesterol: int):
    """Predictive pipeline endpoint taking patient feature vectors."""
    # Process inputs as a structured DataFrame
    input_data = pd.DataFrame([{"age": age, "bmi": bmi, "cholesterol": cholesterol}])
    
    # Mathematical scoring logic simulating production inference
    risk_score = float((age * 0.4) + (bmi * 0.5) + (cholesterol * 0.1))
    prediction = "High Risk" if risk_score > 45 else "Low Risk"
    
    return {
        "input_features": {"age": age, "bmi": bmi, "cholesterol": cholesterol},
        "risk_score_metric": round(risk_score, 2),
        "prediction_output": prediction
    }
