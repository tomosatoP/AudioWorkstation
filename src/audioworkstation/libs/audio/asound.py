#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Purpose: Detect and configure sound card, adjust volume.

https://www.alsa-project.org/alsa-doc/alsa-lib/index.html
"""

from typing import Callable, Any
from contextlib import contextmanager
from enum import IntEnum, auto
import ctypes as CAS2
from ctypes.util import find_library


class AS2Error(Exception):
    """Exceptions sent out from errcheck func."""

    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        print(f"ASError: {args}")


def errcheck_non_zero(result: Any, cfunc: Callable, args: tuple) -> Any:
    if result != 0:
        raise AS2Error((cfunc, args))
    return result


"""libasound2"""
_libas2 = CAS2.CDLL(name=find_library(name="asound"), use_errno=True)


def prototype(restype: Any, name: str, *params: tuple) -> Any:
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

"""snd_asoundlib_version

:return c_char_p:
"""
snd_asoundlib_version = prototype(CAS2.c_char_p, "snd_asoundlib_version")

"""The control interface."""


@contextmanager
def open_device_name_hint(card: int, iface: str):
    """Get a aset of device name hints(array of hint) .

    :param int card: index of physical sound card
    :param str iface: "ctl", "pcm", "rawmidi", "timer", "seq"
    :return CAS2.POINTER(CAS2.POINTER(CAS2.c_void_p)): deviece name hints
    """
    resource = snd_device_name_hint(CAS2.c_int(card), iface.encode())
    try:
        yield resource
    finally:
        snd_device_name_free_hint(hints=resource.contents)


snd_device_name_hint = prototype(
    CAS2.c_int,
    "snd_device_name_hint",
    (CAS2.c_int, 1, "card"),
    (CAS2.c_char_p, 1, "iface"),
    (CAS2.POINTER(CAS2.POINTER(CAS2.c_void_p)), 2, "hints"),
)


def errcheck_snd_device_name_hint(result: Any, cfunc: Callable, args: tuple) -> Any:
    if result != 0:
        raise AS2Error((cfunc, args))
    return args[2]


snd_device_name_hint.errcheck = errcheck_snd_device_name_hint

snd_device_name_free_hint = prototype(
    CAS2.c_int, "snd_device_name_free_hint", (CAS2.POINTER(CAS2.c_void_p), 1, "hints")
)
snd_device_name_free_hint.errcheck = errcheck_non_zero


""" snd_device_name_get_hint

The return value should be freed when no longer needed.
:param c_void_p hint:
:param c_char_p id: b"NAME", b"DESC", b"IOID"
:return c_char_p: an allocated ASCII string
"""
snd_device_name_get_hint = prototype(
    CAS2.c_char_p,
    "snd_device_name_get_hint",
    (CAS2.c_void_p, 1, "hint"),
    (CAS2.c_char_p, 1, "id"),
)


""" snd_card_next

:param POINTER(c_int) rcard:
:return c_int:
"""
snd_card_next = prototype(
    CAS2.c_int, "snd_card_next", (CAS2.POINTER(CAS2.c_int), 1, "rcard")
)
snd_card_next.errcheck = errcheck_non_zero


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
def open_mixer(name: str, mode: int = 0, options=None, classp=None):
    """Opens an empty mixer.

    :param c_int mode: 0(0x0000) is blocking mode
        SND_CTL_NOBLOCK  0x0001: Non blocking mode  (flag for open mode)
        SND_CTL_ASYNC    0x0002: Async notification (flag for open mode)
        SND_CTL_READONLY 0x0004: Read only          (flag for open mode)
    :return snd_mixer_t*: mixer handler, otherwise a negative error code
    """
    resource = snd_mixer_open(mode=CAS2.c_int(mode))
    snd_mixer_attach(mixer=resource, name=name.encode())
    snd_mixer_selem_register(mixer=resource, options=options, classp=classp)
    snd_mixer_load(mixer=resource)
    try:
        yield resource
    finally:
        snd_mixer_close(mixer=resource)


snd_mixer_open = prototype(
    CAS2.c_int,
    "snd_mixer_open",
    (CAS2.POINTER(CAS2.c_void_p), 2, "mixerp"),
    (CAS2.c_int, 1, "mode"),
)


def errcheck_snd_mixer_open(result: Any, cfunc: Callable, args: tuple) -> Any:
    if result != 0:
        raise AS2Error((cfunc, args))
    return args[0].value


snd_mixer_open.errcheck = errcheck_snd_mixer_open

snd_mixer_close = prototype(CAS2.c_int, "snd_mixer_close", (CAS2.c_void_p, 1, "mixer"))
snd_mixer_close.errcheck = errcheck_non_zero


"""snd_mixer_attach

