# SPDX-FileCopyrightText: 2026 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""Hardware-free tests for manual recovery in Python environments without pip."""

import io
import shlex
import sys
from types import SimpleNamespace

import pytest

from adafruit_blinka import importing
from adafruit_blinka import platform_dependencies

# Pytest supplies the named fixtures.
# pylint: disable=redefined-outer-name


@pytest.fixture(autouse=True)
def dependency_check_environment(monkeypatch):
    """Isolate host tools while retaining the real detector for focused tests."""
    monkeypatch.delenv("BLINKA_SKIP_DEPENDENCY_CHECK", raising=False)
    # pylint: disable-next=protected-access
    pip_available = platform_dependencies._pip_available
    monkeypatch.setattr(platform_dependencies, "_pip_available", lambda: True)
    monkeypatch.setattr(
        platform_dependencies.subprocess,
        "run",
        lambda *_args, **_kwargs: pytest.fail("Real package installation is forbidden"),
    )
    return pip_available


@pytest.fixture
def detector():
    """Provide a synthetic platform without detecting or importing hardware."""
    return SimpleNamespace(
        board=SimpleNamespace(
            any_raspberry_pi=False,
            any_raspberry_pi_5_board=False,
            any_jetson_board=False,
        ),
        chip=SimpleNamespace(id="AM33XX"),
    )


