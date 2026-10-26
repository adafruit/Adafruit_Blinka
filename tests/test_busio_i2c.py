# SPDX-FileCopyrightText: 2026 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""Public I2C transfer arguments without board detection or hardware access."""

import importlib.util
import inspect
import sys
from pathlib import Path
from types import ModuleType, SimpleNamespace

import pytest

import adafruit_blinka

# Pytest supplies the named fixture.
# pylint: disable=redefined-outer-name


class RecordingBackend:
    """Record the wrapper boundary while simulating writes into caller buffers."""

    def __init__(self):
        self.calls = []
        self.result = object()
        self.error = None

    def _record(self, name, address, *buffers, **kwargs):
        call = SimpleNamespace(
            name=name, address=address, buffers=buffers, kwargs=kwargs
        )
        self.calls.append(call)
        if self.error is not None:
            raise self.error
        return call

    def readfrom_into(self, address, buffer, *, stop):
        self._record("readfrom_into", address, buffer, stop=stop)
        buffer[:] = b"\xa5" * len(buffer)
        return self.result

    def writeto(self, address, buffer, *, stop):
        call = self._record("writeto", address, buffer, stop=stop)
        call.written = bytes(buffer)
        return self.result

    def writeto_then_readfrom(  # pylint: disable=too-many-arguments
        self,
        address,
        buffer_out,
        buffer_in,
        *,
        out_start,
        out_end,
        in_start,
        in_end,
        stop,
    ):
        # Backend names deliberately differ from the public CircuitPython names.
        call = self._record(
            "writeto_then_readfrom",
            address,
            buffer_out,
            buffer_in,
            out_start=out_start,
            out_end=out_end,
            in_start=in_start,
            in_end=in_end,
            stop=stop,
        )
        call.written = bytes(memoryview(buffer_out)[out_start:out_end])
        view = memoryview(buffer_in)[in_start:in_end]
        view[:] = b"\xa5" * len(view)
        return self.result


@pytest.fixture
def i2c(monkeypatch):
    """Load the real wrapper with an inert detector and recording backend."""
    agnostic = ModuleType("adafruit_blinka.agnostic")
    agnostic.board_id = "TEST_BOARD"
    agnostic.detector = SimpleNamespace()
    monkeypatch.setitem(sys.modules, "adafruit_blinka.agnostic", agnostic)
    monkeypatch.setattr(adafruit_blinka, "agnostic", agnostic, raising=False)
    path = Path(__file__).parents[1] / "src/busio.py"
    spec = importlib.util.spec_from_file_location("_test_i2c_busio", path)
    module = importlib.util.module_from_spec(spec)
    monkeypatch.setitem(sys.modules, spec.name, module)
    spec.loader.exec_module(module)
    instance = object.__new__(module.I2C)
    instance._i2c = RecordingBackend()  # pylint: disable=protected-access
    return instance


@pytest.mark.parametrize(
    "method, positional, defaults",
    [
        ("readfrom_into", ["address", "buffer"], {"start": 0, "end": None}),
        ("writeto", ["address", "buffer"], {"start": 0, "end": None}),
        (
            "writeto_then_readfrom",
            ["address", "out_buffer", "in_buffer"],
            {
                "out_start": 0,
                "out_end": None,
                "in_start": 0,
                "in_end": None,
                "stop": False,
            },
        ),
    ],
)
def test_transfer_signatures(i2c, method, positional, defaults):
    parameters = inspect.signature(getattr(i2c, method)).parameters
    assert list(parameters) == positional + list(defaults)
    for name in positional:
        assert parameters[name].kind == inspect.Parameter.POSITIONAL_OR_KEYWORD
        assert parameters[name].default is inspect.Parameter.empty
    for name, default in defaults.items():
        assert parameters[name].kind == inspect.Parameter.KEYWORD_ONLY
        assert parameters[name].default is default


@pytest.mark.parametrize("use_keywords", [False, True])
def test_combined_transfer_default_arguments(i2c, use_keywords):
    out_buffer = bytearray(b"\x10\x20\x30")
    in_buffer = bytearray(3)
    if use_keywords:
        result = i2c.writeto_then_readfrom(
            address=0x40, out_buffer=out_buffer, in_buffer=in_buffer
        )
    else:
        result = i2c.writeto_then_readfrom(0x40, out_buffer, in_buffer)

    backend = i2c._i2c  # pylint: disable=protected-access
    assert result is backend.result
    assert len(backend.calls) == 1
    call = backend.calls[0]
    assert call.address == 0x40
    assert call.buffers[0] is out_buffer
    assert call.buffers[1] is in_buffer
    assert call.kwargs == {
        "out_start": 0,
        "out_end": None,
        "in_start": 0,
        "in_end": None,
        "stop": False,
    }
    assert call.written == out_buffer
    assert in_buffer == b"\xa5\xa5\xa5"


