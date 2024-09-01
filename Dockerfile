# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
# WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install pytorch
# RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# # Command to run multiple scripts in parallel
# CMD python 02-asset-search/main.py & \
#     python 03-rag/main.py & \
#     python 05-caption-api/main.py & \
#     wait