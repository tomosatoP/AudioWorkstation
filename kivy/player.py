#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('../AudioWorkstation')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.togglebutton import ToggleButton
from kivy.properties import (ListProperty, NumericProperty, StringProperty, ObjectProperty)

# To use japanese font in Kivy
from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.resources import resource_add_path
resource_add_path('/usr/share/fonts/opentype/ipaexfont-gothic')
LabelBase.register(DEFAULT_FONT, 'ipaexg.ttf')

from concurrent import futures
from midifile import *

class MidiTitleButton(ToggleButton):
    index = NumericProperty()
    filename = StringProperty()
    channels_preset = ListProperty()

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            print(f'{self.text}, {self.index}, {self.filename}')
            app = App.get_running_app()
            app.root.set_presets_for_rule_list(self.index)
        return super().on_touch_down(touch)

class PlayerView(Widget):
    rules = ObjectProperty(None)
    playlist= ObjectProperty(None)
    sfont_presets_name = list()
    midi_player = MidiPlayer()
    executor = futures.ThreadPoolExecutor()
    
    def open_list_and_rules(self) -> None:
        ''' todo: MIDIファイル情報取得の待ち時間を工夫 '''
        extension = ['.mid','.MID']
        list_midifile = [i for i in Path().glob('mid/*.*') if i.suffix in extension]
        for i in list_midifile:
            self._add_play_list(i)
        self._add_rule_list()
        self.select_midi_for_play_list(0)
        self.set_presets_for_rule_list(0)

    def sound_on(self) -> None:
        self._disable_buttons(True)
        self.executor.submit(
            self.midi_player.start, self._selected_midi_filename())
        print('sound on')

    def sound_off(self) -> None:
        self._disable_buttons(False)
        self.midi_player.stop()
        print('sound off')

    def select_midi_for_play_list(self, num:int) -> None:
        length = len(self.playlist.children)
        self.playlist.children[(length - 1) - num].state = 'down'

    def set_presets_for_rule_list(self, num:int) -> None:
        for i in range(16):
            preset_num = self.playlist.children[23 - num].channels_preset[i]
            ''' todo: 全曲数をちゃんと取得する '''
            text = str(preset_num)
            self.rules.children[15 - i].text = text
            self.rules.children[15 - i].state = 'down' if text != '-' else 'normal'

    def _disable_buttons(self, disable:bool) -> None:
        self.playlist.disabled = disable
        self.rules.disabled = disable

    def _selected_midi_filename(self) -> str:
        for i in self.playlist.children:
            if i.state == 'down':
                return(i.filename)

    def _add_play_list(self, midifile:Path) -> int:
        smf = StandardMidiFile(midifile)
        index = len(self.playlist.children)
        self.playlist.add_widget(
            MidiTitleButton(
                text=smf.title(),
                index=index,
                filename='mid/' + midifile.name,
                channels_preset=smf.channels_preset()))
        return(index)

    def _add_rule_list(self) -> int:
        for i in range(16):
            self.rules.add_widget(ToggleButton(text=f'channel {i}'))
        return(i + 1)

class Player(App):
    def build(self):
        p = PlayerView()
        p.open_list_and_rules()
        return(p)

if __name__ == '__main__':
    Player().run()