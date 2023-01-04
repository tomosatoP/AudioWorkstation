#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
from items.standardmidifile import *
from audio.fluidsynth import *

class MidiPlayer():

    def __init__(self) -> None:
        kwargs = {
            'settings': 'audio/settings.json',
            'soundfont': 'sf2/FluidR3_GM.sf2'}
        self._player = MidiPlayerFS(**kwargs)

    def start(self, filename:str) -> None:
        self._player.gain(30)
        self._player.play(filename)

    def stop(self) -> None:
        self._player.stop()

class SoundFont():

    def __init__(self) -> None:
        kwargs = {
            'settings': 'audio/settings.json',
            'soundfont': 'sf2/FluidR3_GM.sf2'}
        self._synthesizer = SynthesizerFS(**kwargs)

    def preset_names(self) -> list:
        names = list()
        for i in self._synthesizer.sfonts_preset[0]:
            names += [i['name']]
        return(names)
