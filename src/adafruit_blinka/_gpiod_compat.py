# SPDX-FileCopyrightText: 2026 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""Recognize maintained Debian bindings whose Python version is misleading.

Keep this helper mirrored in Adafruit_Blinka_Raspberry_Pi_PWM. It trusts the
installed OS package database and administrator, not checksums or import order.
Package facts are cached per process: restart Python after OS package changes.
No GPIO devices are opened.
"""

import importlib
import importlib.metadata
import os
import subprocess
import sys
from functools import lru_cache
from pathlib import Path

from packaging.version import Version

_SYSTEM_SITE = Path("/usr/lib/python3/dist-packages")


def _maintained_version(version):
    """The libgpiod 2.2.1 source release fixed the Python line-request bug."""
    parsed = Version(version)
    return not parsed.is_prerelease and Version("2.2.1") <= parsed < Version("3")


@lru_cache(maxsize=1)
def _system_package_files():
    """Read installed source version and ownership once from the OS database."""
    environment = os.environ.copy()
    environment.update(LC_ALL="C", LANGUAGE="C")
    try:
        output = subprocess.run(
            [
                "/usr/bin/dpkg-query",
                "--root=/",
                "--admindir=/var/lib/dpkg",
                "--no-pager",
                "--show",
                "--showformat=${Status}\\t${source:Package}\\t"
                "${source:Upstream-Version}\\n${db-fsys:Files}",
                "python3-libgpiod",
            ],
            check=True,
            capture_output=True,
            text=True,
            stdin=subprocess.DEVNULL,
            timeout=3,
            env=environment,
        ).stdout
        header, *files = output.splitlines()
        status, source, upstream = header.split("\t")
        if (
            status != "install ok installed"
            or source != "libgpiod"
            or not _maintained_version(upstream)
        ):
            return frozenset()
        return frozenset(Path(name.strip()) for name in files)
    except Exception:  # pylint: disable=broad-exception-caught
        return frozenset()


def _same_path(path, expected):
    """Exclude alternate installations and symlinks outside the system package."""
    return Path(path) == expected and Path(path).resolve(strict=True) == expected


def is_supported_system_gpiod():
    """Accept the OS-maintained 2.2.0 label, including already imported bindings.

    This exception is separate from callers' normal PyPI version bounds. PyPI
    2.2.0 is unsafe even when linked with a newer system libgpiod. Require the
    selected Python package, metadata and native extension to belong to the
    maintained OS package; native library version alone is insufficient.
    """
    # Keep the inexpensive predicates together, before the cached package query.
    # pylint: disable=too-many-boolean-expressions
    try:
        if sys.platform != "linux":
            return False
        module = importlib.import_module("gpiod")
        native = importlib.import_module("gpiod._ext")
        distribution = importlib.metadata.distribution("gpiod")
        package = _SYSTEM_SITE / "gpiod"
        metadata = _SYSTEM_SITE / "gpiod-2.2.0.dist-info" / "METADATA"
        # locate_file() uses the installation root, not the selected metadata
        # directory. PathDistribution exposes that origin only through _path;
        # decline the exception if another provider cannot identify its origin.
        metadata_directory = getattr(distribution, "_path", None)
        extension = Path(native.__file__)
        if (
            module.__version__ != "2.2.0"
            or distribution.version != "2.2.0"
            or not _same_path(module.__file__, package / "__init__.py")
            or list(module.__path__) != [str(package)]
            or not _same_path(distribution.locate_file(""), _SYSTEM_SITE)
            or metadata_directory is None
            or not _same_path(Path(metadata_directory) / "METADATA", metadata)
            or extension.parent != package
            or extension.suffix != ".so"
            or not _same_path(extension, extension)
            or not _maintained_version(native.api_version)
        ):
            return False
        required = {package / "__init__.py", extension, metadata}
        return required <= _system_package_files()
    except Exception:  # pylint: disable=broad-exception-caught
        return False
