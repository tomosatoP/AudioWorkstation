#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from items.standardmidifile import *
from audio.fluidsynth import *

class MidiPlayer():
    pause_tick:int=0

    def __init__(self) -> None:
        kwargs = {
            'settings': 'audio/settings.json',
            'soundfont': 'sf2/FluidR3_GM.sf2'}
        self._player = MidiPlayerFS(**kwargs)

    def start(self, filename:str) -> str:
        self._player.gain(0.5)
        self._player.change_rule('kivy/rule.mute_chan.json')
        self._player.start(midifile=filename, start_tick=self.pause_tick)
        return(f'{filename}')

    def close(self) -> None:
        self.pause_tick = 0
        self._player.close()

    def pause(self) -> None:
        self.pause_tick = self._player.stop()
        self._player.close()

def gm_sound_set_names() -> tuple:
    kwargs = {
        'settings': 'audio/settings.json',
        'soundfont': 'sf2/FluidR3_GM.sf2'}
    synthesizer = SynthesizerFS(**kwargs)

    names = list()
    pnames = list()
    for i in synthesizer.gm_sound_set(is_percussion=False)[0]:
        names += [i['name']]
    for i in synthesizer.gm_sound_set(is_percussion=True)[0]:
        pnames += [i['name']]
    return(names, pnames)

def mute_rules(**kwargs) -> str:
    '''
    {'0':True, '1':False, ..., '15':False}
        True: mute
        False: unmute
    '''
    rules = dict()
    filename = 'kivy/rule.mute_chan.json'

    for chan in list(kwargs):
        if kwargs[chan]:
            # NOTE: mute channel
            comment = 'NOTE: mute chan ' + chan
            rules[comment] = {'type': FLUID_MIDI_ROUTER_RULE_TYPE.NOTE, 'chan': None, 'param1': None, 'param2': None}
            rules[comment]['chan'] = {'min': int(chan), 'max': int(chan), 'mul':1.0, 'add':0}
            rules[comment]['param2'] = {'min': 0, 'max': 127, 'mul':0.0, 'add':0}
        else:
            # NOTE: without change
            comment = 'NOTE: unmute chan ' + chan
            rules[comment] = {'type': FLUID_MIDI_ROUTER_RULE_TYPE.NOTE, 'chan': None, 'param1': None, 'param2': None}
            rules[comment]['chan'] = {'min': int(chan), 'max': int(chan), 'mul':1.0, 'add':0}

    # CC: without change
    rules['CC'] = {'type': FLUID_MIDI_ROUTER_RULE_TYPE.CC, 'chan': None, 'param1': None, 'param2': None}
    # PROG_CHANGER: without change
    rules['PROG_CHANGER'] = {'type': FLUID_MIDI_ROUTER_RULE_TYPE.PROG_CHANGER, 'chan': None, 'param1': None, 'param2': None}
    # PITCH_BEND: without change
    rules['PITCH_BEND'] = {'type': FLUID_MIDI_ROUTER_RULE_TYPE.PITCH_BEND, 'chan': None, 'param1': None, 'param2': None}
    # CHANNEL_PRESSURE: without change
    rules['CHANNEL_PRESSURE'] = {'type': FLUID_MIDI_ROUTER_RULE_TYPE.CHANNEL_PRESSURE, 'chan': None, 'param1': None, 'param2': None}
    # KEY_PRESSURE: without change
    rules['KEY_PRESSURE'] = {'type': FLUID_MIDI_ROUTER_RULE_TYPE.KEY_PRESSURE, 'chan': None, 'param1': None, 'param2': None}

    with open(filename, 'w') as fw:
        dump(rules, fw, indent=4)

    return(filename)

if __name__ == '__main__':
    print('midi file')