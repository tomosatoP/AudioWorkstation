#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Connect to jack server and set MASTER volume

:method bool start():
:method str volume(Optional[str] percentage):
"""


import subprocess
from typing import Optional

# Master Volume (PulseAudio)
_amixer_master = ["amixer", "sset", "Master", "50%,50%", "-M", "unmute"]


def start() -> bool:
    """start jackd server"""
    with open(file="config/linkbuds-aac.jack", mode="r") as f:
        for line in f:
            result = subprocess.run(line.strip("\n").split(" "))
            if result.returncode != 0:
                return False
    return True


def volume(percentage: Optional[str] = None) -> str:
    """Master playback volume settings

    [args]
    - None: returns the current volume setting as a percentage
    - If both left and right are set to 100%, '100%,100%'
    - If both left and right are 10% larger, '10%+,10%+'
    - If both left and right are 10% smaller, '10%-,10%-'
    """

    if percentage is not None:
        _amixer_master[3] = percentage

    result = subprocess.run(_amixer_master, capture_output=True, text=True)
    dict_master = dict()
    for line_buffer in result.stdout.splitlines():
        listb = line_buffer.strip().split(":")
        if len(listb) > 1:
            dict_master[listb[0]] = listb[1].strip()

    l_vol = dict_master["Front Left"].split()[2].strip("[]")
    r_vol = dict_master["Front Right"].split()[2].strip("[]")

    return f"{l_vol},{r_vol}"


if __name__ == "__main__":
    print(__file__)

    start()
