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
