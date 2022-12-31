#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('../AudioWorkstation')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.properties import (NumericProperty, StringProperty, ObjectProperty)

# To use japanese font in Kivy
from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.resources import resource_add_path
resource_add_path('/usr/share/fonts/opentype/ipaexfont-gothic')
LabelBase.register(DEFAULT_FONT, 'ipaexg.ttf')

from midifile import *

class MidiTitleButton(ToggleButton):
    index = NumericProperty()
    filename = StringProperty()

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            print(f'{self.text}, {self.index}, {self.filename}')
            app = App.get_running_app()
            app.root.set_presets_for_rule_list(self.index)
        return super().on_touch_down(touch)



class PlayerView(Widget):
    rules = ObjectProperty(None)
    playlist= ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super(PlayerView, self).__init__(**kwargs)

        self.midifiles = MidiFiles()
        self._add_play_list()
        self._add_rule_list()
        self.select_midi_for_play_list(0)
        self.set_presets_for_rule_list(0)

    def select_midi_for_play_list(self, num:int) -> None:
        length = len(self.playlist.children)
        self.playlist.children[(length - 1) - num].state = 'down'

    def set_presets_for_rule_list(self, num:int) -> None:
        for i in range(16):
            text = self.midifiles.presets(num, i)
            self.rules.children[15 - i].text = text
            self.rules.children[15 - i].state = 'down' if text != '-' else 'normal'

    def _add_play_list(self) -> int:        
        for i in range(self.midifiles.count()):
            text = self.midifiles.title(i)
            filename = self.midifiles.filename(i)
            self.playlist.add_widget(
                MidiTitleButton(text=text, index=i, filename=filename))
        return(i + 1)

    def _add_rule_list(self) -> int:
        for i in range(16):
            self.rules.add_widget(ToggleButton(text=str(i)))
        return(i + 1)

class Player(App):
    def build(self):
        return(PlayerView())

if __name__ == '__main__':
    Player().run()