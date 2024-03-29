#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Piano playing practice with MIDI keyboard.

Use this module from Kivy as a separate thread.

Module 'concurrent.futures.ThreadPoolExecutor' is recommended.

:referrence: https://www.fluidsynth.org/api/
"""

from typing import Union, Callable, Any
from enum import IntEnum, IntFlag, auto
from json import load
from time import sleep
from ctypes.util import find_library
import logging as LFS
import ctypes as CFS
from pathlib import Path

# Logger
logger = LFS.getLogger(__name__)
# level: NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL
logger.setLevel(LFS.WARNING)
_logger_formatter = LFS.Formatter("%(asctime)s %(levelname)s %(message)s")
# Logger FileHandler
_logger_fh = LFS.FileHandler("logs/fluidsynth.log")
_logger_fh.setFormatter(_logger_formatter)
logger.addHandler(_logger_fh)
# Logger StreamHandler
_logger_sh = LFS.StreamHandler()
_logger_sh.setFormatter(_logger_formatter)
logger.addHandler(_logger_sh)

# fluidsynth
FLUID_FAILED = -1
FLUID_OK = 0

# Handle exception


class FSError(Exception):
    """Exceptions sent out from errcheck func."""

    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        logger.error(f"FSError: {args}")


def _errcheck(result: Any, cfunc: Callable, args: tuple) -> Any:
    if result == FLUID_FAILED:
        raise FSError((cfunc, args))
    return result


"""libfluidsynth"""
_libfs = CFS.CDLL(name=find_library(name="fluidsynth"), use_errno=True)


def _prototype(restype: Any, name: str, *params: tuple) -> Any:
    """Returns a foreign function exported by a shared library.

    :param Any restype: foreign function restype
    :param str name: foreign function name
    :param tuple params: type, flag, name[, default]

    :return: foreign function object
    """
    if hasattr(_libfs, name):
        argtypes: list = list([])
        paramflags: list = list([])
        for param in params:
            argtypes.append(param[0])
            paramflags.append(param[1:])
        func_spec = (name, _libfs)
        return CFS.CFUNCTYPE(restype, *argtypes, use_errno=True)(
            func_spec, tuple(paramflags)
        )
    else:
        return None


# Audio output
# Audio output - Audio driver
# [API prototype]
new_fluid_audio_driver = _prototype(
    CFS.c_void_p,
    "new_fluid_audio_driver",
    (CFS.c_void_p, 1, "settings"),
    (CFS.c_void_p, 1, "synth"),
)
new_fluid_audio_driver.errcheck = _errcheck

delete_fluid_audio_driver = _prototype(
    None, "delete_fluid_audio_driver", (CFS.c_void_p, 1, "driver")
)

fluid_audio_driver_register = _prototype(
    CFS.c_int, "fluid_audio_driver_register", (CFS.POINTER(CFS.c_char_p), 1, "adrivers")
)
fluid_audio_driver_register.errcheck = _errcheck

# Audio output - File Renderer

# Command Interface
# Command Interface - Command Handler
# [API prototype]
new_fluid_cmd_handler = _prototype(
    CFS.c_void_p,
    "new_fluid_cmd_handler",
    (CFS.c_void_p, 1, "synth"),
    (CFS.c_void_p, 1, "router"),
)
new_fluid_cmd_handler.errcheck = _errcheck

delete_fluid_cmd_handler = _prototype(
    None, "delete_fluid_cmd_handler", (CFS.c_void_p, 1, "handler")
)

# Command Interface - Command Server
# Command Interface - Command Shell

# Logging
# [ENUM]


class FLUID_LOG_LEVEL(IntEnum):
    PANIC = 0
    ERR = auto()
    WARN = auto()
    INFO = auto()
    DBG = auto()
    LAST_LOG_LEVEL = auto()


# [user defined data type]


class LogUserData(CFS.Structure):
    """Structure of data for Log function handler"""

    pass


# [Typedef]
FLUID_LOG_FUNCTION_T = CFS.CFUNCTYPE(
    None, CFS.c_int, CFS.c_char_p, CFS.POINTER(LogUserData)
)
"""Log function handler callback type used by fluid_set_log_function()

:param c_int level:
:param c_char_p message:
:param POINTER(LogUserData) data:
"""
# [API prototype]
fluid_default_log_function = _prototype(
    None,
    "fluid_default_log_function",
    (CFS.c_int, 1, "level"),
    (CFS.c_char_p, 1, "message"),
    (CFS.POINTER(LogUserData), 1, "data"),
)

fluid_log = _prototype(
    CFS.c_int,
    "fluid_log",
    (CFS.c_int, 1, "level"),
    (CFS.c_char_p, 1, "fmt"),
    (CFS.c_char_p, 1, "message"),
)

fluid_set_log_function = _prototype(
    FLUID_LOG_FUNCTION_T,
    "fluid_set_log_function",
    (CFS.c_int, 1, "level"),
    (FLUID_LOG_FUNCTION_T, 1, "fun"),
    (CFS.POINTER(LogUserData), 1, "data"),
)
fluid_set_log_function.errcheck = _errcheck

# [user function]


@FLUID_LOG_FUNCTION_T
def _log_func(level, message, data) -> None:
    mes = bytes(message).decode()
    if int(level) == FLUID_LOG_LEVEL.PANIC:
        logger.critical(f"{mes}")
    elif int(level) == FLUID_LOG_LEVEL.ERR:
        logger.error(f"{mes}")
    elif int(level) == FLUID_LOG_LEVEL.WARN:
        logger.warning(f"{mes}")
    elif int(level) == FLUID_LOG_LEVEL.INFO:
        logger.info(f"{mes}")
    elif int(level) == FLUID_LOG_LEVEL.DBG:
        logger.debug(f"{mes}")


# MIDI Input
# [typedef] handle_midi_event_func_t
HANDLE_MIDI_EVENT_FUNC_T = CFS.CFUNCTYPE(CFS.c_int, CFS.c_void_p, CFS.c_void_p)
"""Generic callback function prototype for MIDI event handler.

:param c_void_p data:
:param c_void_p event:

