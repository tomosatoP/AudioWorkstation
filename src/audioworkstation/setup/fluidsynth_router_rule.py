#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Create a 'json file' of rule descriptions for class MidiRouter.

The rules apply even when they are duplicated, and the results are terrible.

MIDI note rule.
---------------
    type: FLUID_MIDI_ROUTER_RULE_TYPE.NOTE
        +-------+---------+--------+
        |chan   |param1   |param2  |
        +=======+=========+========+
        |channel|key(note)|velocity|
        +-------+---------+--------+
        |0..15  |0..127   |0..127  |
        +-------+---------+--------+

MIDI controller rule.
---------------------
Only compatible with the GM1 system.
    type: FLUID_MIDI_ROUTER_RULE_TYPE.CC
        modulation
            +-------+----------+------+
            |chan   |param1    |param2|
            +=======+==========+======+
            |channel|modulation|value |
            +-------+----------+------+
            |0..15  |1         |0..127|
            +-------+----------+------+
        volume
            +-------+------+------+
            |chan   |param1|param2|
            +=======+======+======+
            |channel|volume|value |
            +-------+------+------+
            |0..15  |7     |0..127|
            +-------+------+------+
        pan
            +-------+------+----------------------------+
            |chan   |param1|param2                      |
            +=======+======+============================+
            |channel|pan   |value                       |
            +-------+------+----------------------------+
            |0..15  |10    |Right:0..Center:64..Left:127|
            +-------+------+----------------------------+
        expression
            +-------+----------+------+
            |chan   |param1    |param2|
            +=======+==========+======+
            |channel|expression|value |
            +-------+----------+------+
            |0..15  |11        |0..127|
            +-------+----------+------+
        sustaion
            +-------+--------+----------------------------------+
            |chan   |param1  |param2                            |
            +=======+========+==================================+
            |channel|sustaion|value                             |
            +-------+--------+----------------------------------+
            |0..15  |64      |on:32(0b*1*****), off:0(0b*0*****)|
            +-------+--------+----------------------------------+

MIDI program change rule.
-------------------------
    type: FLUID_MIDI_ROUTER_RULE_TYPE.PROG_CHANGER
        +-------+----------------------+--------+
        |chan   |param1                |param2  |
        +=======+======================+========+
        |channel|program(preset) number|not used|
        +-------+----------------------+--------+
        |0..15  |0..127                |not used|
        +-------+----------------------+--------+

MIDI pitch bend rule.
---------------------
    type: FLUID_MIDI_ROUTER_RULE_TYPE.PITCH_BEND
        +-------+------+------+
        |chan   |param1|param2|
        +=======+======+======+
        |channel|LSB   |MSB   |
        +-------+------+------+
        |0..15  |0..127|0..127|
        +-------+------+------+

        +------+-----+--------------+--------------+
        |      |     |LSB           |MSB           |
        +======+=====+==============+==============+
        |min   |    0|  0(0b0000000)|  0(0b0000000)|
        +------+-----+--------------+--------------+
        |center| 8192|  0(0b0000000)| 64(0b1000000)|
        +------+-----+--------------+--------------+
        |max   |16383|127(0b1111111)|127(0b1111111)|
        +------+-----+--------------+--------------+

MIDI channel pressure (Aftertouch) rule.
----------------------------------------
    type: FLUID_MIDI_ROUTER_RULE_TYPE.CHANNEL_PRESSURE
        +-------+--------+--------+
        |chan   |param1  |param2  |
        +=======+========+========+
        |channel|pressure|not used|
        +-------+--------+--------+
        |0..15  |0..127  |not used|
        +-------+--------+--------+

MIDI key pressure (Aftertouch) rule.
------------------------------------
Not supported in GM1 system
    type: FLUID_MIDI_ROUTER_RULE_TYPE.KEY_PRESSURE
        +-------+---------+--------+
        |chan   |param1   |param2  |
        +=======+=========+========+
        |channel|key(note)|pressure|
        +-------+---------+--------+
        |0..15  |0..127   |0..127  |
        +-------+---------+--------+

:note:
typedef struct _fluid_midi_router_rule_t => fluid_midi_router_rule_t
    default is [min=0, max=999999, mul=1.0, add=0]

:reference:
https://github.com/FluidSynth/fluidsynth/blob/master/src/midi/fluid_midi_router.c
"""

from ..libs.audio import fluidsynth as FS
from json import dump


def router_rule_example() -> bool:
    """This is an example of creating mute channel 0

    :note: "example/rule.mute_chan_0.json".
    :var dict rules: {"name": {"type":"", "chan":"", "param1":"", "param2":""}}
    :return: True on success, otherwise False.
    """

    print("Create example file 'example/rule.mute_chan_0.json'...")

    rules: dict = dict()

    # NOTE: mute channel 0
    rules["NOTE: mute chan 0"] = {
        "type": FS.FLUID_MIDI_ROUTER_RULE_TYPE.NOTE,
        "chan": None,
        "param1": None,
        "param2": None,
    }
    rules["NOTE: mute chan 0"]["chan"] = {"min": 0, "max": 0, "mul": 1.0, "add": 0}
    rules["NOTE: mute chan 0"]["param2"] = {"min": 0, "max": 127, "mul": 0.0, "add": 0}

    # NOTE: without change, channel 1-15
    rules["NOTE: unmute chan 1-15"] = {
        "type": FS.FLUID_MIDI_ROUTER_RULE_TYPE.NOTE,
        "chan": None,
        "param1": None,
        "param2": None,
    }
    rules["NOTE: unmute chan 1-15"]["chan"] = {
        "min": 1,
        "max": 15,
        "mul": 1.0,
        "add": 0,
    }

    # CC: without change
    rules["CC"] = {
        "type": FS.FLUID_MIDI_ROUTER_RULE_TYPE.CC,
        "chan": None,
        "param1": None,
        "param2": None,
    }

    # PROG_CHANGER: without change
    rules["PROG_CHANGER"] = {
        "type": FS.FLUID_MIDI_ROUTER_RULE_TYPE.PROG_CHANGER,
        "chan": None,
        "param1": None,
        "param2": None,
    }

    # PITCH_BEND: without change
    rules["PITCH_BEND"] = {
        "type": FS.FLUID_MIDI_ROUTER_RULE_TYPE.PITCH_BEND,
        "chan": None,
        "param1": None,
        "param2": None,
    }

    # CHANNEL_PRESSURE: without change
    rules["CHANNEL_PRESSURE"] = {
        "type": FS.FLUID_MIDI_ROUTER_RULE_TYPE.CHANNEL_PRESSURE,
        "chan": None,
        "param1": None,
        "param2": None,
    }

    # KEY_PRESSURE: without change
    rules["KEY_PRESSURE"] = {
        "type": FS.FLUID_MIDI_ROUTER_RULE_TYPE.KEY_PRESSURE,
        "chan": None,
        "param1": None,
        "param2": None,
    }

    with open("example/rule.mute_chan_0.json", "w") as fw:
        dump(rules, fw, indent=4)

    return True


if __name__ == "__main__":
    print(__file__)
