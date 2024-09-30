# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container
COPY . .

# Install any needed packages
RUN pip install --no-cache-dir requests

# Make the Python script executable
RUN chmod +x goat-report.py

# Define the command to run the script
CMD ["python", "./goat-report.py"]