#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Create a configuration file for the JACK server."""

from json import dump


def jacks() -> None:
    """Create a configuration file for the JACK server for each sound device.

    :note: "config/jack.json"
    """

    settings = dict()
    jack_controls = [
        "jack_control stop",
        "jack_control exit",
        "jack_control ds alsa",
        "jack_control eps realtime True",
        "jack_control dps duplex True",
        "jack_control dps device hw:Headphones",
        "jack_control dps playback hw:Headphones",
        "jack_control dps capture hw:0",
        "jack_control dps rate 44100",
        "jack_control dps nperiods 2",
        "jack_control dps period 2048",
        "jack_control dps outchannels 2",
        "jack_control start",
    ]
    settings["hw:CARD=Headphones"] = {"jack_control": jack_controls}

    jack_controls = [
        "jack_control stop",
        "jack_control exit",
        "jack_control ds alsa",
        "jack_control eps realtime True",
        "jack_control dps duplex True",
        "jack_control dps device bluealsa:00:00:00:00:00:00",
        "jack_control dps playback bluealsa:00:00:00:00:00:00",
        "jack_control dps capture hw:0",
        "jack_control dps rate 48000",
        "jack_control dps nperiods 3",
        "jack_control dps period 1024",
        "jack_control dps outchannels 2",
        "jack_control start",
    ]
    settings["bluealsa:00:00:00:00:00:00"] = {"jack_control": jack_controls}

    jack_controls = [
        "jack_control stop",
        "jack_control exit",
        "jack_control ds alsa",
        "jack_control eps realtime True",
        "jack_control dps duplex True",
        "jack_control dps device hw:S",
        "jack_control dps playback hw:S",
        "jack_control dps capture hw:0",
        "jack_control dps rate 96000",
        "jack_control dps nperiods 3",
        "jack_control dps period 1024",
        "jack_control dps outchannels 2",
        "jack_control start",
    ]
    settings["hw:CARD=S"] = {"jack_control": jack_controls}

    with open(file="config/jack.json", mode="wt") as f:
        dump(obj=settings, fp=f, indent=4)


if __name__ == "__main__":
    print(__file__)
