# Mordin Solus - Ambient lights

import math
import time
import board
import random
import analogio
import neopixel
import digitalio
import adafruit_fancyled.adafruit_fancyled as fancy

import button

console = neopixel.NeoPixel(board.D0, 3, brightness=0.2, auto_write=False)
omnitool = neopixel.NeoPixel(board.D2, 1, brightness=0.3, auto_write=False)

button = button.Button(board.D4, digitalio.Pull.UP)

analog_out = analogio.AnalogOut(board.A0)

sine_length = 500
sine_wave = [int((1 + math.sin(2 * math.pi * ii / sine_length)) * (2 ** 15 - 1)) for ii in range(sine_length)]
square_wave = [(2 ** 15 - 1) if math.sin(2 * math.pi * ii / sine_length) > 0 else 0 for ii in range(sine_length)]

def buzz_till_button():
    while not button.pressed():
        button.update()
        for _ in range(2):
            for ii in range(0, 65535, 64):
                analog_out.value = ii

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
c_brit = 0.2

o_varb = 0.1
o_brit = 0.3
o_hue = random.random()
o_step = 0.01

mode = "ambient"
timer_limit = 0
timer_step = 5
timer_start = time.monotonic()

while True:

    print(mode, timer_limit)

    button.update()
    if button.just_pressed():
        mode = "timer"
        timer_limit = timer_step
        t0 = time.monotonic()
        while time.monotonic() - t0 < 1:
            button.update()
            if button.just_pressed():
                timer_limit += timer_step
                console.brightness = timer_limit / 60.0
                console.show()
                t0 = time.monotonic()
            time.sleep(0.01)
        timer_start = time.monotonic()

    o_hue += o_step * (2*random.random() - 1)
    omnitool[0] = fancy.palette_lookup(palette, o_hue).pack()
    omnitool.brightness = o_brit + o_varb * (2*random.random() - 1)
    omnitool.show()

    if mode == "ambient":
        console[0] = fancy.CHSV(c_hue - c_delta).pack()
        console[1] = fancy.CHSV(c_hue).pack()
        console[2] = fancy.CHSV(c_hue + c_delta).pack()
        c_hue += c_step
        if c_hue > 1:
            c_hue -= 1
        console.show()
    elif mode == "timer":
        t = time.monotonic()
        elapsed = t - timer_start
        remaining = timer_limit - elapsed
        print(timer_limit, timer_start, elapsed, remaining)
        if (t - timer_start) < timer_limit:
            console.brightness = remaining / timer_limit
        else:
            buzz_till_button()
            mode = "ambient"
            console.brightness = c_brit
        console.show()

    time.sleep(0.1)
