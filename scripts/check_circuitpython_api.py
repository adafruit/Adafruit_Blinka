# SPDX-FileCopyrightText: 2026 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""Inventory CircuitPython APIs and compare safe Blinka imports with their stubs.

Inspired by elpekenin's stubtest prototype in Adafruit_Blinka#884. This is
development tooling only: it must never configure hardware or install packages.
"""

import argparse
from collections import Counter
import importlib
from importlib import metadata
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "src"
BASELINE = Path(__file__).with_name("circuitpython_api_baseline.json")
REFERENCE = {"circuitpython-stubs": "10.3.1", "mypy": "2.4.0"}
TARGET = "OS_AGNOSTIC"

# Audited imports only. Being importable does not mean a driver is implemented
# or that its behavior is correct. Never construct drivers for this comparison.
CHECKED_MODULES = (
    "analogio",
    "bitbangio",
    "board",
    "busio",
    "digitalio",
    "keypad",
    "microcontroller",
    "micropython",
    "neopixel_write",
    "onewireio",
    "pwmio",
    "rainbowio",
)
SEPARATE_PACKAGES = {
    "adafruit_bus_device": "Adafruit-CircuitPython-BusDevice",
    "adafruit_pixelbuf": "Adafruit-CircuitPython-Pixelbuf",
    "displayio": "Adafruit-Blinka-Displayio",
    "bitmaptools": "Adafruit-Blinka-Displayio",
    "busdisplay": "Adafruit-Blinka-Displayio",
    "epaperdisplay": "Adafruit-Blinka-Displayio",
    "fontio": "Adafruit-Blinka-Displayio",
    "fourwire": "Adafruit-Blinka-Displayio",
    "i2cdisplaybus": "Adafruit-Blinka-Displayio",
    "paralleldisplaybus": "Adafruit-Blinka-Displayio",
    "terminalio": "Adafruit-Blinka-Displayio",
    "vectorio": "Adafruit-Blinka-Displayio",
}
NOT_CHECKED = {
    "pulseio": "No OS-agnostic backend; hardware/platform-specific.",
    "rotaryio": "No OS-agnostic backend; hardware/platform-specific.",
    "usb_hid": "Import/exit hooks access kernel USB gadget configuration.",
}


class CheckError(Exception):
    """A checker/import failure, never an acceptable compatibility baseline."""


def stub_modules(distribution):
    """Find modules/packages in the stub distribution, not in the host runtime."""
    modules = set()
    for entry in distribution.files or ():
        path = PurePosixPath(str(entry))
        if not path.parts[0].endswith("-stubs") or path.suffix != ".pyi":
            continue
        parts = [path.parts[0][: -len("-stubs")], *path.parts[1:]]
        if parts[-1] == "__init__.pyi":
            parts.pop()
        else:
            parts[-1] = PurePosixPath(parts[-1]).stem
        if all(part.isidentifier() for part in parts):
            modules.add(".".join(parts))
    if not modules:
        raise CheckError("The circuitpython-stubs distribution has no module files.")
    return sorted(modules)


def source_modules(source):
    """Find source modules, including packages, without executing their code."""
    modules = set()
    for path in source.rglob("*.py"):
        parts = list(path.relative_to(source).with_suffix("").parts)
        if parts[-1] == "__init__":
            parts.pop()
        if parts and all(part.isidentifier() for part in parts):
            modules.add(".".join(parts))
    return modules


def inventory(modules, implemented):
    """Classify availability separately from the signature-checking result."""
    result = []
    for name in modules:
        root = name.split(".")[0]
        if name in implemented:
            if root in CHECKED_MODULES:
                status, reason = "checked", "API surface only, OS-agnostic target."
            else:
                status = "not_checked"
                reason = NOT_CHECKED.get(
                    root, "Source present; no audited import profile."
                )
        elif root in SEPARATE_PACKAGES:
            status, reason = "separate_package", SEPARATE_PACKAGES[root]
        elif root in sys.stdlib_module_names:
            status, reason = (
                "host_provided",
                "CPython module; API equivalence not checked.",
            )
        else:
            status, reason = "missing", "No implementation in this repository."
        if root == "onewireio":
            reason += " OneWire is an unimplemented placeholder."
        result.append({"name": name, "status": status, "reason": reason})
    return result


def worker_environment(scratch):
    """Do not inherit a connected-device selection or user Python/mypy paths."""
    environment = {
        key: value
        for key, value in os.environ.items()
        if not key.startswith(("BLINKA_", "PYTHON", "MYPY"))
    }
    environment.update(
        BLINKA_FORCECHIP=TARGET,
        BLINKA_FORCEBOARD="OS_AGNOSTIC_BOARD",
        BLINKA_SKIP_DEPENDENCY_CHECK="1",
        MYPY_CACHE_DIR=str(Path(scratch) / "mypy-cache"),
        TMPDIR=str(scratch),
    )
    return environment


def audit_guard(scratch):
    """Defense in depth for the fixed import profile, not a malicious-code sandbox."""
    scratch = Path(scratch).resolve()
    failures = []
    blocked_imports = {
        "hid",
        "gpiod",
        "lgpio",
        "RPi",
        "usb",
        "pyftdi",
        "serial",
        "usb_hid",
    }

    def reject(message):
        # Introspection tools sometimes catch exceptions themselves. Retain the
        # attempt so a swallowed guard failure cannot produce a passing report.
        failures.append(message)
        raise CheckError(message)

    def check_path(value, write=False):
        if not isinstance(value, (str, bytes, os.PathLike)):
            return
        path = Path(os.fsdecode(value)).resolve()
        if path == Path(os.devnull):
            return
        if any(
            path == base or base in path.parents
            for base in (Path("/dev"), Path("/proc"), Path("/sys"))
        ):
            reject(f"Blocked hardware/kernel access: {path}")
        if write and path != scratch and scratch not in path.parents:
            reject(f"Blocked write outside checker scratch directory: {path}")

    def guard(event, args):
        if event == "import":
            name = args[0]
            if name.split(".")[0] in blocked_imports:
                reject(f"Blocked hardware import: {name}")
            prefix = "adafruit_blinka.microcontroller."
            if name.startswith(prefix) and not name.startswith(
                prefix + "generic_agnostic_board"
            ):
                reject(f"Blocked non-agnostic backend: {name}")
        elif event == "open":
            mode, flags = args[1:3]
            write = bool(flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC))
            write = write or (isinstance(mode, str) and any(c in mode for c in "wax+"))
            check_path(args[0], write)
        elif event in ("os.listdir", "os.scandir"):
            check_path(args[0])
        elif event in ("os.remove", "os.rmdir", "os.mkdir", "os.chmod"):
            check_path(args[0], True)
        elif event in ("os.rename", "os.link", "os.symlink"):
            check_path(args[0], True)
            check_path(args[1], True)
        elif event.startswith(
            ("subprocess.", "socket.", "os.exec", "os.spawn")
        ) or event in ("os.system", "os.fork", "ctypes.dlopen"):
            reject(f"Blocked external/native operation: {event}")

    guard.failures = failures
    return guard


def stubtest_worker():
    """Run the pinned checker in a fresh process, with no real hardware backends."""
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(SOURCE))
    guard = audit_guard(Path.cwd())
    sys.addaudithook(guard)
    agnostic = importlib.import_module("adafruit_blinka.agnostic")
    if (agnostic.chip_id, agnostic.board_id) != (TARGET, "OS_AGNOSTIC_BOARD"):
        raise CheckError("The checker did not select the OS-agnostic target.")
    for name in CHECKED_MODULES:
        module = importlib.import_module(name)
        if SOURCE not in Path(module.__file__).resolve().parents:
            raise CheckError(f"{name} did not load from the Blinka source tree.")
    # Keep the prototype's runtime/stub comparison, but not its unbounded import
    # scan. The CLI and concise output are pinned along with the tool version.
    from mypy import stubtest  # pylint: disable=import-outside-toplevel

    config = Path.cwd() / "mypy.ini"
    config.write_text("[mypy]\n", encoding="utf-8")
    sys.argv = [
        "stubtest",
        *CHECKED_MODULES,
        "--concise",
        "--ignore-missing-stub",
        "--mypy-config-file",
        str(config),
    ]
    result = stubtest.main()
    if guard.failures:
        raise CheckError(
            "A verification step caught an audit failure: " + guard.failures[0]
        )
    return result


def parse_diagnostics(process):
    """Accept only concise API findings; failures cannot be hidden in a baseline."""
    if process.stderr.strip() or process.returncode not in (0, 1):
        raise CheckError(
            process.stderr.strip() or f"stubtest exited {process.returncode}"
        )
    diagnostics = []
    for line in process.stdout.splitlines():
        if not line.strip():
            continue
        match = re.fullmatch(r"([A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*) (.+)", line)
        if (
            not match
            or match[1].split(".")[0] not in CHECKED_MODULES
            # These pinned-tool formats mean comparison did not finish,
            # including when stubtest catches one of our audit exceptions.
            # Actual API findings use several verbs; do not filter those out.
            or match[2].startswith(
                (
                    "failed to ",
                    "encountered unexpected error",
                    "is an unknown mypy node",
                )
            )
        ):
            raise CheckError("Unexpected stubtest output:\n" + process.stdout.strip())
        diagnostics.append(line)
    if bool(diagnostics) != bool(process.returncode):
        raise CheckError("stubtest exit status does not match its diagnostics.")
    return sorted(set(diagnostics))


def run_stubtest():
    """Use an isolated child and temporary cwd, not the caller's hardware target."""
    with tempfile.TemporaryDirectory(prefix="blinka-api-") as scratch:
        try:
            process = subprocess.run(
                [sys.executable, "-I", str(Path(__file__).resolve()), "--_worker"],
                cwd=scratch,
                env=worker_environment(scratch),
                capture_output=True,
                text=True,
                check=False,
                timeout=120,
            )
        except subprocess.TimeoutExpired as error:
            raise CheckError("stubtest timed out; no baseline was changed.") from error
    return parse_diagnostics(process)


