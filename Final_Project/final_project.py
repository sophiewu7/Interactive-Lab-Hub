import time
import board
import busio
from adafruit_seesaw import seesaw, neopixel, rotaryio
import qwiic_joystick
import math
import sys
import random

# Configuration constants
RESTING_POSITION_X, RESTING_POSITION_Y = 512, 512
PULL_THRESHOLD = 100
SPEED = 0.5
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

class NeoPixelPatterns:
    def __init__(self, lights, joystick):
        self.lights = lights
        self.joystick = joystick
        self.current_pattern = 0
        self.desired_pattern = 0
        self.last_position = None
        self.patterns = [self.pattern_normal, 
                         self.pattern_reverse, 
                         self.pattern_color_chase_random,
                         self.pattern_random_flicker]
        
    def switch_pattern(self):
        self.desired_pattern = (self.desired_pattern + 1) % len(self.patterns)
        self.current_pattern = self.desired_pattern

    def run_current_pattern(self, start_pos):
        return self.patterns[self.current_pattern](start_pos)

    def check_joystick_for_color(self):
        global COLOR
        try:
            x_position, y_position = self.joystick.horizontal, self.joystick.vertical
        except OSError as e:
            print(f"Error reading from joystick: {e}")
            return
        x_normalized = (x_position - RESTING_POSITION_X) / 512.0
        y_normalized = (y_position - RESTING_POSITION_Y) / 512.0
        if abs(x_normalized) > PULL_THRESHOLD / 512.0 or abs(y_normalized) > PULL_THRESHOLD / 512.0:
            angle = (math.degrees(math.atan2(y_normalized, x_normalized)) + 360) % 360
            new_color = joystick_to_color(angle)
            if new_color != COLOR:
                COLOR = new_color
                
    def adjust_speed(self):
        global SPEED
        if abs(encoder.position) <= 200:
            encoder_position = -encoder.position
            SPEED = get_speed_adjustment(encoder_position, self.last_position)
            self.last_position = encoder_position
        else:
            pass
        return SPEED
    
    def pattern_normal(self, start_pos=0):
        global COLOR, SPEED
        for row_index, row in enumerate(self.lights):
            if row_index < start_pos:
                continue
            SPEED = self.adjust_speed()
            for i in row:
                self.check_joystick_for_color()
                pixels[i] = COLOR
            pixels.show()
            time.sleep(SPEED)
            if self.joystick.button == 0:
                for i in row:
                    pixels[i] = 0
                pixels.show()
                self.current_pattern = self.desired_pattern
                return row_index
            for i in row:
                pixels[i] = 0
            pixels.show()
            time.sleep(0.01)
        return -1

    def pattern_reverse(self, start_pos=0):
        global COLOR, SPEED
        num_rows = len(self.lights)
        for row_index in range(num_rows - 1, -1, -1):
            if num_rows - 1 - row_index < start_pos:
                continue
            row = self.lights[row_index]
            SPEED = self.adjust_speed()
            for i in reversed(row):
                self.check_joystick_for_color()
                pixels[i] = COLOR
            pixels.show()
            time.sleep(SPEED)
            if self.joystick.button == 0:
                for i in reversed(row):
                    pixels[i] = 0
                pixels.show()
                self.current_pattern = self.desired_pattern
                return num_rows - 1 - row_index
            for i in reversed(row):
                pixels[i] = 0
            pixels.show()
            time.sleep(0.01)
        return -1

    def pattern_random_flicker(self, start_pos=0):
        global COLOR, SPEED
        num_rows = len(self.lights)
        SPEED = self.adjust_speed()
        for _ in range(num_rows):
            row = random.choice(self.lights)
            original_colors = [pixels[pixel] for pixel in row]
            new_color = (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255)
            )
            for pixel in row:
                pixels[pixel] = new_color
            pixels.show()
            time.sleep(SPEED)
            if self.joystick.button == 0:
                for pixel, original_color in zip(row, original_colors):
                    pixels[pixel] = original_color
                pixels.show()
                self.current_pattern = self.desired_pattern
                return 0
            SPEED = self.adjust_speed()
            for pixel, original_color in zip(row, original_colors):
                pixels[pixel] = original_color
        pixels.show()
        return -1
    
    def pattern_color_chase_random(self, start_pos=0):
        global SPEED, COLOR
        for row_index, row in enumerate(self.lights):
            if row_index < start_pos:
                continue
            SPEED = self.adjust_speed()
            for i in range(len(row)):
                self.check_joystick_for_color()
                r_offset = random.randint(-50, 50)
                g_offset = random.randint(-50, 50)
                b_offset = random.randint(-50, 50)
                COLOR = (
                    min(255, max(0, COLOR[0] + r_offset)),
                    min(255, max(0, COLOR[1] + g_offset)),
                    min(255, max(0, COLOR[2] + b_offset))
                )
                pixels[row[i]] = COLOR
            pixels.show()
            time.sleep(SPEED)
            if self.joystick.button == 0:
                for i in row:
                    pixels[i] = (0, 0, 0)
                pixels.show()
                self.current_pattern = self.desired_pattern
                return row_index
            for i in row:
                pixels[i] = (0, 0, 0)
            pixels.show()
            time.sleep(0.01)
        return -1

def joystick_to_color(angle):
    for color, start_angle, end_angle in color_ranges:
        if start_angle <= angle < end_angle:
            return color
    return (255, 255, 255)

def get_speed_adjustment(encoder_position, last_position):
    if last_position is None:
        return SPEED
    delta = encoder_position - last_position
    new_speed = SPEED + delta * SPEED_DELTA_MULTIPLIER
    new_speed = max(SPEED_MIN, min(new_speed, SPEED_MAX))
    return new_speed

def runLuminArt():
    global COLOR
    last_button_state = 1
    patterns = NeoPixelPatterns(lights, myJoystick)
    start_pos = 0
    while True:
        current_button_state = myJoystick.button
        if current_button_state == 0 and last_button_state == 1:
            patterns.switch_pattern()
            time.sleep(0.01)
        stop_pos = patterns.run_current_pattern(start_pos)
        if stop_pos != -1:
            if patterns.current_pattern == 0:
                start_pos = len(lights) - 1 - stop_pos
            else:
                start_pos = stop_pos
            patterns.current_pattern = patterns.desired_pattern
        else:
            start_pos = 0
        last_button_state = current_button_state

if __name__ == '__main__':
    try:
        runLuminArt()
    except (KeyboardInterrupt, SystemExit):
        print("\nEnding LuminArt")
        sys.exit(0)
