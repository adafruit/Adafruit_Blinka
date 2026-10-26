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

# Keep the safety and differential-regression matrix together; pytest supplies fixtures.
# pylint: disable=redefined-outer-name,too-many-lines

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


def empty_report(checker):
    """Construct a report for exercising revision comparison directly."""
    return {
        "reference": dict(checker.REFERENCE),
        "target": checker.TARGET,
        "mode": "revision",
        "checked_modules": [],
        "selection_reason": "",
        "unreferenced_modules": [],
        "base_revision": None,
        "head_revision": None,
        "changed_paths": [],
        "modules": [],
        "diagnostics": [],
        "base_diagnostics": [],
        "errors": [],
        "new": [],
        "resolved": [],
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


def test_inventory_marks_unselected_audited_modules_separately(checker):
    result = {
        item["name"]: item["status"]
        for item in checker.inventory(
            ["busio", "keypad", "keypad.Event", "usb_hid", "alarm"],
            {"busio", "keypad", "keypad.Event", "usb_hid"},
            ["busio"],
        )
    }
    assert result == {
        "busio": "checked",
        "keypad": "not_selected",
        "keypad.Event": "not_selected",
        "usb_hid": "not_checked",
        "alarm": "missing",
    }


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
def test_tool_and_import_failures_cannot_become_api_diagnostics(
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
        assert command[3] == "--_worker"
        assert command[4] == str(checker.SOURCE.resolve())
        assert command[5:] == list(checker.CHECKED_MODULES)
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


def test_selected_worker_only_receives_explicit_source_and_modules(
    checker, monkeypatch, tmp_path
):
    calls = []

    def fake_run(command, **_kwargs):
        calls.append(command)
        return SimpleNamespace(returncode=1, stdout=DIAGNOSTIC + "\n", stderr="")

    monkeypatch.setattr(checker.subprocess, "run", fake_run)
    assert checker.run_stubtest(tmp_path, ["busio"]) == [DIAGNOSTIC]
    assert calls[0][3:] == ["--_worker", str(tmp_path.resolve()), "busio"]
    assert checker.run_stubtest(tmp_path, []) == []
    assert len(calls) == 1


def test_diagnostics_from_unselected_modules_are_a_tool_error(checker):
    process = SimpleNamespace(returncode=1, stdout=DIAGNOSTIC + "\n", stderr="")
    with pytest.raises(checker.CheckError, match="Unexpected stubtest output"):
        checker.parse_diagnostics(process, ["board"])


@pytest.fixture
def cli(checker, monkeypatch, tmp_path):
    """Replace every dependency query and worker run before invoking the CLI."""
    monkeypatch.setattr(checker, "CHECKED_MODULES", ("board", "busio"))
    source = tmp_path / "current" / "src"
    source.mkdir(parents=True)
    for name in checker.CHECKED_MODULES:
        (source / (name + ".py")).write_text(
            "raise AssertionError('must not import')\n"
        )
    monkeypatch.setattr(checker, "SOURCE", source)
    monkeypatch.setattr(
        checker.metadata, "version", lambda name: checker.REFERENCE[name]
    )
    monkeypatch.setattr(
        checker.metadata,
        "distribution",
        lambda _name: distribution(
            "board-stubs/__init__.pyi",
            "busio-stubs/__init__.pyi",
            "alarm-stubs/__init__.pyi",
        ),
    )
    monkeypatch.setattr(checker, "run_stubtest", lambda _source, _modules: [DIAGNOSTIC])
    monkeypatch.setattr(
        checker,
        "revision_pair",
        lambda _reference: ("a" * 40, "b" * 40, ["src/busio.py"]),
    )

    def extract(_revision, destination):
        extracted = destination / "src"
        extracted.mkdir(parents=True)
        for name in checker.CHECKED_MODULES:
            (extracted / (name + ".py")).write_text("raise AssertionError\n")
        return extracted

    monkeypatch.setattr(checker, "extract_source", extract)
    return checker


def test_standalone_reports_all_differences_and_missing_catalog_is_informational(
    cli, tmp_path
):
    report_path = tmp_path / "report.json"
    markdown_path = tmp_path / "report.md"
    assert cli.main(["--json", str(report_path), "--markdown", str(markdown_path)]) == 1
    report = json.loads(report_path.read_text())
    assert report["mode"] == "standalone"
    assert report["diagnostics"] == [DIAGNOSTIC]
    assert report["new"] == report["resolved"] == report["errors"] == []
    assert report["base_revision"] is None
    assert report["base_diagnostics"] == []
    assert DIAGNOSTIC in markdown_path.read_text()
    assert "All current stub discrepancies" in markdown_path.read_text()
    assert any(
        item["name"] == "alarm" and item["status"] == "missing"
        for item in report["modules"]
    )
    assert not list(tmp_path.rglob("*baseline*"))


def test_standalone_clean_run_passes_without_creating_a_baseline(cli, monkeypatch):
    monkeypatch.setattr(cli, "run_stubtest", lambda _source, _modules: [])
    assert cli.main([]) == 0


@pytest.mark.parametrize(
    "observation",
    [
        ([DIAGNOSTIC], [DIAGNOSTIC], 0),
        ([DIAGNOSTIC], [], 0),
        ([], [DIAGNOSTIC], 1),
        ([DIAGNOSTIC], [DIAGNOSTIC, "busio.Parity is not present at runtime"], 1),
    ],
)
def test_revision_gate_only_fails_on_new_head_diagnostics(
    cli, monkeypatch, tmp_path, observation
):
    previous, current, expected = observation
    calls = []

    def worker(source, modules):
        calls.append((source.parent.name, list(modules)))
        return previous if source.parent.name == "base" else current

    monkeypatch.setattr(cli, "run_stubtest", worker)
    # A newer stable stub release may add the same findings to both revisions.
    monkeypatch.setattr(
        cli.metadata,
        "version",
        lambda name: "10.4.0" if name == "circuitpython-stubs" else cli.REFERENCE[name],
    )
    report_path = tmp_path / "revisions.json"
    markdown_path = tmp_path / "revisions.md"
    assert (
        cli.main(
            [
                "--base",
                "origin/main",
                "--stable-release",
                "10.4.0",
                "--json",
                str(report_path),
                "--markdown",
                str(markdown_path),
            ]
        )
        == expected
    )
    report = json.loads(report_path.read_text())
    assert report["reference"]["circuitpython-stubs"] == "10.4.0"
    assert report["mode"] == "revision"
    assert report["base_revision"] == "a" * 40
    assert report["head_revision"] == "b" * 40
    assert report["base_diagnostics"] == previous
    assert report["diagnostics"] == current
    assert report["new"] == sorted(set(current) - set(previous))
    assert report["resolved"] == sorted(set(previous) - set(current))
    assert report["errors"] == []
    assert calls == [("base", ["board", "busio"]), ("head", ["board", "busio"])]
    assert "Base revision discrepancies" in markdown_path.read_text()
    assert "a" * 40 in markdown_path.read_text()
    assert not list(tmp_path.rglob("*baseline*"))


def test_matching_stable_tag_runs_normal_check(cli, monkeypatch):
    calls = []

    def worker(_source, _modules):
        calls.append("checked")
        return []

    monkeypatch.setattr(cli, "run_stubtest", worker)
    assert cli.main(["--stable-release", cli.REFERENCE["circuitpython-stubs"]]) == 0
    assert calls == ["checked"]


def test_mismatched_stable_tag_stops_before_inventory_or_worker(
    cli, monkeypatch, tmp_path
):
    def unexpected(*_args):
        pytest.fail("A mismatched stable reference must stop before runtime checks")

    monkeypatch.setattr(cli.metadata, "distribution", unexpected)
    monkeypatch.setattr(cli, "run_stubtest", unexpected)
    report_path = tmp_path / "outdated.json"
    assert cli.main(["--stable-release", "99.0.0", "--json", str(report_path)]) == 2
    report = json.loads(report_path.read_text())
    assert report["diagnostics"] == []
    assert len(report["errors"]) == 1
    assert "CircuitPython stable is 99.0.0" in report["errors"][0]
    assert "Install the matching stubs" in report["errors"][0]


@pytest.mark.parametrize("failure", ["import", "version", "missing_stubs"])
def test_standalone_never_accepts_a_checker_failure(
    cli, monkeypatch, failure, tmp_path
):
    if failure == "import":

        def fail(_source, _modules):
            raise cli.CheckError("busio failed to import")

        monkeypatch.setattr(cli, "run_stubtest", fail)
    elif failure == "version":
        monkeypatch.setattr(cli.metadata, "version", lambda _name: "unexpected")
    else:
        monkeypatch.setattr(cli.metadata, "distribution", lambda _name: distribution())
    report_path = tmp_path / "failure.json"
    assert cli.main(["--json", str(report_path)]) == 2
    assert json.loads(report_path.read_text())["errors"]


@pytest.mark.parametrize("side", ["base", "head"])
@pytest.mark.parametrize("message", ["busio failed to import", "stubtest timed out"])
def test_revision_checker_failures_on_either_side_are_fatal(
    cli, monkeypatch, tmp_path, side, message
):
    def worker(source, _modules):
        if source.parent.name == side:
            raise cli.CheckError(message)
        return [DIAGNOSTIC]

    monkeypatch.setattr(cli, "run_stubtest", worker)
    report_path = tmp_path / "failure.json"
    assert cli.main(["--base", "origin/main", "--json", str(report_path)]) == 2
    report = json.loads(report_path.read_text())
    assert report["errors"] == [message]
    assert report["new"] == []


@pytest.mark.parametrize("version", ["10.4.0rc1", "10.4.0.dev1", "unexpected"])
def test_nonstable_stub_versions_are_tool_errors(cli, monkeypatch, version):
    monkeypatch.setattr(
        cli.metadata,
        "version",
        lambda name: version if name == "circuitpython-stubs" else cli.REFERENCE[name],
    )
    assert cli.main([]) == 2


def test_baseline_update_flag_is_no_longer_supported(cli):
    with pytest.raises(SystemExit) as error:
        cli.main(["--update-baseline"])
    assert error.value.code == 2


@pytest.mark.parametrize("revision", [False, True])
def test_repeatable_module_selection_is_deduplicated_and_reported(
    cli, monkeypatch, tmp_path, revision
):
    calls = []

    def worker(_source, modules):
        calls.append(list(modules))
        return []

    monkeypatch.setattr(cli, "run_stubtest", worker)
    report_path = tmp_path / "selected.json"
    arguments = ["--module", "busio", "--module", "busio", "--json", str(report_path)]
    if revision:
        arguments.extend(["--base", "origin/main"])
    assert cli.main(arguments) == 0
    report = json.loads(report_path.read_text())
    assert report["checked_modules"] == ["busio"]
    assert report["selection_reason"] == "Explicit module selection."
    assert calls == [["busio"]] * (2 if revision else 1)
    inventory = {item["name"]: item["status"] for item in report["modules"]}
    assert inventory["board"] == "not_selected"
    assert inventory["busio"] == "checked"


@pytest.mark.parametrize("revision", [False, True])
def test_absent_stub_catalog_modules_are_reported_without_false_api_failures(
    cli, monkeypatch, tmp_path, revision
):
    monkeypatch.setattr(
        cli.metadata,
        "distribution",
        lambda _name: distribution("alarm-stubs/__init__.pyi"),
    )

    def worker(_source, modules):
        assert modules == []
        return []

    monkeypatch.setattr(cli, "run_stubtest", worker)
    report_path = tmp_path / "catalog.json"
    arguments = ["--json", str(report_path)]
    if revision:
        arguments.extend(["--base", "origin/main"])
    assert cli.main(arguments) == 0
    report = json.loads(report_path.read_text())
    assert report["checked_modules"] == []
    assert report["unreferenced_modules"] == ["board", "busio"]
    assert report["errors"] == report["diagnostics"] == report["new"] == []


def test_selected_module_deletion_is_a_new_head_regression(cli, monkeypatch, tmp_path):
    extract = cli.extract_source

    def extract_with_deletion(revision, destination):
        source = extract(revision, destination)
        if destination.name == "head":
            (source / "busio.py").unlink()
        return source

    calls = []

    def worker(source, modules):
        calls.append((source.parent.name, list(modules)))
        return []

    monkeypatch.setattr(cli, "extract_source", extract_with_deletion)
    monkeypatch.setattr(cli, "run_stubtest", worker)
    report_path = tmp_path / "deleted.json"
    assert cli.main(["--base", "origin/main", "--json", str(report_path)]) == 1
    report = json.loads(report_path.read_text())
    assert report["base_diagnostics"] == []
    assert report["diagnostics"] == report["new"] == ["busio is not present at runtime"]
    assert calls == [("base", ["board", "busio"]), ("head", ["board"])]


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


def test_cli_cannot_accept_a_caught_audit_failure(cli, monkeypatch, tmp_path):
    process = subprocess.CompletedProcess(
        [],
        1,
        stdout="busio encountered unexpected error, CheckError: "
        "Blocked hardware/kernel access: /dev/example\n",
        stderr="",
    )
    monkeypatch.setattr(
        cli, "run_stubtest", lambda _source, _modules: cli.parse_diagnostics(process)
    )
    report_path = tmp_path / "failure.json"
    assert cli.main(["--json", str(report_path)]) == 2
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
def test_legitimate_non_is_api_findings_are_preserved_in_standalone_reports(
    cli, monkeypatch, tmp_path, message
):
    process = subprocess.CompletedProcess([], 1, stdout=message + "\n", stderr="")
    assert cli.parse_diagnostics(process) == [message]
    monkeypatch.setattr(
        cli, "run_stubtest", lambda _source, _modules: cli.parse_diagnostics(process)
    )
    report_path = tmp_path / "report.json"
    assert cli.main(["--json", str(report_path)]) == 1
    assert json.loads(report_path.read_text())["diagnostics"] == [message]


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


@pytest.mark.parametrize("modules", [[], ["wifi"], ["busio", "usb_hid"]])
def test_worker_rejects_unaudited_or_empty_import_profiles(
    checker, monkeypatch, modules
):
    monkeypatch.setattr(
        checker.sys,
        "addaudithook",
        lambda _guard: pytest.fail(
            "Invalid profiles must stop before registering hooks"
        ),
    )
    with pytest.raises(checker.CheckError, match="audited import profile"):
        checker.stubtest_worker(modules=modules)


def test_worker_uses_selected_revision_source_and_verifies_its_reference(
    checker, monkeypatch, tmp_path
):
    """Emulate imports/tool invocation without installing a permanent audit hook."""
    source = tmp_path / "revision" / "src"
    registered, imported, verified = [], [], []
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(checker.sys, "path", list(checker.sys.path))
    monkeypatch.setattr(checker.sys, "argv", list(checker.sys.argv))
    monkeypatch.setattr(
        checker.sys, "dont_write_bytecode", checker.sys.dont_write_bytecode
    )
    monkeypatch.setattr(checker.sys, "addaudithook", registered.append)

    def import_fake(name):
        imported.append(name)
        if name == "adafruit_blinka.agnostic":
            return SimpleNamespace(chip_id=checker.TARGET, board_id="OS_AGNOSTIC_BOARD")
        return SimpleNamespace(__file__=str(source / (name + ".py")))

    fake_mypy = ModuleType("mypy")
    fake_mypy.stubtest = SimpleNamespace(main=lambda: 0)
    monkeypatch.setitem(checker.sys.modules, "mypy", fake_mypy)
    monkeypatch.setattr(checker.importlib, "import_module", import_fake)
    monkeypatch.setattr(
        checker,
        "verify_reference_stubs",
        lambda tool, modules: verified.append((tool, modules)),
    )
    assert checker.stubtest_worker(source, ["busio"]) == 0
    assert checker.sys.path[0] == str(source.resolve())
    assert imported == ["adafruit_blinka.agnostic", "busio"]
    assert checker.sys.argv[:2] == ["stubtest", "busio"]
    assert "--ignore-missing-stub" in checker.sys.argv
    assert verified == [(fake_mypy.stubtest, ("busio",))]
    assert len(registered) == 1
    assert (tmp_path / "mypy.ini").read_text() == "[mypy]\n"


@pytest.mark.parametrize("failure", ["target", "source"])
def test_worker_rejects_wrong_hardware_target_or_host_runtime_modules(
    checker, monkeypatch, tmp_path, failure
):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(checker.sys, "path", list(checker.sys.path))
    monkeypatch.setattr(
        checker.sys, "dont_write_bytecode", checker.sys.dont_write_bytecode
    )
    monkeypatch.setattr(checker.sys, "addaudithook", lambda _guard: None)

    def import_fake(name):
        if name == "adafruit_blinka.agnostic":
            return SimpleNamespace(
                chip_id="BCM2712" if failure == "target" else checker.TARGET,
                board_id="OS_AGNOSTIC_BOARD",
            )
        return SimpleNamespace(__file__=str(tmp_path / "host" / (name + ".py")))

    monkeypatch.setattr(checker.importlib, "import_module", import_fake)
    with pytest.raises(
        checker.CheckError, match="OS-agnostic target|Blinka source tree"
    ):
        checker.stubtest_worker(tmp_path / "revision" / "src", ["busio"])


@pytest.mark.parametrize(
    "paths,expected",
    [
        (["src/busio.py"], {"busio", "board"}),
        (["src/digitalio.py"], {"digitalio", "keypad", "neopixel_write"}),
        (["src/busio.py", "src/keypad.py"], {"busio", "board", "keypad"}),
        (["src/rainbowio.py"], {"rainbowio"}),
        (["docs/api_compatibility.rst", "tests/test_circuitpython_api.py"], set()),
        (["README.rst", ".github/workflows/tests.yml"], set()),
        ([], set()),
    ],
)
def test_affected_module_selection_includes_consumers(checker, paths, expected):
    selected, reason = checker.affected_modules(paths)
    assert selected == [name for name in checker.CHECKED_MODULES if name in expected]
    assert bool(expected) == reason.startswith("Affected APIs:")


@pytest.mark.parametrize(
    "path",
    [
        "src/adafruit_blinka/microcontroller/generic_agnostic_board/pin.py",
        "src/adafruit_blinka/agnostic/__init__.py",
        "src/microcontroller/__init__.py",
        "src/micropython/__init__.py",
        "src/unknown_backend.py",
        "src/busio/helper.py",
        "src/board_imports.json",
        "src/microcontroller_imports.json",
        "scripts/check_circuitpython_api.py",
        "requirements-api.txt",
        "requirements.txt",
        "setup.py",
        "pyproject.toml",
    ],
)
def test_shared_backend_unknown_source_and_tooling_changes_check_everything(
    checker, path
):
    selected, reason = checker.affected_modules(["docs/index.rst", path])
    assert selected == list(checker.CHECKED_MODULES)
    assert "full audited profile" in reason


def test_resolve_commit_treats_ref_as_data_and_validates_git_result(
    checker, monkeypatch
):
    calls = []

    def git(*arguments):
        calls.append(arguments)
        return ("a" * 40 + "\n").encode()

    monkeypatch.setattr(checker, "git_output", git)
    assert checker.resolve_commit("--output=/untrusted") == "a" * 40
    assert calls == [
        ("rev-parse", "--verify", "--end-of-options", "--output=/untrusted^{commit}")
    ]


@pytest.mark.parametrize("value", [b"", b"HEAD\n", b"--output=elsewhere\n", b"a" * 39])
def test_non_commit_git_output_is_never_used_for_diff_or_source_extraction(
    checker, monkeypatch, value
):
    calls = []

    def git(*arguments):
        calls.append(arguments)
        return value

    monkeypatch.setattr(checker, "git_output", git)
    with pytest.raises(checker.CheckError, match="commit ID"):
        checker.revision_pair("origin/main")
    assert len(calls) == 1
    assert calls[0][0] == "rev-parse"


@pytest.mark.parametrize("width", [40, 64])
def test_revision_pair_uses_merge_base_and_nul_delimited_no_renames_diff(
    checker, monkeypatch, width
):
    head, target, base = "b" * width, "c" * width, "a" * width
    calls = []
    paths = ["src/busio.py", "docs/new\nname.rst", "src/old_name.py"]

    def git(*arguments):
        calls.append(arguments)
        if arguments[0] == "rev-parse":
            return (
                (head if arguments[-1] == "HEAD^{commit}" else target) + "\n"
            ).encode()
        if arguments[0] == "merge-base":
            assert arguments == ("merge-base", target, head)
            return (base + "\n").encode()
        assert arguments == (
            "diff",
            "--no-ext-diff",
            "--no-textconv",
            "--no-renames",
            "--name-only",
            "-z",
            base,
            head,
            "--",
        )
        return "\0".join(paths).encode() + b"\0"

    monkeypatch.setattr(checker, "git_output", git)
    assert checker.revision_pair("origin/main") == (base, head, paths)
    assert [call[0] for call in calls] == [
        "rev-parse",
        "rev-parse",
        "merge-base",
        "diff",
    ]


@pytest.mark.parametrize("base", [b"", b"HEAD\n", b"a" * 39])
def test_invalid_merge_base_stops_before_diff_or_extraction(checker, monkeypatch, base):
    calls = []

    def git(*arguments):
        calls.append(arguments)
        return base if arguments[0] == "merge-base" else b"a" * 40

    monkeypatch.setattr(checker, "git_output", git)
    monkeypatch.setattr(
        checker,
        "extract_source",
        lambda *_args: pytest.fail("An invalid merge base must never be extracted"),
    )
    with pytest.raises(checker.CheckError, match="valid merge base"):
        checker.compare_revisions(empty_report(checker), "origin/main", ["busio"])
    assert [call[0] for call in calls] == ["rev-parse", "rev-parse", "merge-base"]


@pytest.mark.parametrize("failure", ["exit", "timeout"])
def test_git_failures_are_tool_errors(checker, monkeypatch, failure):
    def run(command, **kwargs):
        assert command == ["git", "rev-parse", "HEAD"]
        assert kwargs["cwd"] == checker.ROOT
        assert kwargs["capture_output"] and not kwargs["check"]
        assert kwargs["timeout"] == 60
        if failure == "timeout":
            raise subprocess.TimeoutExpired(command, 60)
        return SimpleNamespace(returncode=128, stdout=b"", stderr=b"bad revision")

    monkeypatch.setattr(checker.subprocess, "run", run)
    with pytest.raises(checker.CheckError):
        checker.git_output("rev-parse", "HEAD")


def test_git_cannot_be_redirected_by_inherited_repository_environment(
    checker, monkeypatch
):
    monkeypatch.setenv("GIT_DIR", "/not/the/selected/repository")
    monkeypatch.setenv("GIT_WORK_TREE", "/not/the/selected/source")
    monkeypatch.setenv("GIT_NO_REPLACE_OBJECTS", "0")
    monkeypatch.setenv("GIT_CONFIG_COUNT", "1")
    monkeypatch.setenv("GIT_CONFIG_KEY_0", "core.worktree")
    monkeypatch.setenv("GIT_CONFIG_VALUE_0", "/not/the/selected/worktree")
    monkeypatch.setenv("CHECKER_TEST_PRESERVE", "kept")

    def run(command, **kwargs):
        assert command == ["git", "cat-file", "--batch"]
        assert kwargs["cwd"] == checker.ROOT
        assert kwargs["input"] == b"a" * 40 + b"\n"
        assert {
            key: value for key, value in kwargs["env"].items() if key.startswith("GIT_")
        } == {"GIT_NO_REPLACE_OBJECTS": "1"}
        assert kwargs["env"]["CHECKER_TEST_PRESERVE"] == "kept"
        return SimpleNamespace(returncode=0, stdout=b"checked\n", stderr=b"")

    monkeypatch.setattr(checker.subprocess, "run", run)
    assert (
        checker.git_output("cat-file", "--batch", input_data=b"a" * 40 + b"\n")
        == b"checked\n"
    )


@pytest.mark.parametrize("export_attributes", [False, True])
def test_real_revision_gate_with_private_git_and_guarded_mypy(
    checker, monkeypatch, tmp_path, export_attributes
):
    """Exercise the actual worker; all source edits and commits stay in a fixture."""
    pytest.importorskip("mypy.stubtest")
    try:
        checker.metadata.distribution("circuitpython-stubs")
        mypy_version = checker.metadata.version("mypy")
    except checker.metadata.PackageNotFoundError:
        pytest.skip(
            "The optional API-checking development requirements are not installed"
        )
    if mypy_version != checker.REFERENCE["mypy"]:
        pytest.skip("This integration test requires the pinned mypy development tool")

    fixture = tmp_path / "repository"
    fixture.mkdir()
    checker.extract_source(checker.resolve_commit("HEAD"), fixture)
    rainbow = fixture / "src/rainbowio.py"
    if export_attributes:
        (fixture / ".gitattributes").write_text(
            "src/rainbowio.py export-ignore export-subst\n"
            "src/export_marker.txt export-subst\n"
        )
        rainbow.write_bytes(rainbow.read_bytes() + b"\n# source revision $Format:%H$\n")
        (fixture / "src/export_marker.txt").write_bytes(b"literal $Format:%H$\r\n")
    environment = {
        key: value for key, value in os.environ.items() if not key.startswith("GIT_")
    }

    def git(*arguments):
        result = subprocess.run(
            [
                "git",
                "-c",
                "core.hooksPath=/dev/null",
                "-c",
                "core.attributesFile=/dev/null",
                "-c",
                "core.autocrlf=false",
                "-c",
                "commit.gpgsign=false",
                "-c",
                "user.name=API checker fixture",
                "-c",
                "user.email=api-checker@example.invalid",
                *arguments,
            ],
            cwd=fixture,
            env=environment,
            capture_output=True,
            text=True,
            check=True,
            timeout=30,
        )
        return result.stdout.strip()

    git("init", "-q")
    git("add", "src")
    if export_attributes:
        git("add", ".gitattributes")
    git("commit", "-qm", "Fixture base")
    base = git("rev-parse", "HEAD")
    base_content = rainbow.read_bytes()
    assert base_content.count(b"def colorwheel(color_value):") == 1
    rainbow.write_bytes(
        base_content.replace(
            b"def colorwheel(color_value):", b"def colorwheel(color_value, extra):"
        )
    )
    git("add", "src/rainbowio.py")
    git("commit", "-qm", "Fixture required argument regression")
    head = git("rev-parse", "HEAD")

    monkeypatch.setattr(checker, "ROOT", fixture)
    if export_attributes:
        assert (
            checker.extract_source(base, tmp_path / "exact-base") / "rainbowio.py"
        ).read_bytes() == base_content
        assert (
            checker.extract_source(head, tmp_path / "exact-head") / "rainbowio.py"
        ).read_bytes() == rainbow.read_bytes()
        assert (
            tmp_path / "exact-head/src/export_marker.txt"
        ).read_bytes() == b"literal $Format:%H$\r\n"
    report_path = tmp_path / "real-revisions.json"
    assert checker.main(["--base", base, "--json", str(report_path)]) == 1
    report = json.loads(report_path.read_text())
    assert report["errors"] == []
    assert report["checked_modules"] == ["rainbowio"]
    assert report["base_revision"] == base
    assert report["head_revision"] == head
    assert report["base_diagnostics"]
    assert set(report["base_diagnostics"]).issubset(report["diagnostics"])
    assert report["new"] == [
        'rainbowio.colorwheel is inconsistent, stub does not have parameter "extra"'
    ]
    assert report["resolved"] == []

    # A later docs-only commit has no audited API changes, even though HEAD's
    # source still has the deliberately introduced discrepancy.
    (fixture / "fixture-docs.rst").write_text("Private fixture documentation.\n")
    git("add", "fixture-docs.rst")
    git("commit", "-qm", "Fixture documentation only")
    assert checker.main(["--base", head, "--json", str(report_path)]) == 0
    docs_report = json.loads(report_path.read_text())
    assert docs_report["errors"] == []
    assert docs_report["checked_modules"] == []
    assert docs_report["base_diagnostics"] == docs_report["diagnostics"] == []


def tree_entry(name, mode=b"100644", kind=b"blob", object_id=b"a" * 40):
    """Encode one NUL-delimited ls-tree entry, including unsafe synthetic paths."""
    return b" ".join((mode, kind, object_id)) + b"\t" + os.fsencode(name) + b"\0"


def blob_response(content, object_id=b"a" * 40):
    """Encode cat-file's exact byte-counted batch response, not a text payload."""
    return object_id + b" blob " + str(len(content)).encode() + b"\n" + content + b"\n"


@pytest.mark.parametrize("width", [40, 64])
def test_tree_extraction_preserves_exact_source_and_executable_blob_bytes(
    checker, monkeypatch, tmp_path, width
):
    revision, first_id, second_id = "c" * width, b"a" * width, b"b" * width
    first = b"raise AssertionError('must not import')\n"
    # Binary bytes, embedded framing-looking text, and export substitutions must
    # remain untouched, including for executable-mode source-tree entries.
    second = b"\x00\xff\r\nliteral $Format:%H$\n" + first_id + b" blob 0\n\n"
    listing = tree_entry("src/busio.py", object_id=first_id) + tree_entry(
        "src/microcontroller/__init__.py", b"100755", object_id=second_id
    )
    calls = []

    def git(*arguments, input_data=None):
        calls.append((arguments, input_data))
        if arguments[0] == "ls-tree":
            return listing
        return blob_response(first, first_id) + blob_response(second, second_id)

    monkeypatch.setattr(checker, "git_output", git)
    destination = tmp_path / "snapshot"
    source = checker.extract_source(revision, destination)
    assert source == destination / "src"
    assert (source / "busio.py").read_bytes() == first
    assert (source / "microcontroller/__init__.py").read_bytes() == second
    assert calls == [
        (("ls-tree", "-r", "-z", "--full-tree", revision, "--", "src"), None),
        (("cat-file", "--batch"), first_id + b"\n" + second_id + b"\n"),
    ]


def test_empty_source_tree_produces_an_empty_source_root_without_batch_call(
    checker, monkeypatch, tmp_path
):
    calls = []

    def git(*arguments, input_data=None):
        calls.append((arguments, input_data))
        assert arguments[0] == "ls-tree"
        return b""

    monkeypatch.setattr(checker, "git_output", git)
    source = checker.extract_source("a" * 40, tmp_path / "snapshot")
    assert source.is_dir()
    assert not list(source.iterdir())
    assert len(calls) == 1


@pytest.mark.parametrize(
    "entry",
    [
        tree_entry("/absolute.py"),
        tree_entry("../outside.py"),
        tree_entry("src/../outside.py"),
        tree_entry("other/file.py"),
        tree_entry("src/link.py", b"120000"),
        tree_entry("src/submodule", b"160000", b"commit"),
        tree_entry("src/tree", b"040000", b"tree"),
        tree_entry("src/pipe", b"010000"),
        tree_entry("src/device", b"020000"),
        tree_entry("src/file.py", b"100644", b"tree"),
    ],
)
def test_unsafe_tree_entries_are_rejected_before_any_write(
    checker, monkeypatch, tmp_path, entry
):
    # Even a valid first entry must not be written before validating all paths.
    def git(*arguments, input_data=None):
        assert arguments[0] == "ls-tree"
        assert input_data is None
        return tree_entry("src/safe.py") + entry

    monkeypatch.setattr(checker, "git_output", git)
    destination = tmp_path / "snapshot"
    before = set(tmp_path.rglob("*"))
    with pytest.raises(checker.CheckError, match="Unsafe Git source|link or special"):
        checker.extract_source("a" * 40, destination)
    assert not destination.exists()
    assert set(tmp_path.rglob("*")) == before


@pytest.mark.parametrize(
    "entry",
    [
        b"missing tab separator\0",
        b"100644 blob\tsrc/file.py\0",
        b"100644 blob " + b"a" * 40 + b" extra\tsrc/file.py\0",
        tree_entry("src/file.py", object_id=b"a" * 39),
        tree_entry("src/file.py", object_id=b"not-an-object-id"),
    ],
)
def test_malformed_source_tree_records_fail_before_any_write(
    checker, monkeypatch, tmp_path, entry
):
    def git(*arguments, input_data=None):
        assert arguments[0] == "ls-tree"
        assert input_data is None
        return tree_entry("src/safe.py") + entry

    monkeypatch.setattr(checker, "git_output", git)
    destination = tmp_path / "snapshot"
    with pytest.raises(checker.CheckError, match="Invalid Git source"):
        checker.extract_source("a" * 40, destination)
    assert not destination.exists()


@pytest.mark.parametrize(
    "response",
    [
        b"",
        b"a" * 40 + b" missing\n",
        b"a" * 40 + b" blob\n",
        b"b" * 40 + b" blob 0\n\n",
        b"a" * 40 + b" tree 0\n\n",
        b"a" * 40 + b" blob -1\n\n",
        b"a" * 40 + b" blob 18446744073709551616\n\n",
        b"a" * 40 + b" blob size\n\n",
        b"a" * 40 + b" blob 0 extra\n\n",
        b"a" * 40 + b" blob 5\nabc\n",
        b"a" * 40 + b" blob 3\nabc",
        b"a" * 40 + b" blob 3\nabcX",
        blob_response(b"valid") + b"unexpected trailing response\n",
    ],
)
def test_invalid_or_truncated_batch_responses_fail_before_any_write(
    checker, monkeypatch, tmp_path, response
):
    def git(*arguments, input_data=None):
        if arguments[0] == "ls-tree":
            return tree_entry("src/file.py")
        assert input_data == b"a" * 40 + b"\n"
        return response

    monkeypatch.setattr(checker, "git_output", git)
    destination = tmp_path / "snapshot"
    with pytest.raises(checker.CheckError, match="Git source-blob response"):
        checker.extract_source("c" * 40, destination)
    assert not destination.exists()


def test_late_batch_error_does_not_write_an_earlier_valid_blob(
    checker, monkeypatch, tmp_path
):
    def git(*arguments, input_data=None):
        if arguments[0] == "ls-tree":
            return tree_entry("src/first.py") + tree_entry(
                "src/second.py", object_id=b"b" * 40
            )
        assert input_data == b"a" * 40 + b"\n" + b"b" * 40 + b"\n"
        return blob_response(b"valid first blob") + b"b" * 40 + b" missing\n"

    monkeypatch.setattr(checker, "git_output", git)
    destination = tmp_path / "snapshot"
    with pytest.raises(checker.CheckError, match="Invalid Git source-blob response"):
        checker.extract_source("c" * 40, destination)
    assert not destination.exists()


@pytest.mark.parametrize("link_is_file", [False, True])
def test_existing_destination_symlink_escape_is_rejected_before_any_write(
    checker, monkeypatch, tmp_path, link_is_file
):
    outside = tmp_path / "outside"
    outside.mkdir()
    destination = tmp_path / "snapshot"
    (destination / "src").mkdir(parents=True)
    if link_is_file:
        outside_file = outside / "escape.py"
        outside_file.write_bytes(b"original outside bytes")
        (destination / "src/escape.py").symlink_to(outside_file)
        escape_path = "src/escape.py"
    else:
        (destination / "src/escape").symlink_to(outside, target_is_directory=True)
        escape_path = "src/escape/file.py"

    def git(*arguments, input_data=None):
        if arguments[0] == "ls-tree":
            return tree_entry("src/safe.py") + tree_entry(escape_path)
        assert input_data == (b"a" * 40 + b"\n") * 2
        return blob_response(b"must not write") * 2

    monkeypatch.setattr(checker, "git_output", git)
    before = {path: path.read_bytes() for path in outside.rglob("*") if path.is_file()}
    with pytest.raises(checker.CheckError, match="escapes the snapshot directory"):
        checker.extract_source("c" * 40, destination)
    assert not (destination / "src/safe.py").exists()
    assert {
        path: path.read_bytes() for path in outside.rglob("*") if path.is_file()
    } == before


@pytest.mark.parametrize("case", ["missing", "other_distribution", "directory"])
def test_selected_roots_require_actual_installed_reference_stubs(
    checker, monkeypatch, tmp_path, case
):
    installed = tmp_path / "installed"
    installed.mkdir()
    reference = installed / "busio-stubs/__init__.pyi"
    metadata_files = [PurePosixPath("busio-stubs/__init__.pyi")]
    monkeypatch.setattr(
        checker.metadata,
        "distribution",
        lambda name: SimpleNamespace(
            files=metadata_files, locate_file=lambda entry: installed / entry
        ),
    )
    stub = None
    if case != "missing":
        path = reference if case == "directory" else tmp_path / "other/busio.pyi"
        stub = SimpleNamespace(path=str(path))
        if case == "directory":
            metadata_files[:] = [PurePosixPath("busio-stubs/py.typed")]
    with pytest.raises(checker.CheckError, match="No CircuitPython reference stub"):
        checker.verify_reference_stubs(
            SimpleNamespace(get_stub=lambda _name: stub), ["busio"]
        )


def test_reference_stub_verification_checks_every_selected_root(
    checker, monkeypatch, tmp_path
):
    files = [PurePosixPath(name + "-stubs/__init__.pyi") for name in ("board", "busio")]
    calls = []
    monkeypatch.setattr(
        checker.metadata,
        "distribution",
        lambda _name: SimpleNamespace(
            files=files, locate_file=lambda entry: tmp_path / entry
        ),
    )

    def get_stub(name):
        calls.append(name)
        return SimpleNamespace(path=str(tmp_path / (name + "-stubs/__init__.pyi")))

    checker.verify_reference_stubs(
        SimpleNamespace(get_stub=get_stub), ["board", "busio"]
    )
    assert calls == ["board", "busio"]
