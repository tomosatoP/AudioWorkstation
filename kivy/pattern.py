#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from audio.fluidsynth import *

SequencerEventCallbackData._fields_ = \
    [('quit', c_bool), ('rhythm', c_char_p), ('beat', c_char_p)]

@FLUID_EVENT_CALLBACK_T
def client_callback(time, event, sequencer, p_data):
    if not p_data.contents.quit:
        pattern(p_data.contents)

def pattern(data: SequencerEventCallbackData) -> None:
    time_marker = sfs.tick()

    key = [75, 76]
    vel = [127, 95, 64]
    rhythm = list(map(int, data.rhythm.decode().split('+')))
    beat = int(sfs.quaternote * 4 / int(data.beat.decode()))

    for i in range(len(rhythm)):
        for j in range(rhythm[i]):
            k = 0 if all([i == 0, j == 0]) else 1
            l = 0 if all([i == 0, j == 0]) else 1 if j == 0 else 2
            sfs.note_at(time_marker, 9, key[k], vel[l], int(beat / 2), 
                destination = sfs.client_ids[0])
            time_marker += beat
    sfs.timer_at(ticks = time_marker, destination = sfs.client_ids[1])

class PatternSeqFS():
    global sfs
    kwargs = {
        'settings': 'kivy/settings.json',
        'soundfont': 'sf2/FluidR3_GM.sf2'}

    sfs = SequencerFS(**kwargs)
    data = SequencerEventCallbackData()
    sfs.register_client('metronome', client_callback, pointer(data))

    def start(self, volume: int, bps: float, beat: list) -> None:
        print(f'sound on [volume: {volume}, tempo: {bps}, beat: {beat}]')
        sfs.gain(volume)
        sfs.set_bps(bps)
        self.data.quit = False
        self.data.rhythm = beat[0].encode()
        self.data.beat = beat[1].encode()
        pattern(self.data)
    
    def stop(self):
        print('sound off')
        self.data.quit = True

if __name__ == '__main__':
    print('pattern')