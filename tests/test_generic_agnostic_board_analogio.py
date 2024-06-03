# SPDX-FileCopyrightText: 2024 Brent Rubell for Adafruit Industries
#
# SPDX-License-Identifier: MIT
import pytest  # pylint: disable=unused-import
import board
import analogio


# Analog Outputs
def test_Ax_OUTPUT():
    """Test analog output pin functionality."""
    assert board.board_id == "OS_AGNOSTIC_BOARD"
    pin_out = analogio.AnalogOut(board.Ax_OUTPUT)

    # Test boundaries of setting the value and reading it back
    pin_out.value = 0
    assert pin_out.value == 0
    pin_out.value = 65535
    assert pin_out.value == 65535

    pin_out.deinit()


# Analog Inputs

# Values for sine wave
# (data points = 20, amplitude=100, frequency=1)
sine_wave = [
    0,
    31,
    59,
    81,
    95,
    100,
    95,
    81,
    59,
    31,
    0,
    -31,
    -59,
    -81,
    -95,
    -100,
    -95,
    -81,
    -59,
    -31,
]

# Values for a sawtooth wave
# (data points = 20, amplitude=100)
sawtooth_wave = [
    -100,
    -80,
    -60,
    -40,
    -20,
    0,
    20,
    40,
    60,
    80,
    -100,
    -80,
    -60,
    -40,
    -20,
    0,
    20,
    40,
    60,
    80,
]


def test_Ax_INPUT_RAND_INT():
    """Test random integer from pin Ax_INPUT_RAND_INT"""
    assert board.board_id == "OS_AGNOSTIC_BOARD"
    pin_random = analogio.AnalogIn(board.Ax_INPUT_RAND_INT)

    assert isinstance(pin_random.value, int)

    pin_random.deinit()


def test_Ax_INPUT_FIXED_INT_PI():
    """Test fixed integer from pin Ax_INPUT_FIXED_INT_PI"""
    assert board.board_id == "OS_AGNOSTIC_BOARD"
    pin_pi = analogio.AnalogIn(board.Ax_INPUT_FIXED_INT_PI)

    assert pin_pi.value == 31415

    pin_pi.deinit()


def test_Ax_INPUT_WAVE_SINE():
    """Test sine wave from pin Ax_INPUT_WAVE_SINE"""
    assert board.board_id == "OS_AGNOSTIC_BOARD"
    pin_sine_wave = analogio.AnalogIn(board.Ax_INPUT_WAVE_SINE)

    # Run through the sine wave once
    for expected_value in sine_wave:
        assert pin_sine_wave.value == expected_value

    # Run through the sine wave again to ensure it loops back correctly
    for expected_value in sine_wave:
        assert pin_sine_wave.value == expected_value

    pin_sine_wave.deinit()


def test_Ax_INPUT_WAVE_SAW():
    """Test sawtooth wave from pin Ax_INPUT_WAVE_SAW"""
    assert board.board_id == "OS_AGNOSTIC_BOARD"
    pin_saw_wave = analogio.AnalogIn(board.Ax_INPUT_WAVE_SAW)

    # Run through the sine wave once
    for expected_value in sawtooth_wave:
        assert pin_saw_wave.value == expected_value

    # Run through the sine wave again to ensure it loops back correctly
    for expected_value in sawtooth_wave:
        assert pin_saw_wave.value == expected_value

    pin_saw_wave.deinit()
