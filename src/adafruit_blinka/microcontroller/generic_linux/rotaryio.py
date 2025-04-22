# SPDX-FileCopyrightText: 2025 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
`rotaryio` - Support for reading rotation sensors
===========================================================
See `CircuitPython:rotaryio` in CircuitPython for more details.

Generic Threading/DigitalIO implementation for Linux

* Author(s): Melissa LeBlanc-Williams
"""

from __future__ import annotations
import threading
import microcontroller
import digitalio

# Define the state transition table for the quadrature encoder
transitions = [
    0,  # 00 -> 00 no movement
    -1,  # 00 -> 01 3/4 ccw (11 detent) or 1/4 ccw (00 at detent)
    +1,  # 00 -> 10 3/4 cw or 1/4 cw
    0,  # 00 -> 11 non-Gray-code transition
    +1,  # 01 -> 00 2/4 or 4/4 cw
    0,  # 01 -> 01 no movement
    0,  # 01 -> 10 non-Gray-code transition
    -1,  # 01 -> 11 4/4 or 2/4 ccw
    -1,  # 10 -> 00 2/4 or 4/4 ccw
    0,  # 10 -> 01 non-Gray-code transition
    0,  # 10 -> 10 no movement
    +1,  # 10 -> 11 4/4 or 2/4 cw
    0,  # 11 -> 00 non-Gray-code transition
    +1,  # 11 -> 01 1/4 or 3/4 cw
    -1,  # 11 -> 10 1/4 or 3/4 ccw
    0,  # 11 -> 11 no movement
]


class IncrementalEncoder:
    """
    IncrementalEncoder determines the relative rotational position based on two series of
    pulses. It assumes that the encoder’s common pin(s) are connected to ground,and enables
    pull-ups on pin_a and pin_b.

    Create an IncrementalEncoder object associated with the given pins. It tracks the
    positional state of an incremental rotary encoder (also known as a quadrature encoder.)
    Position is relative to the position when the object is constructed.
    """

    def __init__(
        self, pin_a: microcontroller.Pin, pin_b: microcontroller.Pin, divisor: int = 4
    ):
        """
        Create an IncrementalEncoder object associated with the given pins. It tracks the
        positional state of an incremental rotary encoder (also known as a quadrature encoder.)
        Position is relative to the position when the object is constructed.

        :param microcontroller.Pin pin_a: The first pin connected to the encoder.
        :param microcontroller.Pin pin_b: The second pin connected to the encoder.
        :param int divisor: The number of pulses per encoder step. Default is 4.
        """
        self._pin_a = digitalio.DigitalInOut(pin_a)
        self._pin_a.switch_to_input(pull=digitalio.Pull.UP)
        self._pin_b = digitalio.DigitalInOut(pin_b)
        self._pin_b.switch_to_input(pull=digitalio.Pull.UP)
        self._position = 0
        self._last_state = 0
        self._divisor = divisor
        self._sub_count = 0
        self._poll_thread = threading.Thread(target=self._polling_loop, daemon=True)
        self._poll_thread.start()

    def deinit(self):
        """Deinitializes the IncrementalEncoder and releases any hardware resources for reuse."""
        self._pin_a.deinit()
        self._pin_b.deinit()
        if self._poll_thread.is_alive():
            self._poll_thread.join()

    def __enter__(self) -> IncrementalEncoder:
        """No-op used by Context Managers."""
        return self

    def __exit__(self, _type, _value, _traceback):
        """
        Automatically deinitializes when exiting a context. See
        :ref:`lifetime-and-contextmanagers` for more info.
        """
        self.deinit()

    @property
    def divisor(self) -> int:
        """The divisor of the quadrature signal. Use 1 for encoders without detents, or encoders
        with 4 detents per cycle. Use 2 for encoders with 2 detents per cycle. Use 4 for encoders
        with 1 detent per cycle."""
        return self._divisor

    @divisor.setter
    def divisor(self, value: int):
        self._divisor = value

    @property
    def position(self) -> int:
        """The current position in terms of pulses. The number of pulses per rotation is defined
        by the specific hardware and by the divisor."""
        return self._position

    @position.setter
    def position(self, value: int):
        self._position = value

    def _get_pin_state(self) -> int:
        """Returns the current state of the pins."""
        return self._pin_a.value << 1 | self._pin_b.value

    def _polling_loop(self):
        while True:
            self._poll_encoder()

    def _poll_encoder(self):
        # Check the state of the pins
        # if either pin has changed, update the state
        new_state = self._get_pin_state()
        if new_state != self._last_state:
            self._state_update(new_state)
            self._last_state = new_state

    def _state_update(self, new_state: int):
        new_state &= 3
        index = self._last_state << 2 | new_state
        sub_increment = transitions[index]
        self._sub_count += sub_increment
        if self._sub_count >= self._divisor:
            self._position += 1
            self._sub_count = 0
        elif self._sub_count <= -self._divisor:
            self._position -= 1
            self._sub_count = 0
