#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""menu bar

#. Switching Child Screens [Keyboard, Metronome, MIDI Player]
#. Control volumes [Master & Child Screen]
#. Exit this application
"""
from kivy.app import App
from kivy.logger import Logger
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget

from .metronome import metronome
from .player import player
from .keyboard import keyboard
from .libs.audio import asound


class MenubarView(Widget):
    """class MenubarView

    :var ObjectProperty panel: child screens
    :var ObjectProperty mode: spinner
    :var ObjectProperty vol1: master volume
    :var ObjectProperty vol2: child screens volume
    """

    panel = ObjectProperty()
    mode = ObjectProperty()
    vol1 = ObjectProperty()
    vol2 = ObjectProperty()

    def __init__(self, **kwargs):
        """Initialize Menubar View"""
        super().__init__(**kwargs)

        self.mixer = asound.mixer_device()
        Logger.debug("Menubar: initializing...")
        self.panel.add_widget(keyboard.KeyboardView(name="keyboard"))
        self.panel.add_widget(metronome.MetronomeView(name="metronome"))
        self.panel.add_widget(player.PlayerView(name="player"))

        self.set_mode(self.mode, "キーボード")
        self.vol1.label.text = "マスター音量"
        self.vol1.slider.bind(value=self.master_volume)
        self.vol2.slider.bind(value=self.mode_volume)
        self.mode.bind(text=self.set_mode)

    def set_mode(self, widget: Widget, text: str) -> None:
        """Set child screens mode.

        :param Widget widget: mode
        :param str text: mode text ["キーボード", "メトロノーム", "伴奏"]
        """
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

    def master_volume(self, widget: Widget, value: int) -> None:
        """Control master volume.

        :param Widget widget: vol1.slider
        :param int value: value[%] to be set
        """
        asound.set_volume(self.mixer[2], self.mixer[3], value)

    def mode_volume(self, widget: Widget, value: int) -> None:
        """Control child screens volume.

        :param Widget widget: vol2.slider
        :param int value: value[%] to be set
        """
        self.panel.current_screen.volume = value


class MenubarApp(App):
    """class MenubarApp"""

    def build(self):
        self.title = "AudioWorkstation"
        return MenubarView()


if __name__ == "__main__":
    MenubarApp().run()
