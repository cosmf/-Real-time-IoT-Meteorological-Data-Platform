# import paho.mqtt.client as mqtt
# from influxdb_client import InfluxDBClient, Point, WriteOptions
# from datetime import datetime
# import json
# import logging as log
# from os import getenv
# from re import match

# # Configuration
# MQTT_BROKER = getenv("BROKER", "localhost")
# MQTT_PORT = int(getenv("MQTT_PORT", 1883))
# MQTT_TOPIC = getenv("MQTT_TOPIC", "#")

# INFLUXDB_URL = getenv("INFLUXDB_URL", "http://localhost:8086")
# INFLUXDB_TOKEN = getenv("INFLUXDB_TOKEN", "USKG8tIr0yrUXY3pjOoLUCJgAqplmfYnzO2VEinWrID3KtIe6pz5JTY-PRdoQVZ4HxbyyhkOcqvWEMVjvx74lg==")
# INFLUXDB_ORG = getenv("INFLUXDB_ORG", "organization")
# INFLUXDB_BUCKET = getenv("INFLUXDB_BUCKET", "iot_data")

# DEBUG_DATA_FLOW = getenv("DEBUG_DATA_FLOW", "true").lower() == "true"

# # Logging Configuration
# log_level = log.DEBUG if DEBUG_DATA_FLOW else log.INFO
# log.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')

# # InfluxDB Client Setup
# influx_client = InfluxDBClient(
#     url=INFLUXDB_URL,
#     token=INFLUXDB_TOKEN,
#     org=INFLUXDB_ORG
# )
# write_api = influx_client.write_api(write_options=WriteOptions(batch_size=1))

# # MQTT Callbacks
# def on_connect(client, userdata, flags, rc):
#     if rc == 0:
#         log.info("Successfully connected to MQTT broker")
#     else:
#         log.error(f"Failed to connect to MQTT broker, return code {rc}")

# def on_disconnect(client, userdata, rc):
#     log.warning("Disconnected from MQTT broker")

# def on_subscribe(client, userdata, mid, granted_qos):
#     log.info(f"Subscribed to topic {MQTT_TOPIC} with QoS {granted_qos}")

# # def on_message(client, args, msg):
# #     if not match(r'^[^/]+/[^/]+$', msg.topic):
# #         log.warning(f"Ignoring message with invalid topic format: {msg.topic}")
# #         return

# #     log.info(f"Received message on topic: {msg.topic}")

# #     location, station = msg.topic.split('/')
# #     try:
# #         data = json.loads(msg.payload.decode())
# #     except json.JSONDecodeError as e:
# #         log.error(f"Failed to decode JSON payload: {e}")
# #         return

# #     try:
# #         tstamp = datetime.strptime(data.get('timestamp', ''), '%Y-%m-%dT%H:%M:%S%z')
# #         log.info(f"Parsed timestamp: {tstamp}")
# #     except Exception:
# #         tstamp = datetime.now()
# #         log.info("Using current timestamp")

# #     json_data = []

# #     for key, val in data.items():
# #         if not isinstance(val, (int, float)):
# #             log.warning(f"Ignoring non-numeric data: {key} = {val}")
# #             continue

# #         point = {
# #             'measurement': f'{station}.{key}',
# #             'tags': {
# #                 'location': location,
# #                 'station': station
# #             },
# #             'time': tstamp.strftime('%Y-%m-%dT%H:%M:%S%z'),
# #             'fields': {
# #                 'value': float(val)
# #             }
# #         }
# #         json_data.append(point)
# #         log.info(f"Prepared data point: {point}")

# #     if json_data:
# #         try:
# #             write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=json_data)
# #             log.info(f"Successfully written {len(json_data)} points to InfluxDB")
# #         except Exception as e:
# #             log.error(f"Failed to write to InfluxDB: {e}")

# def on_message(client, args, msg):
#     if not match(r'^[^/]+/[^/]+$', msg.topic):
#         log.warning(f"Ignoring message with invalid topic format: {msg.topic}")
#         return

#     log.info(f"Received message on topic: {msg.topic}")

#     location, station = msg.topic.split('/')
#     try:
#         data = json.loads(msg.payload.decode())
#     except json.JSONDecodeError as e:
#         log.error(f"Failed to decode JSON payload: {e}")
#         return

#     # Extract tags, time, and fields
#     tags = data.get('tags', {})
#     timestamp = data.get('time')
#     fields = data.get('fields', {})

#     # Validate timestamp
#     try:
#         tstamp = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S%z') if timestamp else datetime.now()
#         log.info(f"Parsed timestamp: {tstamp}")
#     except Exception as e:
#         log.error(f"Invalid timestamp: {e}")
#         return

#     json_data = []

#     # Iterate over fields for numeric data
#     for key, val in fields.items():
#         if not isinstance(val, (int, float)):
#             log.warning(f"Ignoring non-numeric field: {key} = {val}")
#             continue

