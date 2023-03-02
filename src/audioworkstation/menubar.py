#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functools import partial

from kivy.app import App
from kivy.properties import ObjectProperty
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
        self.panel.add_widget(metronome.MetronomeView(name="metronome"))
        self.panel.add_widget(player.PlayerView(name="player"))

        self.set_mode(self.mode, "キーボード")
        self.vol1.label.text = "マスター音量"
        self.vol1.slider.bind(value=partial(self.master_volume))
        self.vol2.slider.bind(value=partial(self.mode_volume))
        self.mode.bind(text=self.set_mode)

    def set_mode(self, widget, text) -> None:
        self.panel.current_screen.sound_stop()

        if text == "キーボード":
            self.panel.current = "keyboard"
            self.vol2.label.text = "キーボード音量"
        elif text == "メトローム":
            self.panel.current = "metronome"
            self.vol2.label.text = "メトローム音量"
        elif text == "伴奏":
            self.panel.current = "player"
            self.vol2.label.text = "伴奏音量"

        self.vol2.slider.value = self.panel.current_screen.sound_volume

    def master_volume(self, widget, value):
        amixer.volume(f"{value}%,{value}%")

    def mode_volume(self, widget, value):
        self.panel.current_screen.sound_volume = value


class MenubarApp(App):
    def build(self):
        self.title = "AudioWorkstation"
        return MenubarView()


if __name__ == "__main__":
    MenubarApp().run()