#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functools import partial
from concurrent import futures
from typing import Optional
from pathlib import Path

from kivy.resources import resource_add_path
from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.logger import Logger
from kivy.properties import (
    ListProperty, NumericProperty, StringProperty, ObjectProperty)
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.app import App

from src.audioworkstation import midifile as MF


# To use japanese font in Kivy
resource_add_path('/usr/share/fonts/opentype/ipaexfont-gothic')
LabelBase.register(DEFAULT_FONT, 'ipaexg.ttf')


class MidiTitleButton(ToggleButton):
    index = NumericProperty()
    total_tick = NumericProperty()
    filename = StringProperty()
    channels_preset = ListProperty()

    def __init__(self, **kwargs):
        super(MidiTitleButton, self).__init__(**kwargs)
        self.register_event_type('on_select')

    def on_select(self):
        pass

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            log = f'index: {self.index}' + ', '
            log += f'ticks: {self.total_tick}' + ', '
            log += f'title: {self.text}' + ', '
            log += f'filename: {self.filename}'
            Logger.debug('select: ' + log)
            self.dispatch('on_select')
        return super().on_touch_down(touch)


class PlayerView(Widget):
    play_button = ObjectProperty(None)
    pause_button = ObjectProperty(None)
    midifiles = ObjectProperty(None)
    channels = ObjectProperty(None)
    sound_set = list()
    percussion_sound_set = list()
    midi_player = MF.MidiPlayer()
    executor = futures.ThreadPoolExecutor()

    def __init__(self, **kwargs):
        super(PlayerView, self).__init__(**kwargs)

        self.sound_set, self.percussion_sound_set = MF.gm_sound_set_names()
        self.add_channelbuttons()

        extension = ['.mid', '.MID']
        list_midifile = [i for i in Path().glob(
            'mid/*.*') if i.suffix in extension]
        for i in list_midifile:
            Clock.schedule_once(partial(self.clock_callback, i))

    def clock_callback(self, midifile: Path, dt: int) -> int:
        return (self.add_midititlebutton(midifile))

    def future_callback(self, future: futures.Future) -> None:
        self.midi_player.close()
        if self.pause_button.state == 'normal':
            self.play_button.state = 'normal'
        Logger.info('player: End of playback')

    def sound(self, state: str) -> None:
        if state == 'down':
            self.mute_channels()
            mtb = self.selected_midititlebutton()
            if mtb is not None:
                future = self.executor.submit(
                    self.midi_player.start, mtb.filename)
                future.add_done_callback(self.future_callback)
                self.disable_buttons(True)
                Logger.info(
                    f'player: Playback start {mtb.filename}, {mtb.total_tick}')
        elif state == 'normal':
            self.midi_player.close()
            self.disable_buttons(False)
            Logger.info('player: Stop playback')

    def pause(self, state: str) -> None:
        if state == 'normal':
            self.sound(state='down')
            self.play_button.disabled = False
        elif state == 'down':
            self.midi_player.pause()
            self.play_button.disabled = True

    def disable_buttons(self, disable: bool) -> None:
        self.pause_button.disabled = not disable
        self.midifiles.disabled = disable
        self.channels.disabled = disable

    def selected_midititlebutton(self) -> Optional[MidiTitleButton]:
        for midititlebutton in self.midifiles.children:
            if midititlebutton.state == 'down':
                return (midititlebutton)

    def add_midititlebutton(self, midifile: Path) -> int:
        smf: dict = MF.info_midifile(midifile)
        index = len(self.midifiles.children)
        midititlebutton = MidiTitleButton(
            text=smf['title'],
            index=index,
            total_tick=smf['total_tick'],
            filename='mid/' + midifile.name,
            channels_preset=smf['channels_preset'])
        midititlebutton.bind(on_select=self.set_presets_for_each_channel)
        self.midifiles.add_widget(midititlebutton)
        return (index)

    def mute_channels(self) -> str:
        channels = dict()
        chan_num: int = 0
        for chan in self.channels.children[::-1]:
            channels[str(chan_num)] = False if chan.state == 'down' else True
            chan_num += 1
        return (MF.mute_rules(**channels))

    def set_presets_for_each_channel(self, mtb: MidiTitleButton) -> None:
        for chan in range(len(self.channels.children)):
            preset_num = mtb.channels_preset[chan]
            channel = self.channels.children[-(chan + 1)]

            if isinstance(preset_num, int):
                if chan == 9:
                    channel.text = self.percussion_sound_set[preset_num]
                else:
                    channel.text = self.sound_set[preset_num]
            else:
                if chan == 9:
                    channel.text = self.percussion_sound_set[0]
                else:
                    channel.text = '-'

            channel.state = 'down' if channel.text != '-' else 'normal'

    def add_channelbuttons(self, num: int = 16) -> int:
        for i in range(num):
            self.channels.add_widget(widget=ToggleButton(text=f'楽器 {i:02}'))
        return (len(self.channels.children))


class Player(App):
    def build(self):
        pv = PlayerView()
        return (pv)


if __name__ == '__main__':
    Player().run()
