#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Connect to JACK server and set MASTER volume

:method bool jackstart(): connect to JACK server
:method str volume(Optional[str] percentage): set MASTER volume
"""


import subprocess
from json import load
from typing import Optional

from audioworkstation.libs.audio import btaudiosink as BTAS
from audioworkstation.libs.audio import asound as SCARD

# MASTER Volume (PulseAudio)
_master: str = "amixer -D default sset Master 100%,100% -M unmute"


def jackstart() -> tuple[str, str]:
    """start JACK server"""
    btdevice: dict[str, str] = BTAS.btdevicename()
    soundcard: list[str] = SCARD.soundcardname()
    device_name: str = ""
    device_controlname: str = ""
    if "" not in btdevice:
        device_name = "bluealsa"
        device_controlname = "A2DP"
    elif soundcard:
        device_name = soundcard[0].split("CARD=")[1]
        device_controlname = "PCM"
    else:
        device_name = "Headphones"
        device_controlname = "PCM"

    subprocess.run(args=_master.split())
    with open(file="config/jack.json", mode="rt") as f:
        settings = load(f)
        for type, commandlist in settings[device_name].items():
            for command in commandlist:
                result = subprocess.run(command.split())
                if result.returncode:
                    return ("", "")

    return (device_name, device_controlname)


def volume(percentage: Optional[str] = None) -> str:
    """Master playback volume settings

    [args]
    - None: returns the current volume setting as a percentage
    - If both left and right are set to 100%, '100%,100%'
    - If both left and right are 10% larger, '10%+,10%+'
    - If both left and right are 10% smaller, '10%-,10%-'
    """
    master = ["amixer", "sset", "Master", "100%,100%", "-M", "unmute"]
    if percentage is not None:
        master[3] = percentage

    result = subprocess.run(master, capture_output=True, text=True)
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