Attach an HCTL specified with the CTL device name to an opened mixer.
:param snd_mixer_t* mixer: mixer handler
:param const char* name: HCTL name
:return c_int: 0 on success otherwise a negative error code
"""
snd_mixer_attach = prototype(
    CAS2.c_int,
    "snd_mixer_attach",
    (CAS2.c_void_p, 1, "mixer"),
    (CAS2.c_char_p, 1, "name"),
)
snd_mixer_attach.errcheck = errcheck_non_zero

"""snd_mixer_selem_register

Register mixer simple element class.
:param snd_mixet_t* mixer: Mixer handle
:param struct snd_mixer_selem_regopt* options: Options container
:param snd_mixer_class_t** classp:
    Pointer to returned mixer simple element class handle (or NULL)
:return c_int: 0 on success otherwise a negative error code
"""
snd_mixer_selem_register = prototype(
    CAS2.c_int,
    "snd_mixer_selem_register",
    (CAS2.c_void_p, 1, "mixer"),
    (CAS2.c_void_p, 1, "options"),
    (CAS2.POINTER(CAS2.c_void_p), 1, "classp"),
)
snd_mixer_selem_register.errcheck = errcheck_non_zero

"""snd_mixer_load

Load a mixer elements.
:param snd_mixer_t* mixer: Mixer handle
:return c_int: 0 on success otherwise a negative error code
"""
snd_mixer_load = prototype(CAS2.c_int, "snd_mixer_load", (CAS2.c_void_p, 1, "mixer"))
snd_mixer_load.errcheck = errcheck_non_zero


@contextmanager
def open_mixer_selem_id(name: str):
    """allocate an invalid snd_mixer_selem_id_t using standard malloc

    :return snd_mixer_selem_id_t*: ptr otherwise negative error code
    """
    resource = snd_mixer_selem_id_malloc()
    snd_mixer_selem_id_set_index(obj=resource, val=0)
    snd_mixer_selem_id_set_name(obj=resource, val=name.encode())
    try:
        yield resource
    finally:
        snd_mixer_selem_id_free(obj=resource)


snd_mixer_selem_id_malloc = prototype(
    CAS2.c_int, "snd_mixer_selem_id_malloc", (CAS2.POINTER(CAS2.c_void_p), 2, "ptr")
)


def errcheck_snd_mixer_selem_id_malloc(
    result: Any, cfunc: Callable, args: tuple
) -> Any:
    if result != 0:
        raise AS2Error((cfunc, args))
    return args[0].value


snd_mixer_selem_id_malloc.errcheck = errcheck_snd_mixer_selem_id_malloc

snd_mixer_selem_id_free = prototype(
    CAS2.c_void_p, "snd_mixer_selem_id_free", (CAS2.c_void_p, 1, "obj")
)

"""snd_mixer_selem_id_set_index

Set index part of a mixer simple element identifier.
:param snd_mixer_selem_id_t* obj: Mixer simple element identifier
:param c_uint val: index part
"""
snd_mixer_selem_id_set_index = prototype(
    CAS2.c_void_p,
    "snd_mixer_selem_id_set_index",
    (CAS2.c_void_p, 1, "obj"),
    (CAS2.c_uint, 1, "val"),
)


"""snd_mixer_selem_id_set_name

Set name part of a mixer simple element identifier.
:param snd_mixer_selem_id_t* obj: Mixer simple element identifier
:param c_char_p val: name part
"""
snd_mixer_selem_id_set_name = prototype(
    CAS2.c_void_p,
    "snd_mixer_selem_id_set_name",
    (CAS2.c_void_p, 1, "obj"),
    (CAS2.c_char_p, 1, "val"),
)

"""snd_mixer_find_selem

Find a mixer simple element.
:param snd_mixer_t* mixer: Mixer handle
:param id: Mixer simple element identifier
:return snd_mixer_elem_t*: mixer simple element handle or NULL if not found
"""
snd_mixer_find_selem = prototype(
    CAS2.c_void_p,
    "snd_mixer_find_selem",
    (CAS2.c_void_p, 1, "mixer"),
    (CAS2.c_void_p, 1, "id"),
)


def errcheck_snd_mixer_find_selem(result: Any, cfunc: Callable, args: tuple) -> Any:
    if result is None:
        raise AS2Error((cfunc, args))
    return result


snd_mixer_find_selem.errchek = errcheck_snd_mixer_find_selem

"""snd_mixer_selem_get_playback_volume_range

