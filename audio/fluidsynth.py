#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Piano playing practice with MIDI keyboard.
Use this module from Kivy as a separate thread(threading.Thread).
https://www.fluidsynth.org/api/
'''

from ctypes import *
from ctypes.util import find_library
from enum import (Enum, auto)
from json import *
from time import sleep
from math import (pow, log10)

FLUID_FAILED = -1
FLUID_OK = 0

_libfs = CDLL(find_library('fluidsynth'), use_errno=True)

# Structure of data for Sequencer event callback function 
class SequencerEventCallbackData(Structure):
    pass
# Structure of data for MIDI event handler 
class MidiEventHandlerData(Structure):
    pass

# fluid_event_callback_t
# Event callback function prototype for destination clients.
FLUID_EVENT_CALLBACK_T = \
    CFUNCTYPE(None, c_uint, c_void_p, c_void_p, POINTER(SequencerEventCallbackData))
# handle_midi_event_func_t
# Generic callback function prototype for MIDI event handler.
HANDLE_MIDI_EVENT_FUNC_T = \
    CFUNCTYPE(c_int, POINTER(MidiEventHandlerData), c_void_p)
# fluid_settings_foreach_option_t
# Callback function type used with fluid_settings_foreach_option()
FLUID_SETTINGS_FOREACH_OPTION_T = \
    CFUNCTYPE(None, c_void_p, c_char_p, c_char_p)
# fluid_settings_foreach_t
# Callback function type used with fluid_settings_foreach()
FLUID_SETTINGS_FOREACH_T = \
    CFUNCTYPE(None, c_void_p, c_char_p, c_int)


# FluidSynth API prototype: Audio output

# FluidSynth API prototype: Audio output - Audio driver
new_fluid_audio_driver = \
    CFUNCTYPE(c_void_p, c_void_p, c_void_p) \
        (('new_fluid_audio_driver', _libfs),
        ((1, 'settings'), (1, 'synth')))
delete_fluid_audio_driver = \
    CFUNCTYPE(None, c_void_p) \
        (('delete_fluid_audio_driver', _libfs),
        ((1, 'driver'),))
fluid_audio_driver_register = \
    CFUNCTYPE(c_int, c_void_p) \
        (('fluid_audio_driver_register', _libfs), 
        ((1, 'adrivers'),))

# FluidSynth API prototype: Audio output - File Renderer

# FluidSynth API prototype: Command Interface

# FluidSynth API prototype: Command Interface - Command Handler
new_fluid_cmd_handler = \
    CFUNCTYPE(c_void_p, c_void_p, c_void_p) \
        (('new_fluid_cmd_handler', _libfs),
        ((1, 'synth'), (1, 'router'))) 
delete_fluid_cmd_handler = \
    CFUNCTYPE(None, c_void_p) \
        (('delete_fluid_cmd_handler', _libfs),
        ((1, 'handler'),))

# FluidSynth API prototype: Command Interface -Command Server

# FluidSynth API prototype: Command Interface -Command Shell

# FluidSynth API prototype: Logging

# FluidSynth API prototype: MIDI Input
fluid_synth_handle_midi_event = \
    CFUNCTYPE(c_int, c_void_p, c_void_p)\
        (('fluid_synth_handle_midi_event', _libfs),
        ((1, 'data'), (1, 'event')))

# FluidSynth API prototype: MIDI Input - MIDI Driver
new_fluid_midi_driver = \
    CFUNCTYPE(c_void_p, c_void_p, c_void_p, c_void_p) \
        (('new_fluid_midi_driver', _libfs),
        ((1, 'settings'), (1, 'handler'), (1, 'event_handler_data')))
delete_fluid_midi_driver = \
    CFUNCTYPE(None, c_void_p) \
        (('delete_fluid_midi_driver', _libfs),
        ((1, 'driver'),))

# FluidSynth API prototype: MIDI Input - MIDI Event

# FluidSynth API prototype: MIDI Input - MIDI File Player
class FLUID_PLAYER_SET_TEMPO_TYEP(Enum):
    INTERNAL = 0
    EXTERNAL_BPM = auto()
    EXTERNAL_MIDI = auto()
class FLUID_PLAYER_STATUS(Enum):
    READY = 0
    PLAYING = auto()
    STOPPING = auto()
    DONE = auto()
new_fluid_player = \
    CFUNCTYPE(c_void_p, c_void_p) \
        (('new_fluid_player', _libfs),
        ((1, 'synth'),))
delete_fluid_player = \
    CFUNCTYPE(None, c_void_p) \
        (('delete_fluid_player', _libfs),
        ((1, 'player'),))
fluid_player_set_playback_callback = \
    CFUNCTYPE(c_int, c_void_p, c_void_p, c_void_p) \
        (('fluid_player_set_playback_callback', _libfs),
        ((1, 'player'), (1, 'handler'), (1, 'handler_data')))
fluid_player_add = \
    CFUNCTYPE(c_int, c_void_p, c_char_p) \
        (('fluid_player_add', _libfs),
        ((1, 'player'), (1, 'midifile')))
fluid_player_play = \
    CFUNCTYPE(c_int, c_void_p) \
        (('fluid_player_play', _libfs),
        ((1, 'player'),))
fluid_player_get_status = \
    CFUNCTYPE(c_int, c_void_p) \
        (('fluid_player_get_status', _libfs),
        ((1, 'player'),))
fluid_player_stop = \
    CFUNCTYPE(c_int, c_void_p) \
        (('fluid_player_stop', _libfs),
        ((1, 'player'),))
fluid_player_join = \
    CFUNCTYPE(c_int, c_void_p) \
        (('fluid_player_join', _libfs),
        ((1, 'player'),))
fluid_player_get_total_ticks = \
    CFUNCTYPE(c_int, c_void_p) \
        (('fluid_player_get_total_ticks', _libfs),
        ((1, 'player'),))
fluid_player_get_current_tick = \
    CFUNCTYPE(c_int, c_void_p) \
        (('fluid_player_get_current_tick', _libfs),
        ((1, 'player'),))
fluid_player_seek = \
    CFUNCTYPE(c_int, c_void_p, c_int) \
        (('fluid_player_seek', _libfs),
        ((1, 'player'), (1, 'ticks')))
## Disable from version 2.2.0
fluid_player_set_midi_tempo = \
    CFUNCTYPE(c_int, c_void_p, c_int) \
        (('fluid_player_set_midi_tempo', _libfs),
        ((1, 'player'), (1, 'tempo')))

# FluidSynth API prototype: MIDI Input - MIDI Router
class FLUID_MIDI_ROUTER_RULE_TYPE(int, Enum):
    NOTE = 0
    CC = auto()
    PROG_CHANGER = auto()
    PITCH_BEND = auto()
    CHANNEL_PRESSURE = auto()
    KEY_PRESSURE = auto()
    COUNT = auto()
new_fluid_midi_router = \
    CFUNCTYPE(c_void_p, c_void_p, c_void_p, c_void_p) \
        (('new_fluid_midi_router', _libfs),
        ((1, 'settingns'), (1, 'handler'), (1, 'event_handler_data')))
delete_fluid_midi_router = \
    CFUNCTYPE(None, c_void_p) \
        (('delete_fluid_midi_router', _libfs),
        ((1, 'router'),))
fluid_midi_dump_postrouter = \
    CFUNCTYPE(c_int, c_void_p, c_void_p) \
        (('fluid_midi_dump_postrouter', _libfs),
        ((1, 'data'), (1, 'event')))
fluid_midi_dump_prerouter = \
    CFUNCTYPE(c_int, c_void_p, c_void_p) \
        (('fluid_midi_dump_prerouter', _libfs),
        ((1, 'data'), (1, 'event')))
fluid_midi_router_handle_midi_event = \
    CFUNCTYPE(c_int, c_void_p, c_void_p) \
        (('fluid_midi_router_handle_midi_event', _libfs),
        ((1, 'data'), (1, 'event')))
fluid_midi_router_clear_rules = \
    CFUNCTYPE(c_int, c_void_p) \
        (('fluid_midi_router_clear_rules', _libfs),
        ((1, 'router'),))
fluid_midi_router_set_default_rules = \
    CFUNCTYPE(c_int, c_void_p) \
        (('fluid_midi_router_set_default_rules', _libfs),
        ((1, 'router'),)) 
new_fluid_midi_router_rule = \
    CFUNCTYPE(c_void_p) \
        (('new_fluid_midi_router_rule', _libfs))
delete_fluid_midi_router_rule = \
    CFUNCTYPE(None, c_void_p) \
        (('delete_fluid_midi_router_rule', _libfs),
        ((1, 'rule'),))
fluid_midi_router_rule_set_chan = \
    CFUNCTYPE(None, c_void_p, c_int, c_int, c_float, c_int) \
        (('fluid_midi_router_rule_set_chan', _libfs),
        ((1, 'rule'), (1, 'min'), (1, 'max'), (1, 'mul'), (1, 'add')))
fluid_midi_router_rule_set_param1 = \
    CFUNCTYPE(None, c_void_p, c_int, c_int, c_float, c_int) \
        (('fluid_midi_router_rule_set_param1', _libfs),
        ((1, 'rule'), (1, 'min'), (1, 'max'), (1, 'mul'), (1, 'add')))
fluid_midi_router_rule_set_param2 = \
    CFUNCTYPE(None, c_void_p, c_int, c_int, c_float, c_int) \
        (('fluid_midi_router_rule_set_param2', _libfs),
        ((1, 'rule'), (1, 'min'), (1, 'max'), (1, 'mul'), (1, 'add')))
fluid_midi_router_add_rule = \
    CFUNCTYPE(c_int, c_void_p, c_void_p, c_int) \
        (('fluid_midi_router_add_rule', _libfs),
        ((1, 'router'), (1, 'rule'), (1, 'type')))

# FluidSynth API prototype: MIDI Sequencer
new_fluid_sequencer2 = \
    CFUNCTYPE(c_void_p, c_int) \
        (('new_fluid_sequencer2', _libfs),
        ((1, 'use_system_timer'),))
delete_fluid_sequencer = \
    CFUNCTYPE(None, c_void_p) \
        (('delete_fluid_sequencer', _libfs),
        ((1, 'seq'),))
fluid_sequencer_register_fluidsynth = \
    CFUNCTYPE(c_short, c_void_p, c_void_p) \
        (('fluid_sequencer_register_fluidsynth', _libfs),
        ((1, 'seq'),(1, 'synth')))
fluid_sequencer_register_client = \
    CFUNCTYPE(c_short, c_void_p, c_char_p, c_void_p, c_void_p)\
        (('fluid_sequencer_register_client', _libfs),
        ((1, 'seq'),(1, 'name'),(1, 'callback'),(1, 'data')))
fluid_sequencer_unregister_client = \
    CFUNCTYPE(None, c_void_p, c_short) \
        (('fluid_sequencer_unregister_client', _libfs),
        ((1, 'seq'), (1, 'id')))
fluid_sequencer_get_tick = \
    CFUNCTYPE(c_uint, c_void_p) \
        (('fluid_sequencer_get_tick', _libfs),
        ((1, 'seq'),))
fluid_sequencer_set_time_scale = \
    CFUNCTYPE(None, c_void_p, c_double) \
        (('fluid_sequencer_set_time_scale', _libfs),
        ((1, 'seq'),(1, 'scale', c_double(1000))))
fluid_sequencer_get_time_scale = \
    CFUNCTYPE(c_double, c_void_p) \
        (('fluid_sequencer_get_time_scale', _libfs),
        ((1, 'seq'),))
fluid_sequencer_send_at = \
    CFUNCTYPE(c_int, c_void_p, c_void_p, c_uint, c_int) \
        (('fluid_sequencer_send_at', _libfs),
        ((1, 'seq'), (1, 'evt'), (1, 'time'), (1, 'absolute')))

# FluidSynth API prototype: MIDI Sequencer - Sequencer Events
new_fluid_event = \
    CFUNCTYPE(c_void_p) \
        (('new_fluid_event', _libfs))
delete_fluid_event = \
    CFUNCTYPE(None, c_void_p) \
        (('delete_fluid_event', _libfs),
        ((1 ,'evt'),))
fluid_event_set_dest = \
    CFUNCTYPE(None, c_void_p, c_short) \
        (('fluid_event_set_dest', _libfs),
        ((1, 'evt'), (1, 'dest')))
fluid_event_set_source = \
    CFUNCTYPE(None, c_void_p, c_short) \
        (('fluid_event_set_source', _libfs),
        ((1, 'evt'), (1, 'src')))
fluid_event_note = \
    CFUNCTYPE(None, c_void_p, c_int, c_short, c_short, c_uint) \
        (('fluid_event_note', _libfs),
        ((1, 'evt'), (1, 'channel'), (1, 'key'), (1, 'vel'), (1, 'duration')))
fluid_event_timer = \
    CFUNCTYPE(None, c_void_p, c_void_p) \
        (('fluid_event_timer', _libfs),
        ((1, 'evt'), (1, 'data')))

# FluidSynth API prototype: Miscellaneous
fluid_version_str = \
    CFUNCTYPE(c_char_p) \
        (('fluid_version_str', _libfs))

# FluidSynth API prototype: Settings
class FLUID_TYPE(Enum):
    NO = -1
    NUM = auto()
    INT = auto()
    STR = auto()
    SET = auto()
new_fluid_settings = \
    CFUNCTYPE(c_void_p) \
        (('new_fluid_settings', _libfs))
delete_fluid_settings = \
    CFUNCTYPE(None, c_void_p) \
        (('delete_fluid_settings', _libfs),
        ((1, 'settings'),))
fluid_settings_setnum = \
    CFUNCTYPE(c_int, c_void_p, c_char_p, c_double) \
        (('fluid_settings_setnum', _libfs),
        ((1, 'settings'), (1, 'name'), (1, 'value')))
fluid_settings_getnum = \
    CFUNCTYPE(c_int, c_void_p, c_char_p, POINTER(c_double)) \
        (('fluid_settings_getnum', _libfs),
        ((1, 'settings'), (1, 'name'), (1, 'val')))
fluid_settings_getnum_default = \
    CFUNCTYPE(c_int, c_void_p, c_char_p, POINTER(c_double)) \
        (('fluid_settings_getnum_default', _libfs),
        ((1, 'settings'), (1, 'name'), (1, 'val')))
fluid_settings_getnum_range = \
    CFUNCTYPE(c_int, c_void_p, c_char_p, POINTER(c_double), POINTER(c_double)) \
        (('fluid_settings_getnum_range', _libfs),
        ((1, 'settigns'), (1, 'name'), (1, 'min'), (1, 'max')))
fluid_settings_setint = \
    CFUNCTYPE(c_int, c_void_p, c_char_p, c_int) \
        (('fluid_settings_setint', _libfs),
        ((1, 'settings'), (1, 'name'), (1, 'val')))
fluid_settings_getint = \
    CFUNCTYPE(c_int, c_void_p, c_char_p, POINTER(c_int)) \
        (('fluid_settings_getint', _libfs),
        ((1, 'settings'), (1, 'name'), (1, 'val')))
fluid_settings_getint_default = \
    CFUNCTYPE(c_int, c_void_p, c_char_p, POINTER(c_int)) \
        (('fluid_settings_getint_default', _libfs),
        ((1, 'settings'), (1, 'name'), (1, 'val')))
fluid_settings_getint_range = \
    CFUNCTYPE(c_int, c_void_p, c_char_p, POINTER(c_int), POINTER(c_int)) \
        (('fluid_settings_getint_range', _libfs),
        ((1, 'settigns'), (1, 'name'), (1, 'min'), (1, 'max')))
fluid_settings_setstr = \
    CFUNCTYPE(c_int, c_void_p, c_char_p, c_char_p) \
        (('fluid_settings_setstr', _libfs),
        ((1, 'settings'), (1, 'name'), (1, 'str')))
fluid_settings_getstr_default = \
    CFUNCTYPE(c_int, c_void_p, c_char_p, POINTER(c_char_p)) \
        (('fluid_settings_getstr_default', _libfs),
        ((1, 'settings'), (1, 'name'), (1, 'def')))
fluid_settings_copystr = \
    CFUNCTYPE(c_int, c_void_p, c_char_p, c_char_p, c_int) \
        (('fluid_settings_copystr', _libfs),
        ((1, 'settings'), (1, 'name'), (1, 'str'), (1, 'len')))
fluid_settings_foreach = \
    CFUNCTYPE(None, c_void_p, c_void_p, c_void_p) \
        (('fluid_settings_foreach', _libfs),
        ((1, 'settings'), (1, 'data'), (1, 'func')))
fluid_settings_foreach_option = \
    CFUNCTYPE(None, c_void_p, c_char_p, c_void_p, c_void_p) \
        (('fluid_settings_foreach_option', _libfs),
        ((1, 'settings'),(1, 'name'),(1, 'data'),(1, 'func')))
fluid_settings_get_hints = \
    CFUNCTYPE(c_int, c_void_p, c_char_p, POINTER(c_int)) \
        (('fluid_settings_get_hints', _libfs),
        ((1, 'settings'), (1, 'name'), (1, 'hints')))

# FluidSynth API prototype: SoundFonts
# FluidSynth API prototype: SoundFonts - SoundFont Generators
# FluidSynth API prototype: SoundFonts - SoundFont Loader
fluid_synth_get_channel_preset = \
    CFUNCTYPE(c_void_p, c_void_p, c_int) \
        (('fluid_synth_get_channel_preset', _libfs),
        ((1, 'synth'),(1, 'chan')))
fluid_sfont_get_preset = \
    CFUNCTYPE(c_void_p, c_void_p, c_int, c_int) \
        (('fluid_sfont_get_preset', _libfs),
        ((1, 'sfont'), (1, 'bank'), (1, 'prenum')))
fluid_preset_get_banknum = \
    CFUNCTYPE(c_int, c_void_p) \
        (('fluid_preset_get_banknum', _libfs),
        ((1, 'preset'),))
fluid_preset_get_name = \
    CFUNCTYPE(c_char_p, c_void_p) \
        (('fluid_preset_get_name', _libfs),
        ((1, 'preset'),))
fluid_preset_get_num = \
    CFUNCTYPE(c_int, c_void_p) \
        (('fluid_preset_get_num', _libfs),
        ((1, 'preset'),))
fluid_preset_get_sfont = \
    CFUNCTYPE(c_void_p, c_void_p) \
        (('fluid_preset_get_sfont', _libfs),
        ((1, 'preset'),))
fluid_sfont_get_id = \
    CFUNCTYPE(c_int, c_void_p) \
        (('fluid_sfont_get_id', _libfs),
        ((1, 'sfont'),))
# FluidSynth API prototype: SoundFonts - SoundFont Modulators
# FluidSynth API prototype: SoundFonts - SoundFont Maniplation

# FluidSynth API prototype: Synthesizer
new_fluid_synth = \
    CFUNCTYPE(c_void_p, c_void_p) \
        (('new_fluid_synth', _libfs), 
        ((1, 'settings'),))
delete_fluid_synth = \
    CFUNCTYPE(None, c_void_p) \
        (('delete_fluid_synth', _libfs),
        ((1, 'synth'),))

# FluidSynth API prototype: Synthesizer - Audio Rendering
# FluidSynth API prototype: Synthesizer - Effect - Chorus
# FluidSynth API prototype: Synthesizer - Effect - IIR Filter
# FluidSynth API prototype: Synthesizer - Effect - LADSPA
# FluidSynth API prototype: Synthesizer - Effect - Reverb

# FluidSynth API prototype: Synthesizer - MIDI Channel Messages
fluid_synth_cc = \
    CFUNCTYPE(c_int, c_void_p, c_int, c_int, c_int) \
        (('fluid_synth_cc', _libfs),
        ((1, 'synth'), (1, 'chan'), (1, 'num'), (1, 'val')))
fluid_synth_get_cc = \
    CFUNCTYPE(c_int, c_void_p, c_int, c_int, POINTER(c_int)) \
        (('fluid_synth_get_cc', _libfs),
        ((1, 'synth'), (1, 'chan'), (1, 'num'), (1, 'pval')))
fluid_synth_pitch_bend = \
    CFUNCTYPE(c_int, c_void_p, c_int, c_int) \
        (('fluid_synth_pitch_bend', _libfs),
        ((1, 'synth'), (1, 'chan'), (1, 'val')))
fluid_synth_get_pitch_bend = \
    CFUNCTYPE(c_int, c_void_p, c_int, POINTER(c_int)) \
        (('fluid_synth_get_pitch_bend', _libfs),
        ((1, 'synth'), (1, 'chan'), (1, 'ppitch_bend')))
fluid_synth_pitch_wheel_sens = \
    CFUNCTYPE(c_int, c_void_p, c_int, c_int) \
        (('fluid_synth_pitch_wheel_sens', _libfs),
        ((1, 'synth'), (1, 'chan'), (1, 'val')))
fluid_synth_get_pitch_wheel_sens = \
    CFUNCTYPE(c_int, c_void_p, c_int, POINTER(c_int)) \
        (('fluid_synth_get_pitch_wheel_sens', _libfs),
        ((1, 'synth'), (1, 'chan'), (1, 'pval')))
fluid_synth_sysex = \
    CFUNCTYPE(c_int, c_void_p, c_char_p, c_int, c_char_p, POINTER(c_int), POINTER(c_int), c_int) \
        (('fluid_synth_sysex', _libfs),
        ((1, 'synth'), (1, 'data'), (1, 'len'), (1, 'response'), (1, 'response_len'), (1, 'handled'), (1, 'dryrun')))
fluid_synth_program_select = \
    CFUNCTYPE(c_int, c_void_p, c_int, c_int, c_int, c_int) \
        (('fluid_synth_program_select', _libfs),
        ((1, 'synth'), (1, 'chan'), (1, 'sfont_id'), (1, 'bank_num'), (1, 'preset_num')))
fluid_synth_noteon = \
    CFUNCTYPE(c_int, c_void_p, c_int, c_int, c_int) \
        (('fluid_synth_noteon', _libfs),
        ((1, 'synth'), (1, 'chan'), (1, 'key'), (1, 'vel')))
fluid_synth_noteoff = \
    CFUNCTYPE(c_int, c_void_p, c_int, c_int) \
        (('fluid_synth_noteoff', _libfs),
        ((1, 'synth'), (1, 'chan'), (1, 'key')))

# FluidSynth API prototype: Synthesizer - MIDI Channel Setup
# FluidSynth API prototype: Synthesizer - MIDI Tuning

# FluidSynth API prototype: Synthesizer - SoundFont managiment
fluid_synth_sfload = \
    CFUNCTYPE(c_void_p, c_void_p, c_char_p, c_int) \
        (('fluid_synth_sfload', _libfs),
        ((1, 'synth'),(1, 'filename'),(1, 'reset_preset')))
fluid_synth_sfcount = \
    CFUNCTYPE(c_int, c_void_p) \
        (('fluid_synth_sfcount', _libfs), 
        ((1, 'synth'),))
fluid_synth_get_sfont = \
    CFUNCTYPE(c_void_p, c_void_p, c_uint) \
        (('fluid_synth_get_sfont', _libfs),
        ((1, 'synth'), (1, 'num')))
fluid_synth_get_sfont_by_id = \
    CFUNCTYPE(c_void_p, c_void_p, c_int) \
        (('fluid_synth_get_sfont_by_id', _libfs),
        ((1, 'synth'), (1, 'id')))

# FluidSynth API prototype: Synthesizer - Synthesis Parameters
fluid_synth_get_gain = \
    CFUNCTYPE(c_float, c_void_p) \
        (('fluid_synth_get_gain', _libfs),
        ((1, 'synth'), ))
fluid_synth_set_gain = \
    CFUNCTYPE(c_void_p, c_void_p, c_float) \
        (('fluid_synth_set_gain', _libfs),
        ((1, 'synth'), (1, 'gain')))

# FluidSynth API prototype: Synthesizer - Voice Control

class SynthesizerFS:
    ''' Send MIDI events to the synthesizer. '''
    settings = c_void_p()
    audio_driver = c_void_p()
    soundfont_ids = list()

    def __init__(self, **kwargs) -> None:
        self._set_audio_driver_options()

        self.settings = new_fluid_settings()

        if 'settings' in kwargs:
            with open(kwargs['settings'], 'r') as fp:
                settings_json = load(fp)

            for name, sd in settings_json.items():
                if sd['value'] is not None:
                    if FLUID_TYPE(sd['type']) == FLUID_TYPE.NUM:
                        fluid_settings_setnum(
                            self.settings, name.encode(), c_double(sd['value']))
                    elif FLUID_TYPE(sd['type']) == FLUID_TYPE.INT:
                        fluid_settings_setint(
                            self.settings, name.encode(), sd['value'])
                    elif FLUID_TYPE(sd['type']) == FLUID_TYPE.STR:
                        fluid_settings_setstr(
                            self.settings, name.encode(), sd['value'].encode())
                    else:
                        pass

        self.synthesizer = new_fluid_synth(self.settings)

        if 'soundfont' in kwargs:
            self.soundfont_ids += \
                [fluid_synth_sfload(
                    self.synthesizer, kwargs['soundfont'].encode(), True)]
        else:
            fn_soundfont = c_char_p()
            if fluid_settings_getstr_default(
                    self.settings,
                    b'synth.default-soundfont',
                    byref(fn_soundfont)) is FLUID_OK:
                self.soundfont_ids += \
                    [fluid_synth_sfload(
                        self.synthesizer, fn_soundfont, True)]

        self._gm_system_on()

        if type(self) == SynthesizerFS:
            self._assign_audio_driver()
        print(self.vesion())

    def __del__(self) -> None:
        if type(self) == SynthesizerFS:
            self._delete_auido_driver()
        delete_fluid_synth(self.synthesizer)
        delete_fluid_settings(self.settings)
        print('good-bye')

    def _set_audio_driver_options(self):
        ''' Register to avoid warnings by sdl2 audio driver. '''
        audio_drivers = (b'jack', b'alsa', b'pulseaudio', None)
        p_array = (c_char_p * len(audio_drivers))(*audio_drivers)
        fluid_audio_driver_register(byref(p_array))

    def _assign_audio_driver(self):
        self.audio_driver = new_fluid_audio_driver(self.settings, self.synthesizer)

    def _delete_auido_driver(self):
        delete_fluid_audio_driver(self.audio_driver)
    
    def vesion(self) -> str:
        return(fluid_version_str().decode())
    
    def _gm_system_on(self) -> int:
        print('gm system on')
        result = fluid_synth_sysex(
            synth=self.synthesizer,
            data=(c_char*3)(0x7E, 0x09, 0x01),
            len=3,
            response=None,
            response_len=None,
            handled=None,
            dryrun=False)
        return(result)

    def gain(self, value:float=None) -> float:
        if value != None:
            fluid_synth_set_gain(self.synthesizer, value)
        return(fluid_synth_get_gain(self.synthesizer))

    def sfonts_preset(self, is_percussion:bool = False) -> list:
        result = list()
        ''' GM system level 1'''
        bank = 0 if not(is_percussion) else 128
        for n in range(fluid_synth_sfcount(self.synthesizer)):
            sfont = fluid_synth_get_sfont(self.synthesizer, n)
            result += [self._sfont_preset(sfont, bank)]
        return(result)

    def _sfont_preset(self, sfont: c_void_p, bank:int) -> list:
        result = list()
        for n in range(128):
            preset = fluid_sfont_get_preset(sfont, bank, n)
            result += [self._preset(preset)]
        return(result)

    def channels_preset(self) -> list:
        result = list()
        for chan in range(15):
            result += [self._channel_preset(chan)]
        return(result)

    def _channel_preset(self, chan: int) -> dict:
        preset = fluid_synth_get_channel_preset(self.synthesizer, chan)
        return(self._preset(preset))
    
    def _preset(self, preset:int) -> dict:
        result = dict()
        if preset:
            result['name'] = fluid_preset_get_name(preset).decode()
            result['num'] = fluid_preset_get_num(preset)
            result['bank'] = fluid_preset_get_banknum(preset)
            result['sfont_id'] = fluid_sfont_get_id(fluid_preset_get_sfont(preset))
        else:
            result['name'] = None
            result['num'] = None
            result['bank'] = None
            result['sfont_id'] = None
        return(result)

    def pitch_bend(self, chan:int, val:int) -> int:
        return(fluid_synth_pitch_bend(self.synthesizer, chan, val))

    def pitch_wheel_sens(self, chan:int, val:int) ->int:
        return(fluid_synth_pitch_wheel_sens(self.synthesizer,chan, val))

    def program_select(self, chan:int, sfont_id:int, bank:int, preset:int) -> int:
        return(fluid_synth_program_select(self.synthesizer, chan, sfont_id, bank, preset))

    def note_on(self, channel: int, keyNumber: int, velocity: int) -> int:
        return(fluid_synth_noteon(self.synthesizer, channel, keyNumber, velocity))

    def note_off(self, channel: int, keyNumber: int) -> int:
        return(fluid_synth_noteoff(self.synthesizer, channel, keyNumber))

    def modulation_wheel(self, chan:int, val:int) -> int:
        ''' The sound amplifies like vibrato. '''
        return(fluid_synth_cc(self.synthesizer, chan, int(0x01), val))

    def volume(self, chan:int, val:int) -> int:
        ''' Set the maximum allowable value of velocity. '''
        return(fluid_synth_cc(self.synthesizer, chan, int(0x07), val))

    def sustain_on(self, chan: int) -> int:
        ''' The sound echoes for a long time. '''
        return(fluid_synth_cc(self.synthesizer, chan, int(0x40), int(0b00100000)))

    def sustain_off(self, chan: int) -> int:
        return(fluid_synth_cc(self.synthesizer, chan, int(0x40), int(0b00000000)))
    
    def pan(self, chan:int, val:int) -> int:
        return(fluid_synth_cc(self.synthesizer, chan, int(0x0A), val))

    def expression(self, chan:int, val:int) -> int:
        ''' Temporary velocity can be set above volume '''
        return(fluid_synth_cc(self.synthesizer, chan, int(0x0B), val))


class SequencerFS(SynthesizerFS):
    ''' Send MIDI events scheduled by the sequencer to the synthesizer. '''
    quaternote = 240
    bps = 120
    sequencer = c_void_p()
    client_callbacks = list()
    client_ids = list()

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.sequencer = new_fluid_sequencer2(False)
        self.client_ids += \
            [fluid_sequencer_register_fluidsynth(self.sequencer, self.synthesizer)]
        fluid_sequencer_set_time_scale(
            self.sequencer, c_double(self.quaternote / (60 / self.bps)))
        self._assign_audio_driver()
    
    def __del__(self) -> None:
        self._delete_auido_driver()
        for i in reversed(self.client_ids):
            fluid_sequencer_unregister_client(self.sequencer, i)
        delete_fluid_sequencer(self.sequencer)
        super().__del__()
    
    def register_client(
            self, name: c_char_p, callback: c_void_p, data: c_void_p = None) -> c_short:
        self.client_ids += \
            [fluid_sequencer_register_client(
                self.sequencer, name.encode(), callback, data)]
        self.client_callbacks += [callback]
        return(self.client_ids[len(self.client_ids) - 1])

    def time_scale(self) -> float:
        return(fluid_sequencer_get_time_scale(self.sequencer))

    def set_bps(self, bps: float) -> None:
        ''' Set the time scale of a sequencer. "time_scale" in ticks per second '''
        self.bps = bps
        fluid_sequencer_set_time_scale(
            self.sequencer, c_double(self.quaternote / (60 / self.bps)))
    
    def synthesizer_client_id(self) -> int:
        return(self.client_ids[0])

    def tick(self) -> int:
        ''' Get the current tick of the sequencer scaled by the time scale currently set '''
        return(fluid_sequencer_get_tick(self.sequencer))
        
    def note_at(
            self,
            ticks: c_uint,
            channel: c_uint,
            key_number: c_short,
            velocity: c_short,
            duration: c_uint,
            source: c_short = -1,
            destination: c_short = -1,
            absolute: bool = True) -> None:
        event = self._assign_event(source, destination)
        fluid_event_note(event, channel, key_number, velocity, duration)
        self._send_event_at(event, ticks, absolute)

    def timer_at(
            self,
            ticks: c_uint,
            data: POINTER(SequencerEventCallbackData) = None,
            source: c_short = -1,
            destination: c_short = -1,
            absolute: bool = True) -> None:
        event = self._assign_event(source, destination)
        fluid_event_timer(event, data)
        self._send_event_at(event, ticks, absolute)

    def _assign_event(self, source: c_short, destination: c_short) -> c_void_p:
        event = new_fluid_event()
        fluid_event_set_source(event, source)
        fluid_event_set_dest(event, destination)
        return(event)

    def _send_event_at(self, event: c_void_p, ticks: c_uint, absolute: bool) -> None:
        result = fluid_sequencer_send_at(self.sequencer, event, ticks, absolute)
        delete_fluid_event(event)

class MidiRouterFS(SynthesizerFS):
    ''' Rule based transformation and filtering of MIDI events. '''
    midi_router = c_void_p()
    cmd_handler = c_void_p()

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        handler = fluid_synth_handle_midi_event
        self.midi_router = \
            new_fluid_midi_router(self.settings, handler, self.synthesizer)
        self.cmd_handler = \
            new_fluid_cmd_handler(self.synthesizer, self.midi_router)

    def __del__(self) -> None:
        delete_fluid_cmd_handler(self.cmd_handler)
        delete_fluid_midi_router(self.midi_router)
        super().__del__()

    def apply_default_rules(self) -> None:
        fluid_midi_router_clear_rules(self.midi_router)
        fluid_midi_router_set_default_rules(self.midi_router)

    def change_rule(self, rule_file:str) -> int:
        fluid_midi_router_clear_rules(self.midi_router)
        
        with open(rule_file, 'r') as fp:
            rules_json = load(fp)

        for rd in rules_json.values():
            rule = new_fluid_midi_router_rule()
            if rd['chan'] is not None:
                fluid_midi_router_rule_set_chan(rule, *rd['chan'].values())
            if rd['param1'] is not None:
                fluid_midi_router_rule_set_param1(rule, *rd['param1'].values())
            if rd['param2'] is not None:
                fluid_midi_router_rule_set_param2(rule, *rd['param2'].values())
            fluid_midi_router_add_rule(self.midi_router, rule, rd['type'])
        return(FLUID_OK)

class MidiDriverFS(MidiRouterFS):
    ''' Sends MIDI events received at the MIDI input to the synthesizer. '''
    midi_driver = c_void_p()

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        if 'handler' in kwargs:
            callback = kwargs['handler']
        else:
            callback = fluid_midi_router_handle_midi_event
        self.midi_driver = \
            new_fluid_midi_driver(self.settings, callback, self.midi_router)
        self._assign_audio_driver()

    def __del__(self) -> None:
        self._delete_auido_driver()
        delete_fluid_midi_driver(self.midi_driver)
        super().__del__()

class MidiPlayerFS(MidiRouterFS):
    ''' Parse standard MIDI files and emit MIDI events. '''
    player = c_void_p()
    pause_tick = int()

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.player = new_fluid_player(self.synthesizer)
        
        if 'handler' in kwargs:
            callback = kwargs['handler']
        else:
            callback = fluid_midi_router_handle_midi_event
        fluid_player_set_playback_callback(self.player, callback, self.midi_router)
        self._assign_audio_driver()
    
    def __del__(self) -> None:
        self._delete_auido_driver()
        delete_fluid_player(self.player)
        super().__del__()
    
    def play(self, midifile:str, wait:bool=True) -> None:
        status = fluid_player_get_status(self.player)
        if FLUID_PLAYER_STATUS(status) is FLUID_PLAYER_STATUS.STOPPING:
            fluid_player_add(self.player, midifile.encode())
            fluid_player_play(self.player)
            if wait:
                fluid_player_join(self.player)
    
    def restart(self) -> None:
        status = fluid_player_get_status(self.player)
        if FLUID_PLAYER_STATUS(status) is FLUID_PLAYER_STATUS.STOPPING:
            fluid_player_seek(self.player, self.pause_tick)
            fluid_player_play(self.player)

    def stop(self) -> None:
        status = fluid_player_get_status(self.player)
        if any([
                FLUID_PLAYER_STATUS(status) is FLUID_PLAYER_STATUS.PLAYING,
                FLUID_PLAYER_STATUS(status) is FLUID_PLAYER_STATUS.STOPPING
            ]):
            fluid_player_stop(self.player)
            fluid_player_seek(self.player, fluid_player_get_total_ticks(self.player))
            fluid_player_join(self.player)
    
    def pause(self) -> None:
        status = fluid_player_get_status(self.player)
        if FLUID_PLAYER_STATUS(status) is FLUID_PLAYER_STATUS.PLAYING:
            self.pause_tick = fluid_player_get_current_tick(self.player)
            fluid_player_stop(self.player)

    def cueing(self, midifile:str, duration:float) -> None:
        self.play(midifile=midifile, wait=False)
        sleep(duration)
        self.stop()

if __name__ == '__main__':
    print('fluidsynth')