#!/usr/bin/env python3
"""PyBluez advanced example read-local-bdaddr.py

Read the local Bluetooth device address
"""

import bluetooth as BT
from subprocess import Popen, run, PIPE


def audiosink(bt_address: str) -> tuple:
    """Get information on "audio sink" service.

    :param str bt_address: device address
    :return tuple: (propocol, port)
    """
    ass = BT.find_service(address=bt_address, uuid=BT.AUDIO_SINK_CLASS)
    if not ass:
        return ("", 0)
    return (ass[0]["protocol"], ass[0]["port"])


def paired_devices() -> dict[str, str]:
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


def isnearby(bt_address: str) -> bool:
    """Find out if the paired device is nearby

    :param str bt_address: paired device address
    :return bool: True is nearby, False is otherwise
    """
    if not BT.lookup_name(address=bt_address):
        return False
    return True


def isconnected(bt_address: str) -> bool:
    """Check the connection of paired devices nearby.

    :param str bt_address: address of paired devices nearby
    :return bool: True is connected, False is otherwise
    """
    pre_pipe = ["bluetoothctl", "--", "info", bt_address]
    post_pipe = ["grep", "Connected"]
    result = Popen(args=pre_pipe, stdout=PIPE, text=True)
    result = Popen(args=post_pipe, stdin=result.stdout, stdout=PIPE, text=True)
    if result.returncode:
        return False
    elif result.communicate()[0].split()[1] != "yes":
        return False
    return True


def connect(bt_address) -> bool:
    protocol, port = audiosink(bt_address=bt_address)

    sock = BT.BluetoothSocket(proto=BT.L2CAP)
    sock.connect((bt_address, port))
    print(f"connect: {sock.get_l2cap_options()}")
    print(f"disconnect: {sock.close()}")

    return True


if __name__ == "__main__":
    print(__file__)

    devices = paired_devices()

    for name, address in devices.items():
        if isnearby(address):
            if isconnected(address):
                print(f"{name} is connected")
            else:
                print(f"{name} connect")
                connect(address)
