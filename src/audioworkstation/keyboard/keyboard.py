#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MIDI sequencer function for USB MIDI Keyboard"""

from pathlib import Path
from json import load

from kivy.logger import Logger  # noqa: F401
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.event import EventDispatcher
from kivy.uix.togglebutton import ToggleButton
from kivy.properties import (
    ObjectProperty,
    NumericProperty,
    DictProperty,
)
from kivy.lang import Builder

from . import mididriver as MD

Builder.load_file(str(Path(__file__).with_name("keyboard.kv")))


class GMSoundSetButton(ToggleButton, EventDispatcher):
    """GMSoundSetButton is placed on GM Sound Set layout."""

    #: NumericProperty: GM Sound Set program(preset) number
    preset_num = NumericProperty()


class GMSoundSetGroupButton(ToggleButton, EventDispatcher):
    """GMSoundSetGroupButton is placed on the GM Sound Set Gourp layout widget."""

    #: DictProperty: GM Sound Set Gourp program(preset) numbers {"Start":int, "End":int}
    presets = DictProperty()


class KeyboardView(Screen):
    """KeyboardView places GM Sound Set and GM Sound Set Group layout widget."""

    #: ObjectProperty: Layout for GM Sound Set Group
    gmssg = ObjectProperty()
    #: ObjectProperty: Layout for GM Sound Set
    gmss = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        Logger.debug("keyboard: initializing...")

        self.msm = MD.MidiSoundModule()
        self.msm.programchange(0)
        Clock.schedule_once(lambda dt: self.msm.sounding())

        with open(file="config/gmsoundsetgroping.json", mode="r") as fp:
            gmssg_json = load(fp)

        for name, presets in gmssg_json.items():
            self.add_gmssg_button(name, presets)

        self.add_gmss_buttons()

    def unregister(self) -> None:
        """Processing when terminating a View."""
        pass

    def select_gmss(self, gmss_button: GMSoundSetButton) -> None:
        """Select program(preset) number assigned to the button.

        :param GMSoundSetButton gmss_button: selected button
        """
        Logger.debug(f"keyboard: program change {gmss_button.preset_num}")
        self.msm.programchange(gmss_button.preset_num)
        Clock.schedule_once(lambda dt: self.msm.sounding())

    def select_gmssg(self, gmssg_button: GMSoundSetGroupButton) -> None:
        """Select GM Sound Set Group assigned to the button.

        :param GMSoundSetGroupButton gmssg_button: selected button
        """
        presets_num: list = list(
            reversed(
                range(gmssg_button.presets["Start"], gmssg_button.presets["End"] + 1)
            )
        )

        for i in range(8):
            self.gmss.children[i].text = self.msm.preset_name(presets_num[i])
            self.gmss.children[i].preset_num = presets_num[i]

    def add_gmss_buttons(self) -> None:
        """Add GMSoundSetButtons that has not been assigned a program(preset) number."""
        for i in range(8):
            button = GMSoundSetButton(text=f"楽器 {i}", preset_num=0)
            button.bind(on_press=self.select_gmss)
            self.gmss.add_widget(button)

    def add_gmssg_button(self, name: str, presets: dict) -> None:
        """Add GMSoundSetGroupButton

        :param str name: button text
        :param dict presets: GM Sound Set Group program(preset) numbers
        """
        button = GMSoundSetGroupButton(text=name, presets=presets)
        button.bind(on_press=self.select_gmssg)
        self.gmssg.add_widget(button)

    @property
    def volume(self) -> int:
        """int: volume"""
        return self.msm.volume

    @volume.setter
    def volume(self, value: int) -> None:
        self.msm.volume = value


if __name__ == "__main__":
    print(__file__)