def snapshot(report):
    """Keep exact diagnostics and inventory states, never wildcard suppressions."""
    return {
        "reference": REFERENCE,
        "target": TARGET,
        "modules": {item["name"]: item["status"] for item in report["modules"]},
        "diagnostics": report["diagnostics"],
    }


def compare_baseline(current, previous):
    """Return new and resolved observations, including coverage changes."""
    if not isinstance(previous, dict):
        raise CheckError("Invalid baseline schema.")
    if previous.get("reference") != REFERENCE or previous.get("target") != TARGET:
        raise CheckError(
            "Baseline reference/target differs; review and update it explicitly."
        )
    if not isinstance(previous.get("modules"), dict) or not isinstance(
        previous.get("diagnostics"), list
    ):
        raise CheckError("Invalid baseline schema.")
    if not all(isinstance(line, str) for line in previous["diagnostics"]) or not all(
        isinstance(name, str) and isinstance(status, str)
        for name, status in previous["modules"].items()
    ):
        raise CheckError("Invalid baseline schema.")
    observed = set(current["diagnostics"])
    accepted = set(previous["diagnostics"])
    for name, status in current["modules"].items():
        observed.add(f"inventory: {name}: {status}")
    for name, status in previous["modules"].items():
        accepted.add(f"inventory: {name}: {status}")
    return sorted(observed - accepted), sorted(accepted - observed)


