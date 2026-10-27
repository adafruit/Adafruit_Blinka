# SPDX-FileCopyrightText: 2026 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""USB gadget report sizing with no kernel, configfs, device, or exit-handler access."""

import builtins
import importlib.util
import io
import sys
from contextlib import contextmanager
from pathlib import Path
from types import ModuleType, SimpleNamespace

import pytest

# Pytest supplies the named fixtures.
# pylint: disable=redefined-outer-name

SOURCE = Path(__file__).parents[1] / "src/usb_hid.py"
ROOT = "/sys/kernel/config/usb_gadget/adafruit-blinka"


@pytest.fixture
def hid_gadget(monkeypatch):
    """Intercept imports before source execution, including its atexit registration."""
    state = SimpleNamespace(
        files={}, directories=set(), sent=[], callbacks=[], writes=[]
    )

    class RecordingPath:
        """Only in-memory path operations; no fallthrough to pathlib."""

        def __init__(self, path):
            self.path = str(path).rstrip("/")

        @property
        def name(self):
            """Return the basename used when binding the fake UDC."""
            return self.path.rsplit("/", 1)[-1]

        def read_text(self, *, encoding):
            """Supply fake kernel-module availability and device numbers."""
            assert encoding == "utf-8"
            if self.path == "/proc/modules":
                return "dwc2 0 0\nlibcomposite 0 0\n"
            assert self.path in state.files, f"unexpected read: {self.path}"
            return state.files[self.path]

        def write_text(self, value, *, encoding):
            """Record configfs values without touching a real filesystem."""
            assert encoding == "utf-8"
            assert self.path.startswith(ROOT + "/")
            state.files[self.path] = value
            state.writes.append(self.path)
            return len(value)

        def write_bytes(self, value):
            """Record the unchanged report descriptor."""
            assert self.path.startswith(ROOT + "/")
            state.files[self.path] = value
            state.writes.append(self.path)
            return len(value)

        def mkdir(self, *, parents=False, exist_ok=False):
            """Create fake directories and kernel-generated dev attributes."""
            assert self.path.startswith(ROOT + "/")
            assert parents
            if self.path in state.directories and not exist_ok:
                raise FileExistsError(self.path)
            state.directories.add(self.path)
            if self.path.startswith(ROOT + "/functions/hid.usb"):
                report_id = self.name[len("hid.usb") :]
                state.files[self.path + "/dev"] = f"240:{report_id}\n"

        def symlink_to(self, target):
            """Record function association without creating a symlink."""
            assert self.path.startswith(ROOT + "/configs/")
            state.files[self.path] = target

        def glob(self, pattern):
            """Expose exactly one inert UDC; cleanup is not part of these tests."""
            assert self.path == "/sys/class/udc"
            assert pattern == "*"
            return iter([RecordingPath("/sys/class/udc/recording-udc")])

    @contextmanager
    def recording_open(path, mode):
        assert path.startswith("/dev/hidg")
        assert mode == "rb+"
        buffer = io.BytesIO()
        try:
            yield buffer
            state.sent.append((path, buffer.getvalue()))
        finally:
            buffer.close()

    fake_pathlib = ModuleType("pathlib")
    fake_pathlib.Path = RecordingPath
    fake_atexit = ModuleType("atexit")
    fake_atexit.register = state.callbacks.append
    real_import = builtins.__import__

    def isolated_import(name, *args, **kwargs):
        if name == "pathlib":
            return fake_pathlib
        if name == "atexit":
            return fake_atexit
        return real_import(name, *args, **kwargs)

    spec = importlib.util.spec_from_file_location("_test_usb_hid", SOURCE)
    module = importlib.util.module_from_spec(spec)
    module.__builtins__ = dict(vars(builtins), __import__=isolated_import)
    module.open = recording_open
    monkeypatch.setitem(sys.modules, "_test_usb_hid", module)
    spec.loader.exec_module(module)
    assert state.callbacks == [module.disable]
    return SimpleNamespace(module=module, state=state)


def report_length(gadget, report_id):
    """Read a fake configfs value for one function."""
    return int(gadget.state.files[f"{ROOT}/functions/hid.usb{report_id}/report_length"])


def test_mouse_descriptor_preserves_report_layout(hid_gadget):
    """Avoid the 64-byte descriptor boundary without changing mouse reports."""
    expected = bytes.fromhex(
        "05010902a10185020901a100"  # Mouse/Pointer collections; report ID 2
        "05091901290515002501950575018102"  # Five buttons, bounds 0..1
        "950175038101"  # Three padding bits
        "0501093009311581257f750895028106"  # X/Y: -127..127, eight bits each
        "09381581257f95018106"  # Wheel inherits eight-bit size; count one
        "c0c0"  # End collections
    )
    mouse = hid_gadget.module.Device.MOUSE
    assert mouse.descriptor == expected
    assert tuple(mouse.report_ids) == (2,)
    assert tuple(mouse.in_report_lengths) == (4,)
    assert tuple(mouse.out_report_lengths) == (0,)
    hid_gadget.module.enable((mouse,))
    assert hid_gadget.state.files[f"{ROOT}/functions/hid.usb2/report_desc"] == expected
    assert report_length(hid_gadget, 2) == 5
    assert hid_gadget.state.sent == []


