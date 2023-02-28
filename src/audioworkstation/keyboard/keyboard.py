#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
from json import load

import kivy  # noqa: F401
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
    preset_num = NumericProperty()

    def __init__(self, **kwargs):
        super(GMSoundSetButton, self).__init__(**kwargs)
        self.register_event_type("on_select")

    def on_select(self):
        pass

    def on_state(self, widget, value):
        if value == "down":
            self.dispatch("on_select")


class GMSoundSetGroupButton(ToggleButton, EventDispatcher):
    presets = DictProperty()

    def __init__(self, **kwargs):
        super(GMSoundSetGroupButton, self).__init__(**kwargs)
        self.register_event_type("on_select")

    def on_select(self):
        pass

    def on_state(self, widget, value):
        if value == "down":
            self.dispatch("on_select")


class KeyboardView(Screen):
    gmssg = ObjectProperty()
    gmss = ObjectProperty()

    def __init__(self, **kwargs):
        super(KeyboardView, self).__init__(**kwargs)

        self.msm = MD.MidiSoundModule()
        self.msm.programchange(0)
        Clock.schedule_once(lambda dt: self.msm.sounding())

        with open(file="config/gmsoundsetgroping.json", mode="r") as fp:
            gmssg_json = load(fp)

        for name, presets in gmssg_json.items():
            self.add_gmssg_button(name, presets)

        self.add_gmss_buttons()

    def select_gmss(self, gmss_button: GMSoundSetButton):
        self.msm.programchange(gmss_button.preset_num)
        Clock.schedule_once(lambda dt: self.msm.sounding())

    def select_gmssg(self, gmssg_button: GMSoundSetGroupButton):
        presets_num: list = list(
            range(gmssg_button.presets["End"], gmssg_button.presets["Start"] - 1, -1)
        )

        for i in range(8):
            self.gmss.children[i].text = self.msm.preset_name(presets_num[i])
            self.gmss.children[i].preset_num = presets_num[i]

    def add_gmss_buttons(self):
        for i in range(8):
            button = GMSoundSetButton(text=f"楽器 {i}", preset_num=0)
            button.bind(on_select=self.select_gmss)
            self.gmss.add_widget(button)

    def add_gmssg_button(self, name: str, presets: dict) -> None:
        button = GMSoundSetGroupButton(text=name, presets=presets)
        button.bind(on_select=self.select_gmssg)
        self.gmssg.add_widget(button)

    def sound_volume(self, value: int) -> None:
        self.msm.volume = value


if __name__ == "__main__":
    print(__file__)
