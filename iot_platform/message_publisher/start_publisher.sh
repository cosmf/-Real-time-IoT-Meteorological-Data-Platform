#!/bin/bash

# Wait for the MQTT broker to be ready
echo "Waiting for MQTT broker to be available..."
while ! nc -z localhost 1883; do
    sleep 1
done
echo "MQTT broker is available."

# Start the Python message publisher
echo "Starting the MQTT message publisher..."
python message_publisher.py
