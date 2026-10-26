# SPDX-FileCopyrightText: 2026 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""Exercise the API checker without importing Blinka drivers or installing tools."""

import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import subprocess
from types import ModuleType, SimpleNamespace

import pytest

# Pytest supplies the named fixtures.
# pylint: disable=redefined-outer-name

ROOT = Path(__file__).parents[1]
SOURCE = ROOT / "scripts/check_circuitpython_api.py"
DIAGNOSTIC = (
    'busio.I2C.__init__ is inconsistent, runtime does not have parameter "timeout"'
)


@pytest.fixture
def checker():
    """Load development tooling only, without importing the production package."""
    spec = importlib.util.spec_from_file_location("_test_circuitpython_api", SOURCE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def distribution(*files):
    """Supply distribution file metadata, never an importable implementation."""
    return SimpleNamespace(files=[PurePosixPath(name) for name in files])


def baseline(checker, diagnostics=(), modules=None):
    """Construct the tracked observations used by the baseline gate."""
    return {
        "reference": dict(checker.REFERENCE),
        "target": checker.TARGET,
        "modules": {"busio": "checked"} if modules is None else modules,
        "diagnostics": list(diagnostics),
    }


def test_stub_inventory_starts_with_reference_and_includes_packages(checker):
    result = checker.stub_modules(
        distribution(
            "busio-stubs/__init__.pyi",
            "missing-stubs/__init__.pyi",
            "alarm-stubs/pin/__init__.pyi",
            "alarm-stubs/time.pyi",
            "alarm-stubs/__init__.pyi",
            "alarm-stubs/py.typed",
            "board_definitions/feather_rp2040/__init__.pyi",
            "circuitpython_stubs-10.3.1.dist-info/METADATA",
            "invalid-name-stubs/__init__.pyi",
        )
    )
    assert result == ["alarm", "alarm.pin", "alarm.time", "busio", "missing"]


@pytest.mark.parametrize("files", [[], None, ["board_definitions/pico/__init__.pyi"]])
def test_missing_stub_payload_is_a_tool_failure(checker, files):
    with pytest.raises(checker.CheckError, match="no module files"):
        checker.stub_modules(SimpleNamespace(files=files))


def test_source_inventory_does_not_execute_modules(checker, tmp_path):
    (tmp_path / "busio.py").write_text("raise AssertionError('must not import')\n")
    (tmp_path / "microcontroller").mkdir()
    (tmp_path / "microcontroller/__init__.py").write_text("raise AssertionError\n")
    (tmp_path / "microcontroller/pin.py").write_text("raise AssertionError\n")
    (tmp_path / "bad-name.py").write_text("raise AssertionError\n")
    (tmp_path / "__init__.py").write_text("raise AssertionError\n")
    assert checker.source_modules(tmp_path) == {
        "busio",
        "microcontroller",
        "microcontroller.pin",
    }


def test_inventory_distinguishes_coverage_from_platform_availability(checker):
    names = [
        "busio",
        "microcontroller",
        "alarm",
        "displayio",
        "adafruit_bus_device.i2c_device",
        "adafruit_pixelbuf",
        "os",
        "usb_hid",
        "pulseio",
        "rotaryio",
        "new_backend",
        "onewireio",
    ]
    implemented = {
        "busio",
        "microcontroller",
        "usb_hid",
        "pulseio",
        "rotaryio",
        "new_backend",
        "onewireio",
    }
    result = {item["name"]: item for item in checker.inventory(names, implemented)}
    assert {name: value["status"] for name, value in result.items()} == {
        "busio": "checked",
        "microcontroller": "checked",
        "alarm": "missing",
        "displayio": "separate_package",
        "adafruit_bus_device.i2c_device": "separate_package",
        "adafruit_pixelbuf": "separate_package",
        "os": "host_provided",
        "usb_hid": "not_checked",
        "pulseio": "not_checked",
        "rotaryio": "not_checked",
        "new_backend": "not_checked",
        "onewireio": "checked",
    }
    assert "not checked" in result["os"]["reason"]
    assert "unimplemented placeholder" in result["onewireio"]["reason"]
    assert result["displayio"]["reason"] == "Adafruit-Blinka-Displayio"


@pytest.mark.parametrize(
    "name",
    [
        "displayio",
        "bitmaptools",
        "busdisplay",
        "epaperdisplay",
        "fontio",
        "fourwire",
        "i2cdisplaybus",
        "paralleldisplaybus",
        "terminalio",
        "vectorio",
    ],
)
def test_displayio_distribution_modules_are_not_reported_as_missing(checker, name):
    assert checker.inventory([name], set()) == [
        {
            "name": name,
            "status": "separate_package",
            "reason": "Adafruit-Blinka-Displayio",
        }
    ]


def test_worker_does_not_inherit_hardware_or_python_target(
    checker, monkeypatch, tmp_path
):
    for name, value in {
        "BLINKA_MCP2221": "1",
        "BLINKA_FT232H": "1",
        "BLINKA_FORCECHIP": "BCM2712",
        "BLINKA_FORCEBOARD": "RASPBERRY_PI_5",
        "BLINKA_SKIP_DEPENDENCY_CHECK": "0",
        "PYTHONPATH": "/untrusted/source",
        "PYTHONSTARTUP": "/untrusted/startup.py",
        "MYPYPATH": "/untrusted/stubs",
        "MYPY_CACHE_DIR": "/untrusted/cache",
        "CHECKER_TEST_PRESERVE": "kept",
    }.items():
        monkeypatch.setenv(name, value)
    result = checker.worker_environment(tmp_path)
    assert result["BLINKA_FORCECHIP"] == checker.TARGET
    assert result["BLINKA_FORCEBOARD"] == "OS_AGNOSTIC_BOARD"
    assert result["BLINKA_SKIP_DEPENDENCY_CHECK"] == "1"
    assert "BLINKA_MCP2221" not in result
    assert "BLINKA_FT232H" not in result
    assert "PYTHONPATH" not in result
    assert "PYTHONSTARTUP" not in result
    assert "MYPYPATH" not in result
    assert result["MYPY_CACHE_DIR"] == str(tmp_path / "mypy-cache")
    assert result["TMPDIR"] == str(tmp_path)
    assert result["CHECKER_TEST_PRESERVE"] == "kept"
    assert os.environ["BLINKA_FORCECHIP"] == "BCM2712"


@pytest.mark.parametrize("path", ["/dev/gpiochip0", "/proc/modules", "/sys/class/pwm"])
@pytest.mark.parametrize("event", ["open", "os.listdir", "os.scandir"])
def test_audit_guard_rejects_kernel_access_without_touching_it(
    checker, tmp_path, path, event
):
    guard = checker.audit_guard(tmp_path)
    args = (path, "r", os.O_RDONLY) if event == "open" else (path,)
    with pytest.raises(checker.CheckError, match="hardware/kernel access"):
        guard(event, args)


@pytest.mark.parametrize(
    "event,args",
    [
        ("import", ("hid",)),
        ("import", ("gpiod.line",)),
        ("import", ("lgpio",)),
        ("import", ("RPi.GPIO",)),
        ("import", ("usb.core",)),
        ("import", ("pyftdi",)),
        ("import", ("serial",)),
        ("import", ("usb_hid",)),
        ("import", ("adafruit_blinka.microcontroller.bcm2712",)),
        ("subprocess.Popen", ("pip",)),
        ("socket.connect", ()),
        ("os.system", ("pip install something",)),
        ("os.exec", ()),
        ("os.spawn", ()),
        ("os.fork", ()),
        ("ctypes.dlopen", ("libgpiod.so",)),
    ],
)
def test_audit_guard_rejects_hardware_imports_and_external_operations(
    checker, tmp_path, event, args
):
    with pytest.raises(checker.CheckError, match="Blocked"):
        checker.audit_guard(tmp_path)(event, args)


def test_audit_guard_permits_source_reads_and_scratch_writes(checker, tmp_path):
    guard = checker.audit_guard(tmp_path)
    guard("open", (SOURCE, "r", os.O_RDONLY))
    guard("open", (tmp_path / "cache", "w", os.O_WRONLY | os.O_CREAT))
    guard("open", (os.devnull, "r", os.O_RDONLY))
    guard("open", (0, "r", os.O_RDONLY))
    guard("os.mkdir", (str(tmp_path / "nested"),))
    guard("import", ("adafruit_blinka.microcontroller.generic_agnostic_board.pin",))
    guard("import", ("json",))


@pytest.mark.parametrize("event", ["os.remove", "os.rmdir", "os.mkdir", "os.chmod"])
def test_audit_guard_rejects_writes_outside_scratch(checker, tmp_path, event):
    with pytest.raises(checker.CheckError, match="outside checker scratch"):
        checker.audit_guard(tmp_path)(event, (str(tmp_path.parent / "not-scratch"),))


@pytest.mark.parametrize("event", ["os.rename", "os.link", "os.symlink"])
@pytest.mark.parametrize("outside_first", [False, True])
def test_audit_guard_checks_both_paths(checker, tmp_path, event, outside_first):
    inside, outside = tmp_path / "inside", tmp_path.parent / "outside"
    paths = (outside, inside) if outside_first else (inside, outside)
    with pytest.raises(checker.CheckError, match="outside checker scratch"):
        checker.audit_guard(tmp_path)(event, paths)


@pytest.mark.parametrize("flags", [os.O_WRONLY, os.O_RDWR, os.O_CREAT, os.O_TRUNC])
def test_audit_guard_checks_native_open_flags(checker, tmp_path, flags):
    with pytest.raises(checker.CheckError, match="outside checker scratch"):
        checker.audit_guard(tmp_path)("open", (SOURCE, None, flags))


def test_diagnostics_are_exact_deduplicated_and_sorted(checker):
    other = "keypad.Event.timestamp is not present at runtime"
    process = SimpleNamespace(
        returncode=1, stdout=f"{other}\n{DIAGNOSTIC}\n{DIAGNOSTIC}\n", stderr=""
    )
    assert checker.parse_diagnostics(process) == sorted([DIAGNOSTIC, other])
    assert (
        checker.parse_diagnostics(SimpleNamespace(returncode=0, stdout="", stderr=""))
        == []
    )


@pytest.mark.parametrize(
    "returncode,stdout,stderr",
    [
        (1, "busio failed to import. ModuleNotFoundError: missing\n", ""),
        (1, "error: not checking stubs due to mypy build errors\n", ""),
        (1, "wifi.Radio is not present at runtime\n", ""),
        (1, "unexpected progress message\n", ""),
        (1, "", ""),
        (0, DIAGNOSTIC + "\n", ""),
        (2, "", "tool crashed"),
        (-9, "", ""),
        (1, DIAGNOSTIC + "\n", "unexpected warning"),
    ],
)
def test_tool_and_import_failures_cannot_become_baseline_entries(
    checker, returncode, stdout, stderr
):
    process = SimpleNamespace(returncode=returncode, stdout=stdout, stderr=stderr)
    with pytest.raises(checker.CheckError):
        checker.parse_diagnostics(process)


def test_run_uses_isolated_subprocess_and_scratch(checker, monkeypatch):
    calls = []

    def fake_run(command, **kwargs):
        calls.append((command, kwargs))
        assert Path(kwargs["cwd"]).is_dir()
        assert command[1] == "-I"
        assert command[-1] == "--_worker"
        assert kwargs["env"]["BLINKA_SKIP_DEPENDENCY_CHECK"] == "1"
        assert kwargs["capture_output"] and kwargs["text"]
        assert kwargs["check"] is False
        assert kwargs["timeout"] > 0
        return SimpleNamespace(returncode=1, stdout=DIAGNOSTIC + "\n", stderr="")

    monkeypatch.setattr(checker.subprocess, "run", fake_run)
    assert checker.run_stubtest() == [DIAGNOSTIC]
    assert len(calls) == 1
    assert not Path(calls[0][1]["cwd"]).exists()


def test_timeout_is_reported_as_a_tool_failure(checker, monkeypatch):
    def timeout(command, **_kwargs):
        raise subprocess.TimeoutExpired(command, 120)

    monkeypatch.setattr(checker.subprocess, "run", timeout)
    with pytest.raises(checker.CheckError, match="timed out"):
        checker.run_stubtest()


def test_snapshot_does_not_hide_exact_diagnostics(checker):
    report = {
        "modules": [{"name": "busio", "status": "checked", "reason": "notes"}],
        "diagnostics": [DIAGNOSTIC],
        "errors": [],
        "new": [],
        "resolved": [],
    }
    assert checker.snapshot(report) == baseline(checker, [DIAGNOSTIC])
    assert DIAGNOSTIC in checker.markdown_report(report)
    assert "All current stub discrepancies" in checker.markdown_report(report)


def test_identical_baseline_passes(checker):
    current = baseline(checker, [DIAGNOSTIC])
    assert checker.compare_baseline(current, current) == ([], [])


def test_diagnostic_changes_identify_both_new_and_resolved(checker):
    old = "busio.I2C.old is not present at runtime"
    assert checker.compare_baseline(
        baseline(checker, [DIAGNOSTIC]), baseline(checker, [old])
    ) == ([DIAGNOSTIC], [old])


def test_inventory_changes_are_not_silently_accepted(checker):
    new, resolved = checker.compare_baseline(
        baseline(checker, modules={"busio": "checked", "alarm": "not_checked"}),
        baseline(checker, modules={"busio": "checked", "alarm": "missing"}),
    )
    assert new == ["inventory: alarm: not_checked"]
    assert resolved == ["inventory: alarm: missing"]


@pytest.mark.parametrize(
    "change",
    [
        {"reference": {"circuitpython-stubs": "different"}},
        {"target": "BCM2712"},
        {"modules": []},
        {"diagnostics": {}},
    ],
)
def test_baseline_reference_and_schema_fail_closed(checker, change):
    previous = baseline(checker)
    previous.update(change)
    with pytest.raises(checker.CheckError):
        checker.compare_baseline(baseline(checker), previous)


@pytest.mark.parametrize("previous", [None, [], "not an object"])
def test_baseline_requires_a_json_object(checker, previous):
    with pytest.raises(checker.CheckError, match="Invalid baseline schema"):
        checker.compare_baseline(baseline(checker), previous)


@pytest.mark.parametrize(
    "change",
    [
        {"diagnostics": [{}]},
        {"diagnostics": [["nested"]]},
        {"diagnostics": [42]},
        {"modules": {42: "checked"}},
        {"modules": {"busio": []}},
        {"modules": {"busio": {}}},
    ],
)
def test_baseline_observations_must_be_strings(checker, change):
    previous = baseline(checker)
    previous.update(change)
    with pytest.raises(checker.CheckError, match="Invalid baseline schema"):
        checker.compare_baseline(baseline(checker), previous)


@pytest.fixture
def cli(checker, monkeypatch, tmp_path):
    """Replace every dependency query and worker run before invoking the CLI."""
    monkeypatch.setattr(checker, "CHECKED_MODULES", ("busio",))
    monkeypatch.setattr(checker, "BASELINE", tmp_path / "baseline.json")
    monkeypatch.setattr(
        checker.metadata, "version", lambda name: checker.REFERENCE[name]
    )
    monkeypatch.setattr(
        checker.metadata,
        "distribution",
        lambda _name: distribution(
            "busio-stubs/__init__.pyi", "alarm-stubs/__init__.pyi"
        ),
    )
    monkeypatch.setattr(checker, "source_modules", lambda _path: {"busio"})
    monkeypatch.setattr(checker, "run_stubtest", lambda: [DIAGNOSTIC])
    checker.BASELINE.write_text(
        json.dumps(
            baseline(checker, [DIAGNOSTIC], {"alarm": "missing", "busio": "checked"})
        )
    )
    return checker


def test_cli_default_is_read_only_and_full_reports_keep_existing_differences(
    cli, tmp_path
):
    previous = cli.BASELINE.read_bytes()
    report_path = tmp_path / "report.json"
    markdown_path = tmp_path / "report.md"
    assert cli.main(["--json", str(report_path), "--markdown", str(markdown_path)]) == 0
    assert cli.BASELINE.read_bytes() == previous
    report = json.loads(report_path.read_text())
    assert report["diagnostics"] == [DIAGNOSTIC]
    assert report["new"] == report["resolved"] == report["errors"] == []
    assert DIAGNOSTIC in markdown_path.read_text()
    assert any(
        item["name"] == "alarm" and item["status"] == "missing"
        for item in report["modules"]
    )


@pytest.mark.parametrize(
    "observed", [[], [DIAGNOSTIC, "busio.Parity is not present at runtime"]]
)
def test_cli_fails_on_new_and_resolved_diagnostics(cli, monkeypatch, observed):
    monkeypatch.setattr(cli, "run_stubtest", lambda: observed)
    previous = cli.BASELINE.read_bytes()
    assert cli.main([]) == 1
    assert cli.BASELINE.read_bytes() == previous


def test_explicit_update_records_current_diagnostics(cli, monkeypatch):
    new_diagnostic = "busio.Parity is not present at runtime"
    monkeypatch.setattr(cli, "run_stubtest", lambda: [new_diagnostic])
    assert cli.main(["--update-baseline"]) == 0
    assert json.loads(cli.BASELINE.read_text())["diagnostics"] == [new_diagnostic]


def test_matching_stable_tag_runs_normal_check(cli, monkeypatch):
    calls = []

    def worker():
        calls.append("checked")
        return [DIAGNOSTIC]

    monkeypatch.setattr(cli, "run_stubtest", worker)
    previous = cli.BASELINE.read_bytes()
    assert cli.main(["--stable-release", cli.REFERENCE["circuitpython-stubs"]]) == 0
    assert calls == ["checked"]
    assert cli.BASELINE.read_bytes() == previous


@pytest.mark.parametrize("update", [[], ["--update-baseline"]])
def test_changed_stable_tag_stops_before_dependency_queries_or_worker(
    cli, monkeypatch, tmp_path, update
):
    def unexpected(*_args):
        pytest.fail(
            "An outdated reference must stop before dependency or runtime checks"
        )

    monkeypatch.setattr(cli.metadata, "version", unexpected)
    monkeypatch.setattr(cli.metadata, "distribution", unexpected)
    monkeypatch.setattr(cli, "run_stubtest", unexpected)
    previous = cli.BASELINE.read_bytes()
    report_path = tmp_path / "outdated.json"
    assert (
        cli.main(["--stable-release", "99.0.0", "--json", str(report_path), *update])
        == 2
    )
    assert cli.BASELINE.read_bytes() == previous
    report = json.loads(report_path.read_text())
    assert report["diagnostics"] == []
    assert len(report["errors"]) == 1
    assert "CircuitPython stable is 99.0.0" in report["errors"][0]
    assert "Update the matching stubs" in report["errors"][0]


@pytest.mark.parametrize("failure", ["import", "version", "missing_stubs"])
def test_explicit_update_never_accepts_a_checker_failure(
    cli, monkeypatch, failure, tmp_path
):
    if failure == "import":

        def fail():
            raise cli.CheckError("busio failed to import")

        monkeypatch.setattr(cli, "run_stubtest", fail)
    elif failure == "version":
        monkeypatch.setattr(cli.metadata, "version", lambda _name: "unexpected")
    else:
        monkeypatch.setattr(cli.metadata, "distribution", lambda _name: distribution())
    previous = cli.BASELINE.read_bytes()
    report_path = tmp_path / "failure.json"
    assert cli.main(["--update-baseline", "--json", str(report_path)]) == 2
    assert cli.BASELINE.read_bytes() == previous
    assert json.loads(report_path.read_text())["errors"]


def test_missing_baseline_is_not_silently_created(cli):
    cli.BASELINE.unlink()
    assert cli.main([]) == 2
    assert not cli.BASELINE.exists()


def test_development_requirements_match_reference_pins(checker):
    pins = {}
    for line in (ROOT / "requirements-api.txt").read_text().splitlines():
        line = line.strip()
        if line and not line.startswith(("#", "-r ")):
            name, version = line.split("==")
            pins[name] = version
    assert pins == checker.REFERENCE


def test_importing_checker_does_not_import_production_modules(checker):
    """The fixture itself intentionally executes no production import statements."""
    assert checker.SOURCE == ROOT / "src"
    assert "usb_hid" not in checker.CHECKED_MODULES
    assert "pulseio" not in checker.CHECKED_MODULES


@pytest.mark.parametrize(
    "message",
    [
        "busio encountered unexpected error, CheckError: "
        "Blocked hardware/kernel access: /dev/example",
        "busio encountered unexpected error, RuntimeError: introspection failed",
        "busio failed to find stubs",
        "busio.Widget is an unknown mypy node",
    ],
)
def test_introspection_failures_are_not_api_diagnostics(checker, message):
    # Real mypy 2.4.0 test_module emits the first format when runtime __dir__
    # raises CheckError. It is not evidence of a completed API comparison.
    process = subprocess.CompletedProcess([], 1, stdout=message + "\n", stderr="")
    with pytest.raises(checker.CheckError, match="Unexpected stubtest output"):
        checker.parse_diagnostics(process)


def test_update_cannot_baseline_a_caught_audit_failure(cli, monkeypatch, tmp_path):
    process = subprocess.CompletedProcess(
        [],
        1,
        stdout="busio encountered unexpected error, CheckError: "
        "Blocked hardware/kernel access: /dev/example\n",
        stderr="",
    )
    monkeypatch.setattr(cli, "run_stubtest", lambda: cli.parse_diagnostics(process))
    previous = cli.BASELINE.read_bytes()
    report_path = tmp_path / "failure.json"
    assert cli.main(["--update-baseline", "--json", str(report_path)]) == 2
    assert cli.BASELINE.read_bytes() == previous
    report = json.loads(report_path.read_text())
    assert report["diagnostics"] == []
    assert "encountered unexpected error" in report["errors"][0]


@pytest.mark.parametrize(
    "message",
    [
        "busio.I2C has `__final__` attribute, but isn't marked with @final in the stub",
        "busio.I2C cannot be subclassed at runtime, but isn't marked with @final in the stub",
        "busio.I2C metaclass mismatch",
        "busio.__all__ names exported from the stub do not correspond "
        "to the names exported at runtime.",
        "busio.value variable differs from runtime type int",
    ],
)
def test_legitimate_non_is_api_findings_can_be_reported_and_baselined(
    cli, monkeypatch, message
):
    process = subprocess.CompletedProcess([], 1, stdout=message + "\n", stderr="")
    assert cli.parse_diagnostics(process) == [message]
    monkeypatch.setattr(cli, "run_stubtest", lambda: cli.parse_diagnostics(process))
    assert cli.main(["--update-baseline"]) == 0
    assert json.loads(cli.BASELINE.read_text())["diagnostics"] == [message]


def test_real_stubtest_introspection_failure_is_rejected(checker, monkeypatch):
    """Exercise the pinned tool, using only synthetic runtime objects."""
    nodes = pytest.importorskip("mypy.nodes")
    stubtest = pytest.importorskip("mypy.stubtest")

    class BrokenModule(ModuleType):
        def __dir__(self):
            raise checker.CheckError("Blocked hardware/kernel access: /dev/example")

    runtime = BrokenModule("busio")
    stub = nodes.MypyFile([], [], False)
    stub._fullname = "busio"  # pylint: disable=protected-access
    stub.names = {}
    monkeypatch.setattr(stubtest, "get_stub", lambda _: stub)
    monkeypatch.setattr(stubtest, "silent_import_module", lambda _: runtime)
    lines = [
        error.get_description(concise=True) for error in stubtest.test_module("busio")
    ]
    assert lines == [
        "busio encountered unexpected error, CheckError: "
        "Blocked hardware/kernel access: /dev/example"
    ]
    process = subprocess.CompletedProcess(
        [], 1, stdout="\n".join(lines) + "\n", stderr=""
    )
    with pytest.raises(checker.CheckError, match="Unexpected stubtest output"):
        checker.parse_diagnostics(process)


def test_real_stubtest_finality_findings_are_preserved(checker):
    nodes = pytest.importorskip("mypy.nodes")
    stubtest = pytest.importorskip("mypy.stubtest")
    stub = nodes.TypeInfo(
        nodes.SymbolTable(), nodes.ClassDef("I2C", nodes.Block([])), "busio"
    )

    class FinalRuntime:  # pylint: disable=too-few-public-methods
        __final__ = True

    class CannotSubclass:  # pylint: disable=too-few-public-methods
        def __init_subclass__(cls):
            raise TypeError("Cannot subclass")

    for runtime, prefix in ((FinalRuntime, "has"), (CannotSubclass, "cannot")):
        # The private helper belongs to the exact pinned development tool.
        # pylint: disable=protected-access
        errors = list(stubtest._verify_final(stub, runtime, ["busio", "I2C"]))
        # pylint: enable=protected-access
        assert len(errors) == 1
        assert not errors[0].is_missing_stub()
        line = errors[0].get_description(concise=True)
        assert line.startswith("busio.I2C " + prefix)
        process = subprocess.CompletedProcess([], 1, stdout=line + "\n", stderr="")
        assert checker.parse_diagnostics(process) == [line]


def test_worker_rejects_swallowed_audit_failure(checker, monkeypatch, tmp_path):
    """No real imports or permanent hooks: emulate a tool catching the exception."""
    guard = checker.audit_guard(tmp_path)
    registered = []
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(checker.sys, "path", list(checker.sys.path))
    monkeypatch.setattr(checker.sys, "argv", list(checker.sys.argv))
    monkeypatch.setattr(
        checker.sys, "dont_write_bytecode", checker.sys.dont_write_bytecode
    )
    monkeypatch.setattr(checker.sys, "addaudithook", registered.append)
    monkeypatch.setattr(checker, "audit_guard", lambda _: guard)

    def import_fake(name):
        if name == "adafruit_blinka.agnostic":
            return SimpleNamespace(chip_id=checker.TARGET, board_id="OS_AGNOSTIC_BOARD")
        return SimpleNamespace(__file__=str(checker.SOURCE / (name + ".py")))

    def swallow():
        try:
            guard("open", ("/dev/example", "r", os.O_RDONLY))
        except checker.CheckError:
            pass
        return 0

    fake_mypy = ModuleType("mypy")
    fake_mypy.stubtest = SimpleNamespace(main=swallow)
    monkeypatch.setitem(checker.sys.modules, "mypy", fake_mypy)
    monkeypatch.setattr(checker.importlib, "import_module", import_fake)
    with pytest.raises(checker.CheckError, match="caught an audit failure"):
        checker.stubtest_worker()
    assert registered == [guard]
    assert len(guard.failures) == 1
