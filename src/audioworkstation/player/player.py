#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Midi Player"""

from functools import partial
from concurrent import futures
from pathlib import Path
from enum import IntEnum, auto
from time import sleep

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
    STANDBY = auto()  #: standby
    PLAYBACK = auto()  #: playback
    PAUSE = auto()  #: pause


class ChannelButton(ToggleButton, EventDispatcher):
    """ChannelButton _summary_"""

    #: NumericProerty:
    index = NumericProperty()


class MidiTitleButton(ToggleButton, EventDispatcher):
    """MidiTitleButton _summary_"""

    #: StringProperty: filename
    filename = StringProperty()
    #: NumericProperty: total ticks
    total_tick = NumericProperty()
    #: ListProperty: channel preset
    channels_preset = ListProperty()

    def __str__(self) -> str:
        result = f"title: {self.text}" + ", "
        result += f"filename: {self.filename}" + ", "
        result += f"ticks: {self.total_tick}"
        return result


class PlayerView(Screen):
    """PlayView"""

    #: ObjectProperty: button playback
    play_button = ObjectProperty(None)
    #: ObjectProperty: button pause
    pause_button = ObjectProperty(None)
    #: ObjectProperty: slider ticks
    ticks_slider = ObjectProperty(None)
    #: ObjectProperty: button group midifile
    midifiles = ObjectProperty(None)
    #: ObjectProperty: button group channel
    channels = ObjectProperty(None)

    sound_set: list = list()
    percussion_sound_set: list = list()
    executor = futures.ThreadPoolExecutor()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        Logger.debug("player: initializing...")

        self.sound_set, self.percussion_sound_set = MF.gm_sound_set_names()
        self.add_channelbuttons()

        extension = [".mid", ".MID"]
        mids = [i for i in Path().glob("mid/*.*") if i.suffix in extension]
        for mid in mids:
            Clock.schedule_once(partial(self.add_midititlebutton, mid))

        self.midi_player = MF.MidiPlayer()

    def unregister(self) -> None:
        """Processing when terminating a View."""
        self.midi_player.stop()

    def playback(self, state: str) -> None:
        """playback _summary_

        :param str state: _description_
        """
        mtb: MidiTitleButton = list(
            filter(
                lambda x: x.state == "down",
                ToggleButton.get_widgets("MidiTitleButtons"),
            )
        )[0]

        if state == "down":
            self.mute_channels()
            self.midi_player.pause_tick = int(self.ticks_slider.value)
            future = self.executor.submit(self.midi_player.start, mtb.filename)
            future.add_done_callback(self.cleanup_playback)
            self.status(PLAYER_STATUS.PLAYBACK)
            sleep(0.5)  # Wait for fsmp instance creation
            self.ev_ticks = Clock.schedule_interval(self.progress_ticks, 0.5)
            Logger.info(f"player: Playback {str(mtb)} - {self.midi_player.pause_tick}")
        elif state == "normal":
            self.ev_ticks.cancel()
            self.midi_player.stop()  # call cleanup_playback

    def pause(self, state: str) -> None:
        """pause _summary_

        :param str state: _description_
        """
        if state == "normal":
            self.playback("down")
        elif state == "down":
            self.ev_ticks.cancel()
            self.midi_player.stop()  # call cleanup_playback

    def cleanup_playback(self, future: futures.Future) -> None:
        """Process after playback is finished.

        :param futures.Future future: playback process
        """
        if self.pause_button.state == "normal":
            if self.play_button.state == "down":
                self.ev_ticks.cancel()
                self.midi_player.stop()
                self.play_button.state = "normal"
            self.status(PLAYER_STATUS.STANDBY)
            Logger.info(
                f"player: End {future.result()} - {int(self.ticks_slider.value)}"
            )
            self.ticks_slider.value = 0
        else:
            self.status(PLAYER_STATUS.PAUSE)
            Logger.info(
                f"player: Pause {future.result()} - {int(self.ticks_slider.value)}"
            )

    @property
    def volume(self) -> int:
        """int: volume"""
        return self.midi_player.volume

    @volume.setter
    def volume(self, value: int) -> None:
        self.midi_player.volume = value

    def status(self, value: PLAYER_STATUS) -> None:
        """status _summary_

        :param PLAYER_STATUS value: _description_
        """
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
            self.play_button.text = "■"
            self.play_button.disabled = True
            self.pause_button.disabled = False
            self.ticks_slider.disabled = False
            self.midifiles.disabled = True
            self.channels.disabled = True

    def progress_ticks(self, dt: int) -> None:
        """Request number of ticks passed at intervals.

        :param int dt: interval time
        """
        self.ticks_slider.value = self.midi_player.tick

    def select(self, mtb: MidiTitleButton):
        """Select the SMF corresponding to the MidiTitleButton

        :param MidiTitleButton mtb: pressed MidiTitleButton
        """
        self.status(PLAYER_STATUS.STANDBY)
        Logger.debug("player: " + str(mtb))
        self.ticks_slider.max = mtb.total_tick

        for cb in self.channels.children:
            preset_num = mtb.channels_preset[cb.index]

            if isinstance(preset_num, int):
                cb.state = "down"
                if cb.index == 9:
                    cb.text = self.percussion_sound_set[preset_num]
                else:
                    cb.text = self.sound_set[preset_num]
            else:
                if cb.index == 9:
                    cb.state = "down"
                    cb.text = self.percussion_sound_set[0]
                else:
                    cb.state = "normal"
                    cb.text = "-"

    def mute_channels(self) -> str:
        """Mutes channels set to "down".

        :return str: filename of rules
        """
        channels = dict()
        for cb in self.channels.children:
            channels[str(cb.index)] = False if cb.state == "down" else True
        return MF.mute_rules(**channels)

    def add_midititlebutton(self, midifile: Path, dt: int) -> None:
        """add_midititlebutton _summary_

        :param Path midifile: _description_
        :param int dt: _description_
        """
        smf: dict = MF.info_midifile(midifile)
        midititlebutton = MidiTitleButton(
            text=smf["title"],
            total_tick=smf["total_tick"],
            filename="mid/" + midifile.name,
            channels_preset=smf["channels_preset"],
        )
        midititlebutton.bind(on_press=self.select)
        self.midifiles.add_widget(midititlebutton)

    def add_channelbuttons(self, num: int = 16) -> None:
        """add_channelbuttons _summary_

        :param int num: _description_, defaults to 16
        """
        for i in range(num):
            channelbutton = ChannelButton(text=f"楽器 {i:02}", index=i)
            self.channels.add_widget(widget=channelbutton)


if __name__ == "__main__":
    print(__file__)
