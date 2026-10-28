# SPDX-FileCopyrightText: 2026 Limor Fried for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""Touchpaint on an ST7796S/FT6336U 3.5-inch capacitive TFT FeatherWing.

Install Adafruit-Blinka>=10.1.0, pymcp2222>=1.0.1.7,
adafruit-circuitpython-focaltouch, and Pillow. Set BLINKA_MCP2222=1 before
running this example with Python.

Use 3.3 V logic. Connect SCK/MOSI/MISO and SCL/SDA to their matching pins,
G0 to FeatherWing 9 (TCS), G1 to 10 (DC), G3 to LITE, and G5 to 6 (IRQ).
Power FeatherWing 3V from 3.3 V and USB from 5 V, with common ground.
Keep its switch ON. Leave G4 disconnected: SPI reserves it as hardware CS.
The FeatherWing resets the display and touch controller at power-up;
its RST header resets an attached Feather, not the display.

Tap a color at the top, then draw. CLR clears the canvas. Press Ctrl+C to
stop. FLIP_X and FLIP_Y below allow for a panel with reversed touch axes.
IRQ prompts immediate reads; a 50 ms poll also catches brief missed pulses.
"""

import struct
import sys
import time

import adafruit_focaltouch
from adafruit_bus_device.spi_device import SPIDevice
from PIL import Image, ImageDraw

import board
import busio
import digitalio

WIDTH = 320
HEIGHT = 480
PALETTE_HEIGHT = 40
BRUSH_RADIUS = 4
FLIP_X = False
FLIP_Y = False
COLORS = ("red", "yellow", "lime", "cyan", "blue", "magenta", "white")

cs = digitalio.DigitalInOut(board.G0)
cs.switch_to_output(value=True)
dc = digitalio.DigitalInOut(board.G1)
dc.switch_to_output(value=True)
backlight = digitalio.DigitalInOut(board.G3)
backlight.switch_to_output(value=True)
irq = digitalio.DigitalInOut(board.G5)
irq.switch_to_input(pull=digitalio.Pull.UP)
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
spi_device = SPIDevice(spi, cs, baudrate=1500000)
i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)
# Check IRQ in the main loop so an idle screen does not block the program.
touch = adafruit_focaltouch.Adafruit_FocalTouch(i2c)
canvas = Image.new("RGB", (WIDTH, HEIGHT), "black")
draw = ImageDraw.Draw(canvas)


def message(text):
    sys.stdout.write(text + "\n\r")
    sys.stdout.flush()


def command(opcode, data=b""):
    with spi_device as bus:
        dc.value = False
        bus.write(bytes([opcode]))
        if data:
            dc.value = True
            bus.write(data)


def initialize_display():
    # Same initialization as Adafruit_ST7796S.cpp in Adafruit-ST7735-Library.
    command(0x01)  # Software reset.
    time.sleep(0.15)
    for opcode, data in (
        (0xF0, b"\xC3"),
        (0xF0, b"\x96"),
        (0xC5, b"\x1C"),
        (0x36, b"\x48"),  # Portrait, BGR color order.
        (0x3A, b"\x55"),  # RGB565 pixels.
        (0xB0, b"\x80"),
        (0xB4, b"\x00"),
        (0xB6, b"\x80\x02\x3B"),
        (0xB7, b"\xC6"),
        (0xF0, b"\x69"),
        (0xF0, b"\x3C"),
    ):
        command(opcode, data)
    command(0x11)  # Exit sleep.
    time.sleep(0.15)
    command(0x29)  # Display on.
    time.sleep(0.15)
    command(0x21)  # Inversion setting for this IPS panel.


def update_region(box):
    """Send only this rectangle, using strips below the 65535-byte limit."""
    left, top, right, bottom = box  # Right and bottom are exclusive.
    for row in range(top, bottom, 48):
        end = min(row + 48, bottom)
        pixels = canvas.crop((left, row, right, end)).tobytes()
        packed = bytearray((right - left) * (end - row) * 2)
        for offset in range(0, len(pixels), 3):
            red, green, blue = pixels[offset : offset + 3]
            color = ((red & 0xF8) << 8) | ((green & 0xFC) << 3) | (blue >> 3)
            index = offset // 3 * 2
            packed[index] = color >> 8
            packed[index + 1] = color & 0xFF
        command(0x2A, struct.pack(">HH", left, right - 1))
        command(0x2B, struct.pack(">HH", row, end - 1))
        command(0x2C, packed)


def palette(selected):
    for index, color in enumerate(COLORS):
        left = index * 40
        draw.rectangle((left, 0, left + 39, PALETTE_HEIGHT - 1), fill=color)
        if index == selected:
            draw.rectangle((left + 3, 3, left + 36, 36), outline="black", width=2)
            draw.rectangle((left + 5, 5, left + 34, 34), outline="white", width=2)
    draw.rectangle((280, 0, 319, PALETTE_HEIGHT - 1), fill="#303030")
    draw.text((289, 14), "CLR", fill="white")


try:
    initialize_display()
    selected_color = 0
    palette(selected_color)
    update_region((0, 0, WIDTH, HEIGHT))
    message("Touchpaint ready: choose a color, draw, or tap CLR. IRQ is G5.")
    previous_points = {}
    previous_controls = set()
    next_touch_read = 0
    irq_seen = False
    next_report = 0
    while True:
        # IRQ is active low, but a short pulse may be missed over USB.
        # Periodic reads also observe release events between strokes.
        irq_active = not irq.value
        if irq_active and not irq_seen:
            message("Touch IRQ detected on G5")
            irq_seen = True
        if not irq_active and time.monotonic() < next_touch_read:
            time.sleep(0.005)
            continue
        next_touch_read = time.monotonic() + 0.05
        points = touch.touches
        current_points = {}
        current_controls = set()
        for point in points:
            x, y = point["x"], point["y"]
            if FLIP_X:
                x = WIDTH - 1 - x
            if FLIP_Y:
                y = HEIGHT - 1 - y
            if not 0 <= x < WIDTH or not 0 <= y < HEIGHT:
                continue
            touch_id = point["id"]
            if y < PALETTE_HEIGHT:
                choice = x // 40
                current_controls.add((touch_id, choice))
                if (touch_id, choice) in previous_controls:
                    continue
                if choice == len(COLORS):
                    draw.rectangle(
                        (0, PALETTE_HEIGHT, WIDTH - 1, HEIGHT - 1), fill="black"
                    )
                    update_region((0, PALETTE_HEIGHT, WIDTH, HEIGHT))
                    previous_points.clear()
                    current_points.clear()
                    message("Canvas cleared")
                else:
                    selected_color = choice
                    palette(selected_color)
                    update_region((0, 0, WIDTH, PALETTE_HEIGHT))
                    message("Color: " + COLORS[selected_color])
                continue
            # Keep the brush inside the canvas, below the palette.
            y = max(PALETTE_HEIGHT + BRUSH_RADIUS, y)
            old_x, old_y = previous_points.get(touch_id, (x, y))
            current_points[touch_id] = (x, y)
            brush_color = COLORS[selected_color]
            draw.line((old_x, old_y, x, y), fill=brush_color, width=BRUSH_RADIUS * 2)
            draw.ellipse(
                (
                    x - BRUSH_RADIUS,
                    y - BRUSH_RADIUS,
                    x + BRUSH_RADIUS,
                    y + BRUSH_RADIUS,
                ),
                fill=brush_color,
            )
            update_region(
                (
                    max(0, min(old_x, x) - BRUSH_RADIUS),
                    max(PALETTE_HEIGHT, min(old_y, y) - BRUSH_RADIUS),
                    min(WIDTH, max(old_x, x) + BRUSH_RADIUS + 1),
                    min(HEIGHT, max(old_y, y) + BRUSH_RADIUS + 1),
                )
            )
            if time.monotonic() >= next_report:
                message(f"Paint: x={x}, y={y}, id={touch_id}")
                next_report = time.monotonic() + 1
        previous_points = current_points
        previous_controls = current_controls
        time.sleep(0.005)
except KeyboardInterrupt:
    message("Touchpaint stopped")
finally:
    cs.value = True
    backlight.value = True
    spi.deinit()
    i2c.deinit()
    cs.deinit()
    dc.deinit()
    irq.deinit()
    backlight.deinit()  # FeatherWing's pull-up leaves the backlight on.
