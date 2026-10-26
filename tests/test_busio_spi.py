# SPDX-FileCopyrightText: 2026 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""Public SPI transfer arguments without board detection or hardware access."""

import importlib.util
import inspect
import sys
from pathlib import Path
from types import ModuleType, SimpleNamespace

import pytest

import adafruit_blinka

# Pytest supplies the named fixture.
# pylint: disable=redefined-outer-name


class RecordingSPI:
    """Record raw forwarding, with optional backend read data or exceptions."""

    def __init__(self):
        self.calls = []
        self.result = object()
        self.error = None
        self.read_data = None

    def _record(self, name, args, kwargs, read_buffer=None):
        self.calls.append(SimpleNamespace(name=name, args=args, kwargs=kwargs))
        if self.error is not None:
            raise self.error
        if read_buffer is not None and self.read_data is not None:
            read_buffer[:] = self.read_data
        return self.result

    # Backend buffer names deliberately retain the legacy spellings. Record the
    # remaining arguments raw so positional versus keyword forwarding is tested.
    def write(self, buf, *args, **kwargs):
        return self._record("write", (buf, *args), kwargs)

    def readinto(self, buf, *args, **kwargs):
        return self._record("readinto", (buf, *args), kwargs, read_buffer=buf)

    def write_readinto(self, buffer_out, buffer_in, *args, **kwargs):
        return self._record(
            "write_readinto",
            (buffer_out, buffer_in, *args),
            kwargs,
            read_buffer=buffer_in,
        )


@pytest.fixture
def spi(monkeypatch):
    """Load the real wrapper with an inert detector and recording backend."""
    agnostic = ModuleType("adafruit_blinka.agnostic")
    agnostic.board_id = "TEST_BOARD"
    agnostic.detector = SimpleNamespace()
    monkeypatch.setitem(sys.modules, "adafruit_blinka.agnostic", agnostic)
    monkeypatch.setattr(adafruit_blinka, "agnostic", agnostic, raising=False)
    path = Path(__file__).parents[1] / "src/busio.py"
    spec = importlib.util.spec_from_file_location("_test_spi_busio", path)
    module = importlib.util.module_from_spec(spec)
    monkeypatch.setitem(sys.modules, spec.name, module)
    spec.loader.exec_module(module)
    instance = object.__new__(module.SPI)
    instance._spi = RecordingSPI()  # pylint: disable=protected-access
    return instance


@pytest.mark.parametrize(
    "method, required, defaults",
    [
        ("write", ["buffer"], {"start": 0, "end": None}),
        ("readinto", ["buffer"], {"start": 0, "end": None, "write_value": 0}),
        (
            "write_readinto",
            ["out_buffer", "in_buffer"],
            {"out_start": 0, "out_end": None, "in_start": 0, "in_end": None},
        ),
    ],
)
def test_transfer_signatures(spi, method, required, defaults):
    parameters = inspect.signature(getattr(spi, method)).parameters
    assert list(parameters) == required + list(defaults)
    for name in required:
        assert parameters[name].kind == inspect.Parameter.POSITIONAL_OR_KEYWORD
        assert parameters[name].default is inspect.Parameter.empty
    for name, default in defaults.items():
        assert parameters[name].kind == inspect.Parameter.POSITIONAL_OR_KEYWORD
        assert parameters[name].default is default


@pytest.mark.parametrize("method", ["write", "readinto", "write_readinto"])
@pytest.mark.parametrize("use_keywords", [False, True])
def test_default_arguments_accept_keywords_and_positionals(spi, method, use_keywords):
    out_buffer = bytearray(b"abcd")
    in_buffer = bytearray(6)
    if method == "write_readinto":
        buffers = (out_buffer, in_buffer)
        keywords = {"out_buffer": out_buffer, "in_buffer": in_buffer}
        ranges = (0, None, 0, None)
    else:
        buffers = (out_buffer,)
        keywords = {"buffer": out_buffer}
        ranges = (0, None)
    transfer = getattr(spi, method)
    result = transfer(**keywords) if use_keywords else transfer(*buffers)

    backend = spi._spi  # pylint: disable=protected-access
    assert result is backend.result
    assert len(backend.calls) == 1
    call = backend.calls[0]
    assert call.name == method
    assert call.args == buffers + ranges
    assert all(actual is expected for actual, expected in zip(call.args, buffers))
    assert call.kwargs == ({"write_value": 0} if method == "readinto" else {})
    assert out_buffer == b"abcd"
    assert in_buffer == bytearray(6)


@pytest.mark.parametrize("method", ["write", "readinto"])
@pytest.mark.parametrize(
    "start, end",
    [(0, None), (1, 3), (2, None), (-3, -1), (0, 99), (-99, 99), (9, 12), (2, 2)],
)
def test_single_transfer_forwards_ranges_without_slicing(spi, method, start, end):
    buffer = bytearray(b"abcd")
    kwargs = {"buffer": buffer, "start": start, "end": end}
    if method == "readinto":
        kwargs["write_value"] = 0xA6
    result = getattr(spi, method)(**kwargs)

    backend = spi._spi  # pylint: disable=protected-access
    assert result is backend.result
    assert len(backend.calls) == 1
    call = backend.calls[0]
    assert call.name == method
    assert call.args[0] is buffer
    assert call.args[1:] == (start, end)
    assert call.kwargs == ({"write_value": 0xA6} if method == "readinto" else {})
    assert buffer == b"abcd"


