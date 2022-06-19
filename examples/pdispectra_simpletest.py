# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2022 Andrew Ferguson for Fergcorp, LLC
#
# SPDX-License-Identifier: Unlicense

"""Simple test script for 1.54" 152x152 tri-color display.
"""

import time
import displayio
import busio
import board
import digitalio
from adafruit_display_text import label
import terminalio
from fergcorp_pdispectra import PDISpectra

BLACK = 0x000000
WHITE = 0xFFFFFF
RED = 0xFF0000

# Change text colors, choose from the following values:
# BLACK, RED, WHITE

FOREGROUND_COLOR = BLACK
BACKGROUND_COLOR = WHITE

displayio.release_displays()

spi_bus = busio.SPI(clock=board.GP18, MOSI=board.GP19, MISO=board.GP16)


# eInk Driver Setup
eink_driver_cs = board.GP17
eink_driver_d_c = board.GP12
eink_driver_busy = board.GP11
eink_driver_res = board.GP2

display_bus = displayio.FourWire(
    spi_bus,
    command=eink_driver_d_c,
    chip_select=eink_driver_cs,
    reset=eink_driver_res,
#    baudrate=100000,
)


'''
RES = digitalio.DigitalInOut(eink_driver_res)
RES.direction = digitalio.Direction.OUTPUT

RES.value = False
time.sleep(5 / 1000)
RES.value = True
time.sleep(5 / 1000)
RES.value = False
time.sleep(10 / 1000)
RES = True
time.sleep(5 / 1000)
print("Reset")
'''

print("Creating display")

display = PDISpectra(
    display_bus,
    height=152,
    width=152,
    rotation=90,
    busy_pin=eink_driver_busy,
    swap_rams=False,
)

g = displayio.Group()

'''
with open("/tmpcb.bmp", "rb") as f:
    pic = displayio.OnDiskBitmap(f)
    # CircuitPython 6 & 7 compatible
    t = displayio.TileGrid(
        pic, pixel_shader=getattr(pic, "pixel_shader", displayio.ColorConverter())
    )
    # CircuitPython 7 compatible only
    #t = displayio.TileGrid(pic, pixel_shader=pic.pixel_shader)
    g.append(t)

    display.show(g)

    display.refresh()
'''

# Set a background
background_bitmap = displayio.Bitmap(152, 152, 1)
# Map colors in a palette
palette = displayio.Palette(1)
palette[0] = BACKGROUND_COLOR

# Create a Tilegrid with the background and put in the displayio group
t = displayio.TileGrid(background_bitmap, pixel_shader=palette)
g.append(t)
'''
# Draw simple text using the built-in font into a displayio group
text_group = displayio.Group(scale=2, x=20, y=40)
TEXT = "Hello World!"
text_area = label.Label(terminalio.FONT, text=TEXT, color=FOREGROUND_COLOR)
text_group.append(text_area)  # Add this text to the text group
g.append(text_group)
'''
# Place the display group on the screen
display.show(g)

# Refresh the display to have everything show on the display
# NOTE: Do not refresh eInk displays more often than 180 seconds!
display.refresh()
'''
print("Refreshed")
time.sleep(120)
print("done")

while True:
    pass
'''