#         point = {
#             'measurement': f'{station}.{key}',
#             'tags': {
#                 'location': location,
#                 'station': station,
#                 **tags  # Merge additional tags
#             },
#             'time': tstamp.strftime('%Y-%m-%dT%H:%M:%S%z'),
#             'fields': {
#                 'value': float(val)
#             }
#         }
#         json_data.append(point)
#         log.info(f"Prepared data point: {point}")

#     # Write data points to InfluxDB
#     if json_data:
#         try:
#             write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=json_data)
#             log.info(f"Successfully written {len(json_data)} points to InfluxDB")
#         except Exception as e:
#             log.error(f"Failed to write to InfluxDB: {e}")

# # Main Function
# def main():
#     mqtt_client = mqtt.Client()
#     mqtt_client.on_connect = on_connect
#     mqtt_client.on_disconnect = on_disconnect
#     mqtt_client.on_subscribe = on_subscribe
#     mqtt_client.on_message = on_message

#     try:
#         mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
#         mqtt_client.subscribe(MQTT_TOPIC)
#         log.info("MQTT client is running")
#         mqtt_client.loop_forever()
#     except KeyboardInterrupt:
#         log.info("Shutting down MQTT client")
#         mqtt_client.disconnect()
#         influx_client.close()

# if __name__ == "__main__":
#     main()
# import os
# import json
# import paho.mqtt.client as mqtt
# from influxdb_client import InfluxDBClient, Point
# from influxdb_client.client.write_api import SYNCHRONOUS

# # Environment variables for configuration
# BROKER_HOST = os.getenv("BROKER_HOST", "localhost")
# BROKER_PORT = int(os.getenv("BROKER_PORT", 1883))
# INFLUXDB_URL = os.getenv("INFLUXDB_URL", "http://localhost:8086")
# INFLUXDB_TOKEN = os.getenv("INFLUXDB_TOKEN", "hfJPXw-ABRWtfSs9gC81N9Jw2bFlw0GOtfc8Ou-k8AjB5aXTMWPx1AWsFx6e40e-CYtVFDP7eoAAo5LAbGHFVg==")
# INFLUXDB_ORG = os.getenv("INFLUXDB_ORG", "my-org")
# INFLUXDB_BUCKET = os.getenv("INFLUXDB_BUCKET", "my-bucket")
# DEBUG = True

# def log_debug(message):
#     if DEBUG:
#         print(message)

# # MQTT callback functions
# def on_connect(client, userdata, flags, rc):
#     log_debug("Connected to MQTT Broker with result code " + str(rc))
#     client.subscribe("#")

# def on_message(client, userdata, message):
#     try:
#         payload = json.loads(message.payload)  # This ensures payload is a valid JSON object
#         print(f"Received message on topic [{message.topic}] with payload: {payload}")

#         # Now you can safely access keys
#         bat = payload.get("BAT")  # Safe access with .get() to avoid KeyError
#         temp = payload.get("TEMP")
#         humid = payload.get("HUMID")
#         timestamp = payload.get("timestamp")
#         points = []

#         for key, value in payload.items():
#             if key == "timestamp" or not isinstance(value, (int, float)):
#                 continue

#             point = Point(message.topic.replace("/", ".")) \
#                 .field(key, value)

#             if timestamp:
#                 point.time(timestamp)

#             points.append(point)
        
#         # Process data further
#     except json.JSONDecodeError:
#         print("Failed to decode JSON payload")
#     except Exception as e:
#         print(f"Error processing message: {e}")


# if __name__ == "__main__":
#     # Initialize InfluxDB client
#     influx_client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)

#     # Initialize MQTT client
#     mqtt_client = mqtt.Client()
#     mqtt_client.on_connect = on_connect
#     mqtt_client.on_message = on_message

#     # Connect to MQTT broker
#     mqtt_client.connect(BROKER_HOST, BROKER_PORT, 60)

#     mqtt_client.subscribe("#")

#     # Blocking loop to process network traffic and dispatch callbacks
#     mqtt_client.loop_forever()

import os
import json
import logging as log
from datetime import datetime
from re import match
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import paho.mqtt.client as mqtt

# Environment variables for configuration
BROKER_HOST = os.getenv("BROKER_HOST", "localhost")
BROKER_PORT = int(os.getenv("BROKER_PORT", 1883))
INFLUXDB_URL = os.getenv("INFLUXDB_URL", "http://localhost:8086")
INFLUXDB_TOKEN = os.getenv("INFLUXDB_TOKEN", "5UOXmCh_Es_Qnfsaw-zYhtjuOwRykjTpr2Vdf90p_jA26bco7rt3VRYgbz4V-MDW82YLK-9SrW_yImbhNrVLWg==")
INFLUXDB_ORG = os.getenv("INFLUXDB_ORG", "vpt.srl")
INFLUXDB_BUCKET = os.getenv("INFLUXDB_BUCKET", "iot_data")
DEBUG = os.getenv("DEBUG_DATA_FLOW", "false").lower() == "true"

