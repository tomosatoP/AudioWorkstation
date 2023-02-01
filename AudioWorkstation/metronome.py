#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pattern as PT

from concurrent import futures
from kivy.resources import resource_add_path
from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.properties import (BoundedNumericProperty, ObjectProperty)
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.uix.widget import Widget
from kivy.app import App
import sys
sys.path.append('../AudioWorkstation')


# To use japanese font in Kivy
resource_add_path('/usr/share/fonts/opentype/ipaexfont-gothic')
LabelBase.register(DEFAULT_FONT, 'ipaexg.ttf')

# To play the metronome pattern in a separate thread.


class MetronomeView(Widget):
    pSFS = PT.Pattern()
    executor = futures.ThreadPoolExecutor()

    bps_layout = ObjectProperty(None)
    bps = BoundedNumericProperty(
        120, min=60, max=240,
        errorhandler=lambda x: 240 if x > 240 else 60)

    def beat(self) -> str:
        return (list(filter(
            lambda x: x.state == 'down',
            ToggleButtonBehavior.get_widgets('BeatSelectButtons')))[0].text)

    def sound_on(self) -> None:
        self.disable_buttons(disable=True)
        self.executor.submit(
            self.pSFS.start, self.bps, self.beat().splitlines())

    def sound_off(self) -> None:
        self.disable_buttons(disable=False)
        self.pSFS.stop()

    def disable_buttons(self, disable: bool) -> None:
        self.bps_layout.disabled = disable
        for button in ToggleButtonBehavior.get_widgets('BeatSelectButtons'):
            button.disabled = disable


class Metronome(App):
    def build(self):
        return (MetronomeView())


if __name__ == '__main__':
    Metronome().run()