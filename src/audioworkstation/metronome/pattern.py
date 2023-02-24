#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ..libs.audio import fluidsynth as FS
from ..parts import _dB2gain, _gain2dB

sfs: FS.Sequencer
schedule_stop: bool = False
rhythm: list[int]
notevalue: int


@FS.FLUID_EVENT_CALLBACK_T
def _pcallback(time, event, sequencer, data):
    if not schedule_stop:
        _pattern()


def _pattern():
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


class Pattern:
    def __init__(self) -> None:
        global sfs, schedule_stop, rhythm, notevalue
        kwargs: dict = {
            "settings": "config/settings.json",
            "soundfont": ["sf2/FluidR3_GM.sf2"],
        }

        sfs = FS.Sequencer(**kwargs)
        sfs.register_client("metronome", _pcallback)

    @property
    def gain(self) -> int:
        return _gain2dB(sfs.gain)

    @gain.setter
    def gain(self, value: int) -> None:
        sfs.gain = _dB2gain(value)

    def start(self, bps: float, beat: list) -> None:
        global sfs, schedule_stop, rhythm, notevalue
        sfs.bps = bps

        schedule_stop = False
        rhythm = list(map(int, str(beat[0]).split("+")))
        notevalue = int(beat[1])
        _pattern()

    def stop(self):
        global schedule_stop
        print("sound off")
        schedule_stop = True


if __name__ == "__main__":
    print(__file__)
