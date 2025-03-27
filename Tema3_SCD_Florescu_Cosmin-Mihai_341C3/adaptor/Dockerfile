# Use the official Python image from the Docker Hub
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Add the application files to the /server directory
ADD adaptor.py start_adaptor.sh /server/

# Change to the /server directory
WORKDIR /server

# Make the script executable
RUN chmod +x start_adaptor.sh

# Run the application
CMD ["./start_adaptor.sh"]