Get range for playback volume of a mixer simple element.

:param snd_mixer_elem_t* elem: Mixer simple element handle
:return c_long, c_long: (minimum, maximum)
"""
snd_mixer_selem_get_playback_volume_range = prototype(
    CAS2.c_int,
    "snd_mixer_selem_get_playback_volume_range",
    (CAS2.c_void_p, 1, "elem"),
    (CAS2.POINTER(CAS2.c_long), 2, "min"),
    (CAS2.POINTER(CAS2.c_long), 2, "max"),
)


def errcheck_snd_mixer_selem_get_playback_volume_range(
    result: Any, cfunc: Callable, args: tuple
) -> Any:
    if result != 0:
        raise AS2Error((cfunc, args))
    return (args[1].value, args[2].value)


snd_mixer_selem_get_playback_volume_range.errcheck = (
    errcheck_snd_mixer_selem_get_playback_volume_range
)


"""snd_mixer_selem_get_playback_volume

Return value of playback volume control of a mixer simple element.
:param snd_mexer_elem_t* elem: Mixer simple element handle
:param c_int[SND_MIXER_SELEM_CHANNEL_ID_T] channel:
    mixer simple element channel identifier
:return c_long: value on success otherwise a negative error code
"""
snd_mixer_selem_get_playback_volume = prototype(
    CAS2.c_int,
    "snd_mixer_selem_get_playback_volume",
    (CAS2.c_void_p, 1, "elem"),
    (CAS2.c_int, 1, "channel"),
    (CAS2.POINTER(CAS2.c_long), 2, "value"),
)


def errcheck_snd_mixer_selem_get_playback_volume(
    result: Any, cfunc: Callable, args: tuple
) -> Any:
    if result != 0:
        raise AS2Error((cfunc, args))
    return args[2].value


snd_mixer_selem_get_playback_volume.errcheck = (
    errcheck_snd_mixer_selem_get_playback_volume
)

"""snd_mixer_selem_is_enumerated

Return true if mixer simple element is an enumerated control.
:param snd_mixer_elem_t* elem: Mixer simple element handle
:param c_int: 0 normal volume/switch control, 1 enumerated control
"""
snd_mixer_selem_is_enumerated = prototype(
    CAS2.c_int, "snd_mixer_selem_is_enumerated", (CAS2.c_void_p, 1, "elem")
)


"""snd_mixer_selem_has_playback_switch

Return info about playback switch control existence of a mixer simple element.
:param snd_mixer_elem_t* elem: Mixer simple element handle
:return c_int: 0 if no control is present, 1 if it's present
"""
snd_mixer_selem_has_playback_switch = prototype(
    CAS2.c_int, "snd_mixer_selem_has_playback_switch", (CAS2.c_void_p, 1, "elem")
)


"""snd_mixer_selem_has_playback_volume

Return info about playback volume control of a mixer simple element.
:param snd_mixer_elem_t* elem: Mixer simple element handle
:return c_int: 0 if no control is present, 1 if it's present
"""
snd_mixer_selem_has_playback_volume = prototype(
    CAS2.c_int, "snd_mixer_selem_has_playback_switch", (CAS2.c_void_p, 1, "elem")
)

"""snd_mixer_selem_channel_name

Return name of mixer simple element channel.
:param c_int[SND_MIXER_SELEM_CHANNNEL_ID_T] channel:
    mixer simple element channel identifier
:return c_char_p :channel name
"""
snd_mixer_selem_channel_name = prototype(
    CAS2.c_char_p, "snd_mixer_selem_channel_name", (CAS2.c_int, 1, "channnel")
)


"""snd_mixer_selem_is_playback_mono

Get info about channels of playback stream of a mixer simple element.
:param snd_mixer_elem_t* elem: Mixer simple element handle
:return: 0 if not mono, 1 if mono
"""
snd_mixer_selem_is_playback_mono = prototype(
    CAS2.c_int, "snd_mixer_selem_is_playback_mono", (CAS2.c_void_p, 1, "elem")
)

"""snd_mixer_selem_has_playback_channel

