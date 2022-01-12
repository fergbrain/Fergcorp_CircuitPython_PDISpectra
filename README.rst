Introduction
============


.. image:: https://readthedocs.org/projects/fergcorp-circuitpython-pdispectra/badge/?version=latest
    :target: https://circuitpython-pdispectra.readthedocs.io/
    :alt: Documentation Status


.. image:: https://img.shields.io/discord/327254708534116352.svg
    :target: https://adafru.it/discord
    :alt: Discord


.. image:: https://github.com/fergbrain/Fergcorp_CircuitPython_PDISpectra/workflows/Build%20CI/badge.svg
    :target: https://github.com/fergbrain/Fergcorp_CircuitPython_PDISpectra/actions
    :alt: Build Status


.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Code Style: Black

CircuitPython displayio driver for Pervasive Displays Spectra-based iTC/COG ePaper Displays


Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://circuitpython.org/libraries>`_
or individual libraries can be installed using
`circup <https://github.com/adafruit/circup>`_.

Installing from PyPI
=====================
.. note:: This library is not available on PyPI yet. Install documentation is included
   as a standard element. Stay tuned for PyPI availability!

On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/fergcorp-circuitpython-pdispectra/>`_.
To install for current user:

.. code-block:: shell

    pip3 install fergcorp-circuitpython-pdispectra

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install fergcorp-circuitpython-pdispectra

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .env
    source .env/bin/activate
    pip3 install fergcorp-circuitpython-pdispectra



Installing to a Connected CircuitPython Device with Circup
==========================================================

Make sure that you have ``circup`` installed in your Python environment.
Install it with the following command if necessary:

.. code-block:: shell

    pip3 install circup

With ``circup`` installed and your CircuitPython device connected use the
following command to install:

.. code-block:: shell

    circup install pdispectra

Or the following command to update an existing version:

.. code-block:: shell

    circup update

Usage Example
=============x

.. code-block:: python

    import displayio
    import busio
    import board
    import digitalio
    import time
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

    display_bus = displayio.FourWire(
        spi_bus,
        command=eink_driver_d_c,
        chip_select=eink_driver_cs,
        reset=None,
        baudrate=100000,
    )

    eink_driver_busy = board.GP11


    eink_driver_res = digitalio.DigitalInOut(board.GP1)
    eink_driver_res.direction = digitalio.Direction.OUTPUT
    eink_driver_res.drive_mode = digitalio.DriveMode.PUSH_PULL

    eink_driver_res.value = False
    time.sleep(5 / 1000)
    eink_driver_res.value = True
    time.sleep(5 / 1000)
    eink_driver_res.value = False
    time.sleep(10 / 1000)
    eink_driver_res = True
    time.sleep(5 / 1000)
    print("Reset")

    print("Creating display")

    display = PDISpectra(
        display_bus,
        height=152,
        width=152,
        rotation=90,
        busy_pin=eink_driver_busy,
        swap_rams=True,
    )

    g = displayio.Group()

    # Set a background
    background_bitmap = displayio.Bitmap(152, 152, 1)
    # Map colors in a palette
    palette = displayio.Palette(1)
    palette[0] = BACKGROUND_COLOR

    # Create a Tilegrid with the background and put in the displayio group
    t = displayio.TileGrid(background_bitmap, pixel_shader=palette)
    g.append(t)

    # Draw simple text using the built-in font into a displayio group
    text_group = displayio.Group(scale=2, x=20, y=40)
    text = "Hello World!"
    text_area = label.Label(terminalio.FONT, text=text, color=FOREGROUND_COLOR)
    text_group.append(text_area)  # Add this text to the text group
    g.append(text_group)

    # Place the display group on the screen
    display.show(g)

    # Refresh the display to have everything show on the display
    # NOTE: Do not refresh eInk displays more often than 180 seconds!
    display.refresh()
    print("Refreshed")
    time.sleep(120)
    print("done")

    while True:
        pass


Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/fergbrain/Fergcorp_CircuitPython_PDISpectra/blob/HEAD/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.

Documentation
=============

For information on building library documentation, please check out
`this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.
