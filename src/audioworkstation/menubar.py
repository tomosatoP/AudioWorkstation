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
from .keyboard import keyboard
from .libs.audio import amixer


class MenubarView(Widget):
    panel = ObjectProperty()
    mode = ObjectProperty()
    vol1 = ObjectProperty()
    vol2 = ObjectProperty()

    def __init__(self, **kwargs):
        super(MenubarView, self).__init__(**kwargs)

        self.panel.add_widget(keyboard.KeyboardView(name="keyboard"))
        Clock.schedule_once(
            partial(self.panel.add_widget, metronome.MetronomeView(name="metronome"))
        )
        Clock.schedule_once(
            partial(self.panel.add_widget, player.PlayerView(name="player"))
        )

        self.set_mode(self.mode, "キーボード")
        self.mode.bind(text=self.set_mode)

    def set_mode(self, widget, text) -> None:
        self.mode.values = "キーボード", "メトローム", "伴奏"
        self.vol1.label.text = "マスター音量"
        self.vol1.slider.value = self.master_volume()
        if text == "キーボード":
            self.panel.current = "keyboard"
            self.mode.text = "キーボード"
            self.vol2.label.text = "キーボード音量"
            self.vol2.slider.value = self.panel.current_screen.sound_volume
        elif text == "メトローム":
            self.panel.current = "metronome"
            self.mode.text = "メトローム"
            self.vol2.label.text = "メトローム音量"
        elif text == "伴奏":
            self.panel.current = "player"
            self.mode.text = "伴奏"
            self.vol2.label.text = "伴奏音量"

    def master_volume(self, value=None) -> int:
        if value is None:
            result = amixer.volume()
        else:
            result = amixer.volume(f"{value}%,{value}%")
        return int(result.split(",")[0].strip("%"))


class MenubarApp(App):
    def build(self):
        self.title = "AudioWorkstation"
        return MenubarView()


if __name__ == "__main__":
    MenubarApp().run()
