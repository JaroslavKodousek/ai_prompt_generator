# Alternative deployment option: Docker container
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for pytesseract (if needed)
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8000

# Run API server
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
