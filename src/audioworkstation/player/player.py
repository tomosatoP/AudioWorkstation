#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functools import partial
from concurrent import futures
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


class ChannelButton(ToggleButton, EventDispatcher):
    index = NumericProperty()


class MidiTitleButton(ToggleButton, EventDispatcher):
    filename = StringProperty()
    total_tick = NumericProperty()
    channels_preset = ListProperty()

    def __str__(self) -> str:
        result = f"ticks: {self.total_tick}" + ", "
        result += f"title: {self.text}" + ", "
        result += f"filename: {self.filename}"
        return result


class PlayerView(Screen):
    play_button = ObjectProperty(None)
    pause_button = ObjectProperty(None)
    ticks_slider = ObjectProperty(None)
    midifiles = ObjectProperty(None)
    channels = ObjectProperty(None)

    sound_set: list = list()
    percussion_sound_set: list = list()
    executor = futures.ThreadPoolExecutor()

    def __init__(self, **kwargs):
        super(PlayerView, self).__init__(**kwargs)

        self.sound_set, self.percussion_sound_set = MF.gm_sound_set_names()
        self.add_channelbuttons()

        extension = [".mid", ".MID"]
        mids = [i for i in Path().glob("mid/*.*") if i.suffix in extension]
        for mid in mids:
            Clock.schedule_once(partial(self.add_midititlebutton, mid))

        self.midi_player = MF.MidiPlayer()

    def sound_stop(self) -> None:
        self.playback("normal")
        self.status(PLAYER_STATUS.STANDBY)

    @property
    def sound_volume(self) -> int:
        return self.midi_player.volume

    @sound_volume.setter
    def sound_volume(self, value: int) -> None:
        self.midi_player.volume = value

    def playback(self, state: str) -> None:
        mtb: MidiTitleButton = list(
            filter(
                lambda x: x.state == "down",
                ToggleButton.get_widgets("MidiTitleButtons"),
            )
        )[0]

        if state == "down":
            self.mute_channels()
            self.midi_player.pause_tick = self.ticks_slider.value
            future = self.executor.submit(self.midi_player.start, mtb.filename)
            future.add_done_callback(self.cleanup_playback)
            self.status(PLAYER_STATUS.PLAYBACK)
            self.ev_ticks = Clock.schedule_interval(self.progress_ticks, 0.5)
            Logger.info(f"player: Playback {str(mtb)}")
        elif state == "normal":
            self.ev_ticks.cancel()
            self.midi_player.close()
            self.status(PLAYER_STATUS.STANDBY)
            Logger.info("player: Stop")

    def pause(self, state: str) -> None:
        if state == "normal":
            self.playback(state="down")
            self.status(PLAYER_STATUS.PLAYBACK)
        elif state == "down":
            self.midi_player.pause()
            self.status(PLAYER_STATUS.PAUSE)
            Logger.info("player: Pause")

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

    def progress_ticks(self, dt: int) -> None:
        """Request number of ticks passed at intervals.

        :param int dt: interval time
        """
        self.ticks_slider.value = self.midi_player.tick

    def cleanup_playback(self, future: futures.Future) -> None:
        """Process after playback is finished.

        :param futures.Future future: playback process
        """
        self.ev_ticks.cancel()
        self.midi_player.close()
        self.status(PLAYER_STATUS.STANDBY)
        self.play_button.state = "normal"
        Logger.info("player: End")

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
        for i in range(num):
            channelbutton = ChannelButton(text=f"楽器 {i:02}", index=i)
            self.channels.add_widget(widget=channelbutton)


if __name__ == "__main__":
    print(__file__)
