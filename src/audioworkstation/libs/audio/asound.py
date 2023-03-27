#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Purpose: Detect and configure sound card, adjust volume.

https://www.alsa-project.org/alsa-doc/alsa-lib/index.html
https://github.com/alsa-project/alsa-python/blob/master/pyalsa/alsacard.c
"""

from typing import Callable, Any
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


""" snd_asoundlib_version

:return c_char_p:
"""
snd_asoundlib_version = prototype(CAS2.c_char_p, "snd_asoundlib_version")

""" snd_device_name_hint

Get a set of device name hints.
hints will receive a NULL-terminated array of device name hints,
which can be passed to snd_device_name_get_hint to extract usable values.
When no longer needed,
hints should be passed to "snd_device_name_free_hint" to release resources.
:param c_int card:
:param c_char_p iface: b"ctl", b"pcm", b"rawmidi", b"timer", b"seq"
:return CAS2.POINTER(CAS2.POINTER(CAS2.c_void_p)): deviece name hints
"""
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

""" snd_device_name_free_hint

Free a list of device name hints.
:param CAS2.POINTER(CAS2.c_void_p) hints: List to free
:return c_int: zero if success, otherwise a negative error code
"""
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

snd_card_load = prototype(CAS2.c_int, "snd_card_load", (CAS2.c_int, 1, "card"))

""" snd_card_get_name

:param c_int card: index of the card
:return c_char_p: card name corresponding to card index
"""
snd_card_get_name = prototype(
    CAS2.c_int,
    "snd_card_get_name",
    (CAS2.c_int, 1, "card"),
    (CAS2.POINTER(CAS2.c_char_p), 2, "name"),
)


def errcheck_snd_card_get_name(result: Any, cfunc: Callable, args: tuple) -> Any:
    if result != 0:
        raise AS2Error((cfunc, args))
    return args[1]


snd_card_get_name.errcheck = errcheck_snd_card_get_name

""" snd_card_get_longname

:param c_int card: index of the card
:return c_char_p: card long name corresponding to card index
"""
snd_card_get_longname = prototype(
    CAS2.c_int,
    "snd_card_get_longname",
    (CAS2.c_int, 1, "card"),
    (CAS2.POINTER(CAS2.c_char_p), 2, "name"),
)


def errcheck_snd_card_get_longname(result: Any, cfunc: Callable, args: tuple) -> Any:
    if result != 0:
        raise AS2Error((cfunc, args))
    return args[1]


snd_card_get_longname.errcheck = errcheck_snd_card_get_longname

""" snd_card_get_index

:param c_char_p string:
:return c_int: index of the card
"""
snd_card_get_index = prototype(
    CAS2.c_int, "snd_card_get_index", (CAS2.c_char_p, 1, "string")
)
snd_card_get_index.errcheck = errcheck_non_zero

""" snd_card_next

:param POINTER(c_int) rcard:
:return c_int:
"""
snd_card_next = prototype(
    CAS2.c_int, "snd_card_next", (CAS2.POINTER(CAS2.c_int), 1, "rcard")
)
snd_card_next.errcheck = errcheck_non_zero

""" snd_ctl_open

:param c_char_p name:
:param c_int mode: default is blocking mode 0x0000
   SND_CTL_NOBLOCK  0x0001: Non blocking mode  (flag for open mode)
   SND_CTL_ASYNC    0x0002: Async notification (flag for open mode)
   SND_CTL_READONLY 0x0004: Read only          (flag for open mode)
:return POINTER(c_void_p): ctlp
"""
snd_ctl_open = prototype(
    CAS2.c_int,
    "snd_ctl_open",
    (CAS2.POINTER(CAS2.c_void_p), 2, "ctlp"),
    (CAS2.c_char_p, 1, "name"),
    (CAS2.c_int, 1, "mode"),
)


def errcheck_snd_ctl_open(result: Any, cfunc: Callable, args: tuple) -> Any:
    if result != 0:
        raise AS2Error((cfunc, args))
    return args[0].value


snd_ctl_open.errcheck = errcheck_snd_ctl_open

""" snd_ctl_close

