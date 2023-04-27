#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Detect and configure sound devices, control volume.

:reference: https://www.alsa-project.org/alsa-doc/alsa-lib/index.html
"""

from typing import Callable, Any
from contextlib import contextmanager
from enum import IntEnum, auto
from subprocess import Popen, PIPE
from json import load
from statistics import mean
import ctypes as CAS2
from ctypes.util import find_library
import logging as LAS


from audioworkstation.libs.audio import btaudiosink

# Logger
logger = LAS.getLogger(__name__)
logger.setLevel(LAS.DEBUG)
_logger_formatter = LAS.Formatter("%(asctime)s %(levelname)s %(message)s")
# Logger StreamHandler
_logger_sh = LAS.StreamHandler()
_logger_sh.setFormatter(_logger_formatter)
logger.addHandler(_logger_sh)


class AS2Error(Exception):
    """Exceptions sent out from errcheck func."""

    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        logger.error(f"Mixer device: {args}")


def _errcheck_non_zero(result: Any, cfunc: Callable, args: tuple) -> Any:
    if result != 0:
        raise AS2Error((cfunc, args))
    return result


"""libasound2"""
_libas2 = CAS2.CDLL(name=find_library(name="asound"), use_errno=True)


def _prototype(restype: Any, name: str, *params: tuple) -> Any:
    """Returns a foreign function exported by a shared library.

    :param Any restype: foreign function restype
    :param str name: foreign function name
    :param tuple params: type, flag, name[, default]
    :return: foreign function object
    """
    if hasattr(_libas2, name):
        argtypes: list = list([])
        paramflags: list = list([])
        for param in params:
            argtypes.append(param[0])
            paramflags.append(param[1:])
        func_spec = (name, _libas2)
        return CAS2.CFUNCTYPE(restype, *argtypes, use_errno=True)(
            func_spec, tuple(paramflags)
        )
    else:
        return None


"""Global defines and functions.

The ALSA library implementation uses these macros and functions.
Most applications probably do not need them.
"""

_snd_asoundlib_version = _prototype(CAS2.c_char_p, "snd_asoundlib_version")
"""Returns the ALSA sound library version in ASCII format.

:return: The ASCII description of the used ALSA sound library.
"""

"""The control interface."""


@contextmanager
def _open_device_name_hint(card: int, iface: str):
    """Get a aset of device name hints(array of hint) .

    :param int card: index of physical sound card
    :param str iface: "ctl", "pcm", "rawmidi", "timer", "seq"

    :return: deviece name hints
    :rtype: CAS2.POINTER(CAS2.POINTER(CAS2.c_void_p))
    """
    resource = _snd_device_name_hint(CAS2.c_int(card), iface.encode())
    try:
        yield resource
    finally:
        _snd_device_name_free_hint(hints=resource.contents)


_snd_device_name_hint = _prototype(
    CAS2.c_int,
    "snd_device_name_hint",
    (CAS2.c_int, 1, "card"),
    (CAS2.c_char_p, 1, "iface"),
    (CAS2.POINTER(CAS2.POINTER(CAS2.c_void_p)), 2, "hints"),
)
"""Called from [_open_device_name_hint]"""


def _errcheck_snd_device_name_hint(result: Any, cfunc: Callable, args: tuple) -> Any:
    if result != 0:
        raise AS2Error((cfunc, args))
    return args[2]


_snd_device_name_hint.errcheck = _errcheck_snd_device_name_hint

_snd_device_name_free_hint = _prototype(
    CAS2.c_int, "snd_device_name_free_hint", (CAS2.POINTER(CAS2.c_void_p), 1, "hints")
)
"""Called from [_open_device_name_hint]"""
_snd_device_name_free_hint.errcheck = _errcheck_non_zero


_snd_device_name_get_hint = _prototype(
    CAS2.c_char_p,
    "snd_device_name_get_hint",
    (CAS2.c_void_p, 1, "hint"),
    (CAS2.c_char_p, 1, "id"),
)
"""Extract the name from hint.

The return value should be freed when no longer needed.
:param c_void_p hint:
:param c_char_p id: b"NAME", b"DESC", b"IOID"
:return: an allocated ASCII string
:rtype: c_char_p
"""


_snd_card_next = _prototype(
    CAS2.c_int, "snd_card_next", (CAS2.POINTER(CAS2.c_int), 1, "rcard")
)
"""Iterate over physical sound cards.

