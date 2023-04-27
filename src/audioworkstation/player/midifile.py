#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MIDI file parsing and playback processing"""

from pathlib import Path
from json import dump, load


from ..libs.sublibs import standardmidifile as SMF
from ..libs.audio import fluidsynth as FS
from ..libs.sublibs.parts import dB2gain, gain2dB


with open("config/screen.json", "rt") as f:
    kwargs = load(f)["player"]


class MidiPlayer:
    """MidiPlayer playbacks MIDI files."""

    #: int: number of ticks at interruption
    pause_tick: int = 0
    #: float: gain
    gain: float = 0.2

    def start(self, filename: str) -> str:
        """Starts playback of the specified midi file.

        :param str filename: midi filename
        :return: filename
        """
        kwargs["standardmidifile"] = [filename]
        self.fsmp = FS.MidiPlayer(**kwargs)
        self.fsmp.apply_rules("config/rule.mute_chan.json")
        self.fsmp.gain = self.gain
        self.fsmp.playback(self.pause_tick)
        return f"{filename}"

    def stop(self) -> None:
        """Stops the playback of Midi files."""

        if hasattr(self, "fsmp"):
            self.pause_tick = self.fsmp.stop()
            self.gain = self.fsmp.gain
            del self.fsmp

    @property
    def tick(self) -> int:
        """int: tick"""
        return self.fsmp.tick if hasattr(self, "fsmp") else self.pause_tick

    @property
    def volume(self) -> int:
        """int: volume"""
        if hasattr(self, "fsmp"):
            return gain2dB(self.fsmp.gain)
        else:
            return gain2dB(self.gain)

    @volume.setter
    def volume(self, value: int) -> None:
        if hasattr(self, "fsmp"):
            self.fsmp.gain = dB2gain(value)
        else:
            self.gain = dB2gain(value)


def info_midifile(midifile: Path) -> dict:
    """Returns information about the Midi file.

    :param Path midifile: Target Midi file
    :return: keywords: "title", "total_ticks", "channel_presets"
    """
    _smf = SMF.StandardMidiFile(midifile)
    items: dict = {}
    items["title"] = _smf.title()
    items["total_tick"] = _smf.total_tick()
    items["channels_preset"] = _smf.channels_preset()
    return items


def gm_sound_set_names() -> tuple:
    """Return GM Sound Set names and GM Percussion Sound Set names

    :return: list of GM Sound Set names
    :return: list of GM Percussion Sound Set names
    """

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


def mute_rules(**mute_flags) -> str:
    """Rule file specifying channels to mute

    :param dict(str, bool) mute_flags:
    {'0':True, '1':False, ..., '15':False}: True is mute, False is unmute
    """

    rules: dict = dict()
    #: str: filename
    filename = "config/rule.mute_chan.json"

    # Note
    for chan in list(mute_flags):
        if mute_flags[chan]:
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
