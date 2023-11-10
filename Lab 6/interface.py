import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import time
import board
import busio
import adafruit_mpr121
import ssl
import paho.mqtt.client as mqtt
import uuid


# Setup MQTT client and connect
client = mqtt.Client(str(uuid.uuid1()))
client.tls_set(cert_reqs=ssl.CERT_NONE)
client.username_pw_set('idd', 'device@theFarm')
client.connect('farlab.infosci.cornell.edu', port=8883)
topic = 'IDD/tarot'

# Create I2C bus and MPR121 object
i2c = busio.I2C(board.SCL, board.SDA)
mpr121 = adafruit_mpr121.MPR121(i2c)

# Tkinter setup
root = tk.Tk()
root.title("Remote Tarot Reader")

# Load the tarot image
tarot_image = Image.open('tarot.jpg')
tarot_photo = ImageTk.PhotoImage(tarot_image)

# Create a label to display the image
image_label = tk.Label(root, image=tarot_photo)
image_label.pack(side="top", fill="both", expand="yes")

def check_sensor():
    for i in range(1, 5):
        if mpr121[i].value:
            val = f"Object {i} touched for option {i}"
            print(val)
            client.publish(topic, i)
            messagebox.showinfo("Selection", f"You selected option {i}")
            break
    root.after(250, check_sensor)

root.after(250, check_sensor)

root.mainloop()
