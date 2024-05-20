import pytest
import board
import analogio

def test_ax_input_rand_int():
  assert board.board_id == "GENERIC_AGNOSTIC_BOARD"
  pin_random = analogio.AnalogIn(board.Ax_INPUT_RAND_INT)
  assert isinstance(pin_random.value, int)
  pin_random.deinit()
