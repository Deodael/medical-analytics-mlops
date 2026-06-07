import os
import joblib
from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from pydantic import BaseModel

app = FastAPI(
    title="Medical Analytics Production Engine",
    docs_url=None,   # Disable default setup to avoid the CDN hang
    redoc_url=None
)

class MedicalMetrics(BaseModel):
    age: int
    bmi: float
    cholesterol: int

MODEL_PATH = os.path.join(os.path.dirname(__file__), "medical_model.pkl")

if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
else:
    model = None

# Custom documentation routes using Cloudflare (cdnjs) mirrors
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/5.9.0/swagger-ui-bundle.js",
        swagger_css_url="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/5.9.0/swagger-ui.css"
    )

@app.get("/redoc", include_in_schema=False)
async def custom_redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="https://cdnjs.cloudflare.com/ajax/libs/redoc/2.1.3/redoc.standalone.js"
    )

@app.post("/predict")
def predict_health_risk(metrics: MedicalMetrics):
    if model is None:
        return {"error": "Machine learning model binary artifact was not found."}
    
    features = [[metrics.age, metrics.bmi, metrics.cholesterol]]
    
    prediction_code = int(model.predict(features)[0])
    probabilities = model.predict_proba(features)[0]
    confidence_score = round(float(probabilities[prediction_code]) * 100, 2)
    
    output_labels = {0: "Low Risk Profile", 1: "High Risk Profile"}
    
    return {
        "input_features": {
            "age": metrics.age,
            "bmi": metrics.bmi,
            "cholesterol": metrics.cholesterol
        },
        "prediction_output": output_labels[prediction_code],
        "inference_confidence_percentage": confidence_score
    }
