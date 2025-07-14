# Use official Python 3 image
FROM python:3.12-slim

# Set working directory
WORKDIR /flask_app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY flask_app/ .

# Expose port
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]