Closes the specified CTL handle and frees all associated resources.
:param snd_ctl_t* ctl: CTL handle
:return int: 0 on success otherwise a negative error code
"""
snd_ctl_close = prototype(CAS2.c_int, "snd_ctl_close", (CAS2.c_void_p, 1, "ctl"))
snd_ctl_close.errcheck = errcheck_non_zero

""" snd_ctl_elem_id_malloc

allocate an invalid snd_ctl_elem_id_t using standard malloc.
:return snd_ctl_elem_id_t* ptr:
"""
snd_ctl_elem_id_malloc = prototype(
    CAS2.c_int, "snd_ctl_elem_id_malloc", (CAS2.POINTER(CAS2.c_void_p), 2, "ptr")
)


def errcheck_snd_ctl_elem_id_malloc(result: Any, cfunc: Callable, args: tuple) -> Any:
    if result != 0:
        raise AS2Error((cfunc, args))
    return args[0].value


snd_ctl_elem_id_malloc.errcheck = errcheck_snd_ctl_elem_id_malloc

""" snd_ctl_elem_id_free

frees a previously allocated snd_ctl_elem_id_t
:param snd_ctl_elem_id_t* obj:
"""
snd_ctl_elem_id_free = prototype(
    CAS2.c_void_p, "snd_ctl_elem_id_free", (CAS2.c_void_p, 1, "obj")
)

""" snd_ctl_elem_value_malloc

Allocate an invalid snd_ctl_elem_value_t on the heap.
The allocated memory must be freed using snd_ctl_elem_value_free().
:param snd_ctl_elem_value_t** ptr:
:return: 0 on success, otherwise a negative error code
"""
snd_ctl_elem_value_malloc = prototype(
    CAS2.c_int, "snd_ctl_elem_value_malloc", (CAS2.POINTER(CAS2.c_void_p), 2, "ptr")
)


def errcheck_snd_ctl_elem_value_malloc(
    result: Any, cfunc: Callable, args: tuple
) -> Any:
    if result != 0:
        raise AS2Error((cfunc, args))
    return args[0].value


snd_ctl_elem_value_malloc.errcheck = errcheck_snd_ctl_elem_value_malloc

""" snd_ctl_elem_value_free

Free an snd_ctl_elem_value_t previously allocated using snd_ctl_elem_value_malloc().
:param the snd_ctl_elem_value_t* obj:
"""
snd_ctl_elem_value_free = prototype(
    CAS2.c_void_p, "snd_ctl_elem_value_free", (CAS2.c_void_p, 1, "obj")
)


class SND_CTL_ELEM_IFACE_T(IntEnum):
    CARD = 0
    HWDEP = auto()
    MIXER = auto()
    PCM = auto()
    RAWMIDI = auto()
    TIMER = auto()
    SEQUENCER = auto()


""" snd_ctl_elem_id_set_interface

Set interface part for a CTL element identifier.
:param snd_ctl_elem_id_t* obj: CTL element identifier
:param c_int[enum SND_CTL_ELEM_IFACE_T] val: CTL element related interface
"""
snd_ctl_elem_id_set_interface = prototype(
    CAS2.c_void_p,
    "snd_ctl_elem_id_set_interface",
    (CAS2.c_void_p, 1, "obj"),
    (CAS2.c_int, 1, "val"),
)

""" snd_ctl_elem_id_set_name

Set name part for a CTL element identifier.
:param snd_ctl_elem_id_t* obj: CTL element identifier
:param c_char_p val: CTL element name
"""
snd_ctl_elem_id_set_name = prototype(
    CAS2.c_void_p,
    "snd_ctl_elem_id_set_name",
    (CAS2.c_void_p, 1, "obj"),
    (CAS2.c_char_p, 1, "val"),
)

""" snd_ctl_elem_info_malloc

