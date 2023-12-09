import time
import board
import busio
from adafruit_seesaw import seesaw, neopixel, rotaryio
import qwiic_joystick
import math
import sys

# Configuration constants
RESTING_POSITION_X, RESTING_POSITION_Y = 512, 512
PULL_THRESHOLD = 100
INITIAL_SPEED = 0.5
SPEED_DELTA_MULTIPLIER = 0.02
SPEED_MIN, SPEED_MAX = 0.01, 1
COLOR = (250, 188, 2)

# Define color-angle mappings and lights array
color_ranges = [
    ((250, 188, 2), 0, 30),
    ((251, 153, 2), 30, 60),
    ((253, 83, 8), 60, 90),
    ((254, 39, 18), 90, 120),
    ((167, 25, 75), 120, 150),
    ((134, 1, 175), 150, 180),
    ((61, 1, 164), 180, 210),
    ((2, 71, 254), 210, 240),
    ((3, 145, 206), 240, 270),
    ((102, 176, 50), 270, 300),
    ((208, 234, 43), 300, 330),
    ((254, 254, 51), 330, 360)
]

lights = [[42, 43, 44, 45],
          [35, 36, 37, 38],
          [28, 29, 30, 31],
          [21, 22, 23, 24],
          [14, 15, 16, 17],
          [8, 9, 10, 11]]

# Initialize I2C
try:
    i2c = busio.I2C(board.SCL, board.SDA)
except ValueError as e:
    print(f"I2C Initialization Error: {e}")
    sys.exit(1)

# Initialize NeoPixel
try:
    ss = seesaw.Seesaw(i2c, addr=0x60)
    neo_pin, num_pixels = 15, 64
    pixels = neopixel.NeoPixel(ss, neo_pin, num_pixels, brightness=1)
except OSError as e:
    print(f"NeoPixel Initialization Error: {e}")
    sys.exit(1)

# Initialize Joystick
try:
    myJoystick = qwiic_joystick.QwiicJoystick()
except Exception as e:
    print(f"Joystick Initialization Error: {e}")
    sys.exit(1)

# Initialize Rotary Encoder
try:
    roter = seesaw.Seesaw(i2c, addr=0x36)
    encoder = rotaryio.IncrementalEncoder(roter)
except OSError as e:
    print(f"Rotary Encoder Initialization Error: {e}")
    sys.exit(1)

button_pin = 24
roter.pin_mode(button_pin, roter.INPUT_PULLUP)

def joystick_to_color(angle):
    for color, start_angle, end_angle in color_ranges:
        if start_angle <= angle < end_angle:
            return color
    return (255, 255, 255)

def set_neopixel_color_normal(speed):
    global COLOR
    for row in lights:
        for i in row:
            try:
                x_position, y_position = myJoystick.horizontal, myJoystick.vertical
            except OSError as e:
                print(f"Error reading from joystick: {e}")
                continue
            x_normalized = (x_position - RESTING_POSITION_X) / 512.0
            y_normalized = (y_position - RESTING_POSITION_Y) / 512.0
            if abs(x_normalized) > PULL_THRESHOLD / 512.0 or abs(y_normalized) > PULL_THRESHOLD / 512.0:
                angle = (math.degrees(math.atan2(y_normalized, x_normalized)) + 360) % 360
                new_color = joystick_to_color(angle)
                if new_color != COLOR:
                    COLOR = new_color
            pixels[i] = COLOR
        pixels.show()
        time.sleep(speed)
        for i in row:
            pixels[i] = 0
        pixels.show()
        time.sleep(0.01)

def set_neopixel_color_reverse(speed):
    global COLOR
    for row in reversed(lights):
        for i in reversed(row):
            try:
                x_position, y_position = myJoystick.horizontal, myJoystick.vertical
            except OSError as e:
                print(f"Error reading from joystick: {e}")
                continue
            x_normalized = (x_position - RESTING_POSITION_X) / 512.0
            y_normalized = (y_position - RESTING_POSITION_Y) / 512.0
            if abs(x_normalized) > PULL_THRESHOLD / 512.0 or abs(y_normalized) > PULL_THRESHOLD / 512.0:
                angle = (math.degrees(math.atan2(y_normalized, x_normalized)) + 360) % 360
                new_color = joystick_to_color(angle)
                if new_color != COLOR:
                    COLOR = new_color
            pixels[i] = COLOR
        pixels.show()
        time.sleep(speed)
        for i in row:
            pixels[i] = 0
        pixels.show()
        time.sleep(0.01)

def get_speed_adjustment(encoder_position, last_position):
    if last_position is None:
        return INITIAL_SPEED
    delta = encoder_position - last_position
    new_speed = INITIAL_SPEED + delta * SPEED_DELTA_MULTIPLIER
    new_speed = max(SPEED_MIN, min(new_speed, SPEED_MAX))
    return new_speed

def runLuminArt():
    global COLOR
    current_pattern = 0
    last_button_state = 1
    
    if not myJoystick.connected:
        print("The Qwiic Joystick device isn't connected to the system. Please check your connection", file=sys.stderr)
        return

    myJoystick.begin()
    print("Initialized. Firmware Version: %s" % myJoystick.version)

    speed = INITIAL_SPEED
    last_position = None

    while True:
        try:
            encoder_position = -encoder.position
        except OSError as e:
            print(f"Error reading from rotary encoder: {e}")
            continue

        current_button_state = myJoystick.button
        if current_button_state != last_button_state:
            current_pattern = 1 - current_pattern
            time.sleep(0.01)
        last_button_state = current_button_state

        speed = get_speed_adjustment(encoder_position, last_position)
        last_position = encoder_position
        print(myJoystick.button)
        if current_pattern == 0:
            set_neopixel_color_normal(speed)
        else:
            set_neopixel_color_reverse(speed)

            
if __name__ == '__main__':
    try:
        runLuminArt()
    except (KeyboardInterrupt, SystemExit):
        print("\nEnding LuminArt")
        sys.exit(0)
