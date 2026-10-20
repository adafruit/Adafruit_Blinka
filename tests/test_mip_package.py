# SPDX-FileCopyrightText: 2026 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""Validate the mip manifest without importing Blinka or accessing hardware/network."""

import json
import re
from pathlib import Path, PurePosixPath

import pytest

ROOT = Path(__file__).parents[1]
MANIFEST = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
MAPPINGS = MANIFEST["urls"]
DESTINATIONS = {entry[0] for entry in MAPPINGS}
PLATFORMDETECT_FILES = {
    "__init__.py",
    "board.py",
    "chip.py",
    "constants/__init__.py",
    "constants/boards.py",
    "constants/chips.py",
    "LICENSE",
}


def require_module(module):
    """Resolve both a single-file module and a regular package in the install tree."""
    stem = module.replace(".", "/")
    assert {stem + ".py", stem + "/__init__.py"} & DESTINATIONS, module


def test_manifest_sources_and_destinations():
    """Keep paths local to the install target and include every package initializer."""
    assert set(MANIFEST) == {"urls"}
    assert len(DESTINATIONS) == len(MAPPINGS)
    external_refs = set()
    for entry in MAPPINGS:
        assert len(entry) == 2 and all(isinstance(value, str) for value in entry)
        destination, source = entry
        path = PurePosixPath(destination)
        assert not path.is_absolute()
        assert all(part not in ("", ".", "..") for part in destination.split("/"))
        assert "\\" not in destination
        for parent in path.parents:
            if parent != PurePosixPath("."):
                assert str(parent / "__init__.py") in DESTINATIONS

        if destination.startswith("adafruit_platformdetect/"):
            match = re.fullmatch(
                r"https://raw\.githubusercontent\.com/adafruit/"
                r"Adafruit_Python_PlatformDetect/([0-9a-f]{40})/(.+)",
                source,
            )
            assert match is not None
            external_refs.add(match[1])
            expected = "LICENSE" if path.name == "LICENSE" else destination
            assert match[2] == expected
        else:
            expected = (
                "LICENSE"
                if destination == "adafruit_blinka/LICENSE"
                else "src/" + destination
            )
            assert source == expected
            assert (ROOT / source).is_file()
    assert len(external_refs) == 1
    assert {
        name.removeprefix("adafruit_platformdetect/")
        for name in DESTINATIONS
        if name.startswith("adafruit_platformdetect/")
    } == PLATFORMDETECT_FILES


def test_only_micropython_sources_are_packaged():
    """Do not bring Linux/native backends, pip dependencies, or the host shim along."""
    top_level = {
        "board.py",
        "busio.py",
        "digitalio.py",
        "bitbangio.py",
        "rainbowio.py",
        "board_imports.json",
        "microcontroller_imports.json",
        "board_imports.json.license",
        "microcontroller_imports.json.license",
    }
    prefixes = (
        "microcontroller/",
        "adafruit_blinka/agnostic/",
        "adafruit_blinka/board/",
        "adafruit_blinka/microcontroller/",
        "adafruit_platformdetect/",
    )
    assert top_level <= DESTINATIONS
    for name in DESTINATIONS:
        assert (
            name in top_level
            or name
            in {
                "adafruit_blinka/__init__.py",
                "adafruit_blinka/importing.py",
                "adafruit_blinka/LICENSE",
            }
            or name.startswith(prefixes)
        )
        if name.startswith("adafruit_blinka/microcontroller/"):
            suffix = name.removeprefix("adafruit_blinka/microcontroller/")
            assert suffix == "__init__.py" or suffix.startswith(
                ("generic_micropython/", "esp8266/", "stm32/", "rp2040/")
            )
        assert name.endswith((".py", ".json", ".license", "/LICENSE"))


@pytest.mark.parametrize(
    "filename, keys",
    [
        (
            "board_imports.json",
            ("FEATHER_HUZZAH", "NODEMCU", "PYBOARD", "any_raspberry_pi_pico_id"),
        ),
        ("microcontroller_imports.json", ("ESP8266", "STM32F405", "RP2040", "RP2350")),
    ],
)
def test_existing_micropython_routes_are_installed(filename, keys):
    """Follow the runtime routing tables rather than duplicating their module paths."""
    routes = json.loads((ROOT / "src" / filename).read_text(encoding="utf-8"))
    for key in keys:
        require_module(routes[key])
        if filename == "microcontroller_imports.json":
            require_module(routes[key] + ".pin")


@pytest.mark.parametrize(
    "module",
    [
        "board",
        "busio",
        "digitalio",
        "bitbangio",
        "rainbowio",
        "microcontroller",
        "microcontroller.pin",
        "adafruit_blinka",
        "adafruit_blinka.importing",
        "adafruit_blinka.agnostic",
        "adafruit_blinka.agnostic.time",
        "adafruit_blinka.microcontroller.generic_micropython",
        "adafruit_blinka.microcontroller.generic_micropython.i2c",
        "adafruit_blinka.microcontroller.generic_micropython.spi",
        "adafruit_blinka.microcontroller.rp2040.i2c",
        "adafruit_blinka.microcontroller.rp2040.spi",
        "adafruit_blinka.microcontroller.rp2040.uart",
    ],
)
def test_shared_and_constructor_imports_are_installed(module):
    """Cover dependencies selected inside constructors, outside the routing tables."""
    require_module(module)
