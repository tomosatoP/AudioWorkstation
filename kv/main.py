#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('../AudioWorkstation')
from libfluidsynth.fluidsynth import *

from time import sleep
from concurrent import futures

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.properties import BoundedNumericProperty

from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.resources import resource_add_path
resource_add_path('/usr/share/fonts/opentype/ipaexfont-gothic')
LabelBase.register(DEFAULT_FONT, 'ipaexg.ttf')

client_data_t._fields_ = [('quit', c_bool), ('c', c_char_p), ('q', c_char_p)]

@FLUID_EVENT_CALLBACK_T
def client_callback(time, event, sequencer, p_data):
    if not p_data.contents.quit:
        metronome_pattern(p_data.contents)

def metronome_pattern(data: client_data_t) -> None:
    time_marker = sfs.tick()

    key = [75, 76]
    vel = [127, 95, 64]
    beat = int(sfs.quaternote * 4 / int(data.q.decode()))
    rhythm = list(map(int, data.c.decode().split('+')))

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
    sfs = SequencerFS('sf2/FluidR3_GM.sf2')
    data = client_data_t()
    sfs.register_client('metronome', client_callback, pointer(data))

    def start(self, volume: int, bps: float, beat: list) -> None:
        print(f'sound on [volume: {volume}, tempo: {bps}, beat: {beat}]')
        sfs.gain(volume)
        sfs.set_bps(bps)
        self.data.quit = False
        self.data.c = beat[0].encode()
        self.data.q = beat[1].encode()
        metronome_pattern(self.data)
    
    def stop(self):
        self.data.quit = True

class MetronomeView(Widget):
    p = PatternSeqFS()
    executor = futures.ThreadPoolExecutor()

    bps = BoundedNumericProperty(
        120, min=60, max=240,
        errorhandler=lambda x: 240 if x > 240 else 60)

    def beat(self) -> str:
        return(list(filter(lambda x: x.state == 'down',
            ToggleButtonBehavior.get_widgets('BeatSelectButtons')))[0].text)

    def sound_on(self):
        self.executor.submit(self.p.start, 40, self.bps, self.beat().splitlines())
    
    def sound_off(self):
        print('sound off')
        self.p.stop()

class Metronome(App):
    def build(self):
        return(MetronomeView())

if __name__ == '__main__':
    Metronome().run()