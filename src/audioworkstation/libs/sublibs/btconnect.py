#!/usr/bin/env python3
"""PyBluez advanced example read-local-bdaddr.py

Read the local Bluetooth device address
"""

import bluetooth as BT
from json import load
from time import sleep


def connect(bt_address) -> bool:
    bt_services = BT.find_service(address=bt_address)
    if not bt_services:
        return False
    audio_sink = list(filter(lambda x: "110B" in x["service-classes"], bt_services))[0]
    # BT.AUDIO_SINK_CLASS = "110b": "protocol": "L2CAP", "port": 25
    if not audio_sink:
        return False

    sock = BT.BluetoothSocket(BT.L2CAP)
    print(f"connect: {sock.connect((bt_address, audio_sink['port']))}")
    print(sock.get_l2cap_options())
    sleep(10)
    print(f"disconnect: {sock.close()}")

    return True


if __name__ == "__main__":
    with open(file="config/address.json", mode="r") as fp:
        adds = load(fp)

    print("Searching...")
    print(f"devices: {BT.discover_devices()}")

    print(BT.lookup_name(address=adds["LinkBuds"]))
    connect(adds["LinkBuds"])
