# SPDX-FileCopyrightText: 2026 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""Recognize the maintained Trixie bindings whose Python version is misleading.

Keep this stdlib-only helper mirrored in Adafruit_Blinka_Raspberry_Pi_PWM.
The installed OS package database is trusted; this is an integrity/compatibility
check, not protection against a privileged attacker. No GPIO devices are opened.
"""

import hashlib
import importlib
import importlib.machinery
import importlib.metadata
import importlib.util
import os
import shlex
import subprocess
import sys
from pathlib import Path

_SYSTEM_SITE = Path("/usr/lib/python3/dist-packages")
_OS_RELEASE = Path("/etc/os-release")
_SOURCE_VERSION = "2.2.1-2+deb13u1"
# Identity attestations are shared only with our mirror, not availability caches.
_VERIFIED_MODULES = {}
_HELPER_MODULES = (
    "adafruit_blinka._gpiod_compat",
    "adafruit_blinka_raspberry_pi_pwm._gpiod_compat",
)


def _loaded_bindings():
    """Snapshot every loaded binding object, including partially failed imports."""
    return {
        name: module
        for name, module in tuple(sys.modules.items())
        if name == "gpiod" or name.startswith("gpiod.")
    }


def _previously_verified(name, module):
    """Require the identical object imported after successful file verification."""
    if module is None:
        return False
    if _VERIFIED_MODULES.get(name) is module:
        return True
    return any(
        getattr(sys.modules.get(helper), "_VERIFIED_MODULES", {}).get(name) is module
        for helper in _HELPER_MODULES
    )


def _dpkg_query(*arguments):
    """Read the real system database, regardless of caller environment settings."""
    environment = os.environ.copy()
    environment.update(LC_ALL="C", LANGUAGE="C")
    return subprocess.run(
        [
            "/usr/bin/dpkg-query",
            "--root=/",
            "--admindir=/var/lib/dpkg",
            "--no-pager",
            *arguments,
        ],
        check=True,
        capture_output=True,
        text=True,
        stdin=subprocess.DEVNULL,
        timeout=3,
        env=environment,
    ).stdout


def _same_path(path, expected):
    """Reject a different installation, including symlinks outside this one."""
    return Path(path) == expected and Path(path).resolve(strict=True) == expected


def _verified_files(package, extension, metadata):
    """Check code against mandatory checksums supplied by the installed package."""
    checksums = {}
    for entry in _dpkg_query(
        "--control-show", "python3-libgpiod", "md5sums"
    ).splitlines():
        digest, relative = entry.split(maxsplit=1)
        path = Path("/") / relative
        if (
            len(digest) != 32
            or any(character not in "0123456789abcdef" for character in digest)
            or relative.startswith("/")
            or ".." in Path(relative).parts
            or path in checksums
        ):
            return set()
        checksums[path] = digest

    required = {package / "__init__.py", extension, metadata}
    required.update(
        path for path in package.rglob("*") if path.suffix in (".py", ".so")
    )
    # Include missing package files as well as unexpected local additions.
    required.update(
        path
        for path in checksums
        if package in path.parents and path.suffix in (".py", ".so")
    )
    for path in required:
        if path not in checksums or not _same_path(path, path):
            return set()
        # MD5 is the format provided by dpkg, not a security/authenticity claim.
        if (
            hashlib.md5(path.read_bytes(), usedforsecurity=False).hexdigest()
            != checksums[path]
        ):
            return set()
    return required


def is_supported_system_gpiod():
    """Return whether the selected 2.2.0 bindings are the verified Trixie build.

    This is only the system-package exception. Callers retain their normal
    supported PyPI version bounds. Unknown versions and unverifiable installs
    are deliberately not accepted. Previously loaded objects need an identity
    attestation from this helper or its mirror; filenames cannot prove their
    source after an OS reinstall. Files and packages are rechecked every call.
    """
    # Keep the explicit fail-closed predicates together for auditability.
    # pylint: disable=too-many-return-statements,too-many-boolean-expressions
    try:
        if sys.platform != "linux":
            return False
        release = {}
        for line in _OS_RELEASE.read_text(encoding="utf-8").splitlines():
            key, separator, value = line.partition("=")
            if separator and key in ("ID", "VERSION_CODENAME"):
                (release[key],) = shlex.split(value, comments=True)
        if (
            release.get("ID") not in ("debian", "raspbian")
            or release.get("VERSION_CODENAME") != "trixie"
        ):
            return False

        package = _SYSTEM_SITE / "gpiod"
        metadata = _SYSTEM_SITE / "gpiod-2.2.0.dist-info" / "METADATA"
        spec = importlib.util.find_spec("gpiod")
        distribution = importlib.metadata.distribution("gpiod")
        if (
            spec is None
            or not _same_path(spec.origin, package / "__init__.py")
            or list(spec.submodule_search_locations or ()) != [str(package)]
            or distribution.version != "2.2.0"
            or not _same_path(distribution.locate_file(""), _SYSTEM_SITE)
            or not _same_path(
                distribution.locate_file("gpiod-2.2.0.dist-info/METADATA"), metadata
            )
        ):
            return False
        spec = importlib.machinery.PathFinder.find_spec("gpiod._ext", [str(package)])
        if spec is None:
            return False
        extension = Path(spec.origin)
        if extension.parent != package:
            return False

        status = _dpkg_query(
            "--show",
            "--showformat=${Status}\t${source:Package}\t${source:Version}\\n",
            "python3-libgpiod",
        )
        if status.strip() != f"install ok installed\tlibgpiod\t{_SOURCE_VERSION}":
            return False
        verified = _verified_files(package, extension, metadata)
        if not verified:
            return False
        if any(
            not _previously_verified(name, loaded)
            for name, loaded in _loaded_bindings().items()
        ):
            return False

        module = importlib.import_module("gpiod")
        native = importlib.import_module("gpiod._ext")
        if (
            module.__version__ != "2.2.0"
            or not _same_path(module.__file__, package / "__init__.py")
            or list(module.__path__) != [str(package)]
            or not _same_path(native.__file__, extension)
            or module.api_version != "2.2.1"
        ):
            return False
        loaded_bindings = _loaded_bindings()
        if not all(
            Path(loaded.__file__) in verified
            and _same_path(loaded.__file__, Path(loaded.__file__))
            for loaded in loaded_bindings.values()
        ):
            return False
        _VERIFIED_MODULES.update(loaded_bindings)
        return True
    # Compatibility detection must not turn a missing/unverifiable package into
    # an unrelated startup exception. Interrupts and SystemExit still propagate.
    except Exception:  # pylint: disable=broad-exception-caught
        return False