:return:
"""
# [API prototype]
fluid_synth_handle_midi_event = _prototype(
    CFS.c_int,
    "fluid_synth_handle_midi_event",
    (CFS.c_void_p, 1, "data"),
    (CFS.c_void_p, 1, "event"),
)
fluid_synth_handle_midi_event.errcheck = _errcheck

# MIDI Input - MIDI Driver
# [API prototype]
new_fluid_midi_driver = _prototype(
    CFS.c_void_p,
    "new_fluid_midi_driver",
    (CFS.c_void_p, 1, "settings"),
    (CFS.c_void_p, 1, "handler"),
    (CFS.c_void_p, 1, "event_handler_data"),
)
new_fluid_midi_driver.errcheck = _errcheck

delete_fluid_midi_driver = _prototype(
    None, "delete_fluid_midi_driver", (CFS.c_void_p, 1, "driver")
)

# MIDI Input - MIDI Event
# MIDI Input - MIDI File Player
# [ENUM]


class FLUID_PLAYER_SET_TEMPO_TYEP(IntEnum):  # Available from version 2.2.0
    INTERNAL = 0
    EXTERNAL_BPM = auto()
    EXTERNAL_MIDI = auto()


class FLUID_PLAYER_STATUS(IntEnum):
    READY = 0
    PLAYING = auto()
    # STOPPING = auto()  # Available from version 2.2.0
    DONE = auto()


# [API prototype]
new_fluid_player = _prototype(
    CFS.c_void_p, "new_fluid_player", (CFS.c_void_p, 1, "synth")
)
new_fluid_player.errcheck = _errcheck

delete_fluid_player = _prototype(
    None, "delete_fluid_player", (CFS.c_void_p, 1, "player")
)

fluid_player_set_playback_callback = _prototype(
    CFS.c_int,
    "fluid_player_set_playback_callback",
    (CFS.c_void_p, 1, "player"),
    (CFS.c_void_p, 1, "handler"),
    (CFS.c_void_p, 1, "handler_data"),
)
fluid_player_set_playback_callback.errcheck = _errcheck

fluid_player_add = _prototype(
    CFS.c_int,
    "fluid_player_add",
    (CFS.c_void_p, 1, "player"),
    (CFS.c_char_p, 1, "midifile"),
)
fluid_player_add.errcheck = _errcheck

fluid_player_add_mem = _prototype(
    CFS.c_int,
    "fluid_player_add_mem",
    (CFS.c_void_p, 1, "player"),
    (CFS.POINTER(CFS.c_char), 1, "buffer"),
    (CFS.c_size_t, 1, "len"),
)
fluid_player_add_mem.errcheck = _errcheck

fluid_player_play = _prototype(
    CFS.c_int, "fluid_player_play", (CFS.c_void_p, 1, "player")
)
fluid_player_play.errcheck = _errcheck

fluid_player_get_status = _prototype(
    CFS.c_int, "fluid_player_get_status", (CFS.c_void_p, 1, "player")
)
fluid_player_get_status.errcheck = _errcheck

fluid_player_stop = _prototype(
    CFS.c_int, "fluid_player_stop", (CFS.c_void_p, 1, "player")
)
fluid_player_stop.errcheck = _errcheck

fluid_player_join = _prototype(
    CFS.c_int, "fluid_player_join", (CFS.c_void_p, 1, "player")
)
fluid_player_join.errcheck = _errcheck

fluid_player_get_total_ticks = _prototype(
    CFS.c_int, "fluid_player_get_total_ticks", (CFS.c_void_p, 1, "player")
)
fluid_player_get_total_ticks.errcheck = _errcheck

fluid_player_get_current_tick = _prototype(
    CFS.c_int, "fluid_player_get_current_tick", (CFS.c_void_p, 1, "player")
)
fluid_player_get_current_tick.errcheck = _errcheck

fluid_player_seek = _prototype(
    CFS.c_int, "fluid_player_seek", (CFS.c_void_p, 1, "player"), (CFS.c_int, 1, "ticks")
)
fluid_player_seek.errcheck = _errcheck

fluid_player_set_loop = _prototype(
    CFS.c_int,
    "fluid_player_set_loop",
    (CFS.c_void_p, 1, "player"),
    (CFS.c_int, 1, "loop"),
)
fluid_player_set_loop.errcheck = _errcheck


# MIDI Input - MIDI Router
# [ENUM]


class FLUID_MIDI_ROUTER_RULE_TYPE(IntEnum):
    NOTE = 0
    CC = auto()
    PROG_CHANGER = auto()
    PITCH_BEND = auto()
    CHANNEL_PRESSURE = auto()
    KEY_PRESSURE = auto()
    COUNT = auto()


# [API prototype]
new_fluid_midi_router = _prototype(
    CFS.c_void_p,
    "new_fluid_midi_router",
    (CFS.c_void_p, 1, "settings"),
    (CFS.c_void_p, 1, "handler"),
    (CFS.c_void_p, 1, "event_handler_data"),
)
new_fluid_midi_router.errcheck = _errcheck

delete_fluid_midi_router = _prototype(
    None, "delete_fluid_midi_router", (CFS.c_void_p, 1, "router")
)

fluid_midi_dump_postrouter = _prototype(
    CFS.c_int,
    "fluid_midi_dump_postrouter",
    (CFS.c_void_p, 1, "data"),
    (CFS.c_void_p, 1, "event"),
)
fluid_midi_dump_postrouter.errcheck = _errcheck

fluid_midi_dump_prerouter = _prototype(
    CFS.c_int,
    "fluid_midi_dump_prerouter",
    (CFS.c_void_p, 1, "data"),
    (CFS.c_void_p, 1, "event"),
)
fluid_midi_dump_prerouter.errcheck = _errcheck

fluid_midi_router_handle_midi_event = _prototype(
    CFS.c_int,
    "fluid_midi_router_handle_midi_event",
    (CFS.c_void_p, 1, "data"),
    (CFS.c_void_p, 1, "event"),
)
fluid_midi_router_handle_midi_event.errcheck = _errcheck

fluid_midi_router_clear_rules = _prototype(
    CFS.c_int, "fluid_midi_router_clear_rules", (CFS.c_void_p, 1, "router")
)
fluid_midi_router_clear_rules.errcheck = _errcheck

fluid_midi_router_set_default_rules = _prototype(
    CFS.c_int, "fluid_midi_router_set_default_rules", (CFS.c_void_p, 1, "router")
)
fluid_midi_router_set_default_rules.errcheck = _errcheck

new_fluid_midi_router_rule = _prototype(CFS.c_void_p, "new_fluid_midi_router_rule")
new_fluid_midi_router_rule.errcheck = _errcheck

delete_fluid_midi_router_rule = _prototype(
    None, "delete_fluid_midi_router_rule", (CFS.c_void_p, 1, "rule")
)

fluid_midi_router_rule_set_chan = _prototype(
    None,
    "fluid_midi_router_rule_set_chan",
    (CFS.c_void_p, 1, "rule"),
    (CFS.c_int, 1, "min"),
    (CFS.c_int, 1, "max"),
    (CFS.c_float, 1, "mul"),
    (CFS.c_int, 1, "add"),
)

fluid_midi_router_rule_set_param1 = _prototype(
    None,
    "fluid_midi_router_rule_set_param1",
    (CFS.c_void_p, 1, "rule"),
    (CFS.c_int, 1, "min"),
    (CFS.c_int, 1, "max"),
    (CFS.c_float, 1, "mul"),
    (CFS.c_int, 1, "add"),
)

fluid_midi_router_rule_set_param2 = _prototype(
    None,
    "fluid_midi_router_rule_set_param2",
    (CFS.c_void_p, 1, "rule"),
    (CFS.c_int, 1, "min"),
    (CFS.c_int, 1, "max"),
    (CFS.c_float, 1, "mul"),
    (CFS.c_int, 1, "add"),
)

fluid_midi_router_add_rule = _prototype(
    CFS.c_int,
    "fluid_midi_router_add_rule",
    (CFS.c_void_p, 1, "router"),
    (CFS.c_void_p, 1, "rule"),
    (CFS.c_int, 1, "type"),
)
fluid_midi_router_add_rule.errcheck = _errcheck

# MIDI sequencer
# [user defined data type]


class EventUserData(CFS.Structure):
    """Structure of data for Sequencer event callback function"""

    pass


# [typedef]
FLUID_EVENT_CALLBACK_T = CFS.CFUNCTYPE(
    None, CFS.c_uint, CFS.c_void_p, CFS.c_void_p, CFS.POINTER(EventUserData)
)
"""Event callback function prototype for destination clients.

