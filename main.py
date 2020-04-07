# Mordin Solis - Ambient lights

import time
import board
import neopixel

console = neopixel.NeoPixel(board.D0, 3, brightness=0.2, auto_write=False)
omnitool = neopixel.NeoPixel(board.D2, 1, brightness=0.3, auto_write=False)


def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)


def rainbow(wait, *args):

    for j in range(255):
        for pixels in args:
            n = len(pixels)
            for i in range(n):
                rc_index = (i * 256 // n) + j
                pixels[i] = wheel(rc_index & 255)

            pixels.show()
        time.sleep(wait)


RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
ORANGE = (255, 50, 0)

console[0] = YELLOW
console[1] = YELLOW
console[2] = YELLOW
console.show()

omnitool[0] = ORANGE
omnitool.show()

while True:
    rainbow(0.1, console, omnitool)
