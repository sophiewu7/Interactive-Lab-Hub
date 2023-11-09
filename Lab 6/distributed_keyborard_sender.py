import time
import board
import busio
import qwiic_keypad
import ssl

import paho.mqtt.client as mqtt
import uuid

client = mqtt.Client(str(uuid.uuid1()))
client.tls_set(cert_reqs=ssl.CERT_NONE)
client.username_pw_set('idd', 'device@theFarm')

client.connect(
    'farlab.infosci.cornell.edu',
    port=8883)

topic = 'IDD/your/topic/keyboard'

myKeypad = qwiic_keypad.QwiicKeypad(0x4b)

if myKeypad.is_connected() == False:
    print("The Qwiic Keypad device isn't connected to the system. Please check your connection", 
            file=sys.stderr)
    exit()

myKeypad.begin()

while True:
    myKeypad.update_fifo()
    button = myKeypad.get_button()
    if button != 0:  # Check if the button value is non-zero
        charButton = chr(button)
        val = f"Keypad {charButton} touched!"
        print(val)  # Print the message for debugging purposes
        client.publish(topic, charButton)  # Publish the button press to the MQTT topic
    time.sleep(0.25)

