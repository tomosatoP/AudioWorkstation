#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from concurrent import futures
from pathlib import Path

from kivy.uix.screenmanager import Screen
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.properties import BoundedNumericProperty, ObjectProperty
from kivy.lang import Builder

from . import pattern as PT

Builder.load_file(str(Path(__file__).with_name("metronome.kv")))

# To play the metronome pattern in a separate thread.


class MetronomeView(Screen):
    pSFS = PT.Pattern()
    executor = futures.ThreadPoolExecutor()

    bps_layout = ObjectProperty(None)
    beat_layout = ObjectProperty(None)
    bps = BoundedNumericProperty(
        120, min=60, max=240, errorhandler=lambda x: 240 if x > 240 else 60
    )

    def beat(self) -> str:
        return list(
            filter(
                lambda x: x.state == "down",
                ToggleButtonBehavior.get_widgets("BeatSelectButtons"),
            )
        )[0].text

    def sound(self, on: str) -> None:
        if on == "down":
            self.status(disable=True)
            print(f"BPS:{self.bps}, RHYTHM:{self.beat().splitlines()}")
            self.executor.submit(self.pSFS.start, self.bps, self.beat().splitlines())
        else:
            self.status(disable=False)
            self.pSFS.stop()

    def status(self, disable: bool) -> None:
        self.bps_layout.disabled = disable
        self.beat_layout.disabled = disable

    def sound_volume(self, value) -> None:
        self.pSFS.volume = value


if __name__ == "__main__":
    print(__file__)
