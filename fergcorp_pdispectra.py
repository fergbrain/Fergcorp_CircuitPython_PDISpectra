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

* Pervasive Displays 1.54" Tri-Color (BRW) Display E2154FS091
  https://www.digikey.com/en/products/detail/pervasive-displays/E2154FS091/7897287

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

"""

import time
from micropython import const
from digitalio import Direction
import adafruit_framebuf
from adafruit_epd.epd import Adafruit_EPD

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/fergbrain/Fergcorp_CircuitPython_PDISpectra.git"

_PDISPECTRA_SOFT_RESET = const(0x00)
_PDISPECTRA_INPUT_TEMP = const(0xE5)
_PDISPECTRA_ACTIVE_TEMP = const(0xE0)
_PDISPECTRA_PANEL_SETTINGS = const(0x00)
_PDISPECTRA_DCDC_POWER_ON = const(0x04)
_PDISPECTRA_DCDC_POWER_OFF = const(0x02)
_PDISPECTR_DISPLAY_REFRESH = const(0x12)

_PDISPECTRA_DTM1 = const(0x10)
_PDISPECTRA_DTM2 = const(0x13)


# pylint: disable=too-few-public-methods
class PDISpectra(Adafruit_EPD):

    # pylint: disable=too-many-arguments
    def __init__(
        self, width, height, spi, *, cs_pin, dc_pin, sramcs_pin, rst_pin, busy_pin
    ):


        # TODO: Implement
        '''
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
        '''
        # TODO Verify: Always_toggle_chip_select=True
        super().__init__(
            width, height, spi, cs_pin, dc_pin, sramcs_pin, rst_pin, busy_pin
        )

        self._buffer1_size = int(width * height / 8)
        self._buffer2_size = int(width * height / 8)

        if sramcs_pin:
            self._buffer1 = self.sram.get_view(0)
            self._buffer2 = self.sram.get_view(self._buffer1_size)
        else:
            self._buffer1 = bytearray((width * height) // 8)
            self._buffer2 = bytearray((width * height) // 8)
        # since we have *two* framebuffers - one for red and one for black
        # we dont subclass but manage manually
        self._framebuf1 = adafruit_framebuf.FrameBuffer(
            self._buffer1, width, height, buf_format=adafruit_framebuf.MHMSB
        )
        self._framebuf2 = adafruit_framebuf.FrameBuffer(
            self._buffer2, width, height, buf_format=adafruit_framebuf.MHMSB
        )
        self.set_black_buffer(0, True)
        self.set_color_buffer(1, True)
        self._single_byte_tx = True


        self._black_inverted = False
        self._color_inverted = False
        # pylint: enable=too-many-arguments

    def power_up(self):
        """Power up the display in preparation for writing RAM and updating"""
        if self._busy:
            self._busy.direction = Direction.INPUT
        self._dc.value = True
        if self._rst:
            self._rst.value = True
        self._cs.value = True
        self.power_on_cog()

    def power_down(self):
        """Power down"""
        self.command(_PDISPECTRA_DCDC_POWER_OFF, bytearray([0x00]))  # Technically only need the command, not the data
        self.busy_wait()

        self._dc.value = False
        self._cs.value = False
        if self._busy:
            self._busy.direction = Direction.OUTPUT
            self._busy.value = False
        time.sleep(150 / 1000)
        if self._rst:
            self._rst.value = False

    def power_on_cog(self):
        """ Power on the COG"""
        self.hardware_reset()
        self.soft_reset()

        self.command(_PDISPECTRA_INPUT_TEMP, bytearray([0x19]))  # Input Temperature; 0x19=25C ---- 0x12 = 65F/18C
        self.command(_PDISPECTRA_ACTIVE_TEMP, bytearray([0x02])) # Active Temperature

        # TODO (or maybe 0x8D instead of 0x89?...see line 197 of https://github.com/PervasiveDisplays/EPD_Driver_GU_small/blob/main/src/EPD_Configuration.h
        self.command(_PDISPECTRA_PANEL_SETTINGS, bytearray([0xCF, 0x89]))  # Panel Settings

    def hardware_reset(self):
        if self._rst:
            self._rst.value = False
            time.sleep(1 / 1000)
            self._rst.value = True
            time.sleep(5 / 1000)
            self._rst.value = False
            time.sleep(10 / 1000)
            self._rst.value = True
            time.sleep(5 / 1000)

    def soft_reset(self):
        """Perform a soft reset"""
        self.command(_PDISPECTRA_SOFT_RESET, bytearray([0x0E]))
        self.busy_wait()


    def busy_wait(self):
        """Wait for display to be done with current task, either by polling the
        busy pin, or pausing"""
        if self._busy:
            while not self._busy.value:
                time.sleep(0.01)
        else:
            time.sleep(0.5)

    def dcdc_power_on(self):
        self.command(_PDISPECTRA_DCDC_POWER_ON, bytearray([0x00]))  # Technically only need the command, not the data
        self.busy_wait()

    def update(self):
        self.dcdc_power_on()
        self.command(_PDISPECTR_DISPLAY_REFRESH)
        self.busy_wait()

        self.power_down()


    def write_ram(self, index):
        """Send the one byte command for starting the RAM write process. Returns
        the byte read at the same time over SPI. index is the RAM buffer, can be
        0 or 1 for tri-color displays."""
        if index == 0:
            return self.command(_PDISPECTRA_DTM1, end=False)
        if index == 1:
            return self.command(_PDISPECTRA_DTM2, end=False)
        raise RuntimeError("RAM index must be 0 or 1")

    def set_ram_address(self, x, y):  # pylint: disable=unused-argument, no-self-use
        """Set the RAM address location, not used on this chipset but required by
        the superclass"""
        return  # on this chip it does nothing

    def flush(self):
        pass

    def clear(self):
        pass