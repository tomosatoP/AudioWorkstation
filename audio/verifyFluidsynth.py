#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from fluidsynth import *
from time import sleep

# test class SynthesizerFS
def verify_synthesizer():
    kwargs = {'settings': 'audio/settings.json'}
    fs = SynthesizerFS(**kwargs)

    print('soundfont preset')
    for i in fs.sfonts_preset():
        for j in i:
            print(j)
    print('channel preset')
    for i in fs.channels_preset():
        print(i)

    print(fs.gain())
    fs.gain(70)
    print(fs.gain())

    fs.sustain_on(0)
    fs.modulation_wheel(0, 100)
    fs.volume(0, 30)
    for i in fs.sfonts_preset():
        for j in i:
            fs.program_select(0, j['sfont_id'], j['bank'], j['num'])
            print(j['name'])
            fs.note_on(0, 64, 60)
            fs.note_on(0, 66, 60)
            fs.note_on(0, 68, 60)
            sleep(0.5)
            fs.note_off(0, 64)
            fs.note_off(0, 66)
            fs.note_off(0, 68)

    fs.note_on(9, 34, 80)
    sleep(0.5)
    fs.note_off(9, 34)
    return(True)

# test custum MIDI Router handler
MidiEventHandlerData._fields_ = [('router', c_void_p)]

@HANDLE_MIDI_EVENT_FUNC_T
def midi_event_handler(p_data, event):
    pass

# test class MidiDriverFS
def verify_midi_driver():
    kwargs = {
        'settings': 'audio/settings.json',
        'soundfont': 'sf2/FluidR3_GM.sf2',
        'handler': fluid_midi_dump_prerouter}
    
    mdfs = MidiDriverFS(**kwargs)
    
    print('default rule')
    sleep(5)
    
    mdfs.change_rule('audio/rule.mute_chan_0.json')
    print('mute channel 0')
    sleep(5)
    
    mdfs.note_on(9, 34, 80)
    sleep(1)
    return(True)

# test class SequencerFS
SequencerEventCallbackData._fields_ = [
    ('quit', c_bool), ('rhythm', c_char_p), ('beat', c_char_p)]

def metronome_pattern(data: SequencerEventCallbackData) -> None:
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
    kwargs = {
        'settings': 'audio/settings.json',
        'soundfont': 'sf2/FluidR3_GM.sf2'}
    
    sfs = SequencerFS(**kwargs)
    
    sfs.gain(30)
    data = SequencerEventCallbackData()
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
    sfs.note_on(9, 34, 80)
    sleep(1)
    return(True)

# test midi player
def verify_midi_player():
    kwargs = {
        'settings': 'audio/settings.json',
        'soundfont': 'sf2/FluidR3_GM.sf2',
        'handler': fluid_midi_dump_prerouter}

    mpfs = MidiPlayerFS(**kwargs)

    mpfs.change_rule('audio/rule.mute_chan_0.json')

    mpfs.gain(70)
    mpfs.play('mid/bolero_maurice_ravel.mid')
    sleep(8)
    mpfs.pause()
    sleep(1)
    mpfs.restart()
    sleep(8)
    mpfs.stop()

    mpfs.gain(40)
    mpfs.cueing('mid/geki_teikokukagekidan.mid', 7)
    mpfs.cueing('mid/l3008_05.mid', 7)
    mpfs.gain(70)
    mpfs.cueing('mid/bolero_maurice_ravel.mid', 7)

if __name__ == '__main__':
    verify_synthesizer()
    verify_sequencer()
    verify_midi_driver()
    verify_midi_player()