:param c_uint time: Current sequencer tick value
:param c_void_p event: The event being received
:param c_void_p seq: The sequencer instance
:param POINTER(EventUserData) data: User defined data registered with the client
"""
# [API prototype]
new_fluid_sequencer2 = _prototype(
    CFS.c_void_p, "new_fluid_sequencer2", (CFS.c_int, 1, "use_system_timer")
)
new_fluid_sequencer2.errcheck = _errcheck

delete_fluid_sequencer = _prototype(
    None, "delete_fluid_sequencer", (CFS.c_void_p, 1, "seq")
)

fluid_sequencer_register_fluidsynth = _prototype(
    CFS.c_short,
    "fluid_sequencer_register_fluidsynth",
    (CFS.c_void_p, 1, "seq"),
    (CFS.c_void_p, 1, "synth"),
)
fluid_sequencer_register_fluidsynth.errcheck = _errcheck

fluid_sequencer_register_client = _prototype(
    CFS.c_short,
    "fluid_sequencer_register_client",
    (CFS.c_void_p, 1, "seq"),
    (CFS.c_char_p, 1, "name"),
    (FLUID_EVENT_CALLBACK_T, 1, "callback"),
    (CFS.POINTER(EventUserData), 1, "data"),
)
fluid_sequencer_register_client.errcheck = _errcheck

fluid_sequencer_unregister_client = _prototype(
    None,
    "fluid_sequencer_unregister_client",
    (CFS.c_void_p, 1, "seq"),
    (CFS.c_short, 1, "id"),
)

fluid_sequencer_get_client_name = _prototype(
    CFS.c_char_p,
    "fluid_sequencer_get_client_name",
    (CFS.c_void_p, 1, "seq"),
    (CFS.c_void_p, 1, "id"),
)
fluid_sequencer_get_client_name.errcheck = _errcheck

fluid_sequencer_get_tick = _prototype(
    CFS.c_uint, "fluid_sequencer_get_tick", (CFS.c_void_p, 1, "seq")
)
fluid_sequencer_get_tick.errcheck = _errcheck

fluid_sequencer_set_time_scale = _prototype(
    None,
    "fluid_sequencer_set_time_scale",
    (CFS.c_void_p, 1, "seq"),
    (CFS.c_double, 1, "scale", CFS.c_double(1000)),
)

fluid_sequencer_get_time_scale = _prototype(
    CFS.c_double, "fluid_sequencer_get_time_scale", (CFS.c_void_p, 1, "seq")
)
fluid_sequencer_get_time_scale.errcheck = _errcheck

fluid_sequencer_send_at = _prototype(
    CFS.c_int,
    "fluid_sequencer_send_at",
    (CFS.c_void_p, 1, "seq"),
    (CFS.c_void_p, 1, "evt"),
    (CFS.c_uint, 1, "time"),
    (CFS.c_int, 1, "absolute"),
)
fluid_sequencer_send_at.errcheck = _errcheck

# MIDI Sequencer - Sequencer Events
# [API prototype]
new_fluid_event = _prototype(CFS.c_void_p, "new_fluid_event")
new_fluid_event.errcheck = _errcheck

delete_fluid_event = _prototype(None, "delete_fluid_event", (CFS.c_void_p, 1, "evt"))

fluid_event_set_dest = _prototype(
    None, "fluid_event_set_dest", (CFS.c_void_p, 1, "evt"), (CFS.c_short, 1, "dest")
)

fluid_event_set_source = _prototype(
    None, "fluid_event_set_source", (CFS.c_void_p, 1, "evt"), (CFS.c_short, 1, "src")
)

fluid_event_note = _prototype(
    None,
    "fluid_event_note",
    (CFS.c_void_p, 1, "evt"),
    (CFS.c_int, 1, "channel"),
    (CFS.c_short, 1, "key"),
    (CFS.c_short, 1, "vel"),
    (CFS.c_uint, 1, "duration"),
)

fluid_event_timer = _prototype(
    None, "fluid_event_timer", (CFS.c_void_p, 1, "evt"), (CFS.c_void_p, 1, "data")
)

# Miscellaneous
# [API prototype]
fluid_free = _prototype(None, "fluid_free", (CFS.POINTER(CFS.c_int), 1, "ptr"))

fluid_is_midifile = _prototype(
    CFS.c_int, "fluid_is_midifile", (CFS.c_char_p, 1, "filename")
)
fluid_is_midifile.errcheck = _errcheck

fluid_is_soundfont = _prototype(
    CFS.c_int, "fluid_is_soundfont", (CFS.c_char_p, 1, "filename")
)
fluid_is_soundfont.errcheck = _errcheck

fluid_version_str = _prototype(CFS.c_char_p, "fluid_version_str")
fluid_version_str.errcheck = _errcheck

# Settings
# [ENUM]


class FLUID_TYPE(IntEnum):
    NO = -1
    NUM = auto()
    INT = auto()
    STR = auto()
    SET = auto()


class FLUID_HINT(IntFlag):
    BOUNDED_BELOW = 0x1
    BOUNDED_ABOVE = 0x2
    TOGGLED = 0x4
    RANGE = BOUNDED_BELOW | BOUNDED_ABOVE
    ON_OFF = RANGE | TOGGLED


FLUID_HINT_OPTIONLIST = 0x02
# [typedef]
FLUID_SETTINGS_FOREACH_OPTION_T = CFS.CFUNCTYPE(
    None, CFS.c_void_p, CFS.c_char_p, CFS.c_char_p
)
"""Callback function type used with fluid_settings_foreach_option()

:param c_void_p data:
:param c_char_p name:
:param c_char_p option:
"""

FLUID_SETTINGS_FOREACH_T = CFS.CFUNCTYPE(None, CFS.c_void_p, CFS.c_char_p, CFS.c_int)
"""Callback function type used with fluid_settings_foreach()