@pytest.mark.parametrize(
    "out_start, out_end, in_start, in_end",
    [
        (0, None, 0, None),
        (1, 3, 2, 5),
        (1, None, 2, None),
        (-3, -1, -4, -2),
        (0, 99, -99, 99),
        (9, 12, 11, 15),
        (2, 2, 4, 4),
    ],
)
def test_duplex_transfer_forwards_independent_ranges(
    spi, out_start, out_end, in_start, in_end
):
    out_buffer = bytearray(b"abcd")
    in_buffer = bytearray(b"012345")
    result = spi.write_readinto(
        out_buffer=out_buffer,
        in_buffer=in_buffer,
        out_start=out_start,
        out_end=out_end,
        in_start=in_start,
        in_end=in_end,
    )

    backend = spi._spi  # pylint: disable=protected-access
    assert result is backend.result
    assert len(backend.calls) == 1
    call = backend.calls[0]
    assert call.name == "write_readinto"
    assert call.args[0] is out_buffer
    assert call.args[1] is in_buffer
    assert call.args[2:] == (out_start, out_end, in_start, in_end)
    assert call.kwargs == {}
    assert out_buffer == b"abcd"
    assert in_buffer == b"012345"


@pytest.mark.parametrize(
    "method, optional, expected_kwargs",
    [
        ("write", (1, 3), {}),
        ("readinto", (1, 3, 0x96), {"write_value": 0x96}),
        ("write_readinto", (1, 4, 2, None), {}),
    ],
)
def test_all_optional_arguments_remain_positional(
    spi, method, optional, expected_kwargs
):
    buffer = bytearray(b"abcd")
    buffers = (buffer, bytearray(6)) if method == "write_readinto" else (buffer,)
    result = getattr(spi, method)(*buffers, *optional)

    backend = spi._spi  # pylint: disable=protected-access
    assert result is backend.result
    assert len(backend.calls) == 1
    call = backend.calls[0]
    ranges = optional[:-1] if method == "readinto" else optional
    assert call.args == buffers + ranges
    assert all(actual is expected for actual, expected in zip(call.args, buffers))
    assert call.kwargs == expected_kwargs


@pytest.mark.parametrize("write_value", [0, 0xA6, 0xFF])
def test_readinto_preserves_backend_mutation_and_write_value(spi, write_value):
    buffer = bytearray(4)
    backend = spi._spi  # pylint: disable=protected-access
    backend.read_data = b"\xa5\x10\x20\x30"
    result = spi.readinto(buffer=buffer, write_value=write_value)

    assert result is backend.result
    assert len(backend.calls) == 1
    call = backend.calls[0]
    assert call.args[0] is buffer
    assert call.args[1:] == (0, None)
    assert call.kwargs == {"write_value": write_value}
    assert buffer == backend.read_data


@pytest.mark.parametrize("shared", [False, True])
@pytest.mark.parametrize("original", [b"abcd", b""])
def test_duplex_preserves_distinct_shared_and_empty_buffers(spi, shared, original):
    out_buffer = bytearray(original)
    in_buffer = out_buffer if shared else bytearray(len(original))
    backend = spi._spi  # pylint: disable=protected-access
    backend.read_data = b"\xa5" * len(original)
    result = spi.write_readinto(out_buffer=out_buffer, in_buffer=in_buffer)

    assert result is backend.result
    assert len(backend.calls) == 1
    call = backend.calls[0]
    assert call.args[0] is out_buffer
    assert call.args[1] is in_buffer
    assert call.args[2:] == (0, None, 0, None)
    assert call.kwargs == {}
    assert in_buffer == backend.read_data
    assert out_buffer == (backend.read_data if shared else original)


@pytest.mark.parametrize("method", ["write", "readinto"])
def test_empty_single_buffers_still_reach_backend(spi, method):
    buffer = bytearray()
    backend = spi._spi  # pylint: disable=protected-access
    assert getattr(spi, method)(buffer=buffer) is backend.result
    assert len(backend.calls) == 1
    assert backend.calls[0].args[0] is buffer


@pytest.mark.parametrize("method", ["write", "readinto", "write_readinto"])
@pytest.mark.parametrize(
    "error", [ValueError("invalid range"), OSError("SPI transfer")]
)
def test_backend_exception_identity_is_preserved(spi, method, error):
    backend = spi._spi  # pylint: disable=protected-access
    backend.error = error
    backend.read_data = b"\xa5\xa5"
    buffer = bytearray(2)
    buffers = (buffer, buffer) if method == "write_readinto" else (buffer,)
    with pytest.raises(type(error)) as raised:
        getattr(spi, method)(*buffers)
    assert raised.value is error
    assert len(backend.calls) == 1
    assert all(
        actual is expected for actual, expected in zip(backend.calls[0].args, buffers)
    )
    assert buffer == bytearray(2)


@pytest.mark.parametrize(
    "method, legacy_name, public_name",
    [
        ("write", "buf", "buffer"),
        ("readinto", "buf", "buffer"),
        ("write_readinto", "buffer_out", "out_buffer"),
        ("write_readinto", "buffer_in", "in_buffer"),
    ],
)
def test_legacy_buffer_keywords_are_not_aliases(spi, method, legacy_name, public_name):
    kwargs = (
        {"out_buffer": b"\x00", "in_buffer": bytearray(1)}
        if method == "write_readinto"
        else {"buffer": bytearray(1)}
    )
    kwargs[legacy_name] = kwargs.pop(public_name)
    with pytest.raises(TypeError, match=f"unexpected keyword argument '{legacy_name}'"):
        getattr(spi, method)(**kwargs)
    assert not spi._spi.calls  # pylint: disable=protected-access
