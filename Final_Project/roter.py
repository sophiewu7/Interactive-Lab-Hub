import time
import board
import busio
from adafruit_seesaw import seesaw, neopixel, rotaryio, digitalio
import qwiic_joystick
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
def set_neopixel_color(color, speed):
    for row in lights:
        for i in row:
            pixels[i] = color
        pixels.show()
        time.sleep(speed)
        for i in row:
            pixels[i] = 0
        pixels.show()
        time.sleep(speed)

# Setup for rotary encoder
roter = seesaw.Seesaw(i2c, addr=0x36)
encoder = rotaryio.IncrementalEncoder(roter)

def runExample():
    global pixels
    if not myJoystick.connected:
        print("The Qwiic Joystick device isn't connected to the system. Please check your connection", file=sys.stderr)
        return

    myJoystick.begin()
    print("Initialized. Firmware Version: %s" % myJoystick.version)

    resting_position_x, resting_position_y = 512, 512
    pull_threshold = 100  # Threshold to determine a "pull"
    last_color = (250, 188, 2)  # Initialize with a default color

    speed = 0.5
    last_position = None
    while True:
        encoder_position = -encoder.position

        if encoder_position != last_position:
            if encoder_position is not None and last_position is not None:
                delta = encoder_position - last_position
                speed += delta * 0.02  # Adjust the multiplier to change sensitivity
                speed = max(0.02, min(speed, 1))  # Keep speed within reasonable bounds
            last_position = encoder_position

        x_position = myJoystick.horizontal
        y_position = myJoystick.vertical
        x_normalized = (x_position - resting_position_x) / 512.0
        y_normalized = (y_position - resting_position_y) / 512.0

        # Check if the joystick is pulled far enough in any direction
        if abs(x_normalized) > pull_threshold / 512.0 or abs(y_normalized) > pull_threshold / 512.0:
            angle = (math.degrees(math.atan2(y_normalized, x_normalized)) + 360) % 360
            last_color = joystick_to_color(angle)  # Update color only on pull
            print(f"Joystick Angle: {angle}, Color selected: RGB{last_color}")

        set_neopixel_color(last_color, speed)  # Use the last selected color
        time.sleep(0.01)

if __name__ == '__main__':
    try:
        runExample()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example 1")
        sys.exit(0)
