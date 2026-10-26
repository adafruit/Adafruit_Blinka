# SPDX-FileCopyrightText: 2026 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""Tests for runtime platform dependency handling."""

import builtins
import io
import runpy
import sys
from pathlib import Path
from types import ModuleType, SimpleNamespace

import pytest

from adafruit_blinka import importing
from adafruit_blinka import platform_dependencies
from adafruit_blinka import _gpiod_compat

# Pytest supplies the named fixtures.
# pylint: disable=redefined-outer-name


@pytest.fixture(autouse=True)
def dependency_check_environment(monkeypatch):
    """Isolate startup policy from the host's opt-out and installer tools."""
    monkeypatch.delenv("BLINKA_SKIP_DEPENDENCY_CHECK", raising=False)
    monkeypatch.setattr(platform_dependencies, "_pip_available", lambda: True)
    # System package origin/version handling is tested separately, rather than
    # querying the test host's package database from startup-policy tests.
    monkeypatch.setattr(_gpiod_compat, "is_supported_system_gpiod", lambda: False)


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
            "Adafruit-Blinka-Raspberry-Pi-PWM>=1.0.2",
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
            "Adafruit-Blinka-Raspberry-Pi-PWM>=1.0.2",
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
            "Adafruit-Blinka-Raspberry-Pi-PWM>=1.0.2",
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

    assert requirement == "Adafruit-Blinka-Raspberry-Pi-PWM>=1.0.2"


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
        lambda *_args, **_kwargs: [] if commands else ["Adafruit_BBIO>=1.2.4"],
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


@pytest.mark.parametrize(
    "detector, expected",
    [
        (
            _detector(chip_id="TEGRA234", any_jetson_board=True),
            [("Jetson.GPIO", "Jetson.GPIO")],
        ),
        (
            _detector(chip_id="AM33XX"),
            [("Adafruit_BBIO", "Adafruit_BBIO>=1.2.4")],
        ),
        (_detector(chip_id="AM5729", any_beaglebone=True), []),
        (_detector(chip_id="RK3399"), []),
        (_detector(), []),
    ],
)
def test_other_platforms_only_request_their_existing_backend(detector, expected):
    assert platform_dependencies.get_platform_dependencies(detector) == expected


@pytest.mark.parametrize("import_name", ["Jetson", "Jetson.GPIO", "RPi", "RPi.GPIO"])
def test_jetson_namespaces_use_jetson_gpio_distribution(import_name):
    requirement = platform_dependencies.get_platform_requirement_for_import(
        _detector(any_jetson_board=True), import_name
    )
    assert requirement == "Jetson.GPIO"


@pytest.mark.parametrize(
    "version, missing",
    [
        ("1.6.4", True),
        ("2.2.1", True),
        ("2.2.2rc1", True),
        ("2.2.2", False),
        ("2.3.0rc1", False),
        ("2.5.0", False),
        ("3.0.0", True),
    ],
)
def test_gpiod_version_bounds_are_checked(monkeypatch, version, missing):
    monkeypatch.setattr(
        platform_dependencies,
        "get_platform_dependencies",
        lambda *_args: [("gpiod", "gpiod>=2.2.2,<3")],
    )
    monkeypatch.setattr(
        platform_dependencies.importlib.util, "find_spec", lambda _name: object()
    )
    monkeypatch.setattr(
        platform_dependencies.importlib.metadata, "version", lambda _name: version
    )
    assert platform_dependencies.get_missing_platform_dependencies(_detector()) == (
        ["gpiod>=2.2.2,<3"] if missing else []
    )


def test_importable_module_without_distribution_metadata_is_missing(monkeypatch):
    def no_metadata(name):
        raise platform_dependencies.importlib.metadata.PackageNotFoundError(name)

    monkeypatch.setattr(
        platform_dependencies.importlib.util, "find_spec", lambda _name: object()
    )
    monkeypatch.setattr(
        platform_dependencies.importlib.metadata, "version", no_metadata
    )
    assert not platform_dependencies._requirement_available(  # pylint: disable=protected-access
        "gpiod", "gpiod>=2.2.2,<3"
    )


