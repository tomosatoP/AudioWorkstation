#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
from items.standardmidifile import *
from audio.fluidsynth import *

class MidiFiles():
    _filenames = list()
    _titles = list()
    _channels_preset = list()
    _sfonts_presets = list()

    def __init__(self) -> None:
        extension = ['.mid','.MID']
        list_midifile = [i for i in Path('mid').glob('*.*') if i.suffix in extension]
        for i in list_midifile:
            self._filenames += [i.name]
            midifile = StandardMidiFile(i.read_bytes())
            self._titles += [midifile.title()]
            self._channels_preset += [midifile.channels_preset()]
        
        kwargs = {
            'settings': 'audio/settings.json',
            'soundfont': 'sf2/FluidR3_GM.sf2'}
            
        self._midi_player = MidiPlayerFS(**kwargs)
        self._sfonts_presets = self._midi_player.sfonts_preset()

    def play(self, num:int):

        pass
        
    def pause(self):

        pass


    def filename(self, num:int) -> str:
        ''' MIDI file name of the specified number '''
        return(self._filenames[num])

    def presets(self, num:int, chan:int) -> str:
        '''
        Preset name of the specified channel in the MIDI file of the specified number
        '''
        preset_num = self._channels_preset[num][chan]
        if preset_num:
            return(self._sfonts_presets[0][preset_num]['name'])
        elif chan == 9:
            return('(drum)')
        else:
            return('-')

    def title(self, num:int) -> str:
        return(self._titles[num])

    def count(self) -> int:
        return(len(self._filenames))


if __name__ == '__main__':
    print('playmidifile')