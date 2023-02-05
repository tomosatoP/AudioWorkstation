#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import fluidsynth as FS
from json import dump

'''Create a 'json file' of rule descriptions for class MidiRouter.

This is an example of creating mute channel 0
--------------------
[NOTE] -Note-
chan: channel 0-15
param1: key(note) 0-127
param2: velocity 0-127

[CC] -Control Change-
chan: channel 0-15
param1: controller number
param2: value
 param1             - param2
   1: modulation    - 0-127
   7: volume        - 0-127
  10: pan           - Right:0-Center:64-Left:127
  11: expression    - 0-127
  64: sustain       - on:32(0b*1*****), off:0(0b*0*****)
(memo) Only compatible with the GM1 system.

[PROG_CHANGER] -Program Change-
chan: channel 0-15
param1: program(preset) number 0-127
param2: -

[PITCH_BEND] -Pitch Bend Change-
chan: channel 0-15
param1: LSB 0-127
param2: MSB 0-127
 min:       0 -> LSB=0b0000000(0), MSB=0b0000000(0)
 center: 8192 -> LSB=0b0000000(0), MSB=0b1000000(64)
 max:   16383 -> LSB=0b1111111(127), MSB=0b1111111(127)

[CHANNEL_PRESSURE] -Channel Pressure (Aftertouch)-
chan: channel 0-15
param1: pressure 0-127
param2: -

[KEY_PRESSURE] -Polyphonic Key Pressure (Aftertouch)-
chan: channel 0-15
param1: key(note) 0-127
param2: pressure 0-127
(memo) Not supported in GM1 system

typedef struct _fluid_midi_router_rule_t => fluid_midi_router_rule_t
    default is [min=0, max=999999, mul=1.0, add=0]
https://github.com/FluidSynth/fluidsynth/blob/master/src/midi/fluid_midi_router.c
'''

# test router rule


def verify_rule() -> bool:
    '''The rules apply even when they are duplicated,
    and the results are terrible.
    '''
    rules = dict()

    # NOTE: mute channel 0
    rules['NOTE: mute chan 0'] = {
        'type': FS.FLUID_MIDI_ROUTER_RULE_TYPE.NOTE,
        'chan': None, 'param1': None, 'param2': None}
    rules['NOTE: mute chan 0']['chan'] = {
        'min': 0, 'max': 0, 'mul': 1.0, 'add': 0}
    rules['NOTE: mute chan 0']['param2'] = {
        'min': 0, 'max': 127, 'mul': 0.0, 'add': 0}

    # NOTE: without change, channel 1-15
    rules['NOTE: unmute chan 1-15'] = {
        'type': FS.FLUID_MIDI_ROUTER_RULE_TYPE.NOTE,
        'chan': None, 'param1': None, 'param2': None}
    rules['NOTE: unmute chan 1-15']['chan'] = {
        'min': 1, 'max': 15, 'mul': 1.0, 'add': 0}

    # CC: without change
    rules['CC'] = {
        'type': FS.FLUID_MIDI_ROUTER_RULE_TYPE.CC,
        'chan': None, 'param1': None, 'param2': None}

    # PROG_CHANGER: without change
    rules['PROG_CHANGER'] = {
        'type': FS.FLUID_MIDI_ROUTER_RULE_TYPE.PROG_CHANGER,
        'chan': None, 'param1': None, 'param2': None}

    # PITCH_BEND: without change
    rules['PITCH_BEND'] = {
        'type': FS.FLUID_MIDI_ROUTER_RULE_TYPE.PITCH_BEND,
        'chan': None, 'param1': None, 'param2': None}

    # CHANNEL_PRESSURE: without change
    rules['CHANNEL_PRESSURE'] = {
        'type': FS.FLUID_MIDI_ROUTER_RULE_TYPE.CHANNEL_PRESSURE,
        'chan': None, 'param1': None, 'param2': None}

    # KEY_PRESSURE: without change
    rules['KEY_PRESSURE'] = {
        'type': FS.FLUID_MIDI_ROUTER_RULE_TYPE.KEY_PRESSURE,
        'chan': None, 'param1': None, 'param2': None}

    with open('config/rule.mute_chan_0.json', 'w') as fw:
        dump(rules, fw, indent=4)

    return (True)


if __name__ == '__main__':
    verify_rule()
