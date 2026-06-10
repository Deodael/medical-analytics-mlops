![MLOps CI Status](https://github.com/Deodael/medical-analytics-mlops/actions/workflows/test.yml/badge.svg)

## 📐 System Architecture & MLOps Pipeline

This repository implements a production-grade, containerized MLOps pipeline designed with a separation of concerns between model training, API delivery, and automated verification.

### 🏗️ Core Architecture Components

1. **Training Pipeline (`train_model.py`)**
   * Responsible for ingestion, data preprocessing, and model training.
   * Serializes the final trained model into a production-ready binary format (`src/medical_model.pkl`) using `pickle`.

2. **Prediction Service (`src/main.py`)**
   * Built on **FastAPI** for high-performance, asynchronous REST API serving.
   * Utilizes **Pydantic** data structures to strictly validate incoming biometrics and patient payloads before executing inference.

3. **Automated Verification (`tests/test_api.py`)**
   * Configured with **Pytest** to run deterministic component validation.
   * Verifies API response codes (200 OK, 422 Unprocessable Entity), schema integrity, and model inference accuracy.

4. **Continuous Integration (`.github/workflows/test.yml`)**
   * Automated orchestration via **GitHub Actions** triggered on every `push` or `pull_request` to `main`.
   * Provisions an isolated `ubuntu-latest` runner, configures a cached Python 3.11 environment, installs dependencies, and runs the test suite to guarantee zero-downtime stability.
5. **Interactive Presentation Layer (`src/app.py`)**
   * Built on **Streamlit** to provide an intuitive, web-based graphical user interface for medical staff.
   * Eliminates the need for local execution by serving input elements (biometric sliders, dropdowns) directly via a managed cloud runtime.

## 🌐 Production Infrastructure & Deployment

The entire system operates as a fully decentralized, decoupled microservice cluster in the cloud, completely independent of local hardware constraints:

* **Frontend Client (Streamlit Community Cloud):** Hosts the presentation layer. It manages client-side states, captures real-time biometric indicators, and handles asynchronous HTTPS networking to ship data payloads across the web.
* **API Gateway & Inference Container (Railway):** Automatically intercepts pushes to `main`, compiles your isolated `src/Dockerfile.backend` image, and spins up a public container. It processes inbound JSON metrics through your serialized `medical_model.pkl` pipeline to deliver prediction results in milliseconds.

🚀 **[Access the Live Interactive App](https://deodael-medical-analytics-mlops-srcapp-u4m797.streamlit.app/)**
🐳 **[Explore the Live FastAPI Gateway](https://medical-analytics-mlops-production.up.railway.app/docs)** *(Append `/docs` or `/redoc` to view your interactive Swagger OpenAPI schema!)*
