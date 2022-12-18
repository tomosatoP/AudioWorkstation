#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('../AudioWorkstation')
from libfluidsynth.fluidsynth import SequencerFS

from time import sleep
import threading

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.properties import (
    NumericProperty,
    BoundedNumericProperty,
    ObjectProperty,
)

from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.resources import resource_add_path
resource_add_path('/usr/share/fonts/opentype/ipaexfont-gothic')
LabelBase.register(DEFAULT_FONT, 'ipaexg.ttf')

class MetronomeSFs(SequencerFS):
    def __init__(self, *args) -> None:
        super().__init__(*args)

    def start(self, bps: float, beat: list) -> None:
        print(f'tempo: {bps}')
        print(f'beat: {beat}')
        self.set_bps(bps)
        self.noteOn(9, 34, 100)
        sleep(1)
        self.noteOn(9, 34, 100)
        sleep(1)
        self.noteOn(9, 34, 100)
        sleep(1)

class MetronomeView(Widget):
    bps = BoundedNumericProperty(
        120, min=60, max=240,
        errorhandler=lambda x: 240 if x > 240 else 60)

    def beat(self) -> str:
        return(list(filter(lambda x: x.state == 'down',
            ToggleButtonBehavior.get_widgets('BeatSelectButtons')))[0].text)

    def sound(self):
        thread = threading.Thread(target=self._sound_on())
        thread.start()

    def _sound_on(self):
        p = MetronomeSFs('sf2/FluidR3_GM.sf2')
        p.start(self.bps, self.beat().splitlines())


class Metronome(App):
    def build(self):
        return(MetronomeView())

if __name__ == '__main__':
    Metronome().run()