# Use an official lightweight Python runtime as a base image
FROM python:3.11-slim

# Set the operational directory inside the container box
WORKDIR /app

# Copy dependency configs first to leverage Docker's caching layers
COPY requirements.txt .

# Install the exact software dependencies without saving temporary cache files
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your local source repository code into the container
COPY . .

# Expose network port 8000 for incoming web requests
EXPOSE 8000

# Specify the command to execute your production application web server on startup
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