allocate an invalid snd_ctl_elem_info_t using standard malloc
:param snd_ctl_elem_info_t** ptr: returned pointer
:return c_int:0 on success otherwise negative error code
"""
snd_ctl_elem_info_malloc = prototype(
    CAS2.c_int, "snd_ctl_elem_info_malloc", (CAS2.POINTER(CAS2.c_void_p), 2, "ptr")
)


def errcheck_snd_ctl_elem_info_malloc(result: Any, cfunc: Callable, args: tuple) -> Any:
    if result != 0:
        raise AS2Error((cfunc, args))
    return args[0].value


snd_ctl_elem_info_malloc.errcheck = errcheck_snd_ctl_elem_info_malloc

""" snd_ctl_elem_info_free

frees a previously allocated snd_ctl_elem_info_t
:param snd_ctl_elem_info_t* obj: pointer to object to free
"""
snd_ctl_elem_info_free = prototype(
    CAS2.c_void_p, "snd_ctl_elem_info_free", (CAS2.c_void_p, 1, "obj")
)

""" snd_ctl_elem_info_set_id

Set CTL element identifier of a CTL element id/info.
:param snd_ctl_elem_info_t* obj: CTL element id/info
:param const snd_ctl_elem_id_t* ptr: CTL element identifier
"""
snd_ctl_elem_info_set_id = prototype(
    CAS2.c_void_p,
    "snd_ctl_elem_info_set_id",
    (CAS2.c_void_p, 1, "obj"),
    (CAS2.c_void_p, 1, "ptr"),
)

""" snd_ctl_elem_info

Get CTL element information.
:param snd_ctl_t* ctl: CTL handle
:param snd_ctl_elem_info_t* info: CTL element id/information pointer
0 on success otherwise a negative error code
"""
snd_ctl_elem_info = prototype(
    CAS2.c_int,
    "snd_ctl_elem_info",
    (CAS2.c_void_p, 1, "ctl"),
    (CAS2.c_void_p, 1, "info"),
)
snd_ctl_elem_info.errcheck = errcheck_non_zero

""" snd_ctl_elem_info_get_id

Get CTL element identifier of a CTL element id/info.
:param const snd_ctl_elem_info_t* obj: CTL element id/info
:param snd_ctl_elem_id_t* ptr: Pointer to returned CTL element identifier
"""
snd_ctl_elem_info_get_id = prototype(
    CAS2.c_void_p,
    "snd_ctl_elem_info_get_id",
    (CAS2.c_void_p, 1, "obj"),
    (CAS2.c_void_p, 1, "ptr"),
)

""" snd_ctl_elem_info_get_type

Get type from a CTL element id/info.
:param const snd_ctl_elem_info_t* obj: CTL element id/info
:return snd_ctl_elem_type_t : CTL element content type
"""
snd_ctl_elem_info_get_type = prototype(
    CAS2.c_int, "snd_ctl_elem_info_get_type", (CAS2.c_void_p, 1, "obj")
)

""" snd_ctl_elem_info_get_min

Get minimum value from a SND_CTL_ELEM_TYPE_INTEGER CTL element id/info.
:param const snd_ctl_elem_info_t* obj: CTL element id/info
:return c_long: Minimum value
"""
snd_ctl_elem_info_get_min = prototype(
    CAS2.c_long, "snd_ctl_elem_info_get_min", (CAS2.c_void_p, 1, "obj")
)


""" snd_ctl_elem_value_set_id

Set the element identifier within the given element value.
:param snd_ctl_elem_value_t* obj: The element value
:param const snd_ctl_elem_id_t* ptr: The new identifier
"""
snd_ctl_elem_value_set_id = prototype(
    CAS2.c_void_p,
    "snd_ctl_elem_value_set_id",
    (CAS2.c_void_p, 1, "obj"),
    (CAS2.c_void_p, 1, "ptr"),
)

""" snd_ctl_elem_read

Get CTL element value.
Read information from sound card.
You must set the ID of the element before calling this function.
:param snd_ctl_t* ctl: CTL handle.
:param snd_ctl_elem_value_t* data: The element value.
:return: 0 on success otherwise a negative error code.
"""
snd_ctl_elem_read = prototype(
    CAS2.c_int,
    "snd_ctl_elem_read",
    (CAS2.c_void_p, 1, "ctl"),
    (CAS2.c_void_p, 1, "data"),
)
snd_ctl_elem_read.errcheck = errcheck_non_zero


"""Simple Mixer Interface"""


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


"""snd_mixer_open

