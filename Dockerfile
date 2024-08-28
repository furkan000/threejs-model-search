# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements.txt into the container
COPY requirements.txt .

# Install common dependencies
RUN pip install --no-cache-dir -r requirements.txt
    