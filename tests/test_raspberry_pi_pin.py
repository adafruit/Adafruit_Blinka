# SPDX-FileCopyrightText: 2026 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""Recording gpiod fakes: no hardware, subprocesses or native GPIO requests."""

# Pytest injects named fixtures; ownership checks intentionally inspect backend handles.
# pylint: disable=redefined-outer-name,protected-access

import importlib
import importlib.util
import sys
from enum import Enum
from pathlib import Path
from types import ModuleType, SimpleNamespace

import pytest

PREFIX = "adafruit_blinka.microcontroller.generic_linux"
SOURCE = Path(__file__).parents[1] / "src"


def load_source(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def make_pin(monkeypatch, version="2", *, backend="raspberry_pi_pin", legacy=False):
    # One fake factory keeps all three binding APIs under the same recording state.
    # pylint: disable=too-many-locals
    library = ModuleType("gpiod")
    library.__version__ = "2.5.0" if version == "2" else "1.6.3"
    state = SimpleNamespace(
        devices={3: ("pinctrl-rp1", 54)},
        chips=[],
        requests=[],
        opens=0,
        fail_open=None,
        fail_request=False,
        fail_config=False,
        fail_release=False,
        fail_close=False,
        fail_write=False,
    )

    class Value(Enum):
        INACTIVE = 0
        ACTIVE = 1

    class Direction(Enum):
        AS_IS = 0
        INPUT = 1
        OUTPUT = 2

    class Bias(Enum):
        AS_IS = 0
        PULL_UP = 1
        PULL_DOWN = 2
        DISABLED = 3

    class Settings:  # pylint: disable=too-few-public-methods
        # Match the binding's mutable settings container, not a behavior-rich class.
        def __init__(self):
            self.direction = Direction.AS_IS
            self.bias = Bias.AS_IS
            self.output_value = Value.INACTIVE

    class Request:
        def __init__(self, chip, offset):
            self.chip, self.offset = chip, offset
            self.live = True
            self.value = Value.INACTIVE
            self.configurations = []
            self.release_calls = 0
            state.requests.append(self)

        def reconfigure_lines(self, config):
            if state.fail_config:
                raise OSError("configuration failed")
            settings = config[self.offset]
            self.configurations.append(settings)
            if settings.direction is Direction.OUTPUT:
                self.value = settings.output_value

        def get_value(self, offset):
            assert offset == self.offset
            return self.value

        def set_value(self, offset, value):
            assert offset == self.offset
            if state.fail_write:
                raise OSError("write failed")
            self.value = value

        def release(self):
            self.release_calls += 1
            self.live = False
            if state.fail_release:
                raise OSError("release failed")

    class Line(Request):
        # The 1.x line API omits the offset required by the 2.x request API.
        # pylint: disable=arguments-differ
        def request(self, config=None, **kwargs):
            if state.fail_request:
                raise OSError("request failed")
            if config is not None:
                assert legacy
                assert "default_vals" not in kwargs
                kwargs.update(
                    consumer=config.consumer,
                    type=config.request_type,
                    flags=config.flags,
                )
            else:
                assert not legacy
                assert "default_val" not in kwargs
            self.live = True
            self.configurations.append(kwargs)
            if kwargs["type"] == 2:
                initial = kwargs.get("default_val", kwargs.get("default_vals", [0])[0])
                self.value = Value(initial)

        def get_value(self):
            return self.value.value

        def set_value(self, value):
            if state.fail_write:
                raise OSError("write failed")
            self.value = Value(value)

    class Chip:
        OPEN_BY_NUMBER = 1
        OPEN_BY_NAME = 2

        def __init__(self, path, mode=None):
            state.opens += 1
            if state.opens == state.fail_open:
                raise PermissionError("open failed")
            self.index = int(Path(path).name.removeprefix("gpiochip"))
            self.path = path
            self.open_mode = mode
            self.closed = False
            self.close_calls = 0
            state.chips.append(self)
            if mode is not None:
                assert mode in (self.OPEN_BY_NUMBER, self.OPEN_BY_NAME)

        def get_info(self):
            label, count = state.devices[self.index]
            return SimpleNamespace(label=label, num_lines=count)

        def label(self):
            return self.get_info().label

        def num_lines(self):
            return self.get_info().num_lines

        def request_lines(self, *, config, consumer):
            assert consumer == "adafruit_blinka"
            if state.fail_request:
                raise OSError("request failed")
            return Request(self, next(iter(config)))

        def get_line(self, offset):
            return Line(self, offset)

        def close(self):
            self.closed = True
            self.close_calls += 1
            if state.fail_close:
                raise OSError("close failed")

    class LegacyRequest:  # pylint: disable=too-few-public-methods
        DIRECTION_INPUT = 1
        DIRECTION_OUTPUT = 2
        FLAG_BIAS_PULL_UP = 4
        FLAG_BIAS_PULL_DOWN = 8
        FLAG_BIAS_DISABLE = 16

        def __init__(self):
            self.consumer = ""
            self.request_type = None
            self.flags = 0

    library.Chip = Chip
    library.LineSettings = Settings
    library.line = SimpleNamespace(Value=Value, Direction=Direction, Bias=Bias)
    library.LINE_REQ_DIR_IN = 1
    library.LINE_REQ_DIR_OUT = 2
    library.LINE_REQ_FLAG_BIAS_PULL_UP = 4
    library.LINE_REQ_FLAG_BIAS_PULL_DOWN = 8
    library.LINE_REQ_FLAG_BIAS_DISABLE = 16
    if legacy:
        assert version == "1"
        del library.Chip
        del library.__version__
        del library.LINE_REQ_DIR_IN
        del library.LINE_REQ_DIR_OUT
        del library.LINE_REQ_FLAG_BIAS_PULL_UP
        del library.LINE_REQ_FLAG_BIAS_PULL_DOWN
        del library.LINE_REQ_FLAG_BIAS_DISABLE
        # PyPI's legacy binding uses reset(), not the official binding's close(),
        # and exposes metadata as properties rather than methods.
        Chip.reset = Chip.close
        del Chip.close
        Chip.label = property(lambda self: self.get_info().label)
        Chip.num_lines = property(lambda self: self.get_info().num_lines)
        library.chip = Chip
        library.line_request = LegacyRequest
    monkeypatch.setitem(sys.modules, "gpiod", library)
    for name in list(sys.modules):
        if name == PREFIX + ".raspberry_pi_pin" or name.startswith(
            PREFIX + ".libgpiod"
        ):
            monkeypatch.delitem(sys.modules, name)
    module = importlib.import_module(PREFIX + "." + backend)
    if backend == "raspberry_pi_pin":
        state.filesystem_chip_paths = module._chip_paths
        monkeypatch.setattr(
            module,
            "_chip_paths",
            lambda: [Path(f"/dev/gpiochip{n}") for n in sorted(state.devices)],
        )
    return module, state, library


@pytest.fixture
def pins(monkeypatch):
    return make_pin(monkeypatch)


def test_integer_identity_constructor_does_not_open_hardware(pins):
    module, state, _ = pins
    pin = module.Pin(18)
    # Bool is an int subclass but is not a valid public BCM identity.
    assert type(pin.id) is int and pin.id == 18  # pylint: disable=unidiomatic-typecheck
    assert repr(pin) == "18" and str(pin) == "18" and pin == 18
    assert pin == module.Pin(18) and pin != module.Pin(23)
    assert state.chips == [] and state.requests == []
    pin.deinit()
    pin.deinit()


def test_missing_binding_keeps_installable_module_name(monkeypatch):
    monkeypatch.setitem(sys.modules, "gpiod", None)
    monkeypatch.delitem(sys.modules, PREFIX + ".raspberry_pi_pin", raising=False)
    with pytest.raises(ModuleNotFoundError) as caught:
        importlib.import_module(PREFIX + ".raspberry_pi_pin")
    assert caught.value.name == "gpiod"


@pytest.mark.parametrize("value", [True, False, 1.5, "18", (0, 18), None, -1])
def test_invalid_ids_are_rejected_before_hardware(pins, value):
    module, state, _ = pins
    with pytest.raises((TypeError, ValueError)):
        module.Pin(value)
    assert state.chips == [] and state.requests == []


@pytest.mark.parametrize("label", ["pinctrl-bcm2835", "pinctrl-bcm2711", "pinctrl-rp1"])
def test_discovered_chip_index_closes_metadata_handle(pins, label):
    module, state, _ = pins
    state.devices = {0: ("unrelated", 64), 7: (label, 58)}
    pin = module.Pin(18)
    assert pin.chip_index == 7
    assert all(chip.closed for chip in state.chips)
    assert not state.requests and pin._chip is None


@pytest.mark.parametrize("legacy", [False, True])
def test_1x_discovery_and_owned_handle_use_the_binding_cleanup_api(monkeypatch, legacy):
    module, state, library = make_pin(monkeypatch, version="1", legacy=legacy)
    pin = module.Pin(18)
    assert pin.chip_index == 3
    assert state.chips[-1].closed and state.chips[-1].close_calls == 1
    if legacy:
        assert not hasattr(library.chip, "close")
        assert isinstance(state.chips[-1].label, str)
        assert isinstance(state.chips[-1].num_lines, int)
    pin.init(mode=pin.OUT)
    owned = pin._chip
    assert owned is state.chips[-1] and not owned.closed
    assert all(chip.closed for chip in state.chips[:-1])
    pin.deinit()
    pin.deinit()
    assert owned.closed and owned.close_calls == 1


@pytest.mark.parametrize("version,legacy", [("2", False), ("1", False), ("1", True)])
@pytest.mark.parametrize("owned_open", [False, True])
def test_metadata_error_wins_when_discovery_cleanup_also_fails(
    monkeypatch, version, legacy, owned_open
):
    module, state, _ = make_pin(monkeypatch, version=version, legacy=legacy)
    original_info = module._chip_info

    def inspect(chip):
        if state.opens == (2 if owned_open else 1):
            state.fail_close = True
            raise OSError("metadata failed")
        return original_info(chip)

    monkeypatch.setattr(module, "_chip_info", inspect)
    pin = module.Pin(18)
    with pytest.raises(OSError, match="metadata failed"):
        pin.init()
    assert not state.requests and pin._chip is None
    assert all(chip.close_calls == 1 for chip in state.chips)
    state.fail_close = False
    pin.deinit()


@pytest.mark.parametrize("canonical_index", [0, 6])
@pytest.mark.parametrize("distinct_header", [False, True])
def test_filesystem_alias_deduplicates_but_distinct_header_stays_ambiguous(
    pins, monkeypatch, canonical_index, distinct_header
):
    module, state, _ = pins
    canonical = Path(f"/dev/gpiochip{canonical_index}")
    other = Path("/dev/gpiochip1")
    paths = [
        SimpleNamespace(name=canonical.name, resolve=lambda: canonical),
        SimpleNamespace(name="gpiochip4", resolve=lambda: canonical),
        SimpleNamespace(name=other.name, resolve=lambda: other),
        SimpleNamespace(name="gpiochip-not-a-device"),
    ]
    monkeypatch.setattr(Path, "glob", lambda _self, _pattern: iter(paths))
    monkeypatch.setattr(module, "_chip_paths", state.filesystem_chip_paths)
    state.devices = {
        canonical_index: ("pinctrl-rp1", 54),
        1: ("pinctrl-bcm2711" if distinct_header else "unrelated", 58),
    }
    assert module._chip_paths() == sorted([canonical, other])
    pin = module.Pin(18)
    if distinct_header:
        with pytest.raises(RuntimeError, match="Multiple Raspberry Pi"):
            _ = pin.chip_index
    else:
        assert pin.chip_index == canonical_index
    assert state.opens == 2
    assert all(chip.closed for chip in state.chips)
    assert not state.requests and pin._chip is None


def test_filesystem_alias_outside_numeric_dev_path_is_rejected(pins, monkeypatch):
    module, state, _ = pins
    alias = SimpleNamespace(
        name="gpiochip4", resolve=lambda: Path("/tmp/not-a-controller")
    )
    monkeypatch.setattr(Path, "glob", lambda _self, _pattern: iter([alias]))
    monkeypatch.setattr(module, "_chip_paths", state.filesystem_chip_paths)
    with pytest.raises(RuntimeError, match="must resolve to /dev/gpiochipN"):
        _ = module.Pin(18).chip_index
    assert not state.chips and not state.requests


@pytest.mark.parametrize(
    "devices",
    [
        {},
        {0: ("unrelated", 64)},
        {2: ("pinctrl-rp1", 10)},
        {0: ("pinctrl-rp1", 54), 5: ("pinctrl-bcm2711", 58)},
    ],
)
def test_no_fallback_or_ambiguous_controller(pins, devices):
    module, state, _ = pins
    state.devices = devices
    with pytest.raises(RuntimeError):
        module.Pin(18).init()
    assert all(chip.closed for chip in state.chips) and not state.requests


def test_independent_lines_and_deinit_reinitialization(pins):
    module, state, library = pins
    first, second = module.Pin(18), module.Pin(23)
    first.init(mode=first.OUT)
    second.init(mode=second.OUT)
    request1, request2 = state.requests
    assert first._chip is not second._chip
    first.value(1)
    assert first.value() is True
    assert request1.value == library.line.Value.ACTIVE
    first.deinit()
    first.deinit()
    assert not request1.live and request1.chip.closed
    assert request2.live and not request2.chip.closed
    first.init(mode=first.IN)
    assert first.id == 18 and first.chip_index == 3
    assert state.requests[-1] is not request1
    assert state.requests[-1].offset == 18
    first.deinit()
    second.deinit()
    assert all(chip.closed for chip in state.chips)


def test_input_pull_none_explicitly_disables_previous_pull(pins):
    module, state, library = pins
    pin = module.Pin(18)
    pin.init(mode=pin.IN, pull=pin.PULL_UP)
    pin.init(mode=pin.IN, pull=pin.PULL_DOWN)
    pin.init(mode=pin.IN, pull=None)
    configurations = state.requests[-1].configurations
    assert [settings.bias for settings in configurations] == [
        library.line.Bias.PULL_UP,
        library.line.Bias.PULL_DOWN,
        library.line.Bias.DISABLED,
    ]
    pin.init(mode=None, pull=pin.PULL_UP)
    assert configurations[-1].bias is library.line.Bias.PULL_UP
    pin.deinit()


def test_output_disables_pull_and_reconfiguration_preserves_commanded_value(pins):
    module, state, library = pins
    pin = module.Pin(18)
    pin.init(mode=pin.IN, pull=pin.PULL_UP)
    pin.init(mode=pin.OUT)
    request = state.requests[-1]
    assert request.configurations[-1].bias is library.line.Bias.DISABLED
    assert request.value is library.line.Value.INACTIVE
    pin.value(1)
    pin.init(mode=pin.OUT)
    assert request.value is library.line.Value.ACTIVE
    assert pin.value() is True
    pin.value(0)
    pin.init(mode=pin.OUT)
    assert request.value is library.line.Value.INACTIVE
    assert len(state.requests) == 1
    pin.deinit()


def test_output_still_rejects_explicit_pull_and_invalid_mode(pins):
    module, state, _ = pins
    pin = module.Pin(18)
    with pytest.raises(RuntimeError, match="Cannot set pull resistor"):
        pin.init(mode=pin.OUT, pull=pin.PULL_UP)
    with pytest.raises(RuntimeError, match="Invalid mode"):
        pin.init(mode=99)
    assert pin._chip is None
    assert all(chip.closed for chip in state.chips)
    assert all(not request.live for request in state.requests)


@pytest.mark.parametrize(
    "failure", ["discovery_open", "owned_open", "request", "configuration"]
)
def test_failed_open_or_request_is_cleanup_safe(pins, failure):
    module, state, _ = pins
    pin = module.Pin(18)
    if failure.endswith("open"):
        state.fail_open = 1 if failure == "discovery_open" else 2
    elif failure == "request":
        state.fail_request = True
    else:
        state.fail_config = True
    with pytest.raises(OSError):
        pin.init()
    assert pin.id == 18 and pin._chip is None and pin._line_request is None
    assert all(chip.closed for chip in state.chips)
    assert all(not request.live for request in state.requests)
    pin.deinit()
    # Probe repeat destructor cleanup deterministically, without relying on GC timing.
    pin.__del__()  # pylint: disable=unnecessary-dunder-call


@pytest.mark.parametrize("owned_open", [False, True])
def test_failed_metadata_inspection_closes_discovery_or_owned_handle(
    pins, monkeypatch, owned_open
):
    module, state, _ = pins
    original_info = module._chip_info

    def inspect(chip):
        if state.opens == (2 if owned_open else 1):
            raise OSError("metadata failed")
        return original_info(chip)

    monkeypatch.setattr(module, "_chip_info", inspect)
    pin = module.Pin(18)
    with pytest.raises(OSError, match="metadata failed"):
        pin.init()
    assert pin.id == 18 and pin._chip is None
    assert all(chip.closed for chip in state.chips)
    assert not state.requests
    pin.deinit()


def test_owned_controller_identity_is_rechecked_before_request(pins, monkeypatch):
    module, state, _ = pins
    original_info = module._chip_info
    monkeypatch.setattr(
        module,
        "_chip_info",
        lambda chip: ("unrelated", 54) if state.opens == 2 else original_info(chip),
    )
    pin = module.Pin(18)
    with pytest.raises(RuntimeError, match="controller changed"):
        pin.init()
    assert pin.id == 18 and pin._chip is None
    assert all(chip.closed for chip in state.chips)
    assert not state.requests


def test_release_error_still_closes_only_owned_chip(pins):
    module, state, _ = pins
    pin = module.Pin(18)
    pin.init()
    state.fail_release = True
    with pytest.raises(OSError, match="release failed"):
        pin.deinit()
    assert state.chips[-1].closed
    pin.deinit()


def test_board_aliases_and_bus_tables_have_integer_ids_without_handles(pins):
    module, state, _ = pins
    for family in ("bcm283x", "bcm2711", "bcm2712"):
        board = load_source(
            "_pin_alias_test_" + family,
            SOURCE / "adafruit_blinka/microcontroller" / family / "pin.py",
        )
        assert isinstance(board.D18, module.Pin) and board.D18.id == 18
        # Exact int excludes bool and preserves extension/PIO consumer ID shapes.
        # pylint: disable=unidiomatic-typecheck
        assert all(
            type(getattr(board, name).id) is int
            for name in ("D18", "D23", "SCLK", "MOSI", "MISO", "SCL", "SDA")
        )
        # pylint: enable=unidiomatic-typecheck
        assert [pin.id for pin in board.spiPorts[0][1:]] == [11, 10, 9]
        assert [pin.id for pin in board.i2cPorts[0][1:]] == [3, 2]
    assert not state.chips and not state.requests


def test_actual_digitalio_clones_integer_pin_on_same_header(pins, monkeypatch):
    module, state, library = pins
    agnostic = ModuleType("adafruit_blinka.agnostic")
    agnostic.board_id = "RASPBERRY_PI_4B"
    importing = ModuleType("adafruit_blinka.importing")
    importing.get_import_file = lambda name, _location: SOURCE / name
    importing.import_microcontroller = lambda namespace, *_args: namespace.update(
        Pin=module.Pin
    )
    monkeypatch.setitem(sys.modules, "adafruit_blinka.agnostic", agnostic)
    monkeypatch.setitem(sys.modules, "adafruit_blinka.importing", importing)
    digitalio = load_source("_digitalio_clone_test", SOURCE / "digitalio.py")
    original = module.Pin(18)
    digital = digitalio.DigitalInOut(original)
    assert digital._pin is not original and digital._pin.id == original.id == 18
    assert original._chip is None
    digital.switch_to_input(pull=digitalio.Pull.UP)
    digital.pull = None
    assert state.requests[-1].configurations[-1].bias is library.line.Bias.DISABLED
    digital.switch_to_output(value=True)
    assert digital.value is True
    request = state.requests[-1]
    assert request.configurations[-1].bias is library.line.Bias.DISABLED
    assert request.value is library.line.Value.ACTIVE
    digital.drive_mode = digitalio.DriveMode.PUSH_PULL
    assert digital.value is True
    digital.switch_to_output(value=False)
    assert digital.value is False
    digital.switch_to_output(value=True)
    assert digital.value is True
    digital.deinit()
    assert all(chip.closed for chip in state.chips)


def test_1x_reuses_existing_numeric_chip_driver(monkeypatch):
    module, state, _ = make_pin(monkeypatch, version="1")
    pin = module.Pin(18)
    pin.init(pull=pin.PULL_UP)
    pin.init(pull=None)
    assert pin.id == 18 and pin.chip_index == 3
    assert state.requests[-1].configurations[-1]["flags"] == 16
    pin.value(1)
    assert pin.value() == 1
    pin.deinit()
    pin.init()
    pin.deinit()
    assert all(chip.closed for chip in state.chips)


def test_1x_without_bias_clear_retains_implicit_default_but_rejects_explicit_none(
    monkeypatch,
):
    module, state, library = make_pin(monkeypatch, version="1")
    del library.LINE_REQ_FLAG_BIAS_DISABLE
    pin = module.Pin(18)
    pin.init()
    assert state.requests[-1].configurations[-1]["flags"] == 0
    with pytest.raises(NotImplementedError):
        pin.init(pull=pin.PULL_NONE)
    assert all(chip.closed for chip in state.chips)
    assert all(not request.live for request in state.requests)


@pytest.mark.parametrize(
    "identity,expected_chip", [(18, "gpiochip3"), ((6, 18), "gpiochip6")]
)
def test_pulsein_keeps_tuple_branch_and_discovers_integer_chip(
    pins, monkeypatch, identity, expected_chip
):
    module, _, _ = pins
    ipc = ModuleType("sysv_ipc")
    ipc.IPC_CREX = 1
    ipc.ExistentialError = RuntimeError
    ipc.BusyError = ValueError
    ipc.MessageQueue = lambda *_args, **_kwargs: SimpleNamespace(
        key=7, receive=lambda **_kw: (b"!", 2), remove=lambda: None
    )
    monkeypatch.setitem(sys.modules, "sysv_ipc", ipc)
    signal = ModuleType("signal")
    signal.SIGTERM = 15
    signal.signal = lambda *_args: None
    monkeypatch.setitem(sys.modules, "signal", signal)
    commands = []
    subprocess = importlib.import_module("subprocess")
    monkeypatch.setattr(
        subprocess,
        "Popen",
        lambda arguments: (
            commands.append(arguments) or SimpleNamespace(terminate=lambda: None)
        ),
    )
    pulse = load_source(
        "_pulse_chip_test",
        SOURCE / "adafruit_blinka/microcontroller/bcm283x/pulseio/PulseIn.py",
    )
    pin = (
        module.Pin(identity)
        if isinstance(identity, int)
        else SimpleNamespace(id=identity)
    )
    capture = pulse.PulseIn(pin)
    assert commands[0][-2:] == [expected_chip, "18"]
    capture.deinit()
