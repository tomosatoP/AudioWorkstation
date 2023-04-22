#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Functions for managing MIDI driver for "keyboard"."""

from time import sleep
from json import load

from ..libs.audio import fluidsynth as FS
from ..libs.sublibs.parts import gain2dB, dB2gain


class MidiSoundModule:
    """MidiSoundModule manages MIDI driver for the "keyboard"."""

    #: list: list of GM Sound Set
    gm_sound_set: list = list()
    #: list: list of GM Percussion Sound Set
    gm_percussion_sound_set: list = list()

    def __init__(self) -> None:
        with open("config/screen.json", "rt") as f:
            kwargs = load(f)["keyboard"]

        self.fsmdrv = FS.MidiDriver(**kwargs)

        self.gm_sound_set, self.gm_percussion_sound_set = self.fsmdrv.gm_sound_set()

    @property
    def volume(self) -> int:
        """int: volume"""
        return gain2dB(self.fsmdrv.gain)

    @volume.setter
    def volume(self, value: int) -> None:
        self.fsmdrv.gain = dB2gain(value)

    def preset_name(self, preset_num: int) -> str:
        """Return the program(preset) name assigned to the program(preset) number.

        :param int preset_num: program(preset) number
        :return: program(preset) name
        """
        return self.gm_sound_set[preset_num]["name"]

    def programchange(self, preset_num: int) -> None:
        """change program

        :param int preset_num: program(preset) number
        """
        self.fsmdrv.program_select(
            0,
            self.gm_sound_set[preset_num]["sfont_id"],
            self.gm_sound_set[preset_num]["bank"],
            self.gm_sound_set[preset_num]["num"],
        )

    def sounding(self) -> None:
        """Sound the selected instrument."""
        for i in [60, 62, 64]:
            self.fsmdrv.note_on(0, i, 100)
        sleep(0.3)
        for i in [60, 62, 64]:
            self.fsmdrv.note_off(0, i)


if __name__ == "__main__":
    print(__file__)
