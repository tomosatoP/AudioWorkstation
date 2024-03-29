#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Assists in connecting to Bluetooth device."""

import bluetooth as BT
import logging as LBT
from subprocess import Popen, run, PIPE


# Logger
logger = LBT.getLogger(__name__)
logger.setLevel(LBT.DEBUG)
_logger_formatter = LBT.Formatter("%(asctime)s %(levelname)s %(message)s")
# Logger StreamHandler
_logger_sh = LBT.StreamHandler()
_logger_sh.setFormatter(_logger_formatter)
logger.addHandler(_logger_sh)


def _audiosink(address: str) -> tuple:
    """Get information on "audio sink" service.

    :param str address: device address
    :return: (address, port)
    """
    ass = BT.find_service(uuid=BT.AUDIO_SINK_CLASS, address=address)
    if not ass:
        return ("", 0)
    return (ass[0]["host"], ass[0]["port"])


def _paired_devices() -> dict[str, str]:
    """Returns a list of paired devices.

    :return: name, address
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


def _isnearby_audiosink(address: str) -> bool:
    """Find out if the paired device with Audio Sink is nearby.

    :param str address: paired device address
    :return: True is nearby, False is otherwise
    """
    if not BT.lookup_name(address=address):
        return False

    pre_pipe = ["bluetoothctl", "--", "info", address]
    post_pipe = ["grep", "Audio Sink"]
    result = Popen(args=pre_pipe, stdout=PIPE, text=True)
    result = Popen(args=post_pipe, stdin=result.stdout, stdout=PIPE, text=True)
    return True if result.communicate()[0] else False


def _isconnected(address: str, audio_sink: bool = True) -> bool:
    """Check the connection of paired devices nearby.

    :param str address: address of paired devices nearby
    :return: True is connected, False is otherwise
    """
    pre_pipe = ["bluetoothctl", "--", "info", address]
    post_pipe = ["grep", "Connected"]
    result = Popen(args=pre_pipe, stdout=PIPE, text=True)
    result = Popen(args=post_pipe, stdin=result.stdout, stdout=PIPE, text=True)
    return True if result.communicate()[0].split()[1] == "yes" else False


def _connect(address: str) -> bool:
    """Attempts to connect to a Bluetooth device.

    :param str address: device address
    :return: True is success, False is otherwise
    """
    command = ["bluetoothctl", "--", "connect", address]
    result = run(args=command, capture_output=True, text=True)
    return False if result.returncode else True


def device_info() -> dict[str, str]:
    """Get information on connected Bluetooth devices.

    :return: {name: address}
    :examples: {"name": "00:00:00:00:00:00"}
    :examples: {"": ""} if failed.
    """
    devices = _paired_devices()

    for name, address in devices.items():
        if _isnearby_audiosink(address):
            if _isconnected(address):
                return {name: address}
            elif _connect(address):
                return {name: address}

    logger.info("Bluetooth Audio Sink Device: Not found.")
    return {"": ""}


if __name__ == "__main__":
    print(__file__)