@pytest.fixture
def installer(monkeypatch, detector):
    """Record installer effects using fake discovery, metadata, streams and pip."""
    state = SimpleNamespace(
        detector=detector,
        missing=["Adafruit_BBIO>=1.2.4"],
        availability_checks=[],
        answer="y",
        prompts=[],
        commands=[],
        invalidations=[],
        stdin=io.StringIO(),
        stdout=io.StringIO(),
    )
    state.stdin.isatty = state.stdout.isatty = lambda: True

    def no_metadata(name):
        raise platform_dependencies.importlib.metadata.PackageNotFoundError(name)

    def answer(prompt):
        state.prompts.append(prompt)
        if isinstance(state.answer, BaseException):
            raise state.answer
        return state.answer

    def missing_dependencies(*_args):
        state.availability_checks.append(list(state.missing))
        return state.missing

    def run():
        with monkeypatch.context() as streams:
            streams.setattr(platform_dependencies.sys, "stdin", state.stdin)
            streams.setattr(platform_dependencies.sys, "stdout", state.stdout)
            return platform_dependencies.install_missing_platform_dependencies(
                state.detector, input_func=answer
            )

    state.run = run
    monkeypatch.setattr(
        platform_dependencies, "get_missing_platform_dependencies", missing_dependencies
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


@pytest.mark.parametrize("present", [False, True])
def test_pip_availability_checks_spec_without_importing(
    monkeypatch, dependency_check_environment, present
):
    names = []

    def find_spec(name):
        names.append(name)
        return object() if present else None

    monkeypatch.setattr(platform_dependencies.importlib.util, "find_spec", find_spec)
    assert dependency_check_environment() is present
    assert names == ["pip"]


@pytest.mark.parametrize("failure", [ImportError, ModuleNotFoundError, ValueError])
def test_pip_availability_treats_invalid_spec_as_missing(
    monkeypatch, dependency_check_environment, failure
):
    def invalid_spec(name):
        assert name == "pip"
        raise failure("No usable pip spec")

    monkeypatch.setattr(platform_dependencies.importlib.util, "find_spec", invalid_spec)
    assert dependency_check_environment() is False


def test_manual_command_uses_uv_for_current_python_without_pip(monkeypatch):
    executable = "/python env's/bin/python"
    uv_executable = "/uv tools/bin/uv"
    requirements = ["gpiod>=2.2.2,<3", "Adafruit-Blinka-Raspberry-Pi-PWM>=1.0.2"]
    lookups = []
    monkeypatch.setattr(platform_dependencies.sys, "executable", executable)
    monkeypatch.setattr(platform_dependencies, "_pip_available", lambda: False)

    def which(name):
        lookups.append(name)
        return uv_executable

    monkeypatch.setattr(platform_dependencies.shutil, "which", which)
    command = platform_dependencies.format_install_command(requirements, executable)
    assert shlex.split(command) == [
        "uv",
        "pip",
        "install",
        "--python",
        executable,
        *requirements,
    ]
    assert lookups == ["uv"]


@pytest.mark.parametrize(
    "pip_available, uv_executable, other_python",
    [
        (True, "/uv tools/uv", False),
        (False, None, False),
        (False, "/uv tools/uv", True),
    ],
    ids=["pip_present", "uv_absent", "other_interpreter"],
)
def test_manual_command_keeps_pip_without_usable_uv_target(
    monkeypatch, pip_available, uv_executable, other_python
):
    executable = "/other env/bin/python" if other_python else sys.executable
    lookups = []
    monkeypatch.setattr(platform_dependencies, "_pip_available", lambda: pip_available)

    def which(name):
        lookups.append(name)
        return uv_executable

    monkeypatch.setattr(platform_dependencies.shutil, "which", which)
    command = platform_dependencies.format_install_command(
        ["gpiod>=2.2.2,<3"], executable
    )
    assert shlex.split(command) == [
        executable,
        "-m",
        "pip",
        "install",
        "gpiod>=2.2.2,<3",
    ]
    assert lookups == (["uv"] if not pip_available and not other_python else [])


def test_default_manual_pip_command_does_not_probe_tools(monkeypatch):
    monkeypatch.setattr(
        platform_dependencies,
        "_pip_available",
        lambda: pytest.fail("The default pip command must not inspect this Python"),
    )
    monkeypatch.setattr(
        platform_dependencies.shutil,
        "which",
        lambda _name: pytest.fail("The default pip command must not inspect uv"),
    )
    assert platform_dependencies.format_install_command(["gpiod>=2.2.2,<3"]) == (
        "pip install 'gpiod>=2.2.2,<3'"
    )


@pytest.mark.parametrize("already_loaded", [False, True])
def test_confirmed_install_without_pip_reports_manual_recovery(
    monkeypatch, installer, already_loaded
):
    executable = "/python env's/bin/python"
    requirement = "Adafruit_BBIO>=1.2.4"
    dependency_queries = []
    monkeypatch.setattr(platform_dependencies.sys, "executable", executable)
    monkeypatch.setattr(platform_dependencies, "_pip_available", lambda: False)
    monkeypatch.setattr(
        platform_dependencies,
        "get_platform_dependencies",
        lambda *_args: dependency_queries.append(True)
        or [("Adafruit_BBIO", requirement)],
    )
    if already_loaded:
        monkeypatch.setitem(sys.modules, "Adafruit_BBIO", SimpleNamespace())
    else:
        monkeypatch.delitem(sys.modules, "Adafruit_BBIO", raising=False)

    with pytest.raises(RuntimeError, match="does not contain pip") as raised:
        installer.run()

    message = str(raised.value)
    assert (
        shlex.join(["uv", "pip", "install", "--python", executable, requirement])
        in message
    )
    assert "install pip into this environment" in message
    assert "restart Python" in message
    assert len(installer.prompts) == 1
    # Only optional-dependency classification runs; loaded-state scanning does not.
    assert dependency_queries == [True]
    assert installer.commands == []
    assert installer.invalidations == []
    assert installer.availability_checks == [[requirement]]


@pytest.mark.parametrize("already_loaded", [False, True])
def test_optional_install_without_pip_warns_even_for_loaded_backends(
    monkeypatch, installer, already_loaded
):
    dependencies = [
        ("_rpi_ws281x", "rpi_ws281x>=4.0.0"),
        (
            "adafruit_raspberry_pi5_neopixel_write",
            "Adafruit-Blinka-Raspberry-Pi5-Neopixel",
        ),
        ("adafruit_blinka_raspberry_pi_pwm", "Adafruit-Blinka-Raspberry-Pi-PWM>=1.0.2"),
    ]
    installer.missing = [requirement for _, requirement in dependencies]
    dependency_queries = []
    monkeypatch.setattr(platform_dependencies, "_pip_available", lambda: False)
    monkeypatch.setattr(
        platform_dependencies,
        "get_platform_dependencies",
        lambda *_args: dependency_queries.append(True) or dependencies,
    )
    for module_name, _ in dependencies:
        if already_loaded:
            monkeypatch.setitem(sys.modules, module_name, SimpleNamespace())
        else:
            monkeypatch.delitem(sys.modules, module_name, raising=False)

    with pytest.warns(RuntimeWarning, match="does not contain pip") as caught:
        assert not installer.run()

    message = str(caught[0].message)
    assert (
        shlex.join(
            ["uv", "pip", "install", "--python", sys.executable, *installer.missing]
        )
        in message
    )
    assert "optional features may be unavailable" in message
    assert "restart Python" in message
    assert len(installer.prompts) == 1
    assert dependency_queries == [True]
    assert installer.commands == []
    assert installer.invalidations == []


@pytest.mark.parametrize("skip", ["stdin", "stdout", "decline", "eof", "optout"])
def test_unconfirmed_install_does_not_probe_pip_or_uv(monkeypatch, installer, skip):
    monkeypatch.setattr(
        platform_dependencies,
        "_pip_available",
        lambda: pytest.fail("An unconfirmed install must not inspect pip"),
    )
    monkeypatch.setattr(
        platform_dependencies.shutil,
        "which",
        lambda _name: pytest.fail("An unconfirmed install must not inspect uv"),
    )
    if skip in ("stdin", "stdout"):
        monkeypatch.setattr(getattr(installer, skip), "isatty", lambda: False)
    elif skip == "optout":
        monkeypatch.setenv("BLINKA_SKIP_DEPENDENCY_CHECK", "1")
    else:
        installer.answer = "n" if skip == "decline" else EOFError()

    assert not installer.run()
    assert len(installer.prompts) == (1 if skip in ("decline", "eof") else 0)
    assert installer.commands == []
    assert installer.invalidations == []
    if skip == "optout":
        assert installer.availability_checks == []


@pytest.mark.parametrize(
    "recovery", ["missing_import", "outdated_feature", "outdated_startup"]
)
def test_missing_pip_feature_recovery_uses_uv_without_installing(
    monkeypatch, installer, recovery
):
    executable = "/python env's/bin/python"
    uv_executable = "/uv tools/bin/uv"
    requirement = "Adafruit_BBIO>=1.2.4"
    monkeypatch.setattr(platform_dependencies.sys, "executable", executable)
    monkeypatch.setattr(platform_dependencies, "_pip_available", lambda: False)
    monkeypatch.setattr(
        platform_dependencies.shutil, "which", lambda _name: uv_executable
    )
    monkeypatch.setattr(
        platform_dependencies,
        "get_platform_requirement_for_import",
        lambda *_args, **_kwargs: requirement,
    )
    monkeypatch.setattr(
        platform_dependencies.importlib.metadata, "version", lambda _name: "1.2.3"
    )
    with pytest.raises(RuntimeError) as raised:
        if recovery == "missing_import":
            importing.raise_for_missing_platform_dependency(
                ModuleNotFoundError(name="Adafruit_BBIO")
            )
        elif recovery == "outdated_feature":
            platform_dependencies.check_platform_dependency(
                installer.detector, "Adafruit_BBIO"
            )
        else:
            monkeypatch.setattr(installer.stdin, "isatty", lambda: False)
            installer.run()

    assert shlex.join(
        ["uv", "pip", "install", "--python", executable, requirement]
    ) in str(raised.value)
    assert installer.commands == []
    assert installer.invalidations == []
    assert installer.prompts == []
