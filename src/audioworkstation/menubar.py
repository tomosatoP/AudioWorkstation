#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functools import partial

import kivy  # noqa: F401
from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.uix.widget import Widget

from .metronome import metronome
from .player import player
from .libs.audio import amixer


class MainmenubarView(Widget):
    panel = ObjectProperty()
    mode = ObjectProperty()
    vol1 = ObjectProperty()
    vol2 = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.panel.add_widget(metronome.MetronomeView(name="m"))
        Clock.schedule_once(partial(self.panel.add_widget, player.PlayerView(name="p")))

        self.set_mode(self.mode, "メトローム")
        self.mode.bind(text=self.set_mode)

    def set_mode(self, widget, text) -> None:
        self.mode.values = "メトローム", "伴奏"
        self.vol1.children[2].text = "マスター音量"
        self.vol1.children[1].value = self.master_volume()
        if text == "メトローム":
            self.panel.current = "m"
            self.mode.text = "メトローム"
            self.vol2.children[2].text = "メトローム音量"
        elif text == "伴奏":
            self.panel.current = "p"
            self.mode.text = "伴奏"
            self.vol2.children[2].text = "伴奏音量"

    def master_volume(self, value=None) -> int:
        if value is None:
            result = amixer.volume()
        else:
            result = amixer.volume(f"{value}%,{value}%")
        return int(result.split(",")[0].strip("%"))


class MenubarApp(App):
    def build(self):
        self.title = "AudioWorkstation"
        return MainmenubarView()


if __name__ == "__main__":
    MenubarApp().run()
