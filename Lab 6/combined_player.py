import tkinter as tk
from PIL import Image, ImageTk
import board
import busio
import adafruit_mpr121
import ssl
import paho.mqtt.client as mqtt
import uuid
import io
import base64
import json

# MQTT callback functions
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        client.subscribe("IDD/tarotresult")  # Subscribe to the topic to receive the image

def on_message(client, userdata, msg):
    if msg.topic == "IDD/tarotresult":
        print("Image data received")
        image_data = base64.b64decode(json.loads(msg.payload)['img'])
        image = Image.open(io.BytesIO(image_data))
        image_photo = ImageTk.PhotoImage(image)
        image_label.config(image=image_photo)
        image_label.image = image_photo  # Keep a reference so it's not garbage collected

# Setup MQTT client and connect
client = mqtt.Client(str(uuid.uuid1()))
client.on_connect = on_connect
client.on_message = on_message
client.tls_set(cert_reqs=ssl.CERT_NONE)
client.username_pw_set('idd', 'device@theFarm')
client.connect('farlab.infosci.cornell.edu', port=8883)
client.loop_start()

# Create I2C bus and MPR121 object
i2c = busio.I2C(board.SCL, board.SDA)
mpr121 = adafruit_mpr121.MPR121(i2c)

# Tkinter setup
root = tk.Tk()
root.title("Remote Tarot Reader")
root.geometry("800x480")  # Adjust to your screen

# Load the tarot image
tarot_photo = ImageTk.PhotoImage(Image.open('tarot.jpg'))

# Create a label to display the image or text
image_label = tk.Label(root, image=tarot_photo)
image_label.pack(side="top", fill="both", expand="yes")

def show_divination_progress():
    image_label.config(text="Divination in progress...", image='', font=('Helvetica', 24), bg='black', fg='white')

def check_sensor():
    for i in range(1, 5):
        if mpr121[i].value:
            show_divination_progress()
            val = f"Object {i} touched for option {i}"
            print(val)
            client.publish("IDD/tarot", str(i))
            break
    root.after(250, check_sensor)

root.after(250, check_sensor)
root.mainloop()
