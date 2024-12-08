# Base Image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install system dependencies for OpenCV
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt into the container
COPY requirements.txt /app/

# Install dependencies
RUN pip install -r requirements.txt

# Copy application files
COPY app/ /app/

# Expose port 5001
EXPOSE 5001

# Start the server
CMD ["python", "main.py"]
