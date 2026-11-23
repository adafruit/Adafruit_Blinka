# SPDX-FileCopyrightText: 2026 Bert Outtier
#
# SPDX-License-Identifier: MIT
"""sysfs PWMOut cleanup at exit and across fork(), on a simulated sysfs."""

import json
from pathlib import Path
import subprocess
import sys

MODULE = (
    Path(__file__).resolve().parents[1]
    / "src/adafruit_blinka/microcontroller/generic_linux/sysfs_pwmout.py"
)

# Runs in its own interpreter, so that its exit (atexit handlers, then the
# finalization of the remaining objects) is a real one.
SCRIPT = """
import importlib.util, json, os, sys, types

sysfs, scenario = sys.argv[1], sys.argv[2]
pin = types.ModuleType("microcontroller.pin")
pin.pwmOuts = [((0, 1), "P1"), ((0, 2), "P2")]
sys.modules["microcontroller"] = types.ModuleType("microcontroller")
sys.modules["microcontroller.pin"] = pin
spec = importlib.util.spec_from_file_location("sysfs_pwmout", sys.argv[3])
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
module.PWMOut._sysfs_path = sysfs

# Like sysfs attributes: opening one for writing does not clear its value,
# a write replaces it
real_open = open

class Attribute:
    def __init__(self, path):
        self.path = path
    def __enter__(self):
        return self
    def __exit__(self, *args):
        pass
    def write(self, value):
        with real_open(self.path, "w", encoding="utf-8") as f:
            f.write(value)

def sysfs_open(path, mode="r", **kwargs):
    if "w" in mode:
        return Attribute(path)
    return real_open(path, mode, **kwargs)

module.open = sysfs_open

unexport = os.path.join(sysfs, "pwmchip0", "unexport")

def unexported():
    with open(unexport, encoding="utf-8") as f:
        return f.read().split()

pwm = module.PWMOut("P1", frequency=1000, duty_cycle=1000)
open(unexport, "w", encoding="utf-8").close()
if scenario == "fork":
    pid = os.fork()
    if pid == 0:
        if sys.argv[4] == "child-output":
            child = module.PWMOut("P2", frequency=1000)
            open(unexport, "w", encoding="utf-8").close()
        sys.exit(0)
    os.waitpid(pid, 0)
    print(json.dumps(unexported()))
    pwm.deinit()
# scenario "exit": leave pwm to the atexit handler
"""


def make_sysfs(root):
    chip = root / "pwmchip0"
    for channel in (1, 2):
        (chip / f"pwm{channel}").mkdir(parents=True)
        for name in ("period", "duty_cycle", "enable", "polarity"):
            (chip / f"pwm{channel}" / name).write_text("0\n")
    (chip / "export").write_text("")
    (chip / "unexport").write_text("")
    return chip


def run(tmp_path, scenario, child="none"):
    chip = make_sysfs(tmp_path)
    result = subprocess.run(
        [sys.executable, "-c", SCRIPT, str(tmp_path), scenario, str(MODULE), child],
        capture_output=True,
        text=True,
        check=True,
    )
    return result, chip


def test_output_left_open_is_unexported_at_exit(tmp_path):
    result, chip = run(tmp_path, "exit")
    assert result.stderr == ""
    assert (chip / "unexport").read_text().split() == ["1"]


def test_forked_child_leaves_the_parents_output_exported(tmp_path):
    result, _ = run(tmp_path, "fork")
    assert result.stderr == ""
    assert json.loads(result.stdout) == []


def test_forked_child_unexports_its_own_output(tmp_path):
    result, _ = run(tmp_path, "fork", "child-output")
    assert result.stderr == ""
    assert json.loads(result.stdout) == ["2"]
