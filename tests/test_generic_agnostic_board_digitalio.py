# SPDX-FileCopyrightText: 2024 Brent Rubell for Adafruit Industries
#
# SPDX-License-Identifier: MIT
import pytest  # pylint: disable=unused-import
import board
import digitalio

# Digital output pins


def test_Dx_OUTPUT_TRUE():
    """Test digital output pin functionality."""
    assert board.board_id == "OS_AGNOSTIC_BOARD"
    pin_out = digitalio.DigitalInOut(board.Dx_OUTPUT)
    pin_out.direction = digitalio.Direction.OUTPUT
    # Test setting the value and reading it back
    pin_out.value = True
    assert pin_out.value is True
    pin_out.value = False
    assert pin_out.value is True
    pin_out.deinit()


# Digital Input Pins


def test_Dx_INPUT_TRUE():
    """Test digital input pin Dx_INPUT_TRUE."""
    assert board.board_id == "OS_AGNOSTIC_BOARD"
    pin_true = digitalio.DigitalInOut(board.Dx_INPUT_TRUE)
    pin_true.direction = digitalio.Direction.INPUT
    assert pin_true.value is True
    assert pin_true.value is True  # Test subsequent call does not change value
    pin_true.deinit()


def test_Dx_INPUT_TRUE_PULL_DOWN():
    """Test digital input pin Dx_INPUT_TRUE w/pull down."""
    assert board.board_id == "OS_AGNOSTIC_BOARD"
    pin_true = digitalio.DigitalInOut(board.Dx_INPUT_TRUE)
    pin_true.direction = digitalio.Direction.INPUT
    assert pin_true.value is True
    assert pin_true.value is True  # Test subsequent call does not change value
    pin_true.pull = digitalio.Pull.DOWN
    assert pin_true.value is False
    pin_true.deinit()


def test_Dx_INPUT_FALSE_PULL_UP():
    """Test digital input pin Dx_INPUT_FALSE w/pull up."""
    assert board.board_id == "OS_AGNOSTIC_BOARD"
    pin_false = digitalio.DigitalInOut(board.Dx_INPUT_FALSE)
    pin_false.direction = digitalio.Direction.INPUT
    assert pin_false.value is False
    assert pin_false.value is False  # Test subsequent call does not change value
    pin_false.pull = digitalio.Pull.UP
    assert pin_false.value is False
    pin_false.deinit()


def test_Dx_INPUT_FALSE():
    """Test digital input pin Dx_INPUT_FALSE"""
    assert board.board_id == "OS_AGNOSTIC_BOARD"
    pin_false = digitalio.DigitalInOut(board.Dx_INPUT_FALSE)
    pin_false.direction = digitalio.Direction.INPUT
    assert pin_false.value is False
    assert pin_false.value is False  # Test subsequent call does not change value
    pin_false.deinit()


def test_Dx_INPUT_TOGGLE():
    """Test digital input pin Dx_INPUT_TOGGLE"""
    assert board.board_id == "OS_AGNOSTIC_BOARD"
    pin_toggle = digitalio.DigitalInOut(board.Dx_INPUT_TOGGLE)
    pin_toggle.direction = digitalio.Direction.INPUT
    assert pin_toggle.value is True
    assert (
        pin_toggle.value is False
    )  # Test subsequent call does change value for this pin
    pin_toggle.deinit()
