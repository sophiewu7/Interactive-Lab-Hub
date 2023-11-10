import base64
import json
import paho.mqtt.client as mqtt
import ssl
import uuid

# MQTT configuration
broker = 'farlab.infosci.cornell.edu'
port = 8883
topic = "IDD/ci"  # Ensure this matches the topic used by the sender
username = 'idd'
password = 'device@theFarm'

# Callback when connecting to the MQTT broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        client.subscribe(topic)  # Subscribe to the topic
    else:
        print(f"Failed to connect, return code {rc}")

# Callback when receiving a message from the MQTT broker
def on_message(client, userdata, msg):
    print(f"Received message from `{msg.topic}` topic")
    
    # Load the JSON payload
    payload = json.loads(msg.payload)

    # Decode the Base64 encoded image and save it to a file
    image_data = base64.b64decode(payload['img'])
    filename = "result.jpg"  # Ensure that the sender includes the filename in the payload
    with open(filename, 'wb') as image_file:
        image_file.write(image_data)
    print(f"Image saved as {filename}")

# Create a new MQTT client instance
client = mqtt.Client(str(uuid.uuid1()))

# Set the username and password for MQTT broker
client.username_pw_set(username, password)

# Set TLS settings for secure connection
client.tls_set(cert_reqs=ssl.CERT_NONE)

# Assign the on_connect and on_message callbacks
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT broker
client.connect(broker, port)

# Start the loop to process received messages and handle reconnections
client.loop_forever()
