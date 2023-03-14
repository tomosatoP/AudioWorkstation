#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from concurrent import futures
from pathlib import Path

from kivy.logger import Logger
from kivy.uix.screenmanager import Screen
from kivy.factory import Factory
from kivy.properties import BoundedNumericProperty, ListProperty, ObjectProperty
from kivy.lang import Builder

from . import pattern as PT

Builder.load_file(str(Path(__file__).with_name("metronome.kv")))


class MetronomeView(Screen):
    pSFS = PT.Pattern()
    executor = futures.ThreadPoolExecutor()

    bps_layout = ObjectProperty(None)
    bps = BoundedNumericProperty(
        120, min=60, max=240, errorhandler=lambda x: 240 if x > 240 else 60
    )

    beat_layout = ObjectProperty(None)
    beat = ListProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        Logger.debug("metronome: initializing...")

        for obj in self.bps_layout.walk():
            if isinstance(obj, Factory.BpsChangeButton):
                obj.bind(on_press=self.update_bps)

        for obj in self.beat_layout.walk():
            if isinstance(obj, Factory.BeatSelectButton):
                obj.bind(on_press=self.update_beat)
                if obj.state == "down":
                    self.beat = obj.text.splitlines()

    def sound(self, on: str) -> None:
        if on == "down":
            self.status(disable=True)
            Logger.info(f"metronome: BPS - {self.bps}")
            Logger.info(f"metronome: RHYTHM - {self.beat}")
            self.executor.submit(self.pSFS.start, self.bps, self.beat)
        else:
            self.status(disable=False)
            self.pSFS.stop()

    def update_bps(self, obj):
        self.bps += int(obj.text)

    def update_beat(self, obj):
        self.beat = obj.text.splitlines()

    def status(self, disable: bool) -> None:
        self.bps_layout.disabled = disable
        self.beat_layout.disabled = disable

    @property
    def volume(self) -> int:
        return self.pSFS.volume

    @volume.setter
    def volume(self, value: int) -> None:
        self.pSFS.volume = value


if __name__ == "__main__":
    print(__file__)
