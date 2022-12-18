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
    mfs = MidiRelayFS('../sf2/FluidR3_GM.sf2')
    print('default rule')
    sleep(5)
    mfs.change_rule('./rule.mute_chan_0.json')
    print('mute channel 0')
    sleep(5)
    mfs.noteOn(9, 34, 80)
    sleep(1)
    return(True)

# test class SequencerFS
def metronome_pattern():
    time_marker = sfs.tick()
    beat = sfs.quaternote
    sfs.note_at(time_marker, 9, 75, 30, int(beat / 10), destination = sid)
    time_marker += beat
    for _ in range(3):
        sfs.note_at(time_marker, 9, 76, 30, int(beat / 10), destination = sid)
        time_marker += beat
    sfs.timer_at(ticks = time_marker, destination = cid)

@FLUID_EVENT_CALLBACK_T
def client_callback(time, event, sequencer, data) -> None:
    metronome_pattern()

def verify_sequencer():
    global sfs, sid, cid
    sfs = SequencerFS('../sf2/FluidR3_GM.sf2')
    sfs.gain(80)
    sfs.set_bps(120)
    sid = sfs.synthesizer_client_id()
    cid = sfs.register_client('metronome', client_callback)

    metronome_pattern()
    sleep(6)
    sfs.noteOn(9, 34, 80)
    sleep(1)
    return(True)

# test midi player
def verify_midi_player():
    midi_player = MidiPlayerFS('../sf2/FluidR3_GM.sf2')

    midi_player.change_rule('./rule.mute_chan_0.json')
    midi_player.gain(70)
    midi_player.play('../mid/bolero_maurice_ravel.mid')
    sleep(8)
    midi_player.pause()
    sleep(1)
    midi_player.restart()
    sleep(8)
    midi_player.stop()
    midi_player.gain(40)
    midi_player.cueing('../mid/geki_teikokukagekidan.mid', 7)
    midi_player.cueing('../mid/l3008_05.mid', 7)
    midi_player.gain(70)
    midi_player.cueing('../mid/bolero_maurice_ravel.mid', 7)

if __name__ == '__main__':
    verify_synthesizer()
    verify_sequencer()
    #verify_midi_relay()
    #verify_midi_player()
