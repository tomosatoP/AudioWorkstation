#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from concurrent import futures
from functools import partial
import ctypes as C
from time import sleep
from typing import Callable
from pathlib import Path


from src.audioworkstation.libs.audio import amixer as MASTER
from src.audioworkstation.libs.audio import fluidsynth as FS


@FS.HANDLE_MIDI_EVENT_FUNC_T
def midi_event_handler(data, event) -> int:
    '''test custum MIDI Router handler'''
    try:
        FS.fluid_midi_dump_prerouter(data, event)
    except FS.FSError as mes:
        FS.fluid_log(level=FS.FLUID_LOG_LEVEL.WARN,
                     fmt=b'%s',
                     message=b'midi event ' + str(mes).encode())
        return (FS.FLUID_FAILED)
    return (FS.FLUID_OK)


FS.EventUserData._fields_ = [('quit', C.c_bool),
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
                        destination=sfs.clients[0])
            time_marker += beat

    sfs.timer_at(ticks=time_marker, destination=sfs.clients[1])
    return (True)


@FS.FLUID_EVENT_CALLBACK_T
def client_callback(time, event, sequencer, p_data):
    if not p_data.contents.quit:
        metronome_pattern(p_data.contents)


def future_callback(func: Callable[..., None], future: futures.Future) -> bool:
    func()
    return (future.done())


class TestFluidsynth(unittest.TestCase):

    def setUp(self) -> None:
        MASTER.start()
        MASTER.volume('50%,50%')
        return super().setUp()

    def test_synthesizer(self):
        '''test class FS.SynthesizerFS'''
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

    def test_midi_driver(self):
        '''test class MidiDriverFS'''
        kwargs = {
            'settings': 'config/settings.json',
            'soundfont': ['sf2/FluidR3_GM.sf2',
                          'sf2/SGM-V2.01.sf2']}
        # 'handler': midi_event_handler}

        mdfs = FS.MidiDriver(**kwargs)
        print(f'gain: {mdfs.gain:.1f}')

        mdfs.apply_rules()
        print('default rule')
        sleep(5)

        mdfs.apply_rules('config/rule.mute_chan_0.json')
        print('mute channel 0')
        sleep(5)

        mdfs.note_on(9, 34, 80)
        sleep(0.5)
        del mdfs

    def test_sequencer(self):
        '''test class SequencerFS'''
        global sfs
        kwargs = {
            'settings': 'config/settings.json',
            'soundfont': ['sf2/FluidR3_GM.sf2']}

        sfs = FS.Sequencer(**kwargs)
        print(f'gain: {sfs.gain:.1f}')

        data = FS.EventUserData()
        sfs.register_client('metronome', client_callback, data)

        for i in sfs.clients:
            print(sfs.client_name(id=i))

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

    def test_midi_player(self):
        # test class MidiPlayerFS

        kwargs = {
            'settings': 'config/settings.json',
            'soundfont': ['sf2/FluidR3_GM.sf2',
                          'sf2/SGM-V2.01.sf2',
                          'sf2/YDP-GrandPiano-20160804.sf2']}

        mpfs = FS.MidiPlayer(**kwargs)
        mpfs.apply_rules('config/rule.mute_chan_0.json')
        mpfs.gain = 0.3
        print(f'gain: {mpfs.gain:.1f}')

        extension: list[str] = ['.mid', '.MID']
        files: list = [i for i in Path().glob(
            'mid/*.*') if i.suffix in extension]

        with futures.ThreadPoolExecutor(max_workers=1) as e:
            tick: int = 10000
            for fo in files:
                print(fo.name)
                f = e.submit(mpfs.start, 'mid/' + fo.name, tick)
                f.add_done_callback(partial(future_callback, mpfs.close))
                sleep(2)
                tick = mpfs.stop()
                sleep(0.1)

            filename = 'mid/SenBonZakura.mid'
            f = e.submit(mpfs.start, filename, 140000)
            f.add_done_callback(partial(future_callback, mpfs.close))

        print('channel preset')
        for sound_set in mpfs.channels_preset():
            print(sound_set)
        print(mpfs.soundfonts)

        mpfs.note_on(9, 34, 80)
        sleep(0.5)
        del mpfs
