FROM python:3.11-slim

# Install dependencies
RUN apt-get update && apt-get install -y gcc python3-dev libpq-dev

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container
COPY . .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Make the Python scripts and shell script executable
RUN chmod +x goat_report.py endpoint_agent.py start.sh

# Ensure the endpoints.json file is available in the container
COPY endpoints.json /usr/src/app/endpoints.json

# Set default environment variables
ENV ENDPOINTS_URL=https://raw.githubusercontent.com/1rabbit/goat_servers/refs/heads/main/uptime_endpoints


# Start the container with the shell script
CMD ["/bin/bash", "/usr/src/app/start.sh"]
