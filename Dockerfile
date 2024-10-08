# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container
COPY . .

# Install any needed packages and cron
RUN apt-get update && apt-get install -y cron && pip install --no-cache-dir -r requirements.txt

# Add a cron job
RUN echo "* * * * * python /usr/src/app/goat-report.py >> /var/log/goat-report.log 2>&1" > /etc/cron.d/goat-report

# Apply cron job settings and make it executable
RUN chmod 0644 /etc/cron.d/goat-report && touch /var/log/goat-report.log

# Start cron in the foreground so the container keeps running
CMD cron -f
