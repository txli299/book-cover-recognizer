# Base Image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy application files
COPY app/ /app/

# Install dependencies
RUN pip install -r requirements.txt

# Expose port 5000
EXPOSE 5000

# Start the server
CMD ["python", "main.py"]