def markdown_report(report):
    """Produce a readable artifact without calling unchecked modules compatible."""
    lines = [
        "# CircuitPython API comparison",
        "",
        f"Reference: circuitpython-stubs {REFERENCE['circuitpython-stubs']}; "
        f"mypy {REFERENCE['mypy']}. Target: {TARGET}.",
        "",
        "API surface only; this is not behavior or hardware validation.",
        "",
        "## Module inventory",
        "",
        "| Module | Status | Notes |",
        "| --- | --- | --- |",
    ]
    for item in report["modules"]:
        lines.append(f"| {item['name']} | {item['status']} | {item['reason']} |")
    for title, values in (
        ("Checker errors", report["errors"]),
        ("New observations", report["new"]),
        ("Resolved observations", report["resolved"]),
        ("All current stub discrepancies", report["diagnostics"]),
    ):
        lines.extend(["", "## " + title, ""])
        lines.extend("- " + value for value in values)
        if not values:
            lines.append("None.")
    return "\n".join(lines) + "\n"


def main(argv=None):
    """Run reporting and the baseline gate; never install development dependencies."""
    # Reporting and error paths deliberately share the same result object.
    # pylint: disable=too-many-locals
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", type=Path, help="write the full JSON report")
    parser.add_argument("--markdown", type=Path, help="write the full Markdown report")
    parser.add_argument("--update-baseline", action="store_true")
    parser.add_argument(
        "--stable-release",
        help="official stable tag resolved by CI; reject an outdated stub reference",
    )
    args = parser.parse_args(argv)
    report = {
        "reference": REFERENCE,
        "target": TARGET,
        "modules": [],
        "diagnostics": [],
        "new": [],
        "resolved": [],
        "errors": [],
    }
    try:
        if (
            args.stable_release is not None
            and args.stable_release != REFERENCE["circuitpython-stubs"]
        ):
            raise CheckError(
                f"CircuitPython stable is {args.stable_release}, but the reference is "
                f"{REFERENCE['circuitpython-stubs']}. Update the matching stubs and "
                "review the baseline before continuing."
            )
        for name, expected in REFERENCE.items():
            actual = metadata.version(name)
            if actual != expected:
                raise CheckError(f"Expected {name}=={expected}, found {actual}.")
        names = stub_modules(metadata.distribution("circuitpython-stubs"))
        implemented = source_modules(SOURCE)
        missing = set(CHECKED_MODULES) - set(names).intersection(implemented)
        if missing:
            raise CheckError(
                "Checked modules lack source/stubs: " + ", ".join(sorted(missing))
            )
        report["modules"] = inventory(names, implemented)
        report["diagnostics"] = run_stubtest()
        current = snapshot(report)
        if args.update_baseline:
            BASELINE.write_text(
                json.dumps(current, indent=2, sort_keys=True) + "\n", encoding="utf-8"
            )
            print("Updated baseline; review its diff before committing.")
        else:
            previous = json.loads(BASELINE.read_text(encoding="utf-8"))
            report["new"], report["resolved"] = compare_baseline(current, previous)
    except (CheckError, OSError, ValueError, metadata.PackageNotFoundError) as error:
        report["errors"].append(str(error))
    for flag in ("json", "markdown"):
        path = getattr(args, flag)
        if path:
            content = (
                json.dumps(report, indent=2, sort_keys=True) + "\n"
                if flag == "json"
                else markdown_report(report)
            )
            path.write_text(content, encoding="utf-8")
    counts = Counter(item["status"] for item in report["modules"])
    print(
        "Module inventory:", ", ".join(f"{key}={counts[key]}" for key in sorted(counts))
    )
    print(
        f"Current discrepancies: {len(report['diagnostics'])}; "
        f"new observations: {len(report['new'])}; resolved: {len(report['resolved'])}."
    )
    for field in ("errors", "new", "resolved"):
        for message in report[field]:
            print(field.upper() + ": " + message)
    if report["errors"]:
        return 2
    return int(bool(report["new"] or report["resolved"]))


if __name__ == "__main__":
    if sys.argv[1:] == ["--_worker"]:
        raise SystemExit(stubtest_worker())
    raise SystemExit(main())