# Logging configuration
log_level = log.DEBUG if DEBUG else log.INFO
log.basicConfig(format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=log_level)

# def _on_message(client, write_api, msg):
#     log.debug(f"Processing message: {msg.payload}")
#     if not match(r'^[^/]+/[^/]+$', msg.topic):
#         log.warning(f"Ignored message with invalid topic format: {msg.topic}")
#         return

#     log.info(f"Received a message by topic [{msg.topic}]")
#     try:
#         # Extract location and station from topic
#         location, station = msg.topic.split('/')
#     except ValueError:
#         log.error(f"Failed to split topic into location and station: {msg.topic}")
#         return

#     try:
#         # Decode JSON payload
#         data = json.loads(msg.payload)
#         log.debug(f"Decoded payload: {data}")
#     except json.JSONDecodeError as e:
#         log.error(f"Failed to decode JSON payload: {e}")
#         return

#     # Extract tags, timestamp, and fields
#     tags = data.get("tags", {})
#     timestamp = data.get("time")
#     fields = data.get("fields", {})

#     # Validate timestamp
#     try:
#         tstamp = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S%z') if timestamp else datetime.now()
#         log.info(f"Data timestamp is: {tstamp}")
#     except Exception as e:
#         log.error(f"Invalid timestamp: {e}")
#         return

#     # Process only numeric fields
#     for key, val in fields.items():
#         if not isinstance(val, (int, float)):
#             log.warning(f"Ignoring non-numeric field: {key} = {val}")
#             continue

#         # Create a point for InfluxDB
#         point = Point(f"{station}.{key}") \
#             .tag("location", location) \
#             .tag("station", station) \
#             .tag("extra_tags", json.dumps(tags)) \
#             .field("value", float(val)) \
#             .time(tstamp)

#         # Write the point to InfluxDB
#         try:
#             write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)
#             log.info(f"Written data point: {location}.{station}.{key} = {val}")
#         except Exception as e:
#             log.error(f"Failed to write to InfluxDB: {e}")

def _on_message(client, write_api, msg):
    log.debug(f"Processing message: {msg.payload}")

    # Validate the topic format
    if not match(r'^[^/]+/[^/]+$', msg.topic):
        log.warning(f"Ignored message with invalid topic format: {msg.topic}")
        return

    log.info(f"Received a message by topic [{msg.topic}]")

    try:
        # Extract location and station from topic
        location, station = msg.topic.split('/')
    except ValueError:
        log.error(f"Failed to split topic into location and station: {msg.topic}")
        return

    try:
        # Decode JSON payload
        data = json.loads(msg.payload)
        log.debug(f"Decoded payload: {data}")
    except json.JSONDecodeError as e:
        log.error(f"Failed to decode JSON payload: {e}")
        return

    # Extract timestamp and fields
    timestamp = data.get("time")
    fields = data.get("fields", {})

    # Validate and parse timestamp
    try:
        tstamp = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S%z') if timestamp else datetime.now()
        log.info(f"Data timestamp is: {tstamp}")
    except Exception as e:
        log.error(f"Invalid timestamp: {e}")
        return

    # Process numeric fields and write to InfluxDB
    for key, val in fields.items():
        if not isinstance(val, (int, float)):
            log.warning(f"Ignoring non-numeric field: {key} = {val}")
            continue

        # Create InfluxDB point with key as _measurement
        point = Point(key) \
            .tag("location", location) \
            .tag("station", station) \
            .field("value", float(val)) \
            .time(tstamp)

        # Write the point to InfluxDB
        try:
            write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)
            log.info(f"Written data point: {key} = {val} for {location}/{station}")
        except Exception as e:
            log.error(f"Failed to write to InfluxDB: {e}")


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        log.info("Connected to MQTT Broker")
        client.subscribe("#")
    else:
        log.error(f"Failed to connect to MQTT Broker, return code {rc}")


def main():
    # Initialize InfluxDB client
    db_client = InfluxDBClient(
        url=INFLUXDB_URL,
        token=INFLUXDB_TOKEN,
        org=INFLUXDB_ORG
    )
    write_api = db_client.write_api(write_options=SYNCHRONOUS)

    # Initialize MQTT client
    mqtt_client = mqtt.Client(userdata=write_api)
    mqtt_client.on_message = lambda client, userdata, msg: _on_message(client, write_api, msg)
    mqtt_client.on_connect = on_connect

    try:
        mqtt_client.connect(BROKER_HOST, BROKER_PORT)
        log.info("MQTT client connected and running")
        mqtt_client.loop_forever()
    except KeyboardInterrupt:
        log.info("Shutting down MQTT client and InfluxDB client")
        mqtt_client.disconnect()
        db_client.close()


if __name__ == "__main__":
    main()