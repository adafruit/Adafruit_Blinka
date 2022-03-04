# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
import time
import board
import busio

spi = busio.SPI(board.SCLK, board.MOSI, board.MISO)
while not spi.try_lock():
    pass
spi.configure(baudrate=16000000)
spi.unlock()

while True:
    spi.write(bytes(range(64)))
    time.sleep(0.1)
