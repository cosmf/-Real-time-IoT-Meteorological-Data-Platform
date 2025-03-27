import paho.mqtt.client as mqtt
import json
import time
import random

# MQTT Broker Configuration
BROKER = "localhost"  # IP or hostname of the MQTT broker
PORT = 1883

# Generate payload matching the required JSON structure
def generate_payload(location, station):
    # Generate a simulated payload with tags, time, and fields
    return json.dumps({
        "tags": {
            "location": location,  # Tag for location
            "station": station     # Tag for station
        },
        "time": time.strftime("%Y-%m-%dT%H:%M:%S%z"),  # Current timestamp with timezone
        "fields": {
            "BAT": random.randint(50, 100),  # Simulated battery level
            "HUMID": random.randint(30, 70),  # Simulated humidity level
            "TEMP": round(random.uniform(20.0, 30.0), 2)  # Simulated temperature
        }
    })

# Publish a message to a specific topic
def publish_message(client, topic, payload):
    client.publish(topic, payload)  # Publish the payload to the MQTT broker
    print(f"Published: {payload} to topic: {topic}")

# Initialize the MQTT client
client = mqtt.Client()
client.connect(BROKER, PORT)

# Publish messages in a loop
try:
    location = "UPB"  # Location tag value
    station = "vama_veche"  # Station tag value

    while True:
        # Generate the payload
        payload = generate_payload(location, station)
        topic = f"{location}/{station}"  # Construct the topic dynamically
        # Publish the message
        publish_message(client, topic, payload)
        time.sleep(5)  # Wait 5 seconds before publishing the next message
except KeyboardInterrupt:
    print("Simulation stopped.")
    client.disconnect()
