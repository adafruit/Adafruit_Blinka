# SPDX-FileCopyrightText: 2026 Bert Outtier
#
# SPDX-License-Identifier: MIT
"""Import the Phyx Tess board and the Allwinner T113 pins without hardware."""

import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

# A gpiod 2.x stand-in: importing the pin modules must not open GPIO devices.
GPIOD_STUB = """
from types import SimpleNamespace
__version__ = "2.2.2"
class Chip:
    pass
class LineSettings:
    pass
line = SimpleNamespace(
    Value=SimpleNamespace(INACTIVE=0, ACTIVE=1),
    Direction=SimpleNamespace(INPUT="input", OUTPUT="output"),
    Bias=SimpleNamespace(DISABLED="disabled", PULL_UP="up", PULL_DOWN="down"),
)
"""

PROBE = """
import json
import board
import digitalio
from microcontroller import pin

def ids(row):
    return [row[0]] + [p.id for p in row[1:]]

print(json.dumps({
    "board": {n: getattr(board, n).id for n in ("SDA", "SCL", "SCK", "MOSI",
              "MISO", "TX", "RX", "D10", "G3")},
    "A0": board.A0,
    "i2c": [ids(r) for r in pin.i2cPorts],
    "uart": [ids(r) for r in pin.uartPorts],
    "spi": [ids(r) for r in pin.spiPorts],
    "analog": [list(r) for r in pin.analogIns],
    "has_i2c": hasattr(board, "I2C"),
    "has_spi": hasattr(board, "SPI"),
}))
"""


def probe(tmp_path):
    """Import board and microcontroller.pin as Blinka does on a Tess."""
    (tmp_path / "gpiod.py").write_text(GPIOD_STUB)
    env = dict(os.environ)
    env.update(
        BLINKA_FORCECHIP="T113",
        BLINKA_FORCEBOARD="PHYX_TESS",
        PYTHONPATH=os.pathsep.join(
            [str(tmp_path), str(ROOT / "src"), os.environ.get("PYTHONPATH", "")]
        ),
    )
    result = subprocess.run(
        [sys.executable, "-c", PROBE],
        env=env,
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(result.stdout.splitlines()[-1])


def line(name):
    """Linux GPIO line of an Allwinner pin name like PE7."""
    return (ord(name[1]) - ord("A")) * 32 + int(name[2:])


def test_feather_pins(tmp_path):
    info = probe(tmp_path)
    expected = {
        "SDA": "PE7",
        "SCL": "PE6",
        "SCK": "PD11",
        "MOSI": "PD12",
        "MISO": "PD13",
        "TX": "PB4",
        "RX": "PB5",
        "D10": "PD10",
        "G3": "PG3",
    }
    assert info["board"] == {name: line(p) for name, p in expected.items()}
    assert info["has_i2c"] and info["has_spi"]


def test_feather_buses_are_valid_ports(tmp_path):
    info = probe(tmp_path)
    board = info["board"]
    assert [3, board["SCL"], board["SDA"]] in info["i2c"]
    assert [5, board["TX"], board["RX"]] in info["uart"]
    assert [1, board["SCK"], board["MOSI"], board["MISO"]] in info["spi"]


def test_a0_is_gpadc_channel_0(tmp_path):
    info = probe(tmp_path)
    assert [info["A0"], 0, 0] in info["analog"]
