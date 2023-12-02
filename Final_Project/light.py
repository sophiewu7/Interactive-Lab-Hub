# SPDX-FileCopyrightText: 2023 Liz Clark for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import busio
from rainbowio import colorwheel
from adafruit_seesaw import seesaw, neopixel

i2c = busio.I2C(board.SCL, board.SDA)
ss = seesaw.Seesaw(i2c, addr=0x60)
neo_pin = 15
num_pixels = 64

pixels = neopixel.NeoPixel(ss, neo_pin, num_pixels, brightness = 0.1)

color_offset = 0

lights = [[42, 43, 44, 45],
          [35, 36, 37, 38],
          [28, 29, 30, 31],
          [21, 22, 23, 24],
          [14, 15, 16, 17],
          [8, 9, 10, 11]]

while True:
    for row in lights:
        for i in row:
            rc_index = (i * 256 // num_pixels) + color_offset
            pixels[i] = colorwheel(rc_index & 255)
        pixels.show()
        time.sleep(0.01)
        for i in row:
            pixels[i] = 0
        pixels.show()
        time.sleep(0.01)

    color_offset += 1