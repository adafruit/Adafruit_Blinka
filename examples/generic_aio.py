import pytest
import board
import analogio

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

def test_ax_input_rand_int():
  assert board.board_id == "GENERIC_AGNOSTIC_BOARD"
  pin_random = analogio.AnalogIn(board.Ax_INPUT_RAND_INT)

  assert isinstance(pin_random.value, int)

  pin_random.deinit()

def test_ax_input_fixed_int_pi():
  assert board.board_id == "GENERIC_AGNOSTIC_BOARD"
  pin_pi = analogio.AnalogIn(board.Ax_INPUT_FIXED_INT_PI)

  assert pin_pi.value == 31415

  pin_pi.deinit()

def test_ax_input_sine_wave():
  assert board.board_id == "GENERIC_AGNOSTIC_BOARD"
  pin_sine_wave = analogio.AnalogIn(board.Ax_OUTPUT_WAVE_SINE)

  # Run through the sine wave once
  for i in range(len(sine_wave)):
    assert pin_sine_wave.value == sine_wave[i]

  # Run through the sine wave again to ensure it loops back correctly
  for i in range(len(sine_wave)):
    assert pin_sine_wave.value == sine_wave[i]

  pin_sine_wave.deinit()
