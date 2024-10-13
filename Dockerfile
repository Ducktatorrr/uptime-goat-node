# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Install gcc and libpq-dev for aiohttp
RUN apt-get update && apt-get install -y gcc python3-dev libpq-dev

# Set the working directory in the container
WORKDIR /usr/src/app


# Copy the current directory contents into the container
COPY . .


# Install any needed packages
RUN pip install --no-cache-dir -r requirements.txt

# Make the Python script executable
RUN chmod +x goat-report.py

# Define the command to run the script
CMD ["python", "./goat-report.py"]