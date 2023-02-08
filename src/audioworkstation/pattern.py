#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from src.audioworkstation.libs.audio import fluidsynth as FS
from time import sleep


sfs: FS.Sequencer
pquit: bool
rhythm: list[int]
notevalue: int
pdata: FS.EventUserData


@FS.FLUID_EVENT_CALLBACK_T
def pcallback(time, event, sequencer, data):
    # global sfs, pquit, rhythm, notevalue, pdata
    pattern()


def pattern():
    # global sfs, pquit, rhythm, notevalue, pdata

    time_marker = sfs.tick
    print(time_marker)

    key = [75, 76]
    vel = [127, 95, 64]
    dur = int(sfs._quaternote * 4 / int(notevalue))

    for i in range(len(rhythm)):
        for j in range(rhythm[i]):
            k = 0 if all([i == 0, j == 0]) else 1
            m = 0 if all([i == 0, j == 0]) else 1 if j == 0 else 2
            sfs.note_at(time_marker, 9, key[k], vel[m], int(dur / 2),
                        destination=sfs.clients[0])
            time_marker += dur
    sfs.timer_at(time_marker, destination=sfs.clients[1])
    print(time_marker)


class Pattern():

    def __init__(self) -> None:
        global sfs, pquit, rhythm, notevalue, pdata
        kwargs = {'settings': 'config/settings.json',
                  'soundfont': ['sf2/FluidR3_GM.sf2']}

        sfs = FS.Sequencer(**kwargs)
        pdata = FS.EventUserData()

        sfs.register_client('metronome', pcallback, pdata)
        print(sfs.clients)

    def start(self, bps: float, beat: list) -> None:
        global sfs, pquit, rhythm, notevalue, pdata
        print(f'sound on [tempo: {bps}, beat: {beat}]')
        sfs.bps = bps

        pquit = False
        rhythm = list(map(int, str(beat[0]).split('+')))
        notevalue = int(beat[1])
        pattern()

        sleep(30)

    def stop(self):
        global sfs, pquit, rhythm, notevalue, pdata
        print('sound off')
        pquit = True


if __name__ == '__main__':
    cpt = Pattern()
    cpt.start(120, [4, 4])
    sleep(20)
    print('pattern')