:param POINTER(c_int) rcard:
Index of current card. The index of the next card is stored here.
:return: zero if success, otherwise a negative error code.
:rtype: c_int
"""
_snd_card_next.errcheck = _errcheck_non_zero


"""The simple mixer interface."""


class SND_MIXER_SELEM_CHANNEL_ID_T(IntEnum):
    UNKNOWN = -1
    FRONT_LEFT = auto()
    FRONT_RIGHT = auto()
    REAR_LEFT = auto()
    REAR_RIGHT = auto()
    FRONT_CENTER = auto()
    WOOFER = auto()
    SIDE_LEFT = auto()
    SIDE_RIGHT = auto()
    REAR_CENTER = auto()
    MONO = FRONT_LEFT
    LAST = 31


@contextmanager
def _open_mixer(name: str, mode: int = 0, options=None, classp=None):
    """Opens an empty mixer.

    :param str name: HCTL name
    :param int mode: 0(0x0000) is blocking mode
        SND_CTL_NOBLOCK  0x0001: Non blocking mode  (flag for open mode)
        SND_CTL_ASYNC    0x0002: Async notification (flag for open mode)
        SND_CTL_READONLY 0x0004: Read only          (flag for open mode)
    :return: mixer handler, otherwise a negative error code
    :rtype: snd_mixer_t*
    """
    resource = _snd_mixer_open(mode=CAS2.c_int(mode))
    _snd_mixer_attach(mixer=resource, name=name.encode())
    _snd_mixer_selem_register(mixer=resource, options=options, classp=classp)
    _snd_mixer_load(mixer=resource)
    try:
        yield resource
    finally:
        _snd_mixer_close(mixer=resource)


_snd_mixer_open = _prototype(
    CAS2.c_int,
    "snd_mixer_open",
    (CAS2.POINTER(CAS2.c_void_p), 2, "mixerp"),
    (CAS2.c_int, 1, "mode"),
)
"""Called from [_open_mixer].

Opens an empty mixer.
:param c_int mode: Open mode
:return: mixer handle, otherwise a negative error code
:rtype: snd_mixer_t* or c_int
"""


def _errcheck_snd_mixer_open(result: Any, cfunc: Callable, args: tuple) -> Any:
    if result != 0:
        raise AS2Error((cfunc, args))
    return args[0].value


_snd_mixer_open.errcheck = _errcheck_snd_mixer_open

_snd_mixer_close = _prototype(
    CAS2.c_int, "snd_mixer_close", (CAS2.c_void_p, 1, "mixer")
)
"""Called from [_open_mixer].

Close a mixer and free all related resources.
:param snd_mixer_t* mixer: Mixer handle
:return: 0 on success otherwise a negative error code
:rtype: c_int
"""
_snd_mixer_close.errcheck = _errcheck_non_zero


_snd_mixer_attach = _prototype(
    CAS2.c_int,
    "snd_mixer_attach",
    (CAS2.c_void_p, 1, "mixer"),
    (CAS2.c_char_p, 1, "name"),
)
"""Called from [_open_mixer].

Attach an HCTL specified with the CTL device name to an opened mixer.
:param snd_mixer_t* mixer: mixer handler
:param const char* name: HCTL name
:return: 0 on success otherwise a negative error code
:rtype: c_int
"""
_snd_mixer_attach.errcheck = _errcheck_non_zero

_snd_mixer_selem_register = _prototype(
    CAS2.c_int,
    "snd_mixer_selem_register",
    (CAS2.c_void_p, 1, "mixer"),
    (CAS2.c_void_p, 1, "options"),
    (CAS2.POINTER(CAS2.c_void_p), 1, "classp"),
)
"""Called from [_open_mixer].

Register mixer simple element class.
:param snd_mixet_t* mixer: Mixer handle
:param struct snd_mixer_selem_regopt* options: Options container
:param snd_mixer_class_t** classp:
Pointer to returned mixer simple element class handle (or NULL)
:return: 0 on success otherwise a negative error code
:rtype: c_int
"""
_snd_mixer_selem_register.errcheck = _errcheck_non_zero

_snd_mixer_load = _prototype(CAS2.c_int, "snd_mixer_load", (CAS2.c_void_p, 1, "mixer"))
"""Called from [_open_mixer].

