#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from concurrent import futures
from functools import partial
import ctypes as C
from time import sleep
from typing import Callable

import context as CT

from AudioWorkstation.libs.audio import amixer as MASTER
from AudioWorkstation.libs.audio import fluidsynth as FS

# test class FS.SynthesizerFS


def verify_synthesizer() -> bool:
    kwargs = {'settings': 'config/settings.json'}
    fs = FS.Synthesizer(**kwargs)
    print(f'gain: {fs.gain:.1f}')

    print('GM percussion sound set')
    for sound_set in fs.gm_sound_set(is_percussion=True):
        for preset in sound_set:
            print(preset)
    print('channel preset')
    for sound_set in fs.channels_preset():
        print(sound_set)

    print('sound - GM sound set')
    fs.sustain_on(0)
    fs.modulation_wheel(0, 100)
    fs.volume(0, 100)
    for sound_set in fs.gm_sound_set():
        for preset in sound_set:
            if isinstance(preset['name'], str) and \
                    isinstance(preset['num'], int) and \
                    isinstance(preset['bank'], int) and \
                    isinstance(preset['sfont_id'], int):
                fs.program_select(
                    0, preset['sfont_id'], preset['bank'], preset['num'])
                print(preset['name'])
                fs.note_on(0, 60, 127)  # chord C
                fs.note_on(0, 62, 127)
                fs.note_on(0, 64, 127)
                sleep(0.3)
                fs.note_off(0, 60)
                fs.note_off(0, 62)
                fs.note_off(0, 64)

    fs.note_on(9, 34, 80)
    sleep(0.5)
    del fs
    return (True)


# test custum MIDI Router handler
@FS.HANDLE_MIDI_EVENT_FUNC_T
def midi_event_handler(data, event) -> int:
    try:
        FS.fluid_midi_dump_prerouter(data, event)
    except FS.FSError as mes:
        FS.fluid_log(level=FS.FLUID_LOG_LEVEL.WARN,
                     fmt=b'%s',
                     message=b'midi event ' + str(mes).encode())
        return (FS.FLUID_FAILED)
    return (FS.FLUID_OK)


# test class MidiDriverFS
def verify_midi_driver() -> bool:
    kwargs = {
        'settings': 'config/settings.json',
        'soundfont': ['sf2/FluidR3_GM.sf2',
                      'sf2/SGM-V2.01.sf2'],
        'handler': midi_event_handler}

    mdfs = FS.MidiDriver(**kwargs)
    print(f'gain: {mdfs.gain:.1f}')

    print('default rule')
    sleep(5)

    mdfs.change_rule('config/rule.mute_chan_0.json')
    print('mute channel 0')
    sleep(5)

    mdfs.note_on(9, 34, 80)
    sleep(0.5)
    del mdfs
    return (True)


# test class SequencerFS

FS.EventUserData._fields_ = [
    ('quit', C.c_bool),
    ('rhythm', C.c_char_p),
    ('beat', C.c_char_p)]


def metronome_pattern(data: FS.EventUserData) -> bool:
    time_marker = sfs.tick

    key = [75, 76]
    vel = [127, 95, 64]
    rhythm = list(map(int, data.rhythm.decode().split('+')))
    beat = int(sfs._quaternote * 4 / int(data.beat.decode()))

    for i in range(len(rhythm)):
        for j in range(rhythm[i]):
            k = 0 if all([i == 0, j == 0]) else 1
            m = 0 if all([i == 0, j == 0]) else 1 if j == 0 else 2
            sfs.note_at(time_marker, 9, key[k], vel[m], int(beat / 2),
                        destination=sfs._clients[0])
            time_marker += beat

    sfs.timer_at(ticks=time_marker, destination=sfs._clients[1])
    return (True)


@FS.FLUID_EVENT_CALLBACK_T
def client_callback(time, event, sequencer, p_data):
    if not p_data.contents.quit:
        metronome_pattern(p_data.contents)


def verify_sequencer() -> bool:
    global sfs
    kwargs = {
        'settings': 'config/settings.json',
        'soundfont': ['sf2/FluidR3_GM.sf2']}

    sfs = FS.Sequencer(**kwargs)
    print(f'gain: {sfs.gain:.1f}')

    data = FS.EventUserData()
    sfs.register_client('metronome', client_callback, data)

    sfs.bps = 120
    data.quit = False
    data.rhythm = b'2+2'
    data.beat = b'4'
    metronome_pattern(data)
    sleep(8)

    sfs.bps = 200
    metronome_pattern(data)
    sleep(4)

    data.quit = True
    sleep(4)

    sfs.note_on(9, 34, 80)
    sleep(0.5)
    del sfs
    return (True)


# test class MidiPlayerFS

def future_callback(func: Callable[..., None], future: futures.Future) -> bool:
    func()
    return (future.done())


def verify_midi_player() -> bool:
    kwargs = {
        'settings': 'config/settings.json',
        'soundfont': ['sf2/FluidR3_GM.sf2',
                      'sf2/SGM-V2.01.sf2',
                      'sf2/YDP-GrandPiano-20160804.sf2']}

    mpfs = FS.MidiPlayer(**kwargs)
    mpfs.change_rule('config/rule.mute_chan_0.json')
    mpfs.gain = 0.3
    print(f'gain: {mpfs.gain:.1f}')

    with futures.ThreadPoolExecutor(max_workers=1) as e:
        filename = 'mid/l3007_02.mid'
        tick: int = 0
        for _ in range(3):
            f = e.submit(mpfs.start, filename, tick)
            f.add_done_callback(partial(future_callback, mpfs.close))
            sleep(2)
            tick = mpfs.stop() + 5000
            sleep(0.1)

        filename = 'mid/l3007_03.mid'
        f = e.submit(mpfs.start, filename, 20000)
        f.add_done_callback(partial(future_callback, mpfs.close))
        sleep(10)
        mpfs.stop()

    print('channel preset')
    for sound_set in mpfs.channels_preset():
        print(sound_set)
    print(mpfs.soundfonts)

    mpfs.note_on(9, 34, 80)
    sleep(0.5)
    del mpfs
    return (True)


if __name__ == '__main__':
    CT.check()
    MASTER.volume()
    verify_synthesizer()
    verify_sequencer()
    verify_midi_driver()
    verify_midi_player()