@pytest.mark.parametrize("stop", [False, True])
@pytest.mark.parametrize("start, end", [(1, 3), (1, None), (-3, -1), (0, 99), (2, 2)])
def test_combined_transfer_forwards_slices_and_stop(i2c, start, end, stop):
    out_buffer = bytearray(b"\x10\x20\x30\x40")
    in_buffer = bytearray(b"abcd")
    expected = bytearray(in_buffer)
    expected[start:end] = b"\xa5" * len(expected[start:end])
    result = i2c.writeto_then_readfrom(
        address=0x40,
        out_buffer=out_buffer,
        in_buffer=in_buffer,
        out_start=start,
        out_end=end,
        in_start=start,
        in_end=end,
        stop=stop,
    )

    backend = i2c._i2c  # pylint: disable=protected-access
    call = backend.calls[0]
    assert result is backend.result
    assert call.buffers[0] is out_buffer
    assert call.buffers[1] is in_buffer
    assert call.kwargs == {
        "out_start": start,
        "out_end": end,
        "in_start": start,
        "in_end": end,
        "stop": stop,
    }
    assert call.written == out_buffer[start:end]
    assert in_buffer == expected


def test_combined_transfer_with_shared_buffer(i2c):
    buffer = bytearray(b"\x10\x20\x30\x40")
    i2c.writeto_then_readfrom(
        0x40, out_buffer=buffer, in_buffer=buffer, out_end=2, in_start=1, in_end=3
    )
    call = i2c._i2c.calls[0]  # pylint: disable=protected-access
    assert call.buffers[0] is buffer
    assert call.buffers[1] is buffer
    assert call.written == b"\x10\x20"
    assert buffer == b"\x10\xa5\xa5\x40"


@pytest.mark.parametrize("method", ["readfrom_into", "writeto"])
@pytest.mark.parametrize("start, end", [(0, None), (1, 3), (1, None), (-3, -1), (2, 2)])
def test_single_transfer_buffer_keyword_and_slicing(i2c, method, start, end):
    buffer = bytearray(b"abcd")
    expected = bytearray(buffer)
    expected_written = bytes(buffer[start:end])
    if method == "readfrom_into":
        expected[start:end] = b"\xa5" * len(expected[start:end])
    result = getattr(i2c, method)(address=0x40, buffer=buffer, start=start, end=end)

    backend = i2c._i2c  # pylint: disable=protected-access
    call = backend.calls[0]
    assert result is backend.result
    assert call.name == method
    assert call.address == 0x40
    assert call.kwargs == {"stop": True}
    if start == 0 and end is None:
        assert call.buffers[0] is buffer
    else:
        assert isinstance(call.buffers[0], memoryview)
        assert call.buffers[0].obj is buffer
    if method == "writeto":
        assert call.written == expected_written
    assert buffer == expected


def test_writeto_string_conversion_is_preserved(i2c):
    i2c.writeto(address=0x40, buffer="abcd", start=1, end=3)
    call = i2c._i2c.calls[0]  # pylint: disable=protected-access
    assert call.written == b"bc"


@pytest.mark.parametrize(
    "method", ["readfrom_into", "writeto", "writeto_then_readfrom"]
)
def test_empty_buffers_still_reach_backend(i2c, method):
    buffer = bytearray()
    args = (
        (0x40, buffer, buffer) if method == "writeto_then_readfrom" else (0x40, buffer)
    )
    backend = i2c._i2c  # pylint: disable=protected-access
    assert getattr(i2c, method)(*args) is backend.result
    assert len(backend.calls) == 1
    assert all(item is buffer for item in backend.calls[0].buffers)


@pytest.mark.parametrize(
    "method", ["readfrom_into", "writeto", "writeto_then_readfrom"]
)
@pytest.mark.parametrize("error", [ValueError("invalid address"), OSError("I2C NACK")])
def test_backend_address_validation_and_errors_are_preserved(i2c, method, error):
    backend = i2c._i2c  # pylint: disable=protected-access
    backend.error = error
    address = -1
    buffer = bytearray(2)
    args = (
        (address, buffer, buffer)
        if method == "writeto_then_readfrom"
        else (address, buffer)
    )
    with pytest.raises(type(error)) as raised:
        getattr(i2c, method)(*args)
    assert raised.value is error
    assert len(backend.calls) == 1
    assert backend.calls[0].address == address
    assert buffer == bytearray(2)


@pytest.mark.parametrize("legacy_name", ["buffer_out", "buffer_in"])
def test_legacy_combined_transfer_keywords_are_not_aliases(i2c, legacy_name):
    kwargs = {"out_buffer": b"\x00", "in_buffer": bytearray(1)}
    kwargs[legacy_name] = kwargs.pop(
        "out_buffer" if legacy_name == "buffer_out" else "in_buffer"
    )
    with pytest.raises(TypeError, match="unexpected keyword argument"):
        i2c.writeto_then_readfrom(0x40, **kwargs)
    assert not i2c._i2c.calls  # pylint: disable=protected-access
