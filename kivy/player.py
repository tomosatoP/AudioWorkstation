#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('../AudioWorkstation')

from kivy.app import App
from kivy.clock import Clock
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
from functools import partial


class MidiTitleButton(ToggleButton):
    index = NumericProperty()
    total_tick = NumericProperty()
    filename = StringProperty()
    channels_preset = ListProperty()

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            print(f'{self.index}, {self.total_tick}, {self.text}, {self.filename}')
            app = App.get_running_app()
            app.root.set_presets_for_channels(self.index)
        return super().on_touch_down(touch)

class PlayerView(Widget):
    play_button = ObjectProperty(None)
    pause_button = ObjectProperty(None)
    midifiles = ObjectProperty(None)
    channels = ObjectProperty(None)
    sound_set = list()
    percussion_sound_set = list()
    midi_player = MidiPlayer()
    executor = futures.ThreadPoolExecutor()

    def __init__(self, **kwargs):
        super(PlayerView, self).__init__(**kwargs)

        self.sound_set, self.percussion_sound_set = gm_sound_set_names()
        self.add_channelbuttons()

        extension = ['.mid','.MID']
        list_midifile = [i for i in Path().glob('mid/*.*') if i.suffix in extension]
        for i in list_midifile:
            Clock.schedule_once(partial(self.clock_callback, i))

        #self.set_presets_for_channels(0)

    def clock_callback(self, midifile:Path, dt:int) -> int:
        return(self.add_midititlebutton(midifile))

    def future_callback(self, future:futures.Future) -> None:
        self.midi_player.close()
        if self.pause_button.state == 'normal':
            self.play_button.state = 'normal'


    def sound(self, state:str) -> None:
        if state == 'down':
            print(self.mute_channels())
            filename, total_tick = self.selected_midifile_info()
            print(f'{filename}, {total_tick}')
            future = self.executor.submit(self.midi_player.start, filename)
            future.add_done_callback(self.future_callback)
            self.disable_buttons(True)
        elif state == 'normal':
            self.midi_player.close()
            self.disable_buttons(False)
            print('sound off')

    def pause(self, state:str) -> None:
        if state == 'normal':
            self.sound(state='down')
            self.play_button.disabled = False
        elif state == 'down':
            self.midi_player.pause()
            self.play_button.disabled = True

    def disable_buttons(self, disable:bool) -> None:
        self.pause_button.disabled = not disable
        self.midifiles.disabled = disable
        self.channels.disabled = disable

    def selected_midifile_info(self) -> tuple:
        for i in self.midifiles.children:
            if i.state == 'down':
                return(i.filename, i.total_tick)

    def select_midifile_for_midifiles(self, num:int) -> None:
        length = len(self.midifiles.children)
        self.midifiles.children[(length - 1) - num].state = 'down'

    def add_midititlebutton(self, midifile:Path) -> int:
        smf = StandardMidiFile(midifile)
        index = len(self.midifiles.children)
        self.midifiles.add_widget(
            MidiTitleButton(
                text=smf.title(),
                index=index,
                total_tick=smf.total_tick(),
                filename='mid/' + midifile.name,
                channels_preset=smf.channels_preset()))
        return(index)

    def mute_channels(self) -> str:
        channels = dict()
        chan_num:int=0
        for chan in self.channels.children[::-1]:
            channels[str(chan_num)] = False if chan.state == 'down' else True
            chan_num += 1
        return(mute_rules(**channels))

    def set_presets_for_channels(self, num:int) -> None:
        midifile_button = self.midifiles.children[-(num + 1)]
        for chan in range(len(self.channels.children)):
            preset_num = midifile_button.channels_preset[chan]
            channel = self.channels.children[-(chan + 1)]
            
            if isinstance(preset_num, int):
                channel.text = self.percussion_sound_set[preset_num] \
                    if chan == 9 else self.sound_set[preset_num]
            else:
                channel.text = self.percussion_sound_set[0] \
                    if chan == 9 else '-'

            channel.state = 'down' if channel.text != '-' else 'normal'

    def add_channelbuttons(self, num:int=16) -> int:
        for i in range(num):
            self.channels.add_widget(widget=ToggleButton(text=f'楽器 {i:02}'))
        return(len(self.channels.children))

class Player(App):
    def build(self):
        pv = PlayerView()
        return(pv)

if __name__ == '__main__':
    Player().run()
