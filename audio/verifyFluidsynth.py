#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from concurrent import futures
from functools import partial
import fluidsynth as FS
import amixer as MASTER
import ctypes as C
from time import sleep
from typing import Callable

# test class FS.SynthesizerFS


def verify_synthesizer() -> bool:
    kwargs = {'settings': 'audio/settings.json'}
    fs = FS.Synthesizer(**kwargs)
    print(f'gain: {fs.gain():.1f}')

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
                sleep(0.5)
                fs.note_off(0, 60)
                fs.note_off(0, 62)
                fs.note_off(0, 64)

    fs.note_on(9, 34, 80)
    sleep(0.5)
    fs.note_off(9, 34)
    return (True)


# test custum MIDI Router handler
FS.MidiEventUserData._fields_ = [('router', C.c_void_p)]


@FS.HANDLE_MIDI_EVENT_FUNC_T
def midi_event_handler(p_data, event):
    pass


# test class MidiDriverFS
def verify_midi_driver() -> bool:
    kwargs = {
        'settings': 'audio/settings.json',
        'soundfont': 'sf2/FluidR3_GM.sf2',
        'handler': FS.fluid_midi_dump_prerouter}

    mdfs = FS.MidiDriver(**kwargs)
    print(f'gain: {mdfs.gain():.1f}')

    print('default rule')
    sleep(5)

    mdfs.change_rule('audio/rule.mute_chan_0.json')
    print('mute channel 0')
    sleep(5)

    mdfs.note_on(9, 34, 80)
    sleep(1)
    return (True)


# test class SequencerFS

FS.EventUserData._fields_ = [
    ('quit', C.c_bool), ('rhythm', C.c_char_p), ('beat', C.c_char_p)]


def metronome_pattern(data: FS.EventUserData) -> bool:
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
    return (True)


@FS.FLUID_EVENT_CALLBACK_T
def client_callback(time, event, sequencer, p_data):
    if not p_data.contents.quit:
        metronome_pattern(p_data.contents)


def verify_sequencer() -> bool:
    global sfs
    kwargs = {
        'settings': 'audio/settings.json',
        'soundfont': 'sf2/FluidR3_GM.sf2'}

    sfs = FS.Sequencer(**kwargs)
    print(f'gain: {sfs.gain():.1f}')

    data = FS.EventUserData()
    sfs.register_client('metronome', client_callback, data)

    sfs.set_bps(120)
    data.quit = False
    data.rhythm = b'2+2'
    data.beat = b'4'
    metronome_pattern(data)
    sleep(8)

    sfs.set_bps(200)
    metronome_pattern(data)
    sleep(4)

    data.quit = True
    sleep(4)

    sfs.note_on(9, 34, 80)
    sleep(1)
    return (True)


# test class MidiPlayerFS

def future_callback(func: Callable[..., None], future: futures.Future) -> bool:
    func()
    return (future.done())


def verify_midi_player() -> bool:
    kwargs = {
        'settings': 'audio/settings.json',
        'soundfont': 'sf2/FluidR3_GM.sf2'}

    mpfs = FS.MidiPlayer(**kwargs)
    mpfs.change_rule('audio/rule.mute_chan_0.json')
    print(f'gain: {mpfs.gain(0.2):.1f}')

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
        sleep(3)
        mpfs.stop()

    mpfs.note_on(9, 34, 80)
    sleep(1)
    return (True)


if __name__ == '__main__':
    MASTER.volume()
    verify_synthesizer()
    verify_sequencer()
    verify_midi_driver()
    verify_midi_player()
