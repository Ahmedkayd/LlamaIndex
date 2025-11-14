# Use official Python base image
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    file \
    && rm -rf /var/lib/apt/lists/*

COPY requirements/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
EXPOSE 8504
CMD ["streamlit", "run", "app/app.py", "--server.port=8504", "--server.address=0.0.0.0"]
