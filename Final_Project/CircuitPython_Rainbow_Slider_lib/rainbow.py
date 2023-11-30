import paho.mqtt.client as mqtt
import cv2
import uuid
import ssl
import board
import busio
import time
import paho.mqtt.client as mqtt
import signal
import qwiic_led_stick
from rainbowio import colorwheel
from adafruit_seesaw.seesaw import Seesaw
from adafruit_seesaw.analoginput import AnalogInput
from adafruit_seesaw import neopixel
from Qwiic_LED_Stick_examples.qwiic_led_stick_ex8_walking_rainbow import walking_rainbow 
import json
import base64



import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789


wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)


# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True
buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the ST7789 display:
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)

height =  disp.height
width = disp.width 
image = Image.new("RGB", (width, height))
draw = ImageDraw.Draw(image)


# i2c = busio.I2C(board.SCL, board.SDA)
# sensor = adafruit_apds9960.apds9960.APDS9960(i2c)

# sensor.enable_color = True
# r, g, b, a = sensor.color_data
my_stick = qwiic_led_stick.QwiicLEDStick()
if my_stick.begin() == False:
    print("\nThe Qwiic LED Stick isn't connected to the sytsem. Please check your connection", \
        file=sys.stderr)
print('LED stick connected')


CHOOSE = False
topic = 'IDD/tarot'

def on_connect(client, userdata, flags, rc):
    print(f"connected with result code {rc}")
    client.subscribe(topic)

def on_message(cleint, userdata, msg):
    print(f"topic: {msg.topic} msg: {msg.payload.decode('UTF-8')}")
    # if a message is recieved on the colors topic, parse it and set the color
    if msg.topic == topic:
        print("other user choose")
        global CHOOSE
        CHOOSE = True    

client = mqtt.Client(str(uuid.uuid1()))
client.tls_set(cert_reqs=ssl.CERT_NONE)
client.username_pw_set('idd', 'device@theFarm')
client.on_connect = on_connect
client.on_message = on_message

client.connect(
    'farlab.infosci.cornell.edu',
    port=8883)

client.loop_start()

# this lets us exit gracefully (close the connection to the broker)
def handler(signum, frame):
    print('exit gracefully')
    client.loop_stop()
    exit (0)
    
buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()
# hen sigint happens, do the handler callback function
signal.signal(signal.SIGINT, handler)
# our main loop
LED_length = 10
# my_stick.set_all_LED_brightness(1)
# walking_rainbow(my_stick, 20, 10, 0.1)
my_stick.set_all_LED_brightness(0)
while True:
    if CHOOSE:
        my_stick.set_all_LED_brightness(1)
        walking_rainbow(my_stick, 20, 10, 0.1)
        my_stick.set_all_LED_brightness(0)
        
        # Check if the camera opened successfully
        if not cap.isOpened():
            print("Error: Could not open camera.")
    
        # Capture frames continuously
        while True:
            ret, frame = cap.read()
            if ret:
                # Display the captured image
                cv2.imshow('Tarot Reader Camera', frame)
            # print("Error: Could not read frame.")
                
            if not buttonA.value:
                cv2.imwrite('tarotimg/result.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 30])
                data = {}
                with open('tarotimg/result.jpg', mode='rb') as file:
                    img = file.read()

                data['img'] = base64.b64encode(img).decode('utf-8')
                print("img to json")
                cmd = input('>> topic: IDD/tarotresult')
                if ' ' in cmd:
                    print('sorry white space is a no go for topics')
                else:
                    client.publish('IDD/tarotresult', json.dumps(data))
                    print("json sent")
        CHOOSE = False
        # time.sleep(.1)
        
        
        # my_stick.set_all_LED_brightness(0)

    my_stick.set_all_LED_brightness(0)
    time.sleep(.1)
    