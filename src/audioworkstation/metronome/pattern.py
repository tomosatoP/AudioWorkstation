#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Provide implementation for the metronome module."""

from json import load

from ..libs.audio import fluidsynth as PtFS
from ..libs.sublibs.parts import dB2gain, gain2dB

sfs: PtFS.Sequencer
#: bool: Flag of continuation
schedule_stop: bool = True
#: list(int): beats
rhythm: list[int] = [0]
#: int: notevalue
notevalue: int = 4


@PtFS.FLUID_EVENT_CALLBACK_T
def bar_callback(time, event, sequencer, data):
    """Schedule the next metronome pattern repeatedly.

    :param c_uint time: Current sequencer tick value
    :param c_void_p event: The event being received
    :param c_void_p seq: The sequencer instance
    :param POINTER(EventUserData) data: User defined data registered with the client
    """
    if not schedule_stop:
        bar_pattern()


def bar_pattern() -> bool:
    """Schedule the metronome pattern."""
    time_marker = sfs.tick

    key = [75, 76]
    vel = [127, 95, 64]
    dur = int(sfs._quaternote * 4 / int(notevalue))

    for i in range(len(rhythm)):
        for j in range(rhythm[i]):
            k = 0 if all([i == 0, j == 0]) else 1
            m = 0 if all([i == 0, j == 0]) else 1 if j == 0 else 2
            sfs.note_at(
                time_marker,
                9,
                key[k],
                vel[m],
                int(dur / 2),
                destination=sfs.clients[0],
            )
            time_marker += dur
    sfs.timer_at(time_marker, destination=sfs.clients[1])
    return True


class Metronome:
    """Metronome beats a rhythm."""

    def __init__(self) -> None:
        global sfs, schedule_stop, rhythm, notevalue

        with open("config/screen.json", "rt") as f:
            kwargs = load(f)["metronome"]

        sfs = PtFS.Sequencer(**kwargs)
        sfs.register_client("bar", bar_callback)

    @property
    def volume(self) -> int:
        """int: volume"""
        return gain2dB(sfs.gain)

    @volume.setter
    def volume(self, value: int) -> None:
        sfs.gain = dB2gain(value)

    def start(self, bps: float, beat: list) -> None:
        """Start.

        :param float bps: bps
        :param list beat: beats and notevalue
        """
        global sfs, schedule_stop, rhythm, notevalue
        sfs.bps = bps

        schedule_stop = False
        rhythm = list(map(int, str(beat[0]).split("+")))
        notevalue = int(beat[1])
        bar_pattern()

    def stop(self) -> None:
        """Stop."""
        global schedule_stop
        schedule_stop = True


if __name__ == "__main__":
    print(__file__)
