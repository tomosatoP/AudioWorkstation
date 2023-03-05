#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from time import sleep

from ..libs.audio import fluidsynth as FS
from ..libs.sublibs.parts import gain2dB, dB2gain


class MidiSoundModule:
    gm_sound_set: list = list()
    gm_percussion_sound_set: list = list()

    def __init__(self) -> None:
        kwargs: dict = {
            "settings": "config/settings.json",
            "soundfont": [
                "sf2/FluidR3_GM.sf2",
                "sf2/SGM-V2.01.sf2",
                "sf2/YDP-GrandPiano-20160804.sf2",
            ],
        }

        self.fsmdrv = FS.MidiDriver(**kwargs)

        self.gm_sound_set, self.gm_percussion_sound_set = self.fsmdrv.gm_sound_set()

    @property
    def volume(self) -> int:
        return gain2dB(self.fsmdrv.gain)

    @volume.setter
    def volume(self, value: int) -> None:
        self.fsmdrv.gain = dB2gain(value)

    def preset_name(self, preset_num) -> str:
        return self.gm_sound_set[preset_num]["name"]

    def programchange(self, preset_num):
        self.fsmdrv.program_select(
            0,
            self.gm_sound_set[preset_num]["sfont_id"],
            self.gm_sound_set[preset_num]["bank"],
            self.gm_sound_set[preset_num]["num"],
        )

    def sounding(self):
        for i in [60, 62, 64]:
            self.fsmdrv.note_on(0, i, 100)
        sleep(0.3)
        for i in [60, 62, 64]:
            self.fsmdrv.note_off(0, i)
