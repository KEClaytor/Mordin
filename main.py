# Mordin Solis - Ambient lights

import time
import board
import random
import neopixel
import adafruit_fancyled.adafruit_fancyled as fancy

console = neopixel.NeoPixel(board.D0, 3, brightness=0.2, auto_write=False)
omnitool = neopixel.NeoPixel(board.D2, 1, brightness=0.3, auto_write=False)

RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
ORANGE = (255, 50, 0)

palette = [
    fancy.CRGB(*ORANGE),
    fancy.CRGB(*RED),
    fancy.CRGB(*BLUE),
]

console[0] = RED
console[1] = GREEN
console[2] = BLUE
console.show()

omnitool[0] = ORANGE
omnitool.show()

c_hue = random.random()
c_delta = 0.02
c_step = 0.001

o_hue = random.random()
o_step = 0.01

while True:

    o_hue += o_step * (2*random.random() - 1)
    omnitool[0] = fancy.palette_lookup(palette, o_hue).pack()
    omnitool.show()

    console[0] = fancy.CHSV(c_hue - c_delta).pack()
    console[1] = fancy.CHSV(c_hue).pack()
    console[2] = fancy.CHSV(c_hue + c_delta).pack()
    c_hue += c_step
    if c_hue > 1:
        c_hue -= 1
    console.show()

    time.sleep(0.1)
