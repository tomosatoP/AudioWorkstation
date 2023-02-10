#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from src.audioworkstation.libs.audio import fluidsynth as FS
from src.audioworkstation.libs.items import standardmidifile as SMF
from pathlib import Path
from json import dump


class MidiPlayer():
    pause_tick: int = 0

    def __init__(self) -> None:
        kwargs = {
            'settings': 'config/settings.json',
            'soundfont': ['sf2/FluidR3_GM.sf2',
                          'sf2/SGM-V2.01.sf2',
                          'sf2/YDP-GrandPiano-20160804.sf2']
        }

        self._player = FS.MidiPlayer(**kwargs)

    def start(self, filename: str) -> str:
        self._player.gain = 0.5
        self._player.apply_rules('config/rule.mute_chan.json')
        self._player.start(midifile=filename, start_tick=self.pause_tick)
        return (f'{filename}')

    def close(self) -> None:
        self.pause_tick = 0
        self._player.close()

    def pause(self) -> None:
        self.pause_tick = self._player.stop()
        self._player.close()


def info_midifile(midifile: Path) -> dict:
    _smf = SMF.StandardMidiFile(midifile)
    items: dict = {}
    items['title'] = _smf.title()
    items['total_tick'] = _smf.total_tick()
    items['channels_preset'] = _smf.channels_preset()
    return (items)


def gm_sound_set_names() -> tuple:
    kwargs = {
        'settings': 'config/settings.json',
        'soundfont': ['sf2/FluidR3_GM.sf2']}
    synthesizer = FS.Synthesizer(**kwargs)

    names = list()
    pnames = list()
    for i in synthesizer.gm_sound_set(is_percussion=False)[0]:
        names += [i['name']]
    for i in synthesizer.gm_sound_set(is_percussion=True)[0]:
        pnames += [i['name']]
    return (names, pnames)


def mute_rules(**kwargs) -> str:
    '''
    {'0':True, '1':False, ..., '15':False}
        True: mute
        False: unmute
    '''
    rules = dict()
    filename = 'config/rule.mute_chan.json'

    for chan in list(kwargs):
        if kwargs[chan]:
            # NOTE: mute channel
            comment = 'NOTE: mute chan ' + chan
            rules[comment] = {
                'type': FS.FLUID_MIDI_ROUTER_RULE_TYPE.NOTE,
                'chan': None, 'param1': None, 'param2': None
            }
            rules[comment]['chan'] = {
                'min': int(chan), 'max': int(chan), 'mul': 1.0, 'add': 0
            }
            rules[comment]['param2'] = {
                'min': 0, 'max': 127, 'mul': 0.0, 'add': 0
            }
        else:
            # NOTE: without change
            comment = 'NOTE: unmute chan ' + chan
            rules[comment] = {
                'type': FS.FLUID_MIDI_ROUTER_RULE_TYPE.NOTE,
                'chan': None, 'param1': None, 'param2': None
            }
            rules[comment]['chan'] = {
                'min': int(chan), 'max': int(chan), 'mul': 1.0, 'add': 0
            }

    # CC: without change
    rules['CC'] = {
        'type': FS.FLUID_MIDI_ROUTER_RULE_TYPE.CC,
        'chan': None, 'param1': None, 'param2': None
    }
    # PROG_CHANGER: without change
    rules['PROG_CHANGER'] = {
        'type': FS.FLUID_MIDI_ROUTER_RULE_TYPE.PROG_CHANGER,
        'chan': None, 'param1': None, 'param2': None
    }
    # PITCH_BEND: without change
    rules['PITCH_BEND'] = {
        'type': FS.FLUID_MIDI_ROUTER_RULE_TYPE.PITCH_BEND,
        'chan': None, 'param1': None, 'param2': None
    }
    # CHANNEL_PRESSURE: without change
    rules['CHANNEL_PRESSURE'] = {
        'type': FS.FLUID_MIDI_ROUTER_RULE_TYPE.CHANNEL_PRESSURE,
        'chan': None, 'param1': None, 'param2': None
    }
    # KEY_PRESSURE: without change
    rules['KEY_PRESSURE'] = {
        'type': FS.FLUID_MIDI_ROUTER_RULE_TYPE.KEY_PRESSURE,
        'chan': None, 'param1': None, 'param2': None
    }

    with open(filename, 'w') as fw:
        dump(rules, fw, indent=4)

    return (filename)


if __name__ == '__main__':
    print('midi file')
