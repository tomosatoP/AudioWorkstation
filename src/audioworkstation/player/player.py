#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functools import partial
from concurrent import futures
from typing import Optional
from pathlib import Path
from enum import IntEnum, auto

from kivy.logger import Logger
from kivy.properties import (
    ListProperty,
    NumericProperty,
    StringProperty,
    ObjectProperty,
)
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.event import EventDispatcher
from kivy.lang import Builder

from . import midifile as MF

Builder.load_file(str(Path(__file__).with_name("player.kv")))


class PLAYER_STATUS(IntEnum):
    STANDBY = auto()
    PLAYBACK = auto()
    PAUSE = auto()


class MidiTitleButton(ToggleButton, EventDispatcher):
    index = NumericProperty()
    total_tick = NumericProperty()
    filename = StringProperty()
    channels_preset = ListProperty()

    def __init__(self, **kwargs):
        super(MidiTitleButton, self).__init__(**kwargs)
        self.register_event_type("on_select")

    def on_select(self):
        pass

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            log = f"index: {self.index}" + ", "
            log += f"ticks: {self.total_tick}" + ", "
            log += f"title: {self.text}" + ", "
            log += f"filename: {self.filename}"
            Logger.debug("player: " + log)
            self.dispatch("on_select")
        return super().on_touch_down(touch)


class PlayerView(Screen):
    play_button = ObjectProperty(None)
    pause_button = ObjectProperty(None)
    ticks_slider = ObjectProperty(None)
    midifiles = ObjectProperty(None)
    channels = ObjectProperty(None)
    sound_set: list = list()
    percussion_sound_set: list = list()
    midi_player = MF.MidiPlayer()
    executor = futures.ThreadPoolExecutor()

    def __init__(self, **kwargs):
        super(PlayerView, self).__init__(**kwargs)

        self.sound_set, self.percussion_sound_set = MF.gm_sound_set_names()
        self.add_channelbuttons()

        extension = [".mid", ".MID"]
        mids = [i for i in Path().glob("mid/*.*") if i.suffix in extension]
        for mid in mids:
            Clock.schedule_once(partial(self.add_midititlebutton, mid))

    def get_ticks(self, dt: int) -> None:
        """Request number of ticks passed at intervals.

        :param int dt: interval time
        """
        self.ticks_slider.value = self.midi_player.tick

    def future_callback(self, future: futures.Future) -> None:
        """Process after playback is finished.

        :param futures.Future future: playback process
        """
        self.ev_ticks.cancel()
        self.midi_player.close()
        self.status(PLAYER_STATUS.STANDBY)
        self.play_button.text = "▶"
        self.play_button.state = "normal"
        Logger.info("player: End of playback")

    def sound(self, state: str) -> None:
        mtb = self.selected()
        if mtb is not None and state == "down":
            self.mute_channels()
            self.midi_player.pause_tick = self.ticks_slider.value
            future = self.executor.submit(self.midi_player.start, mtb.filename)
            future.add_done_callback(self.future_callback)
            self.status(PLAYER_STATUS.PLAYBACK)
            self.ev_ticks = Clock.schedule_interval(self.get_ticks, 0.5)
            Logger.info(f"player: Playback start {mtb.filename}, {mtb.total_tick}")
        elif mtb is not None and state == "normal":
            self.ev_ticks.cancel()
            self.midi_player.close()
            self.status(PLAYER_STATUS.STANDBY)
            Logger.info("player: Stop playback")

    def pause(self, state: str) -> None:
        if state == "normal":
            self.sound(state="down")
            self.status(PLAYER_STATUS.PLAYBACK)
        elif state == "down":
            self.midi_player.pause()
            self.status(PLAYER_STATUS.PAUSE)

    def sound_stop(self) -> None:
        self.sound("normal")

    @property
    def sound_volume(self) -> int:
        return self.midi_player.volume

    @sound_volume.setter
    def sound_volume(self, value: int) -> None:
        self.midi_player.volume = value

    def select(self, mtb: MidiTitleButton):
        self.set_slider(mtb)
        self.set_channels(mtb)
        self.status(PLAYER_STATUS.STANDBY)

    def set_slider(self, mtb: MidiTitleButton):
        self.ticks_slider.min = 0
        self.ticks_slider.max = mtb.total_tick
        self.ticks_slider.value = 10000

    def status(self, value: PLAYER_STATUS) -> None:
        if value == PLAYER_STATUS.STANDBY:
            self.play_button.text = "▶"
            self.play_button.disabled = False
            self.pause_button.disabled = True
            self.ticks_slider.disabled = False
            self.midifiles.disabled = False
            self.channels.disabled = False
        elif value == PLAYER_STATUS.PLAYBACK:
            self.play_button.text = "■"
            self.play_button.disabled = False
            self.pause_button.disabled = False
            self.ticks_slider.disabled = True
            self.midifiles.disabled = True
            self.channels.disabled = True
        elif value == PLAYER_STATUS.PAUSE:
            self.play_button.disabled = True
            self.pause_button.disabled = False
            self.ticks_slider.disabled = False
            self.midifiles.disabled = True
            self.channels.disabled = True

    def selected(self) -> Optional[MidiTitleButton]:
        for midititlebutton in self.midifiles.children:
            if midititlebutton.state == "down":
                return midititlebutton
        return None

    def add_midititlebutton(self, midifile: Path, dt: int) -> int:
        smf: dict = MF.info_midifile(midifile)
        index = len(self.midifiles.children)
        midititlebutton = MidiTitleButton(
            text=smf["title"],
            index=index,
            total_tick=smf["total_tick"],
            filename="mid/" + midifile.name,
            channels_preset=smf["channels_preset"],
        )
        midititlebutton.bind(on_select=self.select)
        self.midifiles.add_widget(midititlebutton)
        return index

    def mute_channels(self) -> str:
        channels = dict()
        chan_num: int = 0
        for chan in self.channels.children[::-1]:
            channels[str(chan_num)] = False if chan.state == "down" else True
            chan_num += 1
        return MF.mute_rules(**channels)

    def set_channels(self, mtb: MidiTitleButton) -> None:
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
                    channel.text = "-"

            channel.state = "down" if channel.text != "-" else "normal"

    def add_channelbuttons(self, num: int = 16) -> int:
        for i in range(num):
            self.channels.add_widget(widget=ToggleButton(text=f"楽器 {i:02}"))
        return len(self.channels.children)


if __name__ == "__main__":
    print(__file__)
