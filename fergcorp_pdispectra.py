# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2022 Andrew Ferguson for Fergcorp, LLC
#
# SPDX-License-Identifier: MIT
"""
`fergcorp_pdispectra`
================================================================================

CircuitPython displayio driver for Pervasive Displays Spectra-based iTC/COG ePaper Displays


* Author(s): Andrew Ferguson

Implementation Notes
--------------------

**Hardware:**

* `Pervasive Displays 1.54" Tri-Color (BRW) Display E2154FS091 <https://www.digikey.com/en/products/detail/pervasive-displays/E2154FS091/7897287>`_

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

.. todo:: Uncomment or remove the Bus Device and/or the Register library dependencies
  based on the library's use of either.

# * Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
# * Adafruit's Register library: https://github.com/adafruit/Adafruit_CircuitPython_Register
"""

import displayio


__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/fergbrain/Fergcorp_CircuitPython_PDISpectra.git"


_START_SEQUENCE = (
    # TODO: Update for other epaper sizes.
    # This is specific to small sizes up to and including 4.2" EPD
    b"\x00\x81\x0E\x05"  # Power on COG driver: soft reset and wait 5ms
    b"\xE5\x01\x19"  # Input Temperature; 0x19=25C ---- 0x12 = 65F/18C
    b"\xE0\x01\x02"  # Active Temperature
    b"\xE0\x02\xCF\x89"  # Panel Settings
    b"\x04\x80\xC8"  # Power on DC/DC and wait 200ms
)

_STOP_SEQUENCE = b"\x02\x00"  # Turn-off DC/DC


# pylint: disable=too-few-public-methods
class PDISpectra(displayio.EPaperDisplay):
    r"""PDISpectra driver

    :param bus: The data bus the display is on
    :param bool swap_rams: Color and black rams/commands are swapped
    :param \**kwargs:
        See below

    :Keyword Arguments:
        * *width* (``int``) --
          Display width
        * *height* (``int``) --
          Display height
        * *rotation* (``int``) --
          Display rotation
        * *color_bits_inverted* (``bool``) --
          Invert color bit values
        * *black_bits_inverted* (``bool``) --
          Invert black bit values
    """

    def __init__(self, bus, swap_rams=False, rotation=0, **kwargs):

        width = kwargs["width"]
        height = kwargs["height"]

        if rotation % 180 != 0:
            width, height = height, width

        if swap_rams:
            color_bits_inverted = kwargs.pop("color_bits_inverted", False)
            write_color_ram_command = 0x10
            black_bits_inverted = kwargs.pop("black_bits_inverted", True)
            write_black_ram_command = 0x13
        else:
            write_black_ram_command = 0x10
            write_color_ram_command = 0x13
            color_bits_inverted = kwargs.pop("color_bits_inverted", True)
            black_bits_inverted = kwargs.pop("black_bits_inverted", False)

        super().__init__(
            display_bus=bus,
            start_sequence=_START_SEQUENCE,
            stop_sequence=_STOP_SEQUENCE,
            width=width,
            height=height,
            ram_width=width,
            ram_height=height,
            busy_state=True,
            rotation=rotation,
            write_black_ram_command=write_black_ram_command,
            write_color_ram_command=write_color_ram_command,
            black_bits_inverted=black_bits_inverted,
            color_bits_inverted=color_bits_inverted,
            refresh_display_command=0x12,
            always_toggle_chip_select=True,
        )
