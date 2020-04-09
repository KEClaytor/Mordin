""" Mordin Solus - Ambient lights and Pomodoro Timer
"""

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

RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
ORANGE = (255, 50, 0)

palette = [fancy.CRGB(*ORANGE), fancy.CRGB(*RED), fancy.CRGB(*BLUE)]


def buzz_till_button():
    """ Buzz until until a button press.
    """
    while not button.pressed():
        button.update()
        for _ in range(2):
            for ii in range(0, 65535, 64):
                analog_out.value = ii


def ternary_to_decimal(t):
    """ Convert a ternary key to a decimal.
    """
    d = 0
    for p, k in enumerate(t):
        # print(t, k, p, (3**p) * k)
        d += (3 ** p) * k
    return d


def decimal_to_ternary(d, t_len=3):
    """ Convert a decimal to a ternary key.
    """
    t = [0] * t_len
    for p in range(t_len, 0, -1):
        # print(d, p, 3**(p-1), d // (3**(p-1)) )
        tp = d // 3 ** (p - 1)
        t[p - 1] = tp
        d -= tp * 3 ** (p - 1)
    return t


def color_from_time(time, time_step):
    """ Convert a time into a blend of colors
    Colors are based on the ternary key colors.
    """
    lo = math.floor(time / time_step)
    hi = math.ceil(time / time_step)
    frac = (time - time_step * lo) / time_step
    # Convert to ternary range
    tlo = decimal_to_ternary(lo)
    thi = decimal_to_ternary(hi)
    # And blend the colors
    colors = [fancy.mix(palette[l], palette[h], frac).pack() for l, h in zip(tlo, thi)]
    return colors


def update_console(time, time_step):
    """ Blend the console according to the remaining time.
    """
    colors = color_from_time(time, time_step)
    for ii in range(3):
        console[ii] = colors[ii]
    console.show()


# Default conosle colors
console[0] = RED
console[1] = ORANGE
console[2] = BLUE
console.show()

# Default omnitool colors
omnitool[0] = ORANGE
omnitool.show()

# Console ambinet parameters
c_hue = random.random()
c_delta = 0.02
c_step = 0.001

# Omnitoool parameters
o_varb = 0.1
o_brit = 0.3
o_hue = random.random()
o_step = 0.01

# Adjustable timer step (s)
timer_step = 5

# Initalize timer
timer_limit = 0
timer_start = time.monotonic()
mode = "ambient"
while True:

    # Check for user interaction
    button.update()
    if button.just_pressed():
        mode = "timer"
        clicks = 0
        update_console(clicks, 1)

        t0 = time.monotonic()
        while time.monotonic() - t0 < 1:
            button.update()
            if button.just_pressed():
                clicks += 1
                update_console(clicks, 1)
                # Allow another second to press the button again
                t0 = time.monotonic()
            time.sleep(0.01)

        timer_limit = clicks * timer_step
        timer_start = time.monotonic()

    # Update omnitool
    o_hue += o_step * (2 * random.random() - 1)
    omnitool[0] = fancy.palette_lookup(palette, o_hue).pack()
    omnitool.brightness = o_brit + o_varb * (2 * random.random() - 1)
    omnitool.show()

    # Update console
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
            update_console(remaining, timer_step)
        else:
            buzz_till_button()
            mode = "ambient"
            console.brightness = 0.2
        console.show()

    # Delay
    time.sleep(0.1)
