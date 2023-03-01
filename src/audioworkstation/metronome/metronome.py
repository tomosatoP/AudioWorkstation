#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from concurrent import futures
from pathlib import Path

from kivy.logger import Logger  # noqa: F401
from kivy.uix.screenmanager import Screen
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.properties import BoundedNumericProperty, ObjectProperty
from kivy.lang import Builder

from . import pattern as PT

Builder.load_file(str(Path(__file__).with_name("metronome.kv")))


class MetronomeView(Screen):
    pSFS = PT.Pattern()
    executor = futures.ThreadPoolExecutor()

    bps_layout = ObjectProperty(None)
    beat_layout = ObjectProperty(None)
    bps = BoundedNumericProperty(
        120, min=60, max=240, errorhandler=lambda x: 240 if x > 240 else 60
    )

    def sound(self, on: str) -> None:
        if on == "down":
            self.status(disable=True)
            Logger.info(f"metronome: BPS - {self.bps}")
            Logger.info(f"metronome: RHYTHM - {self.beat().splitlines()}")
            self.executor.submit(self.pSFS.start, self.bps, self.beat().splitlines())
        else:
            self.status(disable=False)
            self.pSFS.stop()

    def beat(self) -> str:
        return list(
            filter(
                lambda x: x.state == "down",
                ToggleButtonBehavior.get_widgets("BeatSelectButtons"),
            )
        )[0].text

    def status(self, disable: bool) -> None:
        self.bps_layout.disabled = disable
        self.beat_layout.disabled = disable

    def sound_stop(self) -> None:
        self.sound("normal")

    @property
    def sound_volume(self) -> int:
        return self.pSFS.volume

    @sound_volume.setter
    def sound_volume(self, value: int) -> None:
        self.pSFS.volume = value


if __name__ == "__main__":
    print(__file__)
