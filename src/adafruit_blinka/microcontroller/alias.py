# SPDX-FileCopyrightText: 2023 Steve Jeong for Hardkernel
#
# SPDX-License-Identifier: MIT

"""
Functions to find aliases for all hardware,
including those defined in the device tree.
"""

from typing import Optional
import os
import re


def get_dts_alias(device: str) -> Optional[str]:
    """Get the Device Tree Alias"""
    uevent_path = "/sys/bus/platform/devices/" + device + "/uevent"
    if os.path.exists(uevent_path):
        with open(uevent_path, "r", encoding="utf-8") as fd:
            pattern = r"^OF_ALIAS_0=(.*)$"
            uevent = fd.read().split("\n")
            for line in uevent:
                match = re.search(pattern, line)
                if match:
                    return match.group(1).upper()
    return None


def get_pwm_chipid(device: str):
    """Get the PWM Chip ID"""
    for chipid in range(32):
        pwm_sys_path = "/sys/class/pwm/pwmchip{}".format(chipid)
        if not os.path.exists(pwm_sys_path):
            continue
        if device in os.path.realpath(pwm_sys_path):
            alias = "PWM" + str(chipid)
            return alias
    return None
