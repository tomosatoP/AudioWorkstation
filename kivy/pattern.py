#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from audio import fluidsynth as FS
import ctypes as C

FS.EventUserData._fields_ = \
    [('quit', C.c_bool),
     ('rhythm', C.c_char_p),
     ('beat', C.c_char_p)]

'''
@FS.FLUID_EVENT_CALLBACK_T
def client_callback(time, event, sequencer, p_data):
    if not p_data.contents.quit:
        pattern(p_data.contents)

def pattern(data: FS.EventUserData) -> None:
    global sfs
    time_marker = sfs.tick()

    key = [75, 76]
    vel = [127, 95, 64]
    rhythm = list(map(int, data.rhythm.decode().split('+')))
    beat = int(sfs.quaternote * 4 / int(data.beat.decode()))

    for i in range(len(rhythm)):
        for j in range(rhythm[i]):
            k = 0 if all([i == 0, j == 0]) else 1
            m = 0 if all([i == 0, j == 0]) else 1 if j == 0 else 2
            sfs.note_at(time_marker, 9, key[k], vel[m], int(beat / 2),
                        destination=sfs.client_ids[0])
            time_marker += beat
    sfs.timer_at(ticks=time_marker, destination=sfs.client_ids[1])
'''


class Pattern():

    def __init__(self) -> None:
        kwargs = {'settings': 'kivy/settings.json',
                  'soundfont': 'sf2/FluidR3_GM.sf2'}

        self.sfs = FS.Sequencer(**kwargs)
        self.data = FS.EventUserData()

        self.sfs.register_client('metronome', self.callback, None)

    def start(self, bps: float, beat: list) -> None:
        print(f'sound on [tempo: {bps}, beat: {beat}]')
        self.sfs.set_bps(bps)
        self.data.quit = False
        self.data.rhythm = beat[0].encode()
        self.data.beat = beat[1].encode()
        self.rhythm = beat[0].encode()
        self.beat = beat[1].encode()
        self.pattern()

    def stop(self):
        print('sound off')
        self.data.quit = True

    @FS.FLUID_EVENT_CALLBACK_T
    def callback(self, time, event, sequencer, data):
        self.pattern()

    def pattern(self):
        time_marker = self.sfs.tick()

        key = [75, 76]
        vel = [127, 95, 64]
        rhythm = list(map(int, self.rhythm.decode().split('+')))
        beat = int(self.sfs.quaternote * 4 / int(self.beat.decode()))

        for i in range(len(rhythm)):
            for j in range(rhythm[i]):
                k = 0 if all([i == 0, j == 0]) else 1
                m = 0 if all([i == 0, j == 0]) else 1 if j == 0 else 2
                self.sfs.note_at(time_marker, 9, key[k], vel[m], int(beat / 2),
                                 destination=self.sfs.client_ids[0])
                time_marker += beat
        self.sfs.timer_at(ticks=time_marker,
                          destination=self.sfs.client_ids[1])


if __name__ == '__main__':
    print('pattern')
