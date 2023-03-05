#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
from json import dump

from ..libs.audio import fluidsynth as FS
from ..libs.sublibs import standardmidifile as SMF
from ..libs.sublibs.parts import dB2gain, gain2dB


class MidiPlayer:
    """MidiPlayer _summary_

    :return _type_: _description_
    """

    pause_tick: int = 0

    def __init__(self) -> None:
        kwargs: dict = {
            "settings": "config/settings.json",
            "soundfont": [
                "sf2/FluidR3_GM.sf2",
                "sf2/SGM-V2.01.sf2",
                "sf2/YDP-GrandPiano-20160804.sf2",
            ],
        }

        self.fsmp = FS.MidiPlayer(**kwargs)

    def start(self, filename: str) -> str:
        """start _summary_

        :param str filename: _description_
        :return str: _description_
        """
        self.fsmp.apply_rules("config/rule.mute_chan.json")
        self.fsmp.start(filename, self.pause_tick)
        return f"{filename}"

    def close(self) -> None:
        """close _summary_"""
        self.pause_tick = 0
        self.fsmp.close()

    def pause(self) -> None:
        """pause _summary_"""
        self.pause_tick = self.fsmp.stop()

    @property
    def tick(self) -> int:
        """tick _summary_

        :return int: _description_
        """
        return self.fsmp.tick

    @property
    def volume(self) -> int:
        return gain2dB(self.fsmp.gain)

    @volume.setter
    def volume(self, value) -> None:
        self.fsmp.gain = dB2gain(value)


def info_midifile(midifile: Path) -> dict:
    """info_midifile _summary_

    :param Path midifile: _description_
    :return dict: _description_
    """
    _smf = SMF.StandardMidiFile(midifile)
    items: dict = {}
    items["title"] = _smf.title()
    items["total_tick"] = _smf.total_tick()
    items["channels_preset"] = _smf.channels_preset()
    return items


def gm_sound_set_names() -> tuple:
    kwargs: dict = {
        "settings": "config/settings.json",
        "soundfont": ["sf2/FluidR3_GM.sf2"],
    }

    synth = FS.Synthesizer(**kwargs)

    gm_sound_sets: list = list()
    gm_percussion_sound_sets: list = list()
    snames: list = list()
    pnames: list = list()

    gm_sound_sets, gm_percussion_sound_sets = synth.gm_sound_set()
    for i in range(128):
        snames += [gm_sound_sets[i]["name"]]
        pnames += [gm_percussion_sound_sets[i]["name"]]

    return (snames, pnames)


def mute_rules(**kwargs) -> str:
    """
    {'0':True, '1':False, ..., '15':False}
        True: mute
        False: unmute
    """
    rules: dict = dict()
    filename = "config/rule.mute_chan.json"

    # Note
    for chan in list(kwargs):
        if kwargs[chan]:
            # NOTE: mute channel
            comment = "NOTE: mute chan " + chan
            rules[comment] = {
                "type": FS.FLUID_MIDI_ROUTER_RULE_TYPE.NOTE,
                "chan": None,
                "param1": None,
                "param2": None,
            }
            rules[comment]["chan"] = {
                "min": int(chan),
                "max": int(chan),
                "mul": 1.0,
                "add": 0,
            }
            rules[comment]["param2"] = {"min": 0, "max": 127, "mul": 0.0, "add": 0}
        else:
            # NOTE: without change
            comment = "NOTE: unmute chan " + chan
            rules[comment] = {
                "type": FS.FLUID_MIDI_ROUTER_RULE_TYPE.NOTE,
                "chan": None,
                "param1": None,
                "param2": None,
            }
            rules[comment]["chan"] = {
                "min": int(chan),
                "max": int(chan),
                "mul": 1.0,
                "add": 0,
            }

    # CC: without change
    rules["CC"] = {
        "type": FS.FLUID_MIDI_ROUTER_RULE_TYPE.CC,
        "chan": None,
        "param1": None,
        "param2": None,
    }
    # PROG_CHANGER: without change
    rules["PROG_CHANGER"] = {
        "type": FS.FLUID_MIDI_ROUTER_RULE_TYPE.PROG_CHANGER,
        "chan": None,
        "param1": None,
        "param2": None,
    }
    # PITCH_BEND: without change
    rules["PITCH_BEND"] = {
        "type": FS.FLUID_MIDI_ROUTER_RULE_TYPE.PITCH_BEND,
        "chan": None,
        "param1": None,
        "param2": None,
    }
    # CHANNEL_PRESSURE: without change
    rules["CHANNEL_PRESSURE"] = {
        "type": FS.FLUID_MIDI_ROUTER_RULE_TYPE.CHANNEL_PRESSURE,
        "chan": None,
        "param1": None,
        "param2": None,
    }
    # KEY_PRESSURE: without change
    rules["KEY_PRESSURE"] = {
        "type": FS.FLUID_MIDI_ROUTER_RULE_TYPE.KEY_PRESSURE,
        "chan": None,
        "param1": None,
        "param2": None,
    }

    with open(filename, "w") as fw:
        dump(rules, fw, indent=4)

    return filename


if __name__ == "__main__":
    print(__file__)
