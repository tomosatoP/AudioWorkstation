#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from fluidsynth import *
from time import sleep

# test class SynthesizerFS
def verify_synthesizer():
    fs = SynthesizerFS()
    print(fs.gain())
    fs.gain(70)
    print(fs.gain())

    fs.noteOn(9, 34, 80)
    sleep(0.5)
    fs.noteOff(9, 34)
    return(True)

# test class MidiRelayFS
def verify_midi_relay():
    mfs = MidiRelayFS('sf2/FluidR3_GM.sf2')
    print('default rule')
    sleep(5)
    mfs.change_rule('libfluidsynth/rule.mute_chan_0.json')
    print('mute channel 0')
    sleep(5)
    mfs.noteOn(9, 34, 80)
    sleep(1)
    return(True)

# test class SequencerFS
client_data_t._fields_ = [('quit', c_bool), ('rhythm', c_char_p), ('beat', c_char_p)]

def metronome_pattern(data: client_data_t) -> None:
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

@FLUID_EVENT_CALLBACK_T
def client_callback(time, event, sequencer, p_data):
    if not p_data.contents.quit:
        metronome_pattern(p_data.contents)

def verify_sequencer():
    global sfs
    sfs = SequencerFS('sf2/FluidR3_GM.sf2')
    sfs.gain(30)
    data = client_data_t()
    sfs.register_client('metronome', client_callback, pointer(data))
    
    sfs.set_bps(120)
    data.quit = False
    data.rhythm = b'2+2'
    data.beat = b'4'
    metronome_pattern(data)
    sleep(4)

    sfs.set_bps(60)
    metronome_pattern(data)
    sleep(4)

    data.quit = True
    sleep(4)

    sfs.gain(50)
    sfs.noteOn(9, 34, 80)
    sleep(1)
    return(True)

# test midi player
def verify_midi_player():
    midi_player = MidiPlayerFS('sf2/FluidR3_GM.sf2')

    midi_player.change_rule('libfluidsynth/rule.mute_chan_0.json')
    midi_player.gain(70)
    midi_player.play('mid/bolero_maurice_ravel.mid')
    sleep(8)
    midi_player.pause()
    sleep(1)
    midi_player.restart()
    sleep(8)
    midi_player.stop()
    midi_player.gain(40)
    midi_player.cueing('mid/geki_teikokukagekidan.mid', 7)
    midi_player.cueing('mid/l3008_05.mid', 7)
    midi_player.gain(70)
    midi_player.cueing('mid/bolero_maurice_ravel.mid', 7)

if __name__ == '__main__':
    verify_synthesizer()
    verify_sequencer()
    verify_midi_relay()
    verify_midi_player()