Opens an empty mixer.
:param int mode: open mode
:return snd_mixer_t*: mixer handler, otherwise a negative error code
"""
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

"""snd_mixer_close

Close a mixer and free all related resources.
:param snd_mixet_t** mixer:
:returns c_int: 0 on success otherwise a negative error code
"""
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

"""snd_mixer_selem_id_malloc

allocate an invalid snd_mixer_selem_id_t using standard malloc
:return snd_mixer_selem_id_t*: ptr otherwise negative error code
"""
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

"""snd_mixer_selem_id_free

frees a previously allocated snd_mixer_selem_id_t
:param snd_mixer_selem_id_t* obj: pointer to object to free
"""
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
snd_mixer_selem_has_playback_switch.errcheck = errcheck_non_zero


"""snd_mixer_selem_has_playback_volume

Return info about playback volume control of a mixer simple element.
:param snd_mixer_elem_t* elem: Mixer simple element handle
:return c_int: 0 if no control is present, 1 if it's present
"""
snd_mixer_selem_has_playback_volume = prototype(
    CAS2.c_int, "snd_mixer_selem_has_playback_switch", (CAS2.c_void_p, 1, "elem")
)
snd_mixer_selem_has_playback_volume.errcheck = errcheck_non_zero

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


def test_card_list():
    card_list = list()
    card_index = CAS2.c_int(0)

    # Get physical sound card list.
    while card_index.value != -1:
        card_list.append(card_index.value)
        snd_card_next(CAS2.byref(card_index))

    for ci in card_list:
        if int(snd_card_load(CAS2.c_int(ci))) == 1:
            d_present = "present"
        else:
            d_present = "not present"

        sname = snd_card_get_name(card=CAS2.c_int(ci)).value
        lname = snd_card_get_longname(card=CAS2.c_int(ci)).value
        print(
            f"index {ci}: driver is {d_present}: name {sname.decode()}/{lname.decode()}"
        )


def test_name_hint():
    print("|iface|NAME|DECS|IOID|")
    print("|---|---|---|---|")
    ifaces: list[str] = ["ctl", "pcm", "rawmidi", "timer", "seq"]
    ncard: int = int(0)  # if all is -1, otherwise 0 to 3
    for iface in ifaces:
        hints = snd_device_name_hint(card=CAS2.c_int(ncard), iface=iface.encode())
        i = 0
        while hints[i]:
            hint = CAS2.c_void_p(hints[i])
            if hint.value is not None:
                name = snd_device_name_get_hint(hint=hint, id=b"NAME")
                decs = snd_device_name_get_hint(hint=hint, id=b"DESC")
                ioid = snd_device_name_get_hint(hint=hint, id=b"IOID")
                print(f"|{iface}|{name}|{decs}|{ioid}|")
            i += 1
        snd_device_name_free_hint(hints=hints.contents)


def test_control_interface():
    print("default, Master Playback Volume")
    ctl_handler = snd_ctl_open(name=b"default", mode=0)
    ctl_elem_id = snd_ctl_elem_id_malloc()
    ctl_elem_value = snd_ctl_elem_value_malloc()

    snd_ctl_elem_id_set_interface(ctl_elem_id, CAS2.c_int(SND_CTL_ELEM_IFACE_T.MIXER))
    snd_ctl_elem_id_set_name(ctl_elem_id, b"Master Playback Volume")

    ctl_elem_info = snd_ctl_elem_info_malloc()
    snd_ctl_elem_info_set_id(ctl_elem_info, ctl_elem_id)
    snd_ctl_elem_info(ctl_handler, ctl_elem_info)
    # snd_ctl_elem_info_get_owner(ctl_elem_info)
    # snd_ctl_elem_info_get_count(ctl_elem_info)
    # snd_ctl_elem_info_get_interface(ctl_elem_info)
    # snd_ctl_elem_info_get_device(ctl_elem_info)
    # snd_ctl_elem_info_get_subdevice(ctl_elem_info)
    # snd_ctl_elem_info_get_name(ctl_elem_info)
    # snd_ctl_elem_info_get_index(ctl_elem_info)
    print(f"type: {snd_ctl_elem_info_get_type(ctl_elem_info)}")
    print(f"min: {snd_ctl_elem_info_get_min(ctl_elem_info)}")
    # snd_ctl_elem_info_get_max(ctl_elem_info)
    # snd_ctl_elem_info_get_step(ctl_elem_info)
    snd_ctl_elem_info_get_id(ctl_elem_info, ctl_elem_id)
    snd_ctl_elem_info_free(ctl_elem_info)

    snd_ctl_elem_value_set_id(ctl_elem_value, ctl_elem_id)
    snd_ctl_elem_read(ctl_handler, ctl_elem_value)
    # snd_ctl_elem_value_get_integer()

    snd_ctl_elem_value_free(ctl_elem_value)
    snd_ctl_elem_id_free(ctl_elem_id)
    snd_ctl_close(ctl_handler)


def test_simple_mixer_interface():
    list_mixer_playback_name = [
        {"CTL": b"default", "SELEM_NAME": b"Master", "SELEM_INDEX": 0},
        {"CTL": b"hw:CARD=Headphones", "SELEM_NAME": b"PCM", "SELEM_INDEX": 0},
        # {"CTL": b"hw:CARD=S", "SELEM_NAME": b"PCM", "SELEM_INDEX": 0},
    ]
    for mixer_playback_name in list_mixer_playback_name:
        mixer_handler = snd_mixer_open(mode=0)
        snd_mixer_attach(mixer=mixer_handler, name=mixer_playback_name["CTL"])
        snd_mixer_selem_register(mixer=mixer_handler, options=None, classp=None)
        snd_mixer_load(mixer=mixer_handler)

        mixer_selem_id = snd_mixer_selem_id_malloc()
        snd_mixer_selem_id_set_name(
            obj=mixer_selem_id, val=mixer_playback_name["SELEM_NAME"]
        )
        snd_mixer_selem_id_set_index(
            obj=mixer_selem_id, val=mixer_playback_name["SELEM_INDEX"]
        )
        mixer_playback = snd_mixer_find_selem(mixer_handler, mixer_selem_id)

        if snd_mixer_selem_is_enumerated(elem=mixer_playback) == 1:
            print("enumerated control")
        else:
            # playback volume control
            if snd_mixer_selem_has_playback_volume == 0:
                print("no volume control")
            else:
                dict_volume = {}
                if snd_mixer_selem_is_playback_mono(elem=mixer_playback) == 1:
                    dict_volume["Mono"] = snd_mixer_selem_get_playback_volume(
                        elem=mixer_playback,
                        channel=SND_MIXER_SELEM_CHANNEL_ID_T.MONO,
                    )
                else:
                    list_channel = list(
                        filter(
                            lambda x: snd_mixer_selem_has_playback_channel(
                                mixer_playback, x
                            )
                            == 1,
                            list(SND_MIXER_SELEM_CHANNEL_ID_T),
                        )
                    )
                    for chan in list_channel:
                        dict_volume[
                            snd_mixer_selem_channel_name(chan).decode()
                        ] = snd_mixer_selem_get_playback_volume(
                            elem=mixer_playback,
                            channel=chan,
                        )
                min, max = snd_mixer_selem_get_playback_volume_range(
                    elem=mixer_playback
                )
                print(
                    f"{mixer_playback_name['CTL'].decode()}, {mixer_playback_name['SELEM_NAME'].decode()} Playback Volume: min={min}, max={max}, value={dict_volume}"
                )

            # playback switch control
            if snd_mixer_selem_has_playback_switch == 0:
                print("no switch control")
            else:
                pass

        snd_mixer_selem_id_free(obj=mixer_selem_id)
        snd_mixer_close(mixer=mixer_handler)


if __name__ == "__main__":
    print(__file__)

    print(f"ALSA sound library version: {bytes(snd_asoundlib_version()).decode()}")

    # "ctl" + "index" で id(hw:CARD=Sなど)リストを取得する

    # test_card_list()
    # test_name_hint()
    # test_control_interface()
    test_simple_mixer_interface()
