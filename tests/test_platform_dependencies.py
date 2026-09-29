# SPDX-FileCopyrightText: 2026 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""Tests for runtime platform dependency handling."""

from types import SimpleNamespace

import pytest

from adafruit_blinka import importing
from adafruit_blinka import platform_dependencies


def _detector(chip_id=None, **board_values):
    values = {
        "any_raspberry_pi_5_board": False,
        "any_raspberry_pi": False,
        "any_jetson_board": False,
        "any_beaglebone": False,
    }
    values.update(board_values)
    return SimpleNamespace(
        board=SimpleNamespace(**values), chip=SimpleNamespace(id=chip_id)
    )


def test_raspberry_pi_5_uses_adafruit_lgpio_on_python_313():
    dependencies = platform_dependencies.get_platform_dependencies(
        _detector(any_raspberry_pi_5_board=True, any_raspberry_pi=True),
        python_version=(3, 13),
    )

    assert dependencies == [
        ("lgpio", "adafruit-lgpio>=0.2.2.0"),
        (
            "adafruit_raspberry_pi5_neopixel_write",
            "Adafruit-Blinka-Raspberry-Pi5-Neopixel",
        ),
    ]


def test_raspberry_pi_5_uses_upstream_lgpio_before_python_313():
    dependencies = platform_dependencies.get_platform_dependencies(
        _detector(any_raspberry_pi_5_board=True, any_raspberry_pi=True),
        python_version=(3, 12),
    )

    assert ("lgpio", "lgpio>=0.2.2.0") in dependencies


def test_raspberry_pi_5_neopixel_requires_python_311():
    detector = _detector(any_raspberry_pi_5_board=True, any_raspberry_pi=True)
    dependencies = platform_dependencies.get_platform_dependencies(
        detector, python_version=(3, 10)
    )

    assert all(
        module_name != "adafruit_raspberry_pi5_neopixel_write"
        for module_name, _ in dependencies
    )
    assert platform_dependencies.get_unsupported_platform_dependency_message(
        detector,
        "adafruit_raspberry_pi5_neopixel_write",
        python_version=(3, 10),
    ) == (
        "Raspberry Pi 5 NeoPixel support requires Python 3.11 or newer; "
        "the current interpreter is Python 3.10."
    )


def test_supported_raspberry_pi_5_neopixel_has_no_unsupported_message():
    message = platform_dependencies.get_unsupported_platform_dependency_message(
        _detector(any_raspberry_pi_5_board=True, any_raspberry_pi=True),
        "adafruit_raspberry_pi5_neopixel_write",
        python_version=(3, 11),
    )

    assert message is None


def test_unsupported_dependency_does_not_fall_back_to_install(monkeypatch):
    monkeypatch.setattr(
        platform_dependencies,
        "get_platform_requirement_for_import",
        lambda *_args, **_kwargs: None,
    )
    monkeypatch.setattr(
        platform_dependencies,
        "get_unsupported_platform_dependency_message",
        lambda *_args, **_kwargs: (
            "Raspberry Pi 5 NeoPixel support requires Python 3.11 or newer."
        ),
    )

    error = ModuleNotFoundError(name="adafruit_raspberry_pi5_neopixel_write")
    with pytest.raises(RuntimeError, match="requires Python 3.11") as raised:
        importing.raise_for_missing_platform_dependency(error)

    assert "pip install" not in str(raised.value)


def test_earlier_raspberry_pi_does_not_install_lgpio():
    dependencies = platform_dependencies.get_platform_dependencies(
        _detector(any_raspberry_pi=True), python_version=(3, 13)
    )

    assert dependencies == [
        ("RPi.GPIO", "RPi.GPIO"),
        ("_rpi_ws281x", "rpi_ws281x>=4.0.0"),
    ]


def test_unrelated_generic_linux_board_does_not_install_lgpio():
    dependencies = platform_dependencies.get_platform_dependencies(
        _detector(chip_id="GENERIC_X86"), python_version=(3, 14)
    )

    assert dependencies == []


def test_import_requirement_uses_detected_python_version():
    detector = _detector(any_raspberry_pi_5_board=True, any_raspberry_pi=True)

    requirement = platform_dependencies.get_platform_requirement_for_import(
        detector, "lgpio", python_version=(3, 12)
    )

    assert requirement == "lgpio>=0.2.2.0"


def test_installer_uses_running_python(monkeypatch):
    detector = _detector(chip_id="AM33XX", any_beaglebone=True)
    commands = []

    monkeypatch.setattr(
        platform_dependencies,
        "get_missing_platform_dependencies",
        lambda *_args, **_kwargs: ["Adafruit_BBIO>=1.2.4"],
    )
    monkeypatch.setattr(platform_dependencies.sys.stdin, "isatty", lambda: True)
    monkeypatch.setattr(platform_dependencies.sys.stdout, "isatty", lambda: True)
    monkeypatch.setattr(
        platform_dependencies.subprocess,
        "run",
        lambda command, check: commands.append((command, check)),
    )

    installed = platform_dependencies.install_missing_platform_dependencies(
        detector, input_func=lambda _prompt: "y"
    )

    assert installed is True
    assert commands == [
        (
            [
                platform_dependencies.sys.executable,
                "-m",
                "pip",
                "install",
                "Adafruit_BBIO>=1.2.4",
            ],
            True,
        )
    ]


def test_installer_skips_prompt_without_terminal(monkeypatch):
    detector = _detector(chip_id="AM33XX", any_beaglebone=True)
    prompted = []

    monkeypatch.setattr(
        platform_dependencies,
        "get_missing_platform_dependencies",
        lambda *_args, **_kwargs: ["Adafruit_BBIO>=1.2.4"],
    )
    monkeypatch.setattr(platform_dependencies.sys.stdin, "isatty", lambda: False)

    installed = platform_dependencies.install_missing_platform_dependencies(
        detector, input_func=prompted.append
    )

    assert installed is False
    assert not prompted


def test_install_command_quotes_requirements_and_interpreter_paths():
    command = platform_dependencies.format_install_command(
        ["lgpio>=0.2.2.0"], executable="/path with spaces/python"
    )

    assert command == "'/path with spaces/python' -m pip install 'lgpio>=0.2.2.0'"