Load a mixer elements.
:param snd_mixer_t* mixer: Mixer handle
:return: 0 on success otherwise a negative error code
:rtype: c_int
"""
_snd_mixer_load.errcheck = _errcheck_non_zero


@contextmanager
def _open_mixer_selem_id(idname: str):
    """allocate an invalid snd_mixer_selem_id_t using standard malloc

    :param * idname: name part
    :return: ptr otherwise negative error code
    :rtype: snd_mixer_selem_id_t*
    """
    resource = _snd_mixer_selem_id_malloc()
    _snd_mixer_selem_id_set_index(obj=resource, val=0)
    _snd_mixer_selem_id_set_name(obj=resource, val=idname.encode())
    try:
        yield resource
    finally:
        _snd_mixer_selem_id_free(obj=resource)


_snd_mixer_selem_id_malloc = _prototype(
    CAS2.c_int, "snd_mixer_selem_id_malloc", (CAS2.POINTER(CAS2.c_void_p), 2, "ptr")
)
"""Called from [_open_mixer_selem_id].

allocate an invalid snd_mixer_selem_id_t using standard malloc
:return: returned pointer, otherwise negative error code
:rtype: snd_mixer_selem_id_t* or c_int
"""


def _errcheck_snd_mixer_selem_id_malloc(
    result: Any, cfunc: Callable, args: tuple
) -> Any:
    if result != 0:
        raise AS2Error((cfunc, args))
    return args[0].value


_snd_mixer_selem_id_malloc.errcheck = _errcheck_snd_mixer_selem_id_malloc

_snd_mixer_selem_id_free = _prototype(
    CAS2.c_void_p, "snd_mixer_selem_id_free", (CAS2.c_void_p, 1, "obj")
)
"""Called from [_open_mixer_selem_id].

frees a previously allocated snd_mixer_selem_id_t
:param snd_mixer_selem_id_t* obj: pointer to object to free
"""

_snd_mixer_selem_id_set_index = _prototype(
    CAS2.c_void_p,
    "snd_mixer_selem_id_set_index",
    (CAS2.c_void_p, 1, "obj"),
    (CAS2.c_uint, 1, "val"),
)
"""Called from [_open_mixer_selem_id].

Set index part of a mixer simple element identifier.
:param snd_mixer_selem_id_t* obj: Mixer simple element identifier
:param c_uint val: index part
"""


_snd_mixer_selem_id_set_name = _prototype(
    CAS2.c_void_p,
    "snd_mixer_selem_id_set_name",
    (CAS2.c_void_p, 1, "obj"),
    (CAS2.c_char_p, 1, "val"),
)
"""Called from [_open_mixer_selem_id].

Set name part of a mixer simple element identifier.
:param snd_mixer_selem_id_t* obj: Mixer simple element identifier
:param c_char_p val: name part
"""

_snd_mixer_find_selem = _prototype(
    CAS2.c_void_p,
    "snd_mixer_find_selem",
    (CAS2.c_void_p, 1, "mixer"),
    (CAS2.c_void_p, 1, "id"),
)
"""Find a mixer simple element.

:param snd_mixer_t* mixer: Mixer handle
:param snd_mixer_selem_id_t* id: Mixer simple element identifier
:return: mixer simple element handle or NULL if not found
:rtype: snd_mixer_elem_t*
"""


def _errcheck_snd_mixer_find_selem(result: Any, cfunc: Callable, args: tuple) -> Any:
    if result is None:
        raise AS2Error((cfunc, args))
    return result


_snd_mixer_find_selem.errchek = _errcheck_snd_mixer_find_selem

_snd_mixer_selem_is_enumerated = _prototype(
    CAS2.c_int, "snd_mixer_selem_is_enumerated", (CAS2.c_void_p, 1, "elem")
)
"""Return true if mixer simple element is an enumerated control.

:param snd_mixer_elem_t* elem: Mixer simple element handle
:param c_int: 0 normal volume/switch control, 1 enumerated control
"""


_snd_mixer_selem_has_playback_volume = _prototype(
    CAS2.c_int, "snd_mixer_selem_has_playback_switch", (CAS2.c_void_p, 1, "elem")
)
"""Return info about playback volume control of a mixer simple element.

:param snd_mixer_elem_t* elem: Mixer simple element handle
:return: 0 if no control is present, 1 if it's present
:rtype: c_int
"""

_snd_mixer_selem_channel_name = _prototype(
    CAS2.c_char_p, "snd_mixer_selem_channel_name", (CAS2.c_int, 1, "channel")
)
"""Return name of mixer simple element channel.

