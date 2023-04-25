#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""menu bar

#. Switching Child Screens [Keyboard, Metronome, MIDI Player]
#. Control volumes [Master & Child Screen]
#. Exit this application
"""
from importlib import import_module

from kivy.app import App
from kivy.logger import Logger
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.animation import Animation

from .libs.audio import asound


class MenubarView(Widget):
    """MenubarView places function switching, volume change, and exit."""

    #: ObjectProperty: child screens
    panel = ObjectProperty()
    #: ObjectProperty: spinner
    mode = ObjectProperty()
    #: ObjectProperty: master volume
    vol1 = ObjectProperty()
    #: ObjectProperty: child scree volume
    vol2 = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        Clock.schedule_once(lambda dt: self.activate_audio(), 4)
        message = Label(text="準備中、ちょっと待ってて", font_size=30)
        self.add_widget(message)
        anim = Animation(x=350, y=200) + Animation(x=150, y=200)
        anim.repeat = True
        anim.start(message)
        Clock.schedule_once(lambda dt: self.register_screens(), 4)
        Clock.schedule_once(lambda dt: self.remove_widget(message), 4)

    def activate_audio(self) -> None:
        """Activate JACK server, control volumes."""

        Logger.debug("JACK server: initializing...")
        asound.set_volume("default", "Master", 100)
        self.mixer: list[str] = asound.start_jackserver()
        asound.set_volume(self.mixer[2], self.mixer[3], 50)

    def register_screens(self) -> None:
        """Regisger screens."""

        keyboard = import_module("src.audioworkstation.keyboard.keyboard")
        metronome = import_module("src.audioworkstation.metronome.metronome")
        player = import_module("src.audioworkstation.player.player")

        self.panel.add_widget(keyboard.KeyboardView(name="keyboard"))
        self.panel.add_widget(metronome.MetronomeView(name="metronome"))
        self.panel.add_widget(player.PlayerView(name="player"))

        self.set_mode(self.mode, "キーボード")
        self.vol1.label.text = self.mixer[4]
        self.vol1.slider.bind(value=self.master_volume)
        self.vol2.slider.bind(value=self.mode_volume)
        self.mode.bind(text=self.set_mode)

    def unregister_screens(self) -> None:
        """Unregister screens."""

        for name in self.panel.screen_names:
            self.panel.get_screen(name).unregister()
            self.panel.remove_widget(self.panel.get_screen(name))

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
    """MenubarApp switches functions, changes volume, and exits."""

    def build(self):
        self.title = "AudioWorkstation"
        self.view = MenubarView()
        return self.view

    def on_stop(self):
        self.view.unregister_screens()
        return super().on_stop()


if __name__ == "__main__":
    MenubarApp().run()
