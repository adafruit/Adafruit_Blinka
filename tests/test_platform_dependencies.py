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


def test_raspberry_pi_5_uses_gpiod_and_native_pwm():
    dependencies = platform_dependencies.get_platform_dependencies(
        _detector(any_raspberry_pi_5_board=True, any_raspberry_pi=True),
        python_version=(3, 13),
    )

    assert dependencies == [
        ("gpiod", "gpiod>=2.2.2,<3"),
        (
            "adafruit_blinka_raspberry_pi_pwm",
            "Adafruit-Blinka-Raspberry-Pi-PWM>=0.0.1.dev0",
        ),
        (
            "adafruit_raspberry_pi5_neopixel_write",
            "Adafruit-Blinka-Raspberry-Pi5-Neopixel",
        ),
    ]


def test_raspberry_pi_5_gpio_pwm_requirements_do_not_depend_on_python_version():
    dependencies = platform_dependencies.get_platform_dependencies(
        _detector(any_raspberry_pi_5_board=True, any_raspberry_pi=True),
        python_version=(3, 12),
    )

    assert dependencies[:2] == [
        ("gpiod", "gpiod>=2.2.2,<3"),
        (
            "adafruit_blinka_raspberry_pi_pwm",
            "Adafruit-Blinka-Raspberry-Pi-PWM>=0.0.1.dev0",
        ),
    ]
    assert all(name not in ("lgpio", "RPi.GPIO") for name, _ in dependencies)


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


def test_earlier_raspberry_pi_uses_gpiod_and_native_pwm_without_legacy_gpio():
    dependencies = platform_dependencies.get_platform_dependencies(
        _detector(any_raspberry_pi=True), python_version=(3, 13)
    )

    assert dependencies == [
        ("gpiod", "gpiod>=2.2.2,<3"),
        (
            "adafruit_blinka_raspberry_pi_pwm",
            "Adafruit-Blinka-Raspberry-Pi-PWM>=0.0.1.dev0",
        ),
        ("_rpi_ws281x", "rpi_ws281x>=4.0.0"),
    ]


def test_unrelated_generic_linux_board_does_not_install_lgpio():
    dependencies = platform_dependencies.get_platform_dependencies(
        _detector(chip_id="GENERIC_X86"), python_version=(3, 14)
    )

    assert dependencies == []


def test_import_requirement_for_gpiod():
    detector = _detector(any_raspberry_pi_5_board=True, any_raspberry_pi=True)

    requirement = platform_dependencies.get_platform_requirement_for_import(
        detector, "gpiod", python_version=(3, 12)
    )

    assert requirement == "gpiod>=2.2.2,<3"


def test_import_requirement_for_new_pwm_package():
    requirement = platform_dependencies.get_platform_requirement_for_import(
        _detector(any_raspberry_pi=True), "adafruit_blinka_raspberry_pi_pwm"
    )

    assert requirement == "Adafruit-Blinka-Raspberry-Pi-PWM>=0.0.1.dev0"


def test_legacy_gpio_imports_are_not_requested_for_raspberry_pi():
    detector = _detector(any_raspberry_pi=True)
    for module in ("RPi.GPIO", "RPi", "lgpio"):
        assert (
            platform_dependencies.get_platform_requirement_for_import(detector, module)
            is None
        )


def test_missing_dependencies_include_old_distribution(monkeypatch):
    monkeypatch.setattr(
        platform_dependencies,
        "get_platform_dependencies",
        lambda *_args, **_kwargs: [("lgpio", "lgpio>=0.2.2.0")],
    )
    monkeypatch.setattr(
        platform_dependencies.importlib.util, "find_spec", lambda _name: object()
    )
    monkeypatch.setattr(
        platform_dependencies.importlib.metadata,
        "version",
        lambda _name: "0.2.1",
    )

    assert platform_dependencies.get_missing_platform_dependencies(_detector()) == [
        "lgpio>=0.2.2.0"
    ]


def test_missing_dependencies_accept_minimum_distribution(monkeypatch):
    monkeypatch.setattr(
        platform_dependencies,
        "get_platform_dependencies",
        lambda *_args, **_kwargs: [("lgpio", "lgpio>=0.2.2.0")],
    )
    monkeypatch.setattr(
        platform_dependencies.importlib.util, "find_spec", lambda _name: object()
    )
    monkeypatch.setattr(
        platform_dependencies.importlib.metadata,
        "version",
        lambda _name: "0.2.2.0",
    )

    assert platform_dependencies.get_missing_platform_dependencies(_detector()) == []


def test_recovery_command_uses_running_python(monkeypatch):
    monkeypatch.setattr(
        platform_dependencies,
        "get_platform_requirement_for_import",
        lambda *_args, **_kwargs: "lgpio>=0.2.2.0",
    )

    error = ModuleNotFoundError(name="lgpio")
    with pytest.raises(RuntimeError) as raised:
        importing.raise_for_missing_platform_dependency(error)

    expected = platform_dependencies.format_install_command(
        ["lgpio>=0.2.2.0"], executable=importing.sys.executable
    )
    assert expected in str(raised.value)


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
