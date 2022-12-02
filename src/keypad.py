# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
`keypad` - Support for scanning keys and key matrices
===========================================================
See `CircuitPython:keypad` in CircuitPython for more details.

* Author(s): Melissa LeBlanc-Williams
"""

import time
import threading
from collections import deque
import digitalio


class Event:
    """A key transition event."""

    def __init__(self, key_number=0, pressed=True):
        """
        Create a key transition event, which reports a key-pressed or key-released transition.

        :param int key_number: the key number
        :param bool pressed: ``True`` if the key was pressed; ``False`` if it was released.
        """
        self._key_number = key_number
        self._pressed = pressed

    @property
    def key_number(self):
        """The key number."""
        return self._key_number

    @property
    def pressed(self):
        """
        ``True`` if the event represents a key down (pressed) transition.
        The opposite of `released`.
        """
        return self._pressed

    @property
    def released(self):
        """
        ``True`` if the event represents a key up (released) transition.
        The opposite of `pressed`.
        """
        return not self._pressed

    def __eq__(self, other):
        """
        Two `Event` objects are equal if their `key_number`
        and `pressed`/`released` values are equal.
        """
        return self.key_number == other.key_number and self.pressed == other.pressed

    def __hash__(self):
        """Returns a hash for the `Event`, so it can be used in dictionaries, etc.."""
        return hash(self._key_number)

    def __repr__(self):
        """Return a textual representation of the object"""
        return "<Event: key_number {} {}>".format(
            self.key_number, "pressed" if self._pressed else "released"
        )


class _EventQueue:
    """
    A queue of `Event` objects, filled by a `keypad` scanner such as `Keys` or `KeyMatrix`.

    You cannot create an instance of `_EventQueue` directly. Each scanner creates an
    instance when it is created.
    """

    def __init__(self, max_events):
        self._events = deque([], max_events)
        self._overflowed = False

    def get(self):
        """
        Return the next key transition event. Return ``None`` if no events are pending.

        Note that the queue size is limited; see ``max_events`` in the constructor of
        a scanner such as `Keys` or `KeyMatrix`.
        If a new event arrives when the queue is full, the event is discarded, and
        `overflowed` is set to ``True``.

        :return: the next queued key transition `Event`
        :rtype: Optional[Event]
        """
        if not self._events:
            return None
        return self._events.popleft()

    def get_into(self, event):
        """Store the next key transition event in the supplied event, if available,
        and return ``True``.
        If there are no queued events, do not touch ``event`` and return ``False``.

        The advantage of this method over ``get()`` is that it does not allocate storage.
        Instead you can reuse an existing ``Event`` object.

        Note that the queue size is limited; see ``max_events`` in the constructor of
        a scanner such as `Keys` or `KeyMatrix`.

        :return ``True`` if an event was available and stored, ``False`` if not.
        :rtype: bool
        """
        if not self._events:
            return False
        next_event = self._events.popleft()
        # pylint: disable=protected-access
        event._key_number = next_event._key_number
        event._pressed = next_event._pressed
        # pylint: enable=protected-access
        return True

    def clear(self):
        """
        Clear any queued key transition events. Also sets `overflowed` to ``False``.
        """
        self._events.clear()
        self._overflowed = False

    def __bool__(self):
        """``True`` if `len()` is greater than zero.
        This is an easy way to check if the queue is empty.
        """
        return len(self._events) > 0

    def __len__(self):
        """Return the number of events currently in the queue. Used to implement ``len()``."""
        return len(self._events)

    @property
    def overflowed(self):
        """
        ``True`` if an event could not be added to the event queue because it was full. (read-only)
        Set to ``False`` by  `clear()`.
        """
        return self._overflowed

    def keypad_eventqueue_record(self, key_number, current):
        """Record a new event"""
        if len(self._events) == self._events.maxlen:
            self._overflowed = True
        else:
            self._events.append(Event(key_number, current))


class _KeysBase:
    def __init__(self, interval, max_events, scanning_function):
        self._interval = interval
        self._last_scan = time.monotonic()
        self._events = _EventQueue(max_events)
        self._scanning_function = scanning_function
        self._scan_thread = threading.Thread(target=self._scanning_loop, daemon=True)
        self._scan_thread.start()

    @property
    def events(self):
        """The EventQueue associated with this Keys object. (read-only)"""
        return self._events

    def deinit(self):
        """Stop scanning"""
        if self._scan_thread.is_alive():
            self._scan_thread.join()

    def __enter__(self):
        """No-op used by Context Managers."""
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        """
        Automatically deinitializes when exiting a context. See
        :ref:`lifetime-and-contextmanagers` for more info.
        """
        self.deinit()

    def _scanning_loop(self):
        while True:
            remaining_delay = self._interval - (time.monotonic() - self._last_scan)
            if remaining_delay > 0:
                time.sleep(remaining_delay)
            self._last_scan = time.monotonic()
            self._scanning_function()


class Keys(_KeysBase):
    """Manage a set of independent keys."""

    def __init__(
        self, pins, *, value_when_pressed, pull=True, interval=0.02, max_events=64
    ):
        """
        Create a `Keys` object that will scan keys attached to the given sequence of pins.
        Each key is independent and attached to its own pin.

        An `EventQueue` is created when this object is created and is available in the
        `events` attribute.

        :param Sequence[microcontroller.Pin] pins: The pins attached to the keys.
          The key numbers correspond to indices into this sequence.
        :param bool value_when_pressed: ``True`` if the pin reads high when the key is pressed.
          ``False`` if the pin reads low (is grounded) when the key is pressed.
          All the pins must be connected in the same way.
        :param bool pull: ``True`` if an internal pull-up or pull-down should be
          enabled on each pin. A pull-up will be used if ``value_when_pressed`` is ``False``;
          a pull-down will be used if it is ``True``.
          If an external pull is already provided for all the pins, you can set
          ``pull`` to ``False``.
          However, enabling an internal pull when an external one is already present is not
          a problem;
          it simply uses slightly more current.
        :param float interval: Scan keys no more often than ``interval`` to allow for debouncing.
          ``interval`` is in float seconds. The default is 0.020 (20 msecs).
        :param int max_events: maximum size of `events` `EventQueue`:
          maximum number of key transition events that are saved.
          Must be >= 1.
          If a new event arrives when the queue is full, the oldest event is discarded.
        """
        self._digitalinouts = []
        for pin in pins:
            dio = digitalio.DigitalInOut(pin)
            if pull:
                dio.pull = (
                    digitalio.Pull.DOWN if value_when_pressed else digitalio.Pull.UP
                )
            self._digitalinouts.append(dio)

        self._currently_pressed = [False] * len(pins)
        self._previously_pressed = [False] * len(pins)
        self._value_when_pressed = value_when_pressed

        super().__init__(interval, max_events, self._keypad_keys_scan)

    def deinit(self):
        """Stop scanning and release the pins."""
        super().deinit()
        for dio in self._digitalinouts:
            dio.deinit()

    def reset(self):
        """Reset the internal state of the scanner to assume that all keys are now released.
        Any key that is already pressed at the time of this call will therefore immediately cause
        a new key-pressed event to occur.
        """
        self._currently_pressed = self._previously_pressed = [False] * self.key_count

    @property
    def key_count(self):
        """The number of keys that are being scanned. (read-only)"""
        return len(self._digitalinouts)

    def _keypad_keys_scan(self):
        for key_number, dio in enumerate(self._digitalinouts):
            self._previously_pressed[key_number] = self._currently_pressed[key_number]
            current = dio.value == self._value_when_pressed
            self._currently_pressed[key_number] = current
            if self._previously_pressed[key_number] != current:
                self._events.keypad_eventqueue_record(key_number, current)


class KeyMatrix(_KeysBase):
    """Manage a 2D matrix of keys with row and column pins."""

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        row_pins,
        column_pins,
        columns_to_anodes=True,
        interval=0.02,
        max_events=64,
    ):
        """
        Create a `Keys` object that will scan the key matrix attached to the given row and
        column pins.
        There should not be any external pull-ups or pull-downs on the matrix:
        ``KeyMatrix`` enables internal pull-ups or pull-downs on the pins as necessary.

        The keys are numbered sequentially from zero. A key number can be computed
        by ``row * len(column_pins) + column``.

        An `EventQueue` is created when this object is created and is available in the `events`
        attribute.

        :param Sequence[microcontroller.Pin] row_pins: The pins attached to the rows.
        :param Sequence[microcontroller.Pin] column_pins: The pins attached to the colums.
        :param bool columns_to_anodes: Default ``True``.
          If the matrix uses diodes, the diode anodes are typically connected to the column pins,
          and the cathodes should be connected to the row pins. If your diodes are reversed,
          set ``columns_to_anodes`` to ``False``.
        :param float interval: Scan keys no more often than ``interval`` to allow for debouncing.
          ``interval`` is in float seconds. The default is 0.020 (20 msecs).
        :param int max_events: maximum size of `events` `EventQueue`:
          maximum number of key transition events that are saved.
          Must be >= 1.
          If a new event arrives when the queue is full, the oldest event is discarded.
        """
        self._row_digitalinouts = []
        for row_pin in row_pins:
            row_dio = digitalio.DigitalInOut(row_pin)
            row_dio.switch_to_input(
                pull=(digitalio.Pull.UP if columns_to_anodes else digitalio.Pull.DOWN)
            )
            self._row_digitalinouts.append(row_dio)

        self._column_digitalinouts = []
        for column_pin in column_pins:
            col_dio = digitalio.DigitalInOut(column_pin)
            col_dio.switch_to_input(
                pull=(digitalio.Pull.UP if columns_to_anodes else digitalio.Pull.DOWN)
            )
            self._column_digitalinouts.append(col_dio)
        self._currently_pressed = [False] * len(column_pins) * len(row_pins)
        self._previously_pressed = [False] * len(column_pins) * len(row_pins)
        self._columns_to_anodes = columns_to_anodes

        super().__init__(interval, max_events, self._keypad_keymatrix_scan)

    # pylint: enable=too-many-arguments

    @property
    def key_count(self):
        """The number of keys that are being scanned. (read-only)"""
        return len(self._row_digitalinouts) * len(self._column_digitalinouts)

    def deinit(self):
        """Stop scanning and release the pins."""
        super().deinit()
        for row_dio in self._row_digitalinouts:
            row_dio.deinit()
        for col_dio in self._column_digitalinouts:
            col_dio.deinit()

    def reset(self):
        """
        Reset the internal state of the scanner to assume that all keys are now released.
        Any key that is already pressed at the time of this call will therefore immediately cause
        a new key-pressed event to occur.
        """
        self._previously_pressed = self._currently_pressed = [False] * self.key_count

    def _row_column_to_key_number(self, row, column):
        return row * len(self._column_digitalinouts) + column

    def _keypad_keymatrix_scan(self):
        for row, row_dio in enumerate(self._row_digitalinouts):
            row_dio.switch_to_output(
                value=(not self._columns_to_anodes),
                drive_mode=digitalio.DriveMode.PUSH_PULL,
            )
            for col, col_dio in enumerate(self._column_digitalinouts):
                key_number = self._row_column_to_key_number(row, col)
                self._previously_pressed[key_number] = self._currently_pressed[
                    key_number
                ]
                current = col_dio.value != self._columns_to_anodes
                self._currently_pressed[key_number] = current
                if self._previously_pressed[key_number] != current:
                    self._events.keypad_eventqueue_record(key_number, current)
            row_dio.value = self._columns_to_anodes
            row_dio.switch_to_input(
                pull=(
                    digitalio.Pull.UP
                    if self._columns_to_anodes
                    else digitalio.Pull.DOWN
                )
            )


class ShiftRegisterKeys(_KeysBase):
    """Manage a set of keys attached to an incoming shift register."""

    def __init__(
        self,
        *,
        clock,
        data,
        latch,
        value_to_latch=True,
        key_count,
        value_when_pressed,
        interval=0.02,
        max_events=64,
    ):
        """
        Create a `Keys` object that will scan keys attached to a parallel-in serial-out
        shift register like the 74HC165 or CD4021.
        Note that you may chain shift registers to load in as many values as you need.

        Key number 0 is the first (or more properly, the zero-th) bit read. In the
        74HC165, this bit is labeled ``Q7``. Key number 1 will be the value of ``Q6``, etc.

        An `EventQueue` is created when this object is created and is available in the
        `events` attribute.

        :param microcontroller.Pin clock: The shift register clock pin.
          The shift register should clock on a low-to-high transition.
        :param microcontroller.Pin data: the incoming shift register data pin
        :param microcontroller.Pin latch:
          Pin used to latch parallel data going into the shift register.
        :param bool value_to_latch: Pin state to latch data being read.
          ``True`` if the data is latched when ``latch`` goes high
          ``False`` if the data is latched when ``latch goes low.
          The default is ``True``, which is how the 74HC165 operates. The CD4021 latch is
          the opposite. Once the data is latched, it will be shifted out by toggling the
          clock pin.
        :param int key_count: number of data lines to clock in
        :param bool value_when_pressed: ``True`` if the pin reads high when the key is pressed.
          ``False`` if the pin reads low (is grounded) when the key is pressed.
        :param float interval: Scan keys no more often than ``interval`` to allow for debouncing.
          ``interval`` is in float seconds. The default is 0.020 (20 msecs).
        :param int max_events: maximum size of `events` `EventQueue`:
          maximum number of key transition events that are saved.
          Must be >= 1.
          If a new event arrives when the queue is full, the oldest event is discarded.
        """
        clock_dio = digitalio.DigitalInOut(clock)
        clock_dio.switch_to_output(
            value=False, drive_mode=digitalio.DriveMode.PUSH_PULL
        )
        self._clock = clock_dio

        data_dio = digitalio.DigitalInOut(data)
        data_dio.switch_to_input()
        self._data = data_dio

        latch_dio = digitalio.DigitalInOut(latch)
        latch_dio.switch_to_output(value=True, drive_mode=digitalio.DriveMode.PUSH_PULL)
        self._latch = latch_dio
        self._value_to_latch = value_to_latch

        self._currently_pressed = [False] * key_count
        self._previously_pressed = [False] * key_count
        self._value_when_pressed = value_when_pressed
        self._key_count = key_count

        super().__init__(interval, max_events, self._keypad_shiftregisterkeys_scan)

    def deinit(self):
        """Stop scanning and release the pins."""
        super().deinit()
        self._clock.deinit()
        self._data.deinit()
        self._latch.deinit()

    def reset(self):
        """
        Reset the internal state of the scanner to assume that all keys are now released.
        Any key that is already pressed at the time of this call will therefore immediately cause
        a new key-pressed event to occur.
        """
        self._currently_pressed = self._previously_pressed = [False] * self._key_count

    @property
    def key_count(self):
        """The number of keys that are being scanned. (read-only)"""
        return self._key_count

    @property
    def events(self):
        """The ``EventQueue`` associated with this `Keys` object. (read-only)"""
        return self._events

    def _keypad_shiftregisterkeys_scan(self):
        self._latch.value = self._value_to_latch
        for key_number in range(self._key_count):
            self._clock.value = False
            self._previously_pressed[key_number] = self._currently_pressed[key_number]
            current = self._data.value == self._value_when_pressed
            self._currently_pressed[key_number] = current
            self._clock.value = True
            if self._previously_pressed[key_number] != current:
                self._events.keypad_eventqueue_record(key_number, current)

        self._latch.value = not self._value_to_latch
