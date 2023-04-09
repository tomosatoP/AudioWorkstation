#!/usr/bin/env python3
"""Assists in connecting to Bluetooth device.

:method dict isavailable(): dict is {name: address}  on connected device
"""

import bluetooth as BT
from subprocess import Popen, run, PIPE


def _paired_devices() -> dict[str, str]:
    """Returns a list of paired devices.

    :return dict[str, str]: name, address
    """
    devices: dict[str, str] = dict()
    command = ["bluetoothctl", "--", "paired-devices"]
    result = run(args=command, capture_output=True, text=True)
    if result.returncode:
        return devices
    for line in result.stdout.splitlines():
        # line: Devices <addres> <name>
        parts = line.split(sep=" ", maxsplit=2)
        devices[parts[2]] = parts[1]
    return devices


def _isnearby_audiosink(bt_address: str) -> bool:
    """Find out if the paired device is nearby.

    :param str bt_address: paired device address
    :return bool: True is nearby, False is otherwise
    """
    if not BT.lookup_name(address=bt_address):
        return False

    pre_pipe = ["bluetoothctl", "--", "info", bt_address]
    post_pipe = ["grep", "Audio Sink"]
    result = Popen(args=pre_pipe, stdout=PIPE, text=True)
    result = Popen(args=post_pipe, stdin=result.stdout, stdout=PIPE, text=True)
    return True if result.communicate()[0] else False


def _isconnected(bt_address: str, audio_sink: bool = True) -> bool:
    """Check the connection of paired devices nearby.

    :param str bt_address: address of paired devices nearby
    :return bool: True is connected, False is otherwise
    """
    pre_pipe = ["bluetoothctl", "--", "info", bt_address]
    post_pipe = ["grep", "Connected"]
    result = Popen(args=pre_pipe, stdout=PIPE, text=True)
    result = Popen(args=post_pipe, stdin=result.stdout, stdout=PIPE, text=True)
    return True if result.communicate()[0].split()[1] == "yes" else False


def _connect(bt_address: str) -> bool:
    """Attempts to connect to a Bluetooth device.

    :param str bt_address: device address
    :return bool: True is success, False is otherwise
    """
    command = ["bluetoothctl", "--", "connect", bt_address]
    result = run(args=command, capture_output=True, text=True)
    return False if result.returncode else True


def isavailable() -> dict[str, str]:
    devices = _paired_devices()

    for name, address in devices.items():
        if _isnearby_audiosink(address):
            if _isconnected(address):
                return {name: address}
            elif _connect(address):
                return {name: address}

    return {"": ""}


if __name__ == "__main__":
    print(__file__)