Get info about channels of playback stream of a mixer simple element.
:param snd_mixer_elem_t* elem: Mixer simple element handle
:param c_int[SND_MIXER_SELEM_CHANNEL_ID_T] channel:
    Mixer simple element channel identifier
:return c_int: 0 if channel is not present, 1 if present
"""
snd_mixer_selem_has_playback_channel = prototype(
    CAS2.c_int,
    "snd_mixer_selem_has_playback_channel",
    (CAS2.c_void_p, 1, "elem"),
    (CAS2.c_int, 1, "channel"),
)


def print_name_hint():
    """print name hint

    :example:
    @ |iface|NAME |DECS |IOID |
    @ | --- | --- | --- | --- |
    @ |ctl  |pulse|None |None |
    """
    print("|iface|NAME|DECS|IOID|")
    print("|---|---|---|---|")
    for iface in ["ctl", "pcm", "rawmidi", "timer", "seq"]:
        with open_device_name_hint(card=-1, iface=iface) as hints:
            for hint in hints:
                if hint is None:
                    break
                name = snd_device_name_get_hint(hint=hint, id=b"NAME")
                decs = snd_device_name_get_hint(hint=hint, id=b"DESC")
                ioid = snd_device_name_get_hint(hint=hint, id=b"IOID")
                print(f"|{iface}|{name}|{decs}|{ioid}|")


def physical_sound_card_indexs() -> list[int]:
    """Returns a list of physical sound card indexes.

    :return list[int]: ex) [0, 1, 2]
    """
    index_list: list[int] = list()
    index: CAS2.c_int = CAS2.c_int(0)
    while index.value != -1:
        index_list.append(index.value)
        snd_card_next(CAS2.byref(index))
    return index_list


def physical_mixer_names() -> list[str]:
    """Returns a list of names of mixer-compatible physical sound cards.

    :return list[str]: ex) ["hw:CARD=Headphones"]
    """
    name_list: list[str] = list()
    index_list = physical_sound_card_indexs()
    for index in index_list:
        with open_device_name_hint(card=index, iface="ctl") as hints:
            name = snd_device_name_get_hint(hint=hints[0], id=b"NAME")

        with open_mixer(name=name.decode()) as mixer:
            with open_mixer_selem_id(name="PCM") as selem_id:
                if snd_mixer_find_selem(mixer=mixer, id=selem_id):
                    name_list.append(name.decode())
    return name_list


def mixer_volume(name: str = "default"):
    """mixer_volume _summary_

    :param str name: _description_, defaults to "default"
    """
    volumes: dict[str, int] = dict()
    volume_range: dict[str, int] = {"min": 0, "max": 0}
    id_name = "Master" if name == "default" else "PCM"
    with open_mixer(name=name) as mixer:
        with open_mixer_selem_id(name=id_name) as id:
            elem = snd_mixer_find_selem(mixer=mixer, id=id)
            if snd_mixer_selem_is_enumerated(elem=elem) == 1:
                raise AS2Error("enumrate control")
            if snd_mixer_selem_has_playback_switch(elem=elem) == 0:
                raise AS2Error("no switch control")
            if snd_mixer_selem_has_playback_volume(elem=elem) == 0:
                raise AS2Error("no volume control")

            (
                volume_range["min"],
                volume_range["max"],
            ) = snd_mixer_selem_get_playback_volume_range(elem=elem)

            if snd_mixer_selem_is_playback_mono(elem=elem) == 1:
                volumes["Mono"] = snd_mixer_selem_get_playback_volume(
                    elem=elem, channel=SND_MIXER_SELEM_CHANNEL_ID_T.MONO
                )
            else:
                channels: list = list(
                    filter(
                        lambda x: snd_mixer_selem_has_playback_channel(
                            elem=elem, channel=x
                        )
                        == 1,
                        list(SND_MIXER_SELEM_CHANNEL_ID_T),
                    )
                )
                for chan in channels:
                    volumes[
                        snd_mixer_selem_channel_name(chan).decode()
                    ] = snd_mixer_selem_get_playback_volume(
                        elem=elem,
                        channel=chan,
                    )

    return volumes


if __name__ == "__main__":
    print(__file__)

    print(f"ALSA sound library version: {bytes(snd_asoundlib_version()).decode()}")

    print_name_hint()
    print(physical_mixer_names())
    print(f"default: volume( )={mixer_volume()}")
    print(f"Headphones: volume( )={mixer_volume('hw:CARD=Headphones')}")
