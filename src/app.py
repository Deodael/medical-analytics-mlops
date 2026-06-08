import os
import streamlit as st
import requests

# 1. Dynamic API URL Resolution for Cloud/Local Environments
# Fall back to localhost if no production URL environment variable is supplied
BASE_URL = os.getenv("BACKEND_API_URL", "https://medical-analytics-mlops-production.up.railway.app")
BACKEND_URL = f"{BASE_URL}/predict"

# 2. Set up clean page configuration
st.set_page_config(
    page_title="Medical Analytics Portal",
    page_icon="🏥",
    layout="centered"
)

st.title("🏥 Medical Analytics & Risk Prediction Portal")
st.markdown("""
This interactive interface communicates directly with a containerized **FastAPI** backend 
to serve machine learning predictions using verified patient metrics.
""")
st.write("---")

st.sidebar.header("📋 Patient Biometrics Input")

# 3. Build interactive UI entry forms
age = st.sidebar.slider("Age", min_value=1, max_value=100, value=45)
bmi = st.sidebar.slider("Body Mass Index (BMI)", min_value=10.0, max_value=50.0, value=24.5, step=0.1)
blood_pressure = st.sidebar.slider("Systolic Blood Pressure", min_value=80, max_value=200, value=120)
cholesterol = st.sidebar.selectbox("Cholesterol Level", options=["Normal", "High", "Critical"])

# Convert text dropdown choices to numeric categories for the model payload
chol_mapping = {"Normal": 0, "High": 1, "Critical": 2}

# 4. Package the inputs into a clean structured dictionary payload
payload = {
    "age": age,
    "bmi": bmi,
    "blood_pressure": blood_pressure,
    "cholesterol": chol_mapping[cholesterol]
}

st.subheader("🔍 Real-time Inference Analysis")

# 5. Create an execution trigger button
if st.button("Run Diagnostic Prediction", type="primary"):
    with st.spinner("Communicating with FastAPI prediction service..."):
        try:
            # Send HTTP POST request to your running backend API
            response = requests.post(BACKEND_URL, json=payload, timeout=5)
            
            if response.status_code == 200:
                result = response.json()
                prediction = result.get("prediction", 0)
                probability = result.get("probability", 0.0)
                
                # Present the analysis dynamically based on the model return value
                st.success("✅ Analysis completed successfully!")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(label="Model Risk Output Classification", value=f"Category {prediction}")
                with col2:
                    st.metric(label="Calculated Statistical Probability", value=f"{probability * 100:.1f}%")
                
                if probability > 0.5:
                    st.warning("⚠️ **Notice:** The model identifies elevated risk markers. Clinical evaluation advised.")
                else:
                    st.info("💚 **Notice:** Metrics fall within baseline statistical regularities.")
            else:
                st.error(f"❌ Backend API returned an error code: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            st.error("❌ Unable to connect to the FastAPI backend. Make sure your backend server is running on port 8000!")

st.write("---")
st.caption("Developed as part of the Medical Analytics MLOps Infrastructure Framework.")
