import time
import board
import busio
from adafruit_seesaw import seesaw, neopixel, rotaryio, digitalio
import qwiic_joystick
import random
import math

# Setup for NeoPixel
i2c = busio.I2C(board.SCL, board.SDA)
ss = seesaw.Seesaw(i2c, addr=0x60)
neo_pin = 15
num_pixels = 64
pixels = neopixel.NeoPixel(ss, neo_pin, num_pixels, brightness=1)

# Define color-angle mappings
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

# Define the lights array
lights = [[42, 43, 44, 45],
          [35, 36, 37, 38],
          [28, 29, 30, 31],
          [21, 22, 23, 24],
          [14, 15, 16, 17],
          [8, 9, 10, 11]]

# Joystick setup
myJoystick = qwiic_joystick.QwiicJoystick()

# Function to determine the color based on the angle
def joystick_to_color(angle):
    for color, start_angle, end_angle in color_ranges:
        if start_angle <= angle < end_angle:
            return color
    return (255, 255, 255)  # Default color

# Function to set NeoPixel color
def set_neopixel_color(color, speed, pattern):
    if pattern == "chase":
        chase(color, speed)
    elif pattern == "solid":
        solid_color(color, speed)
    elif pattern == "confetti":
        confetti(speed)

# Pattern functions
def solid_color(color, wait):
    pixels.fill(color)
    pixels.show()
    time.sleep(wait)

def chase(color, wait):
    for offset in range(num_pixels):
        pixels.fill((0, 0, 0))
        for i in range(num_pixels):
            pixels[(i + offset) % num_pixels] = color
        pixels.show()
        time.sleep(wait)

def confetti(speed):
    for _ in range(5):
        pixels.fill((0, 0, 0))
        pixels[random.randint(0, num_pixels - 1)] = (255, 255, 255)
        pixels.show()
        time.sleep(speed)

# Setup for rotary encoder
roter = seesaw.Seesaw(i2c, addr=0x36)
encoder = rotaryio.IncrementalEncoder(roter)
button = digitalio.DigitalIO(roter, 24)
button_held = False
last_button_state = False

# Function to change patterns
def change_pattern():
    global pattern
    patterns = ["chase", "solid", "confetti"]
    current_index = patterns.index(pattern) if pattern in patterns else -1
    new_index = (current_index + 1) % len(patterns)
    pattern = patterns[new_index]

# Main function
def runExample():
    global pixels, button_held, last_button_state
    if not myJoystick.connected:
        print("The Qwiic Joystick device isn't connected. Please check your connection", file=sys.stderr)
        return

    myJoystick.begin()
    print("Initialized. Firmware Version: %s" % myJoystick.version)

    resting_position_x, resting_position_y = 512, 512
    pull_threshold = 100  # Threshold to determine a "pull"
    last_color = (250, 188, 2)  # Initialize with a default color
    speed = 0.5
    pattern = "solid"
    last_position = None

    while True:
        encoder_position = -encoder.position

        # Button press logic (debouncing)
        button_state = not button.value
        if button_state and not last_button_state and not button_held:
            change_pattern()
            button_held = True
        elif not button_state and button_held:
            button_held = False
        last_button_state = button_state

        # Joystick color selection logic
        x_position = myJoystick.horizontal
        y_position = myJoystick.vertical
        x_normalized = (x_position - resting_position_x) / 512.0
        y_normalized = (y_position - resting_position_y) / 512.0

        if abs(x_normalized) > pull_threshold / 512.0 or abs(y_normalized) > pull_threshold / 512.0:
            angle = (math.degrees(math.atan2(y_normalized, x_normalized)) + 360) % 360
            last_color = joystick_to_color(angle)
            print(f"Joystick Angle: {angle}, Color selected: RGB{last_color}")

        # Update NeoPixel color and pattern
        set_neopixel_color(last_color, speed, pattern)
        time.sleep(0.01)

if __name__ == '__main__':
    try:
        runExample()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example 1")
        sys.exit(0)
