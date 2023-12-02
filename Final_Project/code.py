import time
import board
import busio
import random
from adafruit_seesaw import seesaw, neopixel

i2c = busio.I2C(board.SCL, board.SDA)
ss = seesaw.Seesaw(i2c, addr=0x60)
neo_pin = 15
num_pixels = 6

pixels = neopixel.NeoPixel(ss, neo_pin, num_pixels, brightness=1)

def solid_color(color):
    pixels.fill(color)
    pixels.show()
    time.sleep(1)

def rainbow_cycle():
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(0.1)

def sinelon():
    for i in range(num_pixels * 2):
        pixels.fill((0, 0, 0))
        pixels[i % num_pixels] = (255, 0, 0)
        pixels.show()
        time.sleep(0.1)

def confetti():
    for _ in range(5):
        pixels.fill((0, 0, 0))
        pixels[random.randint(0, num_pixels - 1)] = (255, 255, 255)
        pixels.show()
        time.sleep(0.1)

def bpm(wait):
    for i in range(num_pixels):
        brightness_value = int(pixels.brightness * 255)
        color = wheel(((i * 256 // num_pixels) + brightness_value) & 255)
        pixels.fill(color)
        pixels.show()
        time.sleep(wait)

def jungle():
    pixels.fill((0, 255, 0))
    pixels.show()
    time.sleep(0.5)

def chase(color, wait):
    for offset in range(num_pixels):
        pixels.fill((0, 0, 0))
        for i in range(num_pixels):
            pixels[(i + offset) % num_pixels] = color
        pixels.show()
        time.sleep(wait)

def wheel(pos):
    if pos < 85:
        return (pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return (0, pos * 3, 255 - pos * 3)

while True:
    # Turn off all pixels
    pixels.fill((0, 0, 0))
    pixels.show()

    # Random color
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    # Random lighting pattern
    pattern = random.choice(["chase", "solid","sinelon", "confetti", "bpm", "jungle"])

    if pattern == "chase":
        chase(color, 0.1)
    elif pattern == "solid":
        solid_color(color)
    elif pattern == "rainbow":
        rainbow_cycle()
    elif pattern == "sinelon":
        sinelon()
    elif pattern == "confetti":
        confetti()
    elif pattern == "bpm":
        bpm(0.1)
    elif pattern == "jungle":
        jungle()