:param c_void_p data:
:param c_char_p name:
:param c_int type:
"""

# [API prototype]
new_fluid_settings = _prototype(CFS.c_void_p, "new_fluid_settings")
new_fluid_settings.errcheck = _errcheck

delete_fluid_settings = _prototype(
    None, "delete_fluid_settings", (CFS.c_void_p, 1, "settings")
)

fluid_settings_setnum = _prototype(
    CFS.c_int,
    "fluid_settings_setnum",
    (CFS.c_void_p, 1, "settings"),
    (CFS.c_char_p, 1, "name"),
    (CFS.c_double, 1, "value"),
)
fluid_settings_setnum.errcheck = _errcheck

fluid_settings_getnum = _prototype(
    CFS.c_int,
    "fluid_settings_getnum",
    (CFS.c_void_p, 1, "settings"),
    (CFS.c_char_p, 1, "name"),
    (CFS.POINTER(CFS.c_double), 3, "val"),
)
fluid_settings_getnum.errcheck = _errcheck

fluid_settings_getnum_default = _prototype(
    CFS.c_int,
    "fluid_settings_getnum_default",
    (CFS.c_void_p, 1, "settings"),
    (CFS.c_char_p, 1, "name"),
    (CFS.POINTER(CFS.c_double), 3, "val"),
)
fluid_settings_getnum_default.errcheck = _errcheck

fluid_settings_getnum_range = _prototype(
    CFS.c_int,
    "fluid_settings_getnum_range",
    (CFS.c_void_p, 1, "settings"),
    (CFS.c_char_p, 1, "name"),
    (CFS.POINTER(CFS.c_double), 3, "min"),
    (CFS.POINTER(CFS.c_double), 3, "max"),
)
fluid_settings_getnum_range.errcheck = _errcheck

fluid_settings_setint = _prototype(
    CFS.c_int,
    "fluid_settings_setint",
    (CFS.c_void_p, 1, "settings"),
    (CFS.c_char_p, 1, "name"),
    (CFS.c_int, 1, "val"),
)
fluid_settings_setint.errcheck = _errcheck

fluid_settings_getint = _prototype(
    CFS.c_int,
    "fluid_settings_getint",
    (CFS.c_void_p, 1, "settings"),
    (CFS.c_char_p, 1, "name"),
    (CFS.POINTER(CFS.c_int), 3, "val"),
)
fluid_settings_getint.errcheck = _errcheck

fluid_settings_getint_default = _prototype(
    CFS.c_int,
    "fluid_settings_getint_default",
    (CFS.c_void_p, 1, "settings"),
    (CFS.c_char_p, 1, "name"),
    (CFS.POINTER(CFS.c_int), 3, "val"),
)
fluid_settings_getint_default.errcheck = _errcheck

fluid_settings_getint_range = _prototype(
    CFS.c_int,
    "fluid_settings_getint_range",
    (CFS.c_void_p, 1, "settings"),
    (CFS.c_char_p, 1, "name"),
    (CFS.POINTER(CFS.c_int), 3, "min"),
    (CFS.POINTER(CFS.c_int), 3, "max"),
)
fluid_settings_getint_range.errcheck = _errcheck

fluid_settings_setstr = _prototype(
    CFS.c_int,
    "fluid_settings_setstr",
    (CFS.c_void_p, 1, "settings"),
    (CFS.c_char_p, 1, "name"),
    (CFS.c_char_p, 1, "str"),
)
fluid_settings_setstr.errcheck = _errcheck

fluid_settings_getstr_default = _prototype(
    CFS.c_int,
    "fluid_settings_getstr_default",
    (CFS.c_void_p, 1, "settings"),
    (CFS.c_char_p, 1, "name"),
    (CFS.POINTER(CFS.c_char_p), 3, "str"),
)
fluid_settings_getstr_default.errcheck = _errcheck

fluid_settings_copystr = _prototype(
    CFS.c_int,
    "fluid_settings_copystr",
    (CFS.c_void_p, 1, "settings"),
    (CFS.c_char_p, 1, "name"),
    (CFS.c_char_p, 1, "str"),
    (CFS.c_int, 1, "len"),
)
fluid_settings_copystr.errcheck = _errcheck

fluid_settings_foreach = _prototype(
    None,
    "fluid_settings_foreach",
    (CFS.c_void_p, 1, "settings"),
    (CFS.c_void_p, 1, "data"),
    (FLUID_SETTINGS_FOREACH_T, 1, "func"),
)

fluid_settings_foreach_option = _prototype(
    None,
    "fluid_settings_foreach_option",
    (CFS.c_void_p, 1, "settings"),
    (CFS.c_char_p, 1, "name"),
    (CFS.c_void_p, 1, "data"),
    (FLUID_SETTINGS_FOREACH_OPTION_T, 1, "func"),
)

fluid_settings_get_hints = _prototype(
    CFS.c_int,
    "fluid_settings_get_hints",
    (CFS.c_void_p, 1, "settings"),
    (CFS.c_char_p, 1, "name"),
    (CFS.POINTER(CFS.c_int), 3, "hints"),
)
fluid_settings_get_hints.errcheck = _errcheck


# SoundFonts
# SoundFonts - SoundFont Generators
# SoundFonts - SoundFont Loader
# [API prototype]
fluid_synth_get_channel_preset = _prototype(
    CFS.c_void_p,
    "fluid_synth_get_channel_preset",
    (CFS.c_void_p, 1, "synth"),
    (CFS.c_int, 1, "chan"),
)
fluid_synth_get_channel_preset.errcheck = _errcheck

fluid_sfont_get_preset = _prototype(
    CFS.c_void_p,
    "fluid_sfont_get_preset",
    (CFS.c_void_p, 1, "sfont"),
    (CFS.c_int, 1, "bank"),
    (CFS.c_int, 1, "prenum"),
)
fluid_sfont_get_preset.errcheck = _errcheck

fluid_preset_get_banknum = _prototype(
    CFS.c_int, "fluid_preset_get_banknum", (CFS.c_void_p, 1, "preset")
)
fluid_preset_get_banknum.errcheck = _errcheck

fluid_preset_get_name = _prototype(
    CFS.c_char_p, "fluid_preset_get_name", (CFS.c_void_p, 1, "preset")
)
fluid_preset_get_name.errcheck = _errcheck

fluid_preset_get_num = _prototype(
    CFS.c_int, "fluid_preset_get_num", (CFS.c_void_p, 1, "preset")
)
fluid_preset_get_num.errcheck = _errcheck

fluid_preset_get_sfont = _prototype(
    CFS.c_void_p, "fluid_preset_get_sfont", (CFS.c_void_p, 1, "preset")
)
fluid_preset_get_sfont.errcheck = _errcheck

fluid_sfont_get_id = _prototype(
    CFS.c_int, "fluid_sfont_get_id", (CFS.c_void_p, 1, "sfont")
)
fluid_sfont_get_id.errcheck = _errcheck

# SoundFonts - SoundFont Modulators
# SoundFonts - SoundFont Maniplation

# Synthesizer
# [API prototype]
new_fluid_synth = _prototype(
    CFS.c_void_p, "new_fluid_synth", (CFS.c_void_p, 1, "settings")
)
new_fluid_synth.errcheck = _errcheck

delete_fluid_synth = _prototype(None, "delete_fluid_synth", (CFS.c_void_p, 1, "synth"))

# Synthesizer - Audio Rendering
# Synthesizer - Effect - Chorus
# Synthesizer - Effect - IIR Filter
# Synthesizer - Effect - LADSPA
# Synthesizer - Effect - Reverb

# Synthesizer - MIDI Channel Messages
# [API prototype]
fluid_synth_all_notes_off = _prototype(
    CFS.c_int,
    "fluid_synth_all_notes_off",
    (CFS.c_void_p, 1, "synth"),
    (CFS.c_int, 1, "chan"),
)
fluid_synth_all_notes_off.errcheck = _errcheck

fluid_synth_all_sounds_off = _prototype(
    CFS.c_int,
    "fluid_synth_all_sounds_off",
    (CFS.c_void_p, 1, "synth"),
    (CFS.c_int, 1, "chan"),
)
fluid_synth_all_sounds_off.errcheck = _errcheck

fluid_synth_cc = _prototype(
    CFS.c_int,
    "fluid_synth_cc",
    (CFS.c_void_p, 1, "synth"),
    (CFS.c_int, 1, "chan"),
    (CFS.c_int, 1, "num"),
    (CFS.c_int, 1, "val"),
)
fluid_synth_cc.errcheck = _errcheck

fluid_synth_get_cc = _prototype(
    CFS.c_int,
    "fluid_synth_get_cc",
    (CFS.c_void_p, 1, "synth"),
    (CFS.c_int, 1, "chan"),
    (CFS.c_int, 1, "num"),
    (CFS.POINTER(CFS.c_int), 3, "pval"),
)
fluid_synth_get_cc.errcheck = _errcheck

fluid_synth_pitch_bend = _prototype(
    CFS.c_int,
    "fluid_synth_pitch_bend",
    (CFS.c_void_p, 1, "synth"),
    (CFS.c_int, 1, "chan"),
    (CFS.c_int, 1, "val"),
)
fluid_synth_pitch_bend.errcheck = _errcheck

fluid_synth_get_pitch_bend = _prototype(
    CFS.c_int,
    "fluid_synth_get_pitch_bend",
    (CFS.c_void_p, 1, "synth"),
    (CFS.c_int, 1, "chan"),
    (CFS.POINTER(CFS.c_int), 3, "ppitch_bend"),
)
fluid_synth_get_pitch_bend.errcheck = _errcheck

fluid_synth_pitch_wheel_sens = _prototype(
    CFS.c_int,
    "fluid_synth_pitch_wheel_sens",
    (CFS.c_void_p, 1, "synth"),
    (CFS.c_int, 1, "chan"),
    (CFS.c_int, 1, "val"),
)
fluid_synth_pitch_wheel_sens.errcheck = _errcheck

fluid_synth_get_pitch_wheel_sens = _prototype(
    CFS.c_int,
    "fluid_synth_get_pitch_wheel_sens",
    (CFS.c_void_p, 1, "synth"),
    (CFS.c_int, 1, "chan"),
    (CFS.POINTER(CFS.c_int), 3, "pval"),
)
fluid_synth_get_pitch_wheel_sens.errcheck = _errcheck

fluid_synth_sysex = _prototype(
    CFS.c_int,
    "fluid_synth_sysex",
    (CFS.c_void_p, 1, "synth"),
    (CFS.c_char_p, 1, "data"),
    (CFS.c_int, 1, "len"),
    (CFS.c_char_p, 1, "response"),
    (CFS.POINTER(CFS.c_int), 1, "response_len"),
    (CFS.POINTER(CFS.c_int), 1, "handled"),
    (CFS.c_int, 1, "dryrun"),
)
fluid_synth_sysex.errcheck = _errcheck

fluid_synth_program_select = _prototype(
    CFS.c_int,
    "fluid_synth_program_select",
    (CFS.c_void_p, 1, "synth"),
    (CFS.c_int, 1, "chan"),
    (CFS.c_int, 1, "sfont_id"),
    (CFS.c_int, 1, "bank_num"),
    (CFS.c_int, 1, "preset_num"),
)
fluid_synth_program_select.errcheck = _errcheck

fluid_synth_noteon = _prototype(
    CFS.c_int,
    "fluid_synth_noteon",
    (CFS.c_void_p, 1, "synth"),
    (CFS.c_int, 1, "chan"),
    (CFS.c_int, 1, "key"),
    (CFS.c_int, 1, "vel"),
)
fluid_synth_noteon.errcheck = _errcheck

fluid_synth_noteoff = _prototype(
    CFS.c_int,
    "fluid_synth_noteoff",
    (CFS.c_void_p, 1, "synth"),
    (CFS.c_int, 1, "chan"),
    (CFS.c_int, 1, "key"),
)
fluid_synth_noteoff.errcheck = _errcheck

fluid_synth_system_reset = _prototype(
    CFS.c_int, "fluid_synth_system_reset", (CFS.c_void_p, 1, "synth")
)
fluid_synth_system_reset.errcheck = _errcheck

# Synthesizer - MIDI Channel Setup
# Synthesizer - MIDI Tuning

# Synthesizer - SoundFont managiment
# [API prototype]
fluid_synth_add_sfont = _prototype(
    CFS.c_int,
    "fluid_synth_add_sfont",
    (CFS.c_void_p, 1, "synth"),
    (CFS.c_void_p, 1, "sfont"),
)
fluid_synth_add_sfont.errcheck = _errcheck

fluid_synth_sfload = _prototype(
    CFS.c_int,
    "fluid_synth_sfload",
    (CFS.c_void_p, 1, "synth"),
    (CFS.c_char_p, 1, "filename"),
    (CFS.c_int, 1, "reset_preset"),
)
fluid_synth_sfload.errcheck = _errcheck

fluid_synth_sfreload = _prototype(
    CFS.c_int, "fluid_synth_sfreload", (CFS.c_void_p, 1, "synth"), (CFS.c_int, 1, "id")
)
fluid_synth_sfreload.errcheck = _errcheck

fluid_synth_sfcount = _prototype(
    CFS.c_int, "fluid_synth_sfcount", (CFS.c_void_p, 1, "synth")
)
fluid_synth_sfcount.errcheck = _errcheck

fluid_synth_get_sfont = _prototype(
    CFS.c_void_p,
    "fluid_synth_get_sfont",
    (CFS.c_void_p, 1, "synth"),
    (CFS.c_uint, 1, "num"),
)
fluid_synth_get_sfont.errcheck = _errcheck

fluid_synth_get_sfont_by_id = _prototype(
    CFS.c_void_p,
    "fluid_synth_get_sfont_by_id",
    (CFS.c_void_p, 1, "synth"),
    (CFS.c_int, 1, "id"),
)
fluid_synth_get_sfont_by_id.errcheck = _errcheck

# Synthesizer - Synthesis Parameters
# [API prototype]
fluid_synth_get_gain = _prototype(
    CFS.c_float, "fluid_synth_get_gain", (CFS.c_void_p, 1, "synth")
)
fluid_synth_get_gain.errcheck = _errcheck

fluid_synth_set_gain = _prototype(
    None, "fluid_synth_set_gain", (CFS.c_void_p, 1, "synth"), (CFS.c_float, 1, "gain")
)

# Synthesizer - Voice Control

# [typing alias]
PRESET = dict[str, Union[int, str, None]]


class Synthesizer:
    """SoundFont synthesizer.

    :param dict kwargs: kwargs = {
            'settings':'config/settings.json',
            'soundfont':['sf2/FluidR3_GM.sf2', 'sf2/SGM-V2.01.sf2']}
    """

    def __init__(self, **kwargs: dict[str, Any]) -> None:
        try:
            for i in range(FLUID_LOG_LEVEL.LAST_LOG_LEVEL):
                fluid_set_log_function(level=i, fun=_log_func, data=None)

            self._settings: int = int(new_fluid_settings())
            if "settings" in kwargs:
                self._customaize_settings(json_filename=str(kwargs["settings"]))

            self._synth: int = int(
                new_fluid_synth(settings=CFS.c_void_p(self._settings))
            )

            self._soundfonts: dict[str, int] = dict()  # filename, sfont id
            if "soundfont" in kwargs:
                for s_name in kwargs["soundfont"]:
                    self._soundfonts[s_name] = int(
                        fluid_synth_sfload(
                            synth=CFS.c_void_p(self._synth),
                            filename=s_name.encode(),
                            reset_preset=CFS.c_int(True),
                        )
                    )

            else:
                c_name = CFS.c_char_p()
                fluid_settings_getstr_default(
                    settings=CFS.c_void_p(self._settings),
                    name=b"synth.default-soundfont",
                    str=CFS.byref(c_name),
                )
                if c_name.value is not None:
                    self._soundfonts[c_name.value.decode()] = int(
                        fluid_synth_sfload(
                            synth=CFS.c_void_p(self._synth),
                            filename=c_name.value,
                            reset_preset=CFS.c_int(True),
                        )
                    )

            self._gm_system_on()
            self._log(level=FLUID_LOG_LEVEL.INFO, message="gm system on")

            if type(self) == Synthesizer:
                self._assign_audio_driver()
        except FSError as msg:
            self._log(
                level=FLUID_LOG_LEVEL.ERR, message=f"Synthesizer failed. {str(msg)}"
            )
            self.__del__()
        else:
            self._log(
                level=FLUID_LOG_LEVEL.INFO,
                message=f"libfluidsynth version: {self.version()}",
            )

    def __del__(self) -> None:
        if type(self) == Synthesizer:
            self._delete_auido_driver()
        delete_fluid_synth(synth=CFS.c_void_p(self._synth))
        delete_fluid_settings(settings=CFS.c_void_p(self._settings))
        self._log(level=FLUID_LOG_LEVEL.INFO, message="good-bye")

    def _log(self, level: FLUID_LOG_LEVEL, message: str) -> None:
        fluid_log(level=CFS.c_int(level), fmt=b"%s", message=message.encode())

    def _customaize_settings(self, json_filename: str) -> None:
        with open(file=json_filename, mode="r") as fp:
            settings_json = load(fp)
        for name, dicts in settings_json.items():
            if (
                isinstance(dicts["value"], float)
                and FLUID_TYPE(dicts["type"]) == FLUID_TYPE.NUM
            ):
                fluid_settings_setnum(
                    settings=CFS.c_void_p(self._settings),
                    name=str(name).encode(),
                    value=CFS.c_double(dicts["value"]),
                )
            elif (
                isinstance(dicts["value"], int)
                and FLUID_TYPE(dicts["type"]) == FLUID_TYPE.INT
            ):
                fluid_settings_setint(
                    settings=CFS.c_void_p(self._settings),
                    name=str(name).encode(),
                    val=CFS.c_int(dicts["value"]),
                )
            elif (
                isinstance(dicts["value"], str)
                and FLUID_TYPE(dicts["type"]) == FLUID_TYPE.STR
            ):
                fluid_settings_setstr(
                    settings=CFS.c_void_p(self._settings),
                    name=str(name).encode(),
                    str=str(dicts["value"]).encode(),
                )

    def _assign_audio_driver(self) -> int:
        self._audio_driver = int(
            new_fluid_audio_driver(
                settings=CFS.c_void_p(self._settings), synth=CFS.c_void_p(self._synth)
            )
        )
        return self._audio_driver

    def _delete_auido_driver(self) -> None:
        if hasattr(self, "_audio_driver"):
            delete_fluid_audio_driver(driver=CFS.c_void_p(self._audio_driver))

    def version(self) -> str:
        """version _summary_

        :return: _description_
        """
        return bytes(fluid_version_str()).decode()

    def _gm_system_on(self) -> int:
        return int(
            fluid_synth_sysex(
                synth=CFS.c_void_p(self._synth),
                data=(CFS.c_char * 3)(
                    CFS.c_char(0x7E), CFS.c_char(0x09), CFS.c_char(0x01)
                ),
                len=CFS.c_int(3),
                response=None,
                response_len=None,
                handled=None,
                dryrun=CFS.c_int(False),
            )
        )

    def _all_notes_off(self, chan: int = -1) -> int:
        return fluid_synth_all_notes_off(
            synth=CFS.c_void_p(self._synth), chan=CFS.c_int(chan)
        )

    def _all_sounds_off(self, chan: int = -1) -> int:
        return fluid_synth_all_sounds_off(
            synth=CFS.c_void_p(self._synth), chan=CFS.c_int(chan)
        )

    def _panic(self) -> int:
        return fluid_synth_system_reset(synth=CFS.c_void_p(self._synth))

    @property
    def gain(self) -> float:
        """float: gain - defalt 0.2, Min 0.0, Max 10.0"""
        return float(fluid_synth_get_gain(synth=CFS.c_void_p(self._synth)))

    @gain.setter
    def gain(self, value: float) -> float:
        fluid_synth_set_gain(synth=CFS.c_void_p(self._synth), gain=CFS.c_float(value))
        return float(fluid_synth_get_gain(synth=CFS.c_void_p(self._synth)))

    @property
    def soundfonts(self) -> list:
        """list(str): sonundfont file names"""
        return list(self._soundfonts.keys())  # filename

    def gm_sound_set(self) -> tuple:  # list[list[PRESET]]:
        """Get list of Sound Set (GM system level 1) from soundfont.

        :return: gm sound set - list[list[PRESET]]
        :return: gm percussion sound set - list[list[PRESET]]

        - soundfont
            - bank
                - PRESET(dict)
                    - "name": str | None
                    - "num" : int | None
                    - "bank": int | None
                    - "sfont_id": int | None
        """
        sound_set: list = list()
        percussion_sound_set: list = list()  # bank = 128: percussion

        for sfont_index in range(
            int(fluid_synth_sfcount(synth=CFS.c_void_p(self._synth))) - 1, -1, -1
        ):
            sfont = int(
                fluid_synth_get_sfont(
                    synth=CFS.c_void_p(self._synth), num=CFS.c_uint(sfont_index)
                )
            )

            if sound_set == []:
                sound_set = self._sfont_sound_set(sfont, 0)
            else:
                for preset in self._sfont_sound_set(sfont, 0):
                    if isinstance(preset["num"], int):
                        sound_set[preset["num"]] = preset

            if percussion_sound_set == []:
                percussion_sound_set = self._sfont_sound_set(sfont, 128)
            else:
                for preset in self._sfont_sound_set(sfont, 128):
                    if isinstance(preset["num"], int):
                        percussion_sound_set[preset["num"]] = preset

        return sound_set, percussion_sound_set

    def _sfont_sound_set(self, sfont: int, bank: int) -> list[PRESET]:
        """_sfont_sound_set _summary_

        :param int sfont: soundfont id
        :param int bank: bank
        :return: preset list

        - PRESET(dict)
            - "name": str | None
            - "num" : int | None
            - "bank": int | None
            - "sfont_id": int | None
        """
        result: list[PRESET] = list()
        for n in range(128):
            preset = fluid_sfont_get_preset(
                sfont=CFS.c_void_p(sfont), bank=CFS.c_int(bank), prenum=CFS.c_int(n)
            )
            result += [self._preset(preset)]
        return result

    def channels_preset(self) -> list[PRESET]:
        """Get a list of presets per channel

        :return: preset list

        - PRESET(dict)
            - "name": str | None
            - "num" : int | None
            - "bank": int | None
            - "sfont_id": int | None
        """
        result: list[PRESET] = list()
        for chan in range(15):
            result += [self._channel_preset(chan)]
        return result

    def _channel_preset(self, chan: int) -> PRESET:
        """_channel_preset _summary_

        :param int chan: channel number
        :return: preset

        - PRESET(dict)
            - "name": str | None
            - "num" : int | None
            - "bank": int | None
            - "sfont_id": int | None
        """
        preset = int(
            fluid_synth_get_channel_preset(
                synth=CFS.c_void_p(self._synth), chan=CFS.c_int(chan)
            )
        )
        return self._preset(preset)

    def _preset(self, preset: int) -> PRESET:
        """_preset _summary_

        :param int preset: _description_
        :return: preset

        - PRESET(dict)
            - "name": str | None
            - "num" : int | None
            - "bank": int | None
            - "sfont_id": int | None
        """
        result: dict[str, Union[str, int, None]] = dict()
        if preset:
            result["name"] = bytes(
                fluid_preset_get_name(preset=CFS.c_void_p(preset))
            ).decode()
            result["num"] = fluid_preset_get_num(preset=CFS.c_void_p(preset))
            result["bank"] = fluid_preset_get_banknum(preset=CFS.c_void_p(preset))
            result["sfont_id"] = fluid_sfont_get_id(
                sfont=fluid_preset_get_sfont(preset=CFS.c_void_p(preset))
            )
        else:
            result["name"] = None
            result["num"] = None
            result["bank"] = None
            result["sfont_id"] = None
        return result

    def pitch_bend(self, chan: int, val: int) -> int:
        """pitch_bend _summary_

        :param int chan: _description_
        :param int val: _description_
        :return: _description_
        """
        return fluid_synth_pitch_bend(
            synth=CFS.c_void_p(self._synth), chan=CFS.c_int(chan), val=CFS.c_int(val)
        )

    def pitch_wheel_sens(self, chan: int, val: int) -> int:
        """pitch_wheel_sens _summary_

        :param int chan: _description_
        :param int val: _description_
        :return: _description_
        """
        return fluid_synth_pitch_wheel_sens(
            synth=CFS.c_void_p(self._synth), chan=CFS.c_int(chan), val=CFS.c_int(val)
        )

    def program_select(self, chan: int, sfont_id: int, bank: int, preset: int) -> int:
        """program_select _summary_

        :param int chan: _description_
        :param int sfont_id: _description_
        :param int bank: _description_
        :param int preset: _description_
        :return: _description_
        """
        return fluid_synth_program_select(
            synth=CFS.c_void_p(self._synth),
            chan=CFS.c_int(chan),
            sfont_id=CFS.c_int(sfont_id),
            bank_num=CFS.c_int(bank),
            preset_num=CFS.c_int(preset),
        )

    def note_on(self, channel: int, keyNumber: int, velocity: int) -> int:
        """note_on _summary_

        :param int channel: _description_
        :param int keyNumber: _description_
        :param int velocity: _description_
        :return: _description_
        """
        return fluid_synth_noteon(
            synth=CFS.c_void_p(self._synth),
            chan=CFS.c_int(channel),
            key=CFS.c_int(keyNumber),
            vel=CFS.c_int(velocity),
        )

    def note_off(self, channel: int, keyNumber: int) -> int:
        """note_off _summary_

        :param int channel: _description_
        :param int keyNumber: _description_
        :return: _description_
        """
        try:
            fluid_synth_noteoff(
                synth=CFS.c_void_p(self._synth),
                chan=CFS.c_int(channel),
                key=CFS.c_int(keyNumber),
            )
            return FLUID_OK
        except FSError as msg:
            self._log(level=FLUID_LOG_LEVEL.ERR, message=f"synth noteoff. {str(msg)}")
        return FLUID_FAILED

    def modulation_wheel(self, chan: int, val: int) -> int:
        """The sound amplifies like vibrato.

        :param int chan: _description_
        :param int val: _description_
        :return: _description_
        """
        return fluid_synth_cc(
            synth=CFS.c_void_p(self._synth),
            chan=CFS.c_int(chan),
            num=CFS.c_int(0x01),
            val=CFS.c_int(val),
        )

    def volume(self, chan: int, val: int) -> int:
        """Set the maximum allowable value of velocity.

        :param int chan: _description_
        :param int val: _description_
        :return: _description_
        """
        return fluid_synth_cc(
            synth=CFS.c_void_p(self._synth),
            chan=CFS.c_int(chan),
            num=CFS.c_int(0x07),
            val=CFS.c_int(val),
        )

    def sustain_on(self, chan: int) -> int:
        """The sound echoes for a long time.

        :param int chan: _description_
        :return: _description_
        """
        return fluid_synth_cc(
            synth=CFS.c_void_p(self._synth),
            chan=CFS.c_int(chan),
            num=CFS.c_int(0x40),
            val=CFS.c_int(0b00100000),
        )

    def sustain_off(self, chan: int) -> int:
        """sustain_off _summary_

        :param int chan: _description_
        :return: _description_
        """
        return fluid_synth_cc(
            synth=CFS.c_void_p(self._synth),
            chan=CFS.c_int(chan),
            num=CFS.c_int(0x40),
            val=CFS.c_int(0b00000000),
        )

    def pan(self, chan: int, val: int) -> int:
        """pan _summary_

        :param int chan: _description_
        :param int val: _description_
        :return: _description_
        """
        return fluid_synth_cc(
            synth=CFS.c_void_p(self._synth),
            chan=CFS.c_int(chan),
            num=CFS.c_int(0x0A),
            val=CFS.c_int(val),
        )

    def expression(self, chan: int, val: int) -> int:
        """Temporary velocity can be set above volume.

        :param int chan: _description_
        :param int val: _description_
        :return: _description_
        """
        return fluid_synth_cc(
            synth=CFS.c_void_p(self._synth),
            chan=CFS.c_int(chan),
            num=CFS.c_int(0x0B),
            val=CFS.c_int(val),
        )


class Sequencer(Synthesizer):
    """Send MIDI events scheduled by the sequencer to the synthesizer.

    :param dict kwargs: kwargs = {
            'settings':'config/settings.json',
            'soundfont':['sf2/FluidR3_GM.sf2', 'sf2/SGM-V2.01.sf2']}
    """

    clients: list[int] = list()

    def __init__(self, **kwargs: dict[str, Any]) -> None:
        super().__init__(**kwargs)
        try:
            self._sequencer: int
            self._bps: float = 120.0
            self._quaternote: int = 240
            self._callbacks: list[Callable] = list()

            self._sequencer = int(
                new_fluid_sequencer2(use_system_timer=CFS.c_int(False))
            )
            self.clients += [
                int(
                    fluid_sequencer_register_fluidsynth(
                        seq=CFS.c_void_p(self._sequencer),
                        synth=CFS.c_void_p(self._synth),
                    )
                )
            ]

            self._set_time_scale()
            self._assign_audio_driver()
        except FSError as msg:
            self._log(
                level=FLUID_LOG_LEVEL.ERR, message=f"Sequencer failed. {str(msg)}"
            )
            self.__del__()

    def __del__(self) -> None:
        self._delete_auido_driver()
        for client_id in self.clients[::-1]:
            fluid_sequencer_unregister_client(
                seq=CFS.c_void_p(self._sequencer), id=CFS.c_short(client_id)
            )
        delete_fluid_sequencer(seq=CFS.c_void_p(self._sequencer))
        super().__del__()

    def client_name(self, id: int) -> str:
        """client_name _summary_

        :param int id: _description_
        :return: _description_
        """
        return fluid_sequencer_get_client_name(
            seq=CFS.c_void_p(self._sequencer), id=CFS.c_void_p(id)
        ).decode()

    def register_client(
        self,
        name: str,
        callback: Union[Callable[..., None], None] = None,
        data: Union[EventUserData, None] = None,
    ) -> int:
        """Register a sequencer client.

        :param str name: Name of sequencer client
        :param Callable callback: Sequencer client callback or NULL for a source client.
        :param EventUserData data: User data to pass to the callback

        :return: Unique sequencer ID or FLUID_FAILED on error
        """
        if callback:
            callback = FLUID_EVENT_CALLBACK_T(callback)
            self._callbacks += [callback]

        self.clients += [
            int(
                fluid_sequencer_register_client(
                    seq=CFS.c_void_p(self._sequencer),
                    name=name.encode(),
                    callback=callback if callback else None,
                    data=CFS.byref(data) if data else None,
                )
            )
        ]
        return self.clients[len(self.clients) - 1]

    @property
    def time_scale(self) -> float:
        """Ticks per second"""
        return float(fluid_sequencer_get_time_scale(seq=CFS.c_void_p(self._sequencer)))

    @property
    def bps(self) -> float:
        """Number of quarternotes per second"""
        return self._bps

    @bps.setter
    def bps(self, value: float) -> None:
        self._bps = value
        self._set_time_scale()

    @property
    def tick(self) -> int:
        """current tick of the sequencer scaled
        by the time scale currently set"""
        return int(fluid_sequencer_get_tick(seq=CFS.c_void_p(self._sequencer)))

    def _set_time_scale(self):
        fluid_sequencer_set_time_scale(
            seq=CFS.c_void_p(self._sequencer),
            scale=CFS.c_double(self._quaternote / (60 / self._bps)),
        )

    def note_at(
        self,
        ticks: int,
        channel: int,
        key_number: int,
        velocity: int,
        duration: int,
        source: int = -1,
        destination: int = -1,
        absolute: bool = True,
    ) -> None:
        """note_at _summary_

        :param int ticks: _description_
        :param int channel: _description_
        :param int key_number: _description_
        :param int velocity: _description_
        :param int duration: _description_
        :param int source: _description_, defaults to -1
        :param int destination: _description_, defaults to -1
        :param bool absolute: _description_, defaults to True
        """
        event = self._assign_event(source=source, destination=destination)
        fluid_event_note(
            evt=CFS.c_void_p(event),
            channel=CFS.c_int(channel),
            key=CFS.c_short(key_number),
            vel=CFS.c_short(velocity),
            duration=CFS.c_uint(duration),
        )
        self._send_event_at(event=event, ticks=ticks, absolute=absolute)

    def timer_at(
        self,
        ticks: int,
        data: Union[EventUserData, None] = None,
        source: int = -1,
        destination: int = -1,
        absolute: bool = True,
    ) -> None:
        """timer_at _summary_

        :param int ticks: _description_
        :param Union[EventUserData, None] data: _description_, defaults to None
        :param int source: _description_, defaults to -1
        :param int destination: _description_, defaults to -1
        :param bool absolute: _description_, defaults to True
        """
        event = self._assign_event(source=source, destination=destination)
        fluid_event_timer(
            evt=CFS.c_void_p(event), data=CFS.pointer(data) if data else None
        )
        self._send_event_at(event=event, ticks=ticks, absolute=absolute)

    def _assign_event(self, source: int, destination: int) -> int:
        event = new_fluid_event()
        fluid_event_set_source(evt=event, src=CFS.c_short(source))
        fluid_event_set_dest(evt=event, dest=CFS.c_short(destination))
        return int(event)

    def _send_event_at(self, event: int, ticks: int, absolute: bool) -> int:
        result = fluid_sequencer_send_at(
            seq=CFS.c_void_p(self._sequencer),
            evt=CFS.c_void_p(event),
            time=CFS.c_uint(ticks),
            absolute=CFS.c_int(absolute),
        )
        delete_fluid_event(evt=CFS.c_void_p(event))
        return int(result)


class MidiRouter(Synthesizer):
    """Rule based transformation and filtering of MIDI events.

    :param dict kwargs: kwargs = {
            'settings':'config/settings.json',
            'soundfont':['sf2/FluidR3_GM.sf2', 'sf2/SGM-V2.01.sf2']}
    """

    def __init__(self, **kwargs: dict[str, Any]) -> None:
        super().__init__(**kwargs)
        try:
            handler = fluid_synth_handle_midi_event

            self._midi_router: int = int(
                new_fluid_midi_router(
                    settings=CFS.c_void_p(self._settings),
                    handler=handler,
                    event_handler_data=CFS.c_void_p(self._synth),
                )
            )

            self._cmd_handler: int = int(
                new_fluid_cmd_handler(
                    synth=CFS.c_void_p(self._synth),
                    router=CFS.c_void_p(self._midi_router),
                )
            )
        except FSError as msg:
            self._log(level=FLUID_LOG_LEVEL.ERR, message=f"Midi Router.  {str(msg)}")
            self.__del__()

    def __del__(self) -> None:
        delete_fluid_cmd_handler(handler=CFS.c_void_p(self._cmd_handler))
        delete_fluid_midi_router(router=CFS.c_void_p(self._midi_router))
        super().__del__()

    def apply_rules(self, rule_file: Union[str, None] = None) -> bool:
        """Apply rules for MIDI events.

        :param str rule_file: Rule file to be applied  in json file,
            or default rules if none

        :return: True, or False
        """
        try:
            fluid_midi_router_clear_rules(router=CFS.c_void_p(self._midi_router))

            if rule_file is None:
                fluid_midi_router_set_default_rules(
                    router=CFS.c_void_p(self._midi_router)
                )
            else:
                with open(rule_file, "r") as fp:
                    rules_json = load(fp)

                for rd in rules_json.values():
                    rule = new_fluid_midi_router_rule()
                    if rd["chan"] is not None:
                        fluid_midi_router_rule_set_chan(rule, *rd["chan"].values())
                    if rd["param1"] is not None:
                        fluid_midi_router_rule_set_param1(rule, *rd["param1"].values())
                    if rd["param2"] is not None:
                        fluid_midi_router_rule_set_param2(rule, *rd["param2"].values())
                    fluid_midi_router_add_rule(self._midi_router, rule, rd["type"])
        except FSError as msg:
            self._log(level=FLUID_LOG_LEVEL.ERR, message=f"Midi Router Rule {str(msg)}")
            return False
        else:
            return True


class MidiDriver(MidiRouter):
    """Sends MIDI events received at the MIDI input to the synthesizer.

    :param dict kwargs: kwargs = {
            'settings':'config/settings.json',
            'soundfont':['sf2/FluidR3_GM.sf2', 'sf2/SGM-V2.01.sf2'],
            'handler': fluid_midi_dump_prerouter}
    """

    def __init__(self, **kwargs: dict[str, Any]) -> None:
        super().__init__(**kwargs)
        try:
            if "handler" in kwargs:
                callback = kwargs["handler"]
            else:
                callback = fluid_midi_router_handle_midi_event

            self._midi_driver: int = int(
                new_fluid_midi_driver(
                    settings=CFS.c_void_p(self._settings),
                    handler=callback,
                    event_handler_data=CFS.c_void_p(self._midi_router),
                )
            )
            self._assign_audio_driver()
        except FSError as msg:
            self._log(level=FLUID_LOG_LEVEL.ERR, message=f"Midi Driver. {str(msg)}")
            self.__del__()

    def __del__(self) -> None:
        self._delete_auido_driver()
        delete_fluid_midi_driver(driver=CFS.c_void_p(self._midi_driver))
        super().__del__()


class MidiPlayer(MidiRouter):
    """Parse standard MIDI files and emit MIDI events.

    :param dict kwargs: kwargs = {
            "settings":"config/settings.json",
            "soundfont":["sf2/FluidR3_GM.sf2", "sf2/SGM-V2.01.sf2"],
            "handler": fluid_midi_dump_prerouter,
            "standardmidifile": ["mid/SenBonZakura.mid", "mid/111867.MID"]}
    """

    def __init__(self, **kwargs: dict[str, Any]) -> None:
        super().__init__(**kwargs)
        try:
            self._player: int = int(new_fluid_player(synth=CFS.c_void_p(self._synth)))

            if "handler" in kwargs:
                callback = kwargs["handler"]
            else:
                callback = fluid_midi_router_handle_midi_event

            fluid_player_set_playback_callback(
                player=CFS.c_void_p(self._player),
                handler=callback,
                handler_data=CFS.c_void_p(self._midi_router),
            )

            for filename in kwargs["standardmidifile"]:
                if fluid_is_midifile(filename.encode()):
                    print(filename)
                    ptr: bytes = Path(filename).read_bytes()
                    fluid_player_add_mem(
                        player=CFS.c_void_p(self._player),
                        buffer=ptr,
                        len=CFS.c_size_t(len(ptr)),
                    )

            self._assign_audio_driver()
        except FSError as msg:
            self._log(level=FLUID_LOG_LEVEL.ERR, message=f"Midi Player. {str(msg)}")
            self.__del__()

    def __del__(self) -> None:
        self._delete_auido_driver()
        delete_fluid_player(player=CFS.c_void_p(self._player))
        super().__del__()

    def playback(self, start_tick: int = 0) -> None:
        """Start playback.

        :param start_tick: tick at the position where you want to start
        """

        fluid_player_play(player=CFS.c_void_p(self._player))
        sleep(0.1)  # Wait for seekable
        fluid_player_seek(
            player=CFS.c_void_p(self._player), ticks=CFS.c_int(start_tick)
        )
        fluid_player_join(player=CFS.c_void_p(self._player))

    def stop(self) -> int:
        """Stop or end playback.

        :return: ticks when stopped
        """
        fluid_player_stop(player=CFS.c_void_p(self._player))
        fluid_player_join(player=CFS.c_void_p(self._player))
        self._all_sounds_off()  # Wait to clear Ringbuffer after EOT.
        return self.tick

    @property
    def tick(self) -> int:
        """Get the number of tempo ticks passed."""
        return int(fluid_player_get_current_tick(player=CFS.c_void_p(self._player)))

    @property
    def total_ticks(self) -> int:
        """Get total ticks."""
        return int(fluid_player_get_total_ticks(player=CFS.c_void_p(self._player)))


if __name__ == "__main__":
    print(__file__)
