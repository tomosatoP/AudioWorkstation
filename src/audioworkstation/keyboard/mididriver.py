#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from time import sleep

from ..libs.audio import fluidsynth as FS
from ..libs.sublibs.parts import gain2dB, dB2gain


class MidiSoundModule:
    presets: list = list()

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

        (full_gmsoundset, dummy) = self.fsmdrv.gm_sound_set()
        preset: dict = dict()
        for i in range(128):
            for sfont_gmsoundset in full_gmsoundset:
                if sfont_gmsoundset[i]["name"] is not None:
                    preset = sfont_gmsoundset[i]
                    break
            self.presets.append(preset)

    @property
    def volume(self) -> int:
        return gain2dB(self.fsmdrv.gain)

    @volume.setter
    def volume(self, value: int) -> None:
        self.fsmdrv.gain = dB2gain(value)

    def preset_name(self, preset_num) -> str:
        return self.presets[preset_num]["name"]

    def programchange(self, preset_num):
        self.fsmdrv.program_select(
            0,
            self.presets[preset_num]["sfont_id"],
            self.presets[preset_num]["bank"],
            self.presets[preset_num]["num"],
        )

    def sounding(self):
        for i in [60, 62, 64]:
            self.fsmdrv.note_on(0, i, 100)
        sleep(0.3)
        for i in [60, 62, 64]:
            self.fsmdrv.note_off(0, i)
