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
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "src"
# Known-good local installation defaults. CI may install the matching stubs for
# a newer stable release; both revisions always use that same installed version.
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
    """An incomplete comparison, not an ordinary API discrepancy."""


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


def inventory(modules, implemented, selected=None):
    """Classify availability separately from the signature-checking result."""
    selected = set(CHECKED_MODULES if selected is None else selected)
    result = []
    for name in modules:
        root = name.split(".")[0]
        if name in implemented:
            if root in selected:
                status, reason = "checked", "API surface only, OS-agnostic target."
            elif root in CHECKED_MODULES:
                status, reason = "not_selected", "Not selected for this comparison."
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


def stubtest_worker(source=None, modules=None):
    """Run the pinned checker in a fresh process, with no real hardware backends."""
    source = SOURCE if source is None else Path(source).resolve()
    modules = CHECKED_MODULES if modules is None else tuple(modules)
    if not modules or not set(modules).issubset(CHECKED_MODULES):
        raise CheckError("Worker modules must use an audited import profile.")
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(source))
    guard = audit_guard(Path.cwd())
    sys.addaudithook(guard)
    agnostic = importlib.import_module("adafruit_blinka.agnostic")
    if (agnostic.chip_id, agnostic.board_id) != (TARGET, "OS_AGNOSTIC_BOARD"):
        raise CheckError("The checker did not select the OS-agnostic target.")
    for name in modules:
        module = importlib.import_module(name)
        if source not in Path(module.__file__).resolve().parents:
            raise CheckError(f"{name} did not load from the Blinka source tree.")
    # Keep the prototype's runtime/stub comparison, but not its unbounded import
    # scan. The CLI and concise output are pinned along with the tool version.
    from mypy import stubtest  # pylint: disable=import-outside-toplevel

    config = Path.cwd() / "mypy.ini"
    config.write_text("[mypy]\n", encoding="utf-8")
    sys.argv = [
        "stubtest",
        *modules,
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
    # --ignore-missing-stub is needed for Blinka extensions, but must not hide
    # a missing reference for one of the explicitly selected public modules.
    verify_reference_stubs(stubtest, modules)
    return result


def verify_reference_stubs(stubtest, modules):
    """Confirm selected roots were compared to the installed CP stub files."""
    distribution = metadata.distribution("circuitpython-stubs")
    files = {
        Path(distribution.locate_file(entry)).resolve()
        for entry in distribution.files or ()
        if str(entry).endswith(".pyi")
    }
    for name in modules:
        stub = stubtest.get_stub(name)
        if stub is None or Path(stub.path).resolve() not in files:
            raise CheckError(f"No CircuitPython reference stub was checked for {name}.")


def parse_diagnostics(process, modules=None):
    """Accept only concise API findings; incomplete comparisons must fail."""
    modules = CHECKED_MODULES if modules is None else modules
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
            or match[1].split(".")[0] not in modules
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


def run_stubtest(source=None, modules=None):
    """Use an isolated child and temporary cwd, not the caller's hardware target."""
    source = SOURCE if source is None else Path(source).resolve()
    modules = CHECKED_MODULES if modules is None else tuple(modules)
    if not modules:
        return []
    with tempfile.TemporaryDirectory(prefix="blinka-api-") as scratch:
        try:
            process = subprocess.run(
                [
                    sys.executable,
                    "-I",
                    str(Path(__file__).resolve()),
                    "--_worker",
                    str(source),
                    *modules,
                ],
                cwd=scratch,
                env=worker_environment(scratch),
                capture_output=True,
                text=True,
                check=False,
                timeout=120,
            )
        except subprocess.TimeoutExpired as error:
            raise CheckError("stubtest timed out; comparison is incomplete.") from error
    return parse_diagnostics(process, modules)


def git_output(*arguments, input_data=None):
    """Run bounded read-only Git operations; callers pass resolved commits."""
    environment = {
        key: value for key, value in os.environ.items() if not key.startswith("GIT_")
    }
    environment["GIT_NO_REPLACE_OBJECTS"] = "1"
    try:
        result = subprocess.run(
            ["git", *arguments],
            cwd=ROOT,
            env=environment,
            input=input_data,
            capture_output=True,
            check=False,
            timeout=60,
        )
    except subprocess.TimeoutExpired as error:
        raise CheckError("Git operation timed out.") from error
    if result.returncode:
        raise CheckError(
            "Git comparison failed: " + result.stderr.decode("utf-8", "replace").strip()
        )
    return result.stdout


def resolve_commit(reference):
    """Resolve user input before using it in any Git operation."""
    value = (
        git_output("rev-parse", "--verify", "--end-of-options", reference + "^{commit}")
        .decode()
        .strip()
    )
    if not re.fullmatch(r"(?:[0-9a-f]{40}|[0-9a-f]{64})", value):
        raise CheckError("Git did not return a commit ID.")
    return value


def revision_pair(reference):
    """Compare committed HEAD with its merge base, not unrelated main commits."""
    head = resolve_commit("HEAD")
    target = resolve_commit(reference)
    base = git_output("merge-base", target, head).decode().strip()
    if not re.fullmatch(r"(?:[0-9a-f]{40}|[0-9a-f]{64})", base):
        raise CheckError("No valid merge base found; fetch the comparison history.")
    paths = [
        os.fsdecode(path)
        for path in git_output(
            "diff",
            "--no-ext-diff",
            "--no-textconv",
            "--no-renames",
            "--name-only",
            "-z",
            base,
            head,
            "--",
        ).split(b"\0")
        if path
    ]
    return base, head, paths


def affected_modules(paths):
    """Use conservative consumers; unknown shared/backend edits check everything."""
    selected = set()
    reasons = set()
    broad = ("src/adafruit_blinka/", "src/microcontroller/", "src/micropython/")
    consumers = {
        "busio": {"board"},
        "digitalio": {"keypad", "neopixel_write"},
        "micropython": set(CHECKED_MODULES),
        "microcontroller": set(CHECKED_MODULES),
    }
    for path in paths:
        if path.startswith(broad) or path in (
            "scripts/check_circuitpython_api.py",
            "requirements-api.txt",
            "requirements.txt",
            "setup.py",
            "pyproject.toml",
            ".github/workflows/build.yml",
            "src/board_imports.json",
            "src/microcontroller_imports.json",
        ):
            return (
                list(CHECKED_MODULES),
                "Shared/backend/tooling change: full audited profile.",
            )
        if path.startswith("src/"):
            relative = PurePosixPath(path).relative_to("src")
            if (
                len(relative.parts) == 1
                and relative.suffix == ".py"
                and relative.stem in CHECKED_MODULES
            ):
                name = relative.stem
                selected.add(name)
                selected.update(consumers.get(name, ()))
                reasons.add(name)
            else:
                return (
                    list(CHECKED_MODULES),
                    "Unmapped source change: full audited profile.",
                )
    ordered = [name for name in CHECKED_MODULES if name in selected]
    return (
        ordered,
        "Affected APIs: " + ", ".join(sorted(reasons))
        if ordered
        else "No audited API source changed.",
    )


def extract_source(revision, destination):
    """Read exact committed blobs, ignoring archive/export attributes entirely."""
    # Keep complete manifest/framing validation ahead of every filesystem write.
    # pylint: disable=too-many-locals
    listing = git_output("ls-tree", "-r", "-z", "--full-tree", revision, "--", "src")
    destination = Path(destination).resolve()
    entries = []
    for record in listing.split(b"\0"):
        if not record:
            continue
        try:
            details, raw_path = record.split(b"\t", 1)
            mode, kind, object_id = details.split()
        except ValueError as error:
            raise CheckError("Invalid Git source-tree entry.") from error
        path = PurePosixPath(os.fsdecode(raw_path))
        if (
            path.is_absolute()
            or ".." in path.parts
            or not path.parts
            or path.parts[0] != "src"
        ):
            raise CheckError("Unsafe Git source path: " + str(path))
        if mode not in (b"100644", b"100755") or kind != b"blob":
            raise CheckError(
                "Git source contains a link or special entry: " + str(path)
            )
        if not re.fullmatch(rb"(?:[0-9a-f]{40}|[0-9a-f]{64})", object_id):
            raise CheckError("Invalid Git source object ID.")
        entries.append((path, object_id))
    contents = []
    if entries:
        stream = io.BytesIO(
            git_output(
                "cat-file",
                "--batch",
                input_data=b"".join(object_id + b"\n" for _, object_id in entries),
            )
        )
        for path, object_id in entries:
            fields = stream.readline().rstrip(b"\n").split()
            if (
                len(fields) != 3
                or fields[:2] != [object_id, b"blob"]
                or not fields[2].isdigit()
            ):
                raise CheckError("Invalid Git source-blob response.")
            size = int(fields[2])
            if size > len(stream.getbuffer()) - stream.tell() - 1:
                raise CheckError("Incomplete Git source-blob response.")
            content = stream.read(size)
            if len(content) != size or stream.read(1) != b"\n":
                raise CheckError("Incomplete Git source-blob response.")
            contents.append((path, content))
        if stream.read():
            raise CheckError("Unexpected trailing Git source-blob response.")
    # Validate every target before writing any content. Links in the tree were
    # rejected above; also reject any pre-existing filesystem link escape.
    targets = []
    for path, content in contents:
        target = destination.joinpath(*path.parts)
        if destination not in target.resolve().parents:
            raise CheckError(
                "Source target escapes the snapshot directory: " + str(path)
            )
        targets.append((target, content))
    for target, content in targets:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
    (destination / "src").mkdir(parents=True, exist_ok=True)
    return destination / "src"


def collect_diagnostics(source, modules):
    """Keep selected-module deletion a regression, not a silent skipped check."""
    implemented = source_modules(source)
    present = [name for name in modules if name in implemented]
    missing = [
        name + " is not present at runtime"
        for name in modules
        if name not in implemented
    ]
    return sorted(missing + run_stubtest(source, present))


def compare_revisions(report, reference, names, modules=None):
    """Run the same trusted worker and installed stubs on both committed trees."""
    base, head, paths = revision_pair(reference)
    selected, reason = affected_modules(paths)
    if modules is not None:
        selected = [name for name in CHECKED_MODULES if name in modules]
        reason = "Explicit module selection."
    report["unreferenced_modules"] = [name for name in selected if name not in names]
    selected = [name for name in selected if name in names]
    report.update(
        base_revision=base,
        head_revision=head,
        changed_paths=paths,
        checked_modules=selected,
        selection_reason=reason,
    )
    with tempfile.TemporaryDirectory(prefix="blinka-api-revisions-") as scratch:
        base_source = extract_source(base, Path(scratch) / "base")
        head_source = extract_source(head, Path(scratch) / "head")
        report["modules"] = inventory(names, source_modules(head_source), selected)
        report["base_diagnostics"] = collect_diagnostics(base_source, selected)
        report["diagnostics"] = collect_diagnostics(head_source, selected)
    previous, current = set(report["base_diagnostics"]), set(report["diagnostics"])
    report["new"], report["resolved"] = sorted(current - previous), sorted(
        previous - current
    )


def markdown_report(report):
    """Produce a readable artifact without calling unchecked modules compatible."""
    lines = [
        "# CircuitPython API comparison",
        "",
        f"Reference: {report['reference']}. Target: {TARGET}.",
        f"Mode: {report['mode']}. {report['selection_reason']}",
        f"Checked modules: {', '.join(report['checked_modules']) or 'none'}.",
        "",
        "API surface only; this is not behavior or hardware validation.",
        "",
        "## Module inventory",
        "",
        "| Module | Status | Notes |",
        "| --- | --- | --- |",
    ]
    if report["base_revision"]:
        lines[8:8] = [
            f"Base: `{report['base_revision']}`; head: `{report['head_revision']}`.",
            "",
        ]
    for item in report["modules"]:
        lines.append(f"| {item['name']} | {item['status']} | {item['reason']} |")
    for title, values in (
        ("Checker errors", report["errors"]),
        ("New API differences", report["new"]),
        ("Resolved API differences", report["resolved"]),
        ("Base revision discrepancies", report["base_diagnostics"]),
        ("All current stub discrepancies", report["diagnostics"]),
    ):
        lines.extend(["", "## " + title, ""])
        lines.extend("- " + value for value in values)
        if not values:
            lines.append("None.")
    return "\n".join(lines) + "\n"


def main(argv=None):
    """Report full compatibility or gate regressions; never install dependencies."""
    # Reporting and error paths deliberately share the same result object.
    # pylint: disable=too-many-locals
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", type=Path, help="write the full JSON report")
    parser.add_argument("--markdown", type=Path, help="write the full Markdown report")
    parser.add_argument(
        "--module",
        choices=CHECKED_MODULES,
        action="append",
        help="check only this API (repeatable)",
    )
    parser.add_argument(
        "--base", help="compare committed HEAD with the merge base of this Git ref"
    )
    parser.add_argument(
        "--stable-release",
        help="require installed stubs to match this verified CircuitPython stable tag",
    )
    args = parser.parse_args(argv)
    report = {
        "reference": {},
        "target": TARGET,
        "mode": "revision" if args.base else "standalone",
        "checked_modules": [],
        "selection_reason": "",
        "unreferenced_modules": [],
        "base_revision": None,
        "head_revision": None,
        "changed_paths": [],
        "modules": [],
        "diagnostics": [],
        "base_diagnostics": [],
        "new": [],
        "resolved": [],
        "errors": [],
    }
    try:
        report["reference"] = {name: metadata.version(name) for name in REFERENCE}
        actual = report["reference"]
        if actual["mypy"] != REFERENCE["mypy"]:
            raise CheckError(
                f"Expected mypy=={REFERENCE['mypy']}, found {actual['mypy']}."
            )
        if not re.fullmatch(r"\d+\.\d+\.\d+", actual["circuitpython-stubs"]):
            raise CheckError("Use stubs matching a stable CircuitPython release.")
        if (
            args.stable_release is not None
            and args.stable_release != actual["circuitpython-stubs"]
        ):
            raise CheckError(
                f"CircuitPython stable is {args.stable_release}, but the reference is "
                f"{actual['circuitpython-stubs']}. Install the matching stubs before continuing."
            )
        names = stub_modules(metadata.distribution("circuitpython-stubs"))
        selected = (
            None
            if args.module is None
            else [name for name in CHECKED_MODULES if name in args.module]
        )
        if args.base:
            compare_revisions(report, args.base, names, selected)
        else:
            chosen = list(CHECKED_MODULES) if selected is None else selected
            report["unreferenced_modules"] = [
                name for name in chosen if name not in names
            ]
            chosen = [name for name in chosen if name in names]
            report["checked_modules"] = chosen
            report["selection_reason"] = (
                "Full audited profile."
                if selected is None
                else "Explicit module selection."
            )
            report["modules"] = inventory(names, source_modules(SOURCE), chosen)
            report["diagnostics"] = collect_diagnostics(SOURCE, chosen)
    except (
        CheckError,
        OSError,
        ValueError,
        metadata.PackageNotFoundError,
    ) as error:
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
    print(
        "Reference:",
        ", ".join(f"{key}={value}" for key, value in report["reference"].items()),
    )
    print(f"Mode: {report['mode']}. {report['selection_reason']}")
    if report["unreferenced_modules"]:
        print(
            "NOT CHECKED (no reference stub): "
            + ", ".join(report["unreferenced_modules"])
        )
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
    if report["mode"] == "standalone":
        for message in report["diagnostics"]:
            print("DIFFERENCE: " + message)
    if report["errors"]:
        return 2
    return int(bool(report["new"] if args.base else report["diagnostics"]))


if __name__ == "__main__":
    if sys.argv[1:2] == ["--_worker"]:
        if len(sys.argv) < 4:
            raise SystemExit("Worker requires a source directory and audited modules.")
        raise SystemExit(stubtest_worker(sys.argv[2], sys.argv[3:]))
    raise SystemExit(main())