@pytest.mark.parametrize(
    "name, expected",
    [
        ("KEYBOARD", 9),
        ("MOUSE", 5),
        ("CONSUMER_CONTROL", 3),
        ("BOOT_KEYBOARD", 8),
        ("BOOT_MOUSE", 4),
    ],
)
def test_builtin_wire_capacity(hid_gadget, name, expected):
    device = getattr(hid_gadget.module.Device, name)
    original_lengths = (
        tuple(device.in_report_lengths),
        tuple(device.out_report_lengths),
    )
    hid_gadget.module.enable((device,))
    report_id = device.report_ids[0]
    assert report_length(hid_gadget, report_id) == expected
    assert hid_gadget.state.files[
        f"{ROOT}/functions/hid.usb{report_id}/report_desc"
    ] == (device.descriptor)
    assert (tuple(device.in_report_lengths), tuple(device.out_report_lengths)) == (
        original_lengths
    )
    assert hid_gadget.state.files[ROOT + "/UDC"] == "recording-udc"
    assert hid_gadget.state.writes[-1] == ROOT + "/UDC"
    assert hid_gadget.module.devices == [device]


def vendor_descriptor(ids, input_lengths, output_lengths):
    """Build simple byte-oriented vendor reports for the metadata sizing tests."""
    descriptor = bytearray([0x06, 0x00, 0xFF, 0x09, 0x01, 0xA1, 0x01])
    for report_id, input_length, output_length in zip(
        ids, input_lengths, output_lengths
    ):
        if report_id:
            descriptor.extend([0x85, report_id])
        descriptor.extend([0x15, 0x00, 0x26, 0xFF, 0x00, 0x75, 0x08])
        if input_length:
            descriptor.extend([0x95, input_length, 0x09, 0x01, 0x81, 0x02])
        if output_length:
            descriptor.extend([0x95, output_length, 0x09, 0x01, 0x91, 0x02])
    descriptor.append(0xC0)
    return bytes(descriptor)


def make_device(gadget, ids, input_lengths, output_lengths):
    """Use the production Device constructor without changing payload metadata."""
    return gadget.module.Device(
        descriptor=vendor_descriptor(ids, input_lengths, output_lengths),
        usage_page=0xFF00,
        usage=1,
        report_ids=ids,
        in_report_lengths=input_lengths,
        out_report_lengths=output_lengths,
    )


@pytest.mark.parametrize("report_id", [0, 7, 255])
@pytest.mark.parametrize("input_length, output_length", [(3, 7), (7, 3), (0, 8)])
def test_capacity_fits_both_directions(
    hid_gadget, report_id, input_length, output_length
):
    device = make_device(hid_gadget, (report_id,), (input_length,), (output_length,))
    hid_gadget.module.enable((device,))
    expected = max(input_length, output_length) + (1 if report_id else 0)
    assert report_length(hid_gadget, report_id) == expected


def test_each_report_uses_its_matching_lengths(hid_gadget):
    """Check existing per-ID metadata routing, not full multi-report USB support."""
    device = make_device(hid_gadget, (7, 23), (3, 9), (8, 2))
    hid_gadget.module.enable((device,))
    assert report_length(hid_gadget, 7) == 9
    assert report_length(hid_gadget, 23) == 10


@pytest.mark.parametrize(
    "boot_device, name, expected", [(1, "BOOT_KEYBOARD", 8), (2, "BOOT_MOUSE", 4)]
)
def test_boot_substitution_keeps_unnumbered_capacity(
    hid_gadget, boot_device, name, expected
):
    module = hid_gadget.module
    module.enable(
        (module.Device.KEYBOARD, module.Device.MOUSE), boot_device=boot_device
    )
    assert module.devices == [getattr(module.Device, name)]
    assert module.boot_device == boot_device
    assert report_length(hid_gadget, 0) == expected


@pytest.mark.parametrize("report_id", [0, 7, 255])
def test_send_framing_matches_capacity_without_changing_payload(hid_gadget, report_id):
    payload = bytearray(b"abc")
    device = make_device(hid_gadget, (report_id,), (len(payload),), (0,))
    hid_gadget.module.enable((device,))
    device.send_report(payload)
    wire_report = (bytes([report_id]) if report_id else b"") + payload
    assert hid_gadget.state.sent == [(f"/dev/hidg{report_id}", wire_report)]
    assert payload == b"abc"
    assert len(wire_report) <= report_length(hid_gadget, report_id)
