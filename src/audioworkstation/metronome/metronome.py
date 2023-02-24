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

    def sound_on(self) -> None:
        self._status(disable=True)
        print(f"BPS:{self.bps}, RHYTHM:{self.beat().splitlines()}")
        self.executor.submit(self.pSFS.start, self.bps, self.beat().splitlines())

    def sound_off(self) -> None:
        self._status(disable=False)
        self.pSFS.stop()

    def _status(self, disable: bool) -> None:
        self.bps_layout.disabled = disable
        for button in ToggleButtonBehavior.get_widgets("BeatSelectButtons"):
            button.disabled = disable


if __name__ == "__main__":
    print(__file__)
