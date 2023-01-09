#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('../AudioWorkstation')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.togglebutton import ToggleButton
from kivy.properties import (
    ListProperty, NumericProperty, StringProperty, ObjectProperty)

# To use japanese font in Kivy
from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.resources import resource_add_path
resource_add_path('/usr/share/fonts/opentype/ipaexfont-gothic')
LabelBase.register(DEFAULT_FONT, 'ipaexg.ttf')

from midifile import *
from concurrent import futures


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
    sfont_presets_pname = list()
    midi_player = MidiPlayer()
    executor = futures.ThreadPoolExecutor()
    
    def open_list_and_rules(self) -> None:
        ''' todo: MIDIファイル情報取得の待ち時間に工夫 '''
        extension = ['.mid','.MID']
        list_midifile = [i for i in Path().glob('mid/*.*') if i.suffix in extension]
        for i in list_midifile:
            self._add_play_list(i)

        self.sfont_presets_name = sfont_presets_name()
        self.sfont_presets_pname = sfont_presets_name(is_percussion=True)
        self._add_rule_list()
        self.select_midi_for_play_list(0)
        self.set_presets_for_rule_list(0)

    def sound_on(self) -> None:
        print(self._mute_rules())
        future = self.executor.submit(
            self.midi_player.start, self._selected_midi_filename())
        future.add_done_callback(self.eof_callback)
        self._disable_buttons(True)

    def pause(self):
        self.midi_player.pause()

    def restart(self):
        self.midi_player.restart()

    def eof_callback(self, future):
        self.sound_off()

    def sound_off(self) -> None:
        self.midi_player.stop()
        self._disable_buttons(False)
        print('sound off')

    def select_midi_for_play_list(self, num:int) -> None:
        length = len(self.playlist.children)
        self.playlist.children[(length - 1) - num].state = 'down'

    def set_presets_for_rule_list(self, num:int) -> None:
        total = len(self.playlist.children)
        for i in range(16):
            preset_num = \
                self.playlist.children[(total - 1) - num].channels_preset[i]
            
            if all([i == 9, isinstance(preset_num, int)]):
                text = self.sfont_presets_pname[preset_num]
            elif i == 9:
                text = self.sfont_presets_pname[0]
            else:
                text = self.sfont_presets_name[preset_num] \
                    if isinstance(preset_num, int) else '-'

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

    def _mute_rules(self) -> str:
        mute_ruless = dict()
        for i in range(len(self.rules.children)):
            mute_ruless[str(i)] = \
                False if self.rules.children[15 - i].state == 'down' else True
        return(mute_rules(**mute_ruless))

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