def test_absent_module_does_not_require_distribution_metadata(monkeypatch):
    def unexpected_metadata(_name):
        raise AssertionError("An absent module is already known to be missing")

    monkeypatch.setattr(
        platform_dependencies.importlib.util, "find_spec", lambda _name: None
    )
    monkeypatch.setattr(
        platform_dependencies.importlib.metadata, "version", unexpected_metadata
    )
    assert not platform_dependencies._requirement_available(  # pylint: disable=protected-access
        "gpiod", "gpiod>=2.2.2,<3"
    )


@pytest.mark.parametrize("failure", [ImportError, ModuleNotFoundError])
def test_absent_module_parent_is_a_missing_dependency(monkeypatch, failure):
    def missing_spec(_name):
        raise failure("Missing parent")

    monkeypatch.setattr(platform_dependencies.importlib.util, "find_spec", missing_spec)
    assert not platform_dependencies._requirement_available(  # pylint: disable=protected-access
        "Jetson.GPIO", "Jetson.GPIO"
    )


def test_unversioned_requirement_only_needs_importable_module(monkeypatch):
    def unexpected_metadata(_name):
        raise AssertionError("An unversioned requirement does not need metadata")

    monkeypatch.setattr(
        platform_dependencies.importlib.util, "find_spec", lambda _name: object()
    )
    monkeypatch.setattr(
        platform_dependencies.importlib.metadata, "version", unexpected_metadata
    )
    assert platform_dependencies._requirement_available(  # pylint: disable=protected-access
        "Jetson.GPIO", "Jetson.GPIO"
    )


@pytest.fixture
def installer(monkeypatch):
    """Record prompts and pip calls without installing any real packages."""
    state = SimpleNamespace(
        detector=_detector(chip_id="AM33XX"),
        missing=["Adafruit_BBIO>=1.2.4"],
        after_install_missing=[],
        availability_checks=[],
        answer="y",
        prompts=[],
        commands=[],
        invalidations=[],
        stdin=io.StringIO(),
        stdout=io.StringIO(),
    )
    state.stdin.isatty = lambda: True
    state.stdout.isatty = lambda: True

    def no_metadata(name):
        raise platform_dependencies.importlib.metadata.PackageNotFoundError(name)

    def answer(prompt):
        state.prompts.append(prompt)
        if isinstance(state.answer, BaseException):
            raise state.answer
        return state.answer

    def run():
        # Pytest replaces its capture streams between fixture setup and the call.
        with monkeypatch.context() as streams:
            streams.setattr(platform_dependencies.sys, "stdin", state.stdin)
            streams.setattr(platform_dependencies.sys, "stdout", state.stdout)
            return platform_dependencies.install_missing_platform_dependencies(
                state.detector, input_func=state.input_func
            )

    def missing_dependencies(*_args):
        missing = state.after_install_missing if state.commands else state.missing
        state.availability_checks.append(list(missing))
        return missing

    state.input_func = answer
    state.run = run
    monkeypatch.setattr(
        platform_dependencies,
        "get_missing_platform_dependencies",
        missing_dependencies,
    )
    monkeypatch.setattr(
        platform_dependencies.importlib.metadata, "version", no_metadata
    )
    monkeypatch.setattr(
        platform_dependencies.subprocess,
        "run",
        lambda command, check: state.commands.append((command, check)),
    )
    monkeypatch.setattr(
        platform_dependencies.importlib,
        "invalidate_caches",
        lambda: state.invalidations.append(True),
    )
    return state


@pytest.mark.parametrize("answer", ["", "y", "Y", "yes", " YES "])
def test_installer_accepts_confirmation_and_invalidates_cache(
    monkeypatch, installer, answer
):
    monkeypatch.setattr(
        platform_dependencies.shutil, "which", lambda _name: "/uv tools/bin/uv"
    )
    installer.answer = answer
    assert installer.run()
    assert len(installer.prompts) == 1
    assert installer.commands == [
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
    assert installer.invalidations == [True]
    assert installer.availability_checks == [["Adafruit_BBIO>=1.2.4"], []]


@pytest.mark.parametrize("answer", ["n", "no", "other", EOFError()])
def test_declining_or_eof_does_not_install_missing_package(installer, answer):
    installer.answer = answer
    assert not installer.run()
    assert len(installer.prompts) == 1
    assert installer.commands == []
    assert installer.invalidations == []


@pytest.mark.parametrize("stream_name", ["stdin", "stdout"])
@pytest.mark.parametrize("absent", [False, True])
def test_installer_needs_both_terminal_streams(
    monkeypatch, installer, stream_name, absent
):
    if absent:
        monkeypatch.setattr(installer, stream_name, None)
    else:
        monkeypatch.setattr(getattr(installer, stream_name), "isatty", lambda: False)
    assert not installer.run()
    assert installer.prompts == []
    assert installer.commands == []
    assert installer.invalidations == []


def test_installer_does_nothing_when_requirements_are_satisfied(installer):
    installer.missing = []
    assert not installer.run()
    assert installer.prompts == []
    assert installer.commands == []
    assert installer.invalidations == []


def test_opt_out_skips_discovery_prompt_and_install(monkeypatch, installer):
    monkeypatch.setenv("BLINKA_SKIP_DEPENDENCY_CHECK", "1")
    assert not installer.run()
    assert installer.availability_checks == []
    assert installer.prompts == []
    assert installer.commands == []
    assert installer.invalidations == []


@pytest.mark.parametrize("value", ["0", "", "false"])
def test_only_explicit_opt_out_disables_checks(monkeypatch, installer, value):
    monkeypatch.setenv("BLINKA_SKIP_DEPENDENCY_CHECK", value)
    installer.missing = []
    assert not installer.run()
    assert installer.availability_checks == [[]]


@pytest.mark.parametrize("opt_out", [False, True])
def test_gpiod_220_label_requires_supported_install_or_explicit_opt_out(
    monkeypatch, opt_out
):
    monkeypatch.setattr(
        platform_dependencies,
        "get_platform_dependencies",
        lambda *_args: [("gpiod", "gpiod>=2.2.2,<3")],
    )
    monkeypatch.setattr(
        platform_dependencies.importlib.util, "find_spec", lambda _name: object()
    )
    monkeypatch.setattr(
        platform_dependencies.importlib.metadata, "version", lambda _name: "2.2.0"
    )
    monkeypatch.setattr(sys, "stdin", io.StringIO())
    monkeypatch.setattr(
        platform_dependencies.subprocess,
        "run",
        lambda *_args, **_kwargs: pytest.fail("Non-interactive pip is forbidden"),
    )
    if opt_out:
        monkeypatch.setenv("BLINKA_SKIP_DEPENDENCY_CHECK", "1")
        assert not platform_dependencies.install_missing_platform_dependencies(
            _detector(any_raspberry_pi=True)
        )
    else:
        with pytest.raises(RuntimeError, match="unsupported versions"):
            platform_dependencies.install_missing_platform_dependencies(
                _detector(any_raspberry_pi=True)
            )


@pytest.mark.parametrize("verified", [False, True])
@pytest.mark.parametrize("preloaded", [False, True])
def test_trixie_exception_is_consistent_at_startup_and_feature_use(
    monkeypatch, verified, preloaded
):
    detector = _detector(any_raspberry_pi=True)
    monkeypatch.setattr(
        platform_dependencies,
        "get_platform_dependencies",
        lambda *_args: [("gpiod", "gpiod>=2.2.2,<3")],
    )
    monkeypatch.setattr(
        platform_dependencies.importlib.util, "find_spec", lambda _name: object()
    )
    monkeypatch.setattr(
        platform_dependencies.importlib.metadata, "version", lambda _name: "2.2.0"
    )
    monkeypatch.setattr(_gpiod_compat, "is_supported_system_gpiod", lambda: verified)
    if preloaded:
        monkeypatch.setitem(sys.modules, "gpiod", SimpleNamespace(__version__="2.2.0"))
    else:
        monkeypatch.delitem(sys.modules, "gpiod", raising=False)
    monkeypatch.setattr(sys, "stdin", io.StringIO())
    monkeypatch.setattr(
        platform_dependencies.subprocess,
        "run",
        lambda *_args, **_kwargs: pytest.fail("No pip during non-interactive startup"),
    )
    assert platform_dependencies.get_missing_platform_dependencies(detector) == (
        [] if verified else ["gpiod>=2.2.2,<3"]
    )
    if verified:
        assert not platform_dependencies.install_missing_platform_dependencies(detector)
        platform_dependencies.check_platform_dependency(detector, "gpiod")
    else:
        with pytest.raises(RuntimeError, match="unsupported versions"):
            platform_dependencies.install_missing_platform_dependencies(detector)
        with pytest.raises(RuntimeError, match="unsupported installed version"):
            platform_dependencies.check_platform_dependency(detector, "gpiod")


@pytest.mark.parametrize("loaded_version", ["2.2.0", "3.0.0", "invalid", None])
def test_new_metadata_cannot_hide_an_incompatible_loaded_gpiod(
    monkeypatch, loaded_version
):
    detector = _detector(any_raspberry_pi=True)
    monkeypatch.setattr(
        platform_dependencies,
        "get_platform_dependencies",
        lambda *_args: [("gpiod", "gpiod>=2.2.2,<3")],
    )
    monkeypatch.setattr(
        platform_dependencies.importlib.util, "find_spec", lambda _name: object()
    )
    monkeypatch.setattr(
        platform_dependencies.importlib.metadata, "version", lambda _name: "2.2.2"
    )
    monkeypatch.setitem(
        sys.modules, "gpiod", SimpleNamespace(__version__=loaded_version)
    )
    monkeypatch.setattr(sys, "stdin", io.StringIO())
    assert platform_dependencies.get_missing_platform_dependencies(detector) == [
        "gpiod>=2.2.2,<3"
    ]
    with pytest.raises(RuntimeError, match="restart Python"):
        platform_dependencies.install_missing_platform_dependencies(detector)
    with pytest.raises(RuntimeError, match="restart Python"):
        platform_dependencies.check_platform_dependency(detector, "gpiod")


def test_verified_trixie_does_not_satisfy_a_future_higher_minimum(monkeypatch):
    monkeypatch.setattr(_gpiod_compat, "is_supported_system_gpiod", lambda: True)
    monkeypatch.setattr(
        platform_dependencies.importlib.util, "find_spec", lambda _name: object()
    )
    monkeypatch.setattr(
        platform_dependencies.importlib.metadata, "version", lambda _name: "2.2.0"
    )
    assert not platform_dependencies._requirement_available(  # pylint: disable=protected-access
        "gpiod", "gpiod>=2.3,<3"
    )


@pytest.mark.parametrize(
    "module_name, requirement",
    [
        ("_rpi_ws281x", "rpi_ws281x>=4.0.0"),
        ("adafruit_blinka_raspberry_pi_pwm", "Adafruit-Blinka-Raspberry-Pi-PWM>=1.0.2"),
    ],
)
@pytest.mark.parametrize("skip", ["noninteractive", "decline", "eof"])
def test_unused_optional_old_backend_does_not_block_startup(
    monkeypatch, installer, module_name, requirement, skip
):
    monkeypatch.setattr(
        platform_dependencies,
        "get_platform_dependencies",
        lambda *_args: [(module_name, requirement)],
    )
    installer.missing = [requirement]
    monkeypatch.setattr(
        platform_dependencies.importlib.metadata, "version", lambda _name: "0.1"
    )
    if skip == "noninteractive":
        monkeypatch.setattr(installer.stdin, "isatty", lambda: False)
    else:
        installer.answer = "n" if skip == "decline" else EOFError()
    assert not installer.run()
    assert installer.commands == []
    assert installer.invalidations == []


@pytest.mark.parametrize(
    "failure, already_loaded",
    [("os", False), ("externally_managed", False), ("os", True)],
)
def test_optional_install_failure_warns_without_blocking_startup(
    monkeypatch, installer, failure, already_loaded
):
    requirement = "rpi_ws281x>=4.0.0"
    monkeypatch.setattr(
        platform_dependencies,
        "get_platform_dependencies",
        lambda *_args: [("_rpi_ws281x", requirement)],
    )
    installer.missing = [requirement]
    if already_loaded:
        monkeypatch.setitem(sys.modules, "_rpi_ws281x", SimpleNamespace())

    def failed_install(command, check):
        assert check is True
        if failure == "os":
            raise OSError("Cannot launch pip")
        raise platform_dependencies.subprocess.CalledProcessError(
            1, command, stderr="externally-managed-environment"
        )

    monkeypatch.setattr(platform_dependencies.subprocess, "run", failed_install)
    with pytest.warns(RuntimeWarning, match="optional platform dependencies") as caught:
        assert not installer.run()
    expected = platform_dependencies.format_install_command(
        [requirement], executable=sys.executable
    )
    assert expected in str(caught[0].message)
    assert installer.invalidations == []


def test_partial_upgrade_of_loaded_optional_backend_remains_fatal(
    monkeypatch, installer
):
    requirement = "rpi_ws281x>=4.0.0"
    monkeypatch.setattr(
        platform_dependencies,
        "get_platform_dependencies",
        lambda *_args: [("_rpi_ws281x", requirement)],
    )
    installer.missing = [requirement]
    original = SimpleNamespace()
    monkeypatch.setitem(sys.modules, "_rpi_ws281x", original)
    error = platform_dependencies.subprocess.CalledProcessError(1, ["python"])

    def partial_install(_command, check):
        assert check is True
        raise error

    monkeypatch.setattr(platform_dependencies.subprocess, "run", partial_install)
    with pytest.raises(RuntimeError, match="Unable to install") as raised:
        installer.run()
    assert raised.value.__cause__ is error
    assert sys.modules["_rpi_ws281x"] is original


def test_optional_install_still_invisible_warns_with_restart_guidance(
    monkeypatch, installer
):
    requirement = "Adafruit-Blinka-Raspberry-Pi-PWM>=1.0.2"
    monkeypatch.setattr(
        platform_dependencies,
        "get_platform_dependencies",
        lambda *_args: [("adafruit_blinka_raspberry_pi_pwm", requirement)],
    )
    installer.missing = installer.after_install_missing = [requirement]
    with pytest.warns(RuntimeWarning, match="Restart Python"):
        assert not installer.run()
    assert len(installer.commands) == 1
    assert installer.invalidations == [True]


def test_replacing_loaded_optional_backend_still_requires_restart(
    monkeypatch, installer
):
    requirement = "rpi_ws281x>=4.0.0"
    monkeypatch.setattr(
        platform_dependencies,
        "get_platform_dependencies",
        lambda *_args: [("_rpi_ws281x", requirement)],
    )
    installer.missing = [requirement]
    original = SimpleNamespace()
    monkeypatch.setitem(sys.modules, "_rpi_ws281x", original)
    with pytest.raises(RuntimeError, match="Restart Python"):
        installer.run()
    assert sys.modules["_rpi_ws281x"] is original
    assert len(installer.commands) == 1


@pytest.mark.parametrize("failure", ["os", "pip"])
def test_pip_failure_preserves_cause_and_quotes_recovery_command(
    monkeypatch, installer, failure
):
    error = (
        OSError("Cannot launch Python")
        if failure == "os"
        else platform_dependencies.subprocess.CalledProcessError(1, ["python"])
    )

    def failed_run(_command, check):
        assert check is True
        raise error

    monkeypatch.setattr(
        platform_dependencies.sys, "executable", "/path with spaces/python"
    )
    monkeypatch.setattr(platform_dependencies.subprocess, "run", failed_run)
    with pytest.raises(RuntimeError) as raised:
        installer.run()
    assert raised.value.__cause__ is error
    assert "'/path with spaces/python' -m pip install 'Adafruit_BBIO>=1.2.4'" in str(
        raised.value
    )
    assert installer.invalidations == []


@pytest.mark.parametrize("skip", ["noninteractive", "decline", "eof"])
def test_skipped_upgrade_reports_unsupported_installed_version(
    monkeypatch, installer, skip
):
    monkeypatch.setattr(
        platform_dependencies.importlib.metadata, "version", lambda _name: "1.2.3"
    )
    if skip == "noninteractive":
        monkeypatch.setattr(installer.stdin, "isatty", lambda: False)
    else:
        installer.answer = "n" if skip == "decline" else EOFError()
    with pytest.raises(RuntimeError, match="unsupported versions") as raised:
        installer.run()
    command = platform_dependencies.format_install_command(
        ["Adafruit_BBIO>=1.2.4"], executable=platform_dependencies.sys.executable
    )
    assert command in str(raised.value)
    assert "restart Python" in str(raised.value)
    assert installer.commands == []
    assert installer.invalidations == []


@pytest.mark.parametrize("version", ["1.2.3", None], ids=["outdated", "no_metadata"])
def test_replacing_loaded_module_requires_restart_without_reloading(
    monkeypatch, installer, version
):
    loaded_module = SimpleNamespace()
    monkeypatch.setitem(
        platform_dependencies.sys.modules, "Adafruit_BBIO", loaded_module
    )
    if version is not None:
        monkeypatch.setattr(
            platform_dependencies.importlib.metadata, "version", lambda _name: version
        )
    with pytest.raises(RuntimeError, match="Restart Python"):
        installer.run()
    assert platform_dependencies.sys.modules["Adafruit_BBIO"] is loaded_module
    assert len(installer.commands) == 1
    assert installer.invalidations == [True]


def _load_board_startup(monkeypatch, implementation):
    """Execute the public board module with no platform-specific imports."""
    events = []
    detector = _detector(any_raspberry_pi=True)
    agnostic = ModuleType("adafruit_blinka.agnostic")
    agnostic.detector = detector
    agnostic.board_id = "RUNTIME_TEST_BOARD"
    imports = ModuleType("adafruit_blinka.importing")
    imports.get_import_file = lambda *_args: "_runtime_test_registry"

    def import_board(caller_globals, module_name):
        events.append(("board", module_name))
        caller_globals["TEST_PIN"] = "stubbed pin"

    imports.import_mod = import_board
    dependencies = ModuleType("adafruit_blinka.platform_dependencies")
    if implementation == "cpython":
        dependencies.install_missing_platform_dependencies = (
            lambda selected: events.append(("install", selected))
        )
    original_open = builtins.open

    def open_registry(path, *args, **kwargs):
        if path == "_runtime_test_registry":
            return io.StringIO('{"any_raspberry_pi": "_runtime_test_board"}')
        return original_open(path, *args, **kwargs)

    with monkeypatch.context() as patches:
        patches.setitem(sys.modules, "adafruit_blinka.agnostic", agnostic)
        patches.setitem(sys.modules, "adafruit_blinka.importing", imports)
        patches.setitem(
            sys.modules, "adafruit_blinka.platform_dependencies", dependencies
        )
        patches.setattr(sys.implementation, "name", implementation)
        patches.setattr(builtins, "open", open_registry)
        namespace = runpy.run_path(str(Path(__file__).parents[1] / "src" / "board.py"))
    return detector, events, namespace


def test_public_board_installs_before_importing_detected_board(monkeypatch):
    detector, events, namespace = _load_board_startup(monkeypatch, "cpython")
    assert events == [("install", detector), ("board", "_runtime_test_board")]
    assert namespace["TEST_PIN"] == "stubbed pin"


@pytest.mark.parametrize("implementation", ["micropython", "circuitpython"])
def test_public_board_skips_cpython_only_installer(monkeypatch, implementation):
    _detected, events, namespace = _load_board_startup(monkeypatch, implementation)
    # The dependency stub deliberately has no installer on these interpreters.
    assert events == [("board", "_runtime_test_board")]
    assert namespace["TEST_PIN"] == "stubbed pin"


@pytest.mark.parametrize(
    "on_search_path, installed_version, available",
    [
        (False, "1.0", False),
        (True, "1.0", True),
        (True, "0.9", False),
        (True, None, False),
    ],
    ids=["first_user_site", "existing_search_path", "wrong_version", "no_metadata"],
)
def test_installer_checks_newly_installed_dependency_availability(
    monkeypatch, tmp_path, on_search_path, installed_version, available
):
    module_name = f"blinka_install_probe_{tmp_path.name}"
    distribution_name = module_name.replace("_", "-")
    requirement = f"{distribution_name}>=1.0,<2"
    install_directory = tmp_path / "user-site"
    detector = _detector()
    commands = []
    terminal = SimpleNamespace(stdin=io.StringIO(), stdout=io.StringIO())
    terminal.stdin.isatty = terminal.stdout.isatty = lambda: True

    if on_search_path:
        install_directory.mkdir()
        monkeypatch.syspath_prepend(str(install_directory))
    else:
        assert not install_directory.exists()
        assert str(install_directory) not in sys.path

    monkeypatch.setattr(
        platform_dependencies,
        "get_platform_dependencies",
        lambda *_args, **_kwargs: [(module_name, requirement)],
    )

    def install(command, check):
        assert check is True
        commands.append(command)
        install_directory.mkdir(exist_ok=True)
        (install_directory / f"{module_name}.py").write_text(
            "VALUE = 'installed'\n", encoding="utf-8"
        )
        if installed_version is not None:
            metadata_directory = (
                install_directory / f"{module_name}-{installed_version}.dist-info"
            )
            metadata_directory.mkdir()
            (metadata_directory / "METADATA").write_text(
                "Metadata-Version: 2.1\n"
                f"Name: {distribution_name}\n"
                f"Version: {installed_version}\n",
                encoding="utf-8",
            )

    monkeypatch.setattr(platform_dependencies.subprocess, "run", install)
    assert platform_dependencies.get_missing_platform_dependencies(detector) == [
        requirement
    ]

    with monkeypatch.context() as streams:
        streams.setattr(platform_dependencies.sys, "stdin", terminal.stdin)
        streams.setattr(platform_dependencies.sys, "stdout", terminal.stdout)
        if available:
            assert platform_dependencies.install_missing_platform_dependencies(
                detector, input_func=lambda _prompt: "y"
            )
        else:
            with pytest.raises(RuntimeError, match="[Rr]estart Python") as raised:
                platform_dependencies.install_missing_platform_dependencies(
                    detector, input_func=lambda _prompt: "y"
                )
            assert requirement in str(raised.value)
            assert platform_dependencies.format_install_command(
                [requirement], executable=sys.executable
            ) in str(raised.value)

    assert len(commands) == 1
    assert install_directory.is_dir()
    assert (str(install_directory) in sys.path) is on_search_path
    assert platform_dependencies.get_missing_platform_dependencies(detector) == (
        [] if available else [requirement]
    )