:param c_int[SND_MIXER_SELEM_CHANNNEL_ID_T] channel:
mixer simple element channel identifier
:return:channel name
:rtype: c_char_p
"""


_snd_mixer_selem_is_playback_mono = _prototype(
    CAS2.c_int, "snd_mixer_selem_is_playback_mono", (CAS2.c_void_p, 1, "elem")
)
"""Get info about channels of playback stream of a mixer simple element.

:param snd_mixer_elem_t* elem: Mixer simple element handle
:return: 0 if not mono, 1 if mono
:rtype: c_int
"""

_snd_mixer_selem_has_playback_channel = _prototype(
    CAS2.c_int,
    "snd_mixer_selem_has_playback_channel",
    (CAS2.c_void_p, 1, "elem"),
    (CAS2.c_int, 1, "channel"),
)
"""Get info about channels of playback stream of a mixer simple element.

:param snd_mixer_elem_t* elem: Mixer simple element handle
:param c_int[SND_MIXER_SELEM_CHANNEL_ID_T] channel:
    Mixer simple element channel identifier
:return: 0 if channel is not present, 1 if present
:rtype: c_int
"""


def list_name_hint() -> None:
    """Save the name hints table to a file.

    :var path-like f: "docs/alsa-namehint.md"

    +-----+-----+-----+-----+
    |iface|NAME |DECS |IOID |
    +=====+=====+=====+=====+
    |ctl  |pulse|None |None |
    +-----+-----+-----+-----+
    """
    result: list[str] = list()
    result.append("|iface|NAME|DECS|IOID|")
    result.append("|---|---|---|---|")
    for iface in ["ctl", "pcm", "rawmidi", "timer", "seq"]:
        with _open_device_name_hint(card=-1, iface=iface) as hints:
            for hint in hints:
                if hint is None:
                    break
                name = _snd_device_name_get_hint(hint=hint, id=b"NAME").decode()
                decs = _snd_device_name_get_hint(hint=hint, id=b"DESC")
                decs = "<br>".join(decs.decode().splitlines()) if decs else decs
                ioid = _snd_device_name_get_hint(hint=hint, id=b"IOID")
                ioid = ioid.decode() if ioid else ioid
                result.append(f"|{iface}|{name}|{decs}|{ioid}|")

    with open("memorandum/alsa-namehint.md", "wt") as f:
        print(
            f"# ALSA sound library version: {bytes(_snd_asoundlib_version()).decode()}",
            file=f,
        )
        for name_hint in result:
            print(name_hint, file=f)


def _physical_soundcard_indexs() -> list[int]:
    """Returns a list of physical sound card indexes.

    :return: physical sound card indexes
    :examples: [0, 1, 2]
    """
    index_list: list[int] = list()
    index: CAS2.c_int = CAS2.c_int(0)
    while index.value != -1:
        index_list.append(index.value)
        _snd_card_next(CAS2.byref(index))
    return index_list


def _physical_mixer_names() -> list[str]:
    """Returns a list of names of mixer-compatible physical sound cards.

    :return: names of mixer-compatible physical sound cards
    :examples: ["hw:CARD=Headphones", "hw:CARD=S"]
    """
    mixer_names: list[str] = list()
    mixer_indexs = _physical_soundcard_indexs()
    for index in mixer_indexs:
        with _open_device_name_hint(card=index, iface="ctl") as hints:
            name = _snd_device_name_get_hint(hint=hints[0], id=b"NAME")

        with _open_mixer(name=name.decode()) as mixer:
            with _open_mixer_selem_id(idname="PCM") as selem_id:
                if _snd_mixer_find_selem(mixer=mixer, id=selem_id):
                    mixer_names.append(name.decode())
    return mixer_names


def _amixer_volume(amixer_command: list) -> int:
    """Controlling the volume.

    :param list amixer_command: shell command for amixer volume control
    :examples: ["amixer", "-D", devicename, "--", "sset", idname, svalue, "-M", mute]
    :examples: ["amixer", "-D", devicename, "--", "sget", idname, "-M"]
    :return: volume
    """
    chan_names: list[str] = _channel_names(
        devicename=amixer_command[2], idname=amixer_command[5]
    )
    volumepattern = "/\\[.+%\\]/"
    # unmutepattern = "/\\[(on|off)\\]/"
    volumes = list()

    for chan_name in chan_names:
        awk_command = [
            "awk",
            "/"
            + chan_name
            + ": Playback/ {if(match($0, "
            + volumepattern
            + ")) print substr($0, RSTART+1, RLENGTH-3)}",
        ]
        with Popen(args=amixer_command, stdout=PIPE) as res:
            with Popen(args=awk_command, stdin=res.stdout, stdout=PIPE) as res2:
                volumes.append(int(res2.communicate()[0]))
    return int(mean(volumes))


def get_volume(devicename: str, idname: str) -> int:
    """Get volume.

    :param devicename: devicename
    :param idname: idname
    :return: volume[%]
    """
    command = ["amixer", "-D", devicename, "--", "sget", idname, "-M"]
    return _amixer_volume(command)


def set_volume(devicename: str, idname: str, value: int) -> int:
    """Set volume.

    :param devicename: devicename
    :param idname: idname
    :param value: volume[%] to be set
    :return: volume[%]
    """
    svalue: str = str(value) + "%"
    command = ["amixer", "-D", devicename, "--", "sset", idname, svalue, "-M", "unmute"]
    return _amixer_volume(command)


def _channel_names(devicename: str, idname: str) -> list:
    """channel_names _summary_

    :param str devicename: devicename
    :param str idname: idname
    :raises AS2Error: "enumrate control"
    :raises AS2Error: "no control playback volume"
    :return: channel names
    :examples: ["Mono"]
    :examples: ["Front Left", "Front Right"]
    """
    result: list[str] = list()
    with _open_mixer(name=devicename) as mixer:
        with _open_mixer_selem_id(idname=idname) as id:
            elem = _snd_mixer_find_selem(mixer=mixer, id=id)
            if _snd_mixer_selem_is_enumerated(elem=elem) == 1:
                raise AS2Error("enumrate control")
            if _snd_mixer_selem_has_playback_volume(elem=elem) == 0:
                raise AS2Error("no control playback volume")

            if _snd_mixer_selem_is_playback_mono(elem=elem):
                result = ["Mono"]
            else:
                for channel in list(SND_MIXER_SELEM_CHANNEL_ID_T):
                    if _snd_mixer_selem_has_playback_channel(
                        elem=elem, channel=channel
                    ):
                        buffer = _snd_mixer_selem_channel_name(channel=channel)
                        result.append(buffer.decode())
    return result


def mixer_device() -> list[str]:
    """Returns information on available mixer devices.

    :return: [device name, device idname, control name, control idname, name]
    :examples: ["hw:CARD=Headphones", "PCM", "default", "Master", "Headphones"]
    :examples: ["", "", "", "", ""] if not found.
    """
    result: list[str] = ["", "", "", "", ""]
    logger.info("Mixer Device: Search Bluetooth devices...")
    btdevice: dict[str, str] = btaudiosink.device_info()
    logger.info("Mixer Device: Search Physical Sound devices...")
    soundcard: list[str] = _physical_mixer_names()

    if "" not in btdevice:
        result[0] = "bluealsa:00:00:00:00:00:00"
        result[1] = "A2DP"
        result[2] = result[0]
        result[3] = result[1]
        result[4] = list(btdevice)[0]
    elif len(soundcard):
        result[0] = soundcard[-1]
        result[1] = "PCM"
        result[2] = "default"
        result[3] = "Master"
        result[4] = soundcard[-1].split("=")[1]
    else:
        logger.info("Mixer Device: not found.")

    return result


def start_jackserver() -> list[str]:
    """Start JACK server.

    :return: [device name, device idname, control name, control idname, name]
    :examples: ["hw:CARD=Headphones", "PCM", "default", "Master", "Headphones"]
    :examples: ["", "", "", "", ""] if Not registered.

    :Todo: Connect to Headphones after Bluetooth device disconnects.
    """

    device_info: list[str] = mixer_device()

    if "" not in device_info:
        with open(file="config/jack.json", mode="rt") as f:
            settings = load(f)
            for type, commandlist in settings[device_info[0]].items():
                for command in commandlist:
                    with Popen(command.split()) as res:
                        if res.returncode:
                            logger.info("Mixer Device: Not registered.")
                            return ["", "", "", "", ""]

    return device_info


if __name__ == "__main__":
    print(__file__)
