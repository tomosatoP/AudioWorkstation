#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from kivy.app import App
from kivy.logger import Logger
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
        super().__init__(**kwargs)

        Logger.debug("Menubar: initializing...")

        self.panel.add_widget(keyboard.KeyboardView(name="keyboard"))
        self.panel.add_widget(metronome.MetronomeView(name="metronome"))
        self.panel.add_widget(player.PlayerView(name="player"))

        self.set_mode(self.mode, "キーボード")
        self.vol1.label.text = "マスター音量"
        self.vol1.slider.bind(value=self.master_volume)
        self.vol2.slider.bind(value=self.mode_volume)
        self.mode.bind(text=self.set_mode)

    def set_mode(self, widget, text) -> None:

        if text == "キーボード":
            self.panel.current = "keyboard"
            self.vol2.label.text = "キーボード音量"
        elif text == "メトローム":
            self.panel.current = "metronome"
            self.vol2.label.text = "メトローム音量"
        elif text == "伴奏":
            self.panel.current = "player"
            self.vol2.label.text = "伴奏音量"

        self.vol2.slider.value = self.panel.current_screen.volume

    def master_volume(self, widget, value):
        amixer.volume(f"{value}%,{value}%")

    def mode_volume(self, widget, value):
        self.panel.current_screen.volume = value


class MenubarApp(App):
    def build(self):
        self.title = "AudioWorkstation"
        self.MainView = MenubarView()
        return self.MainView

    def on_stop(self):
        print("mainview: on_stop")
        # self.MainView.panel.clear_widgets()

        return super().on_stop()


if __name__ == "__main__":
    MenubarApp().run()
