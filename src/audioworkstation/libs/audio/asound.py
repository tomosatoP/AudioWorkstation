#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Purpose: Detect and configure sound card, adjust volume.

https://www.alsa-project.org/alsa-doc/alsa-lib/index.html
https://github.com/alsa-project/alsa-python/blob/master/pyalsa/alsacard.c
"""

from typing import Callable, Any
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


snd_asoundlib_version = prototype(CAS2.c_char_p, "snd_asoundlib_version")

# iface: b"ctl", b"pcm", b"rawmidi", b"timer", b"seq"
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

# id: b"NAME", b"DESC", b"IOID"
snd_device_name_get_hint = prototype(
    CAS2.c_char_p,
    "snd_device_name_get_hint",
    (CAS2.c_void_p, 1, "hint"),
    (CAS2.c_char_p, 1, "id"),
)

snd_card_load = prototype(CAS2.c_int, "snd_card_load", (CAS2.c_int, 1, "card"))

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

snd_card_get_index = prototype(
    CAS2.c_int, "snd_card_get_index", (CAS2.c_char_p, 1, "string")
)

snd_card_next = prototype(
    CAS2.c_int, "snd_card_next", (CAS2.POINTER(CAS2.c_int), 1, "rcard")
)


class SND_CTL_T(CAS2.Structure):
    _fields_ = [("a", CAS2.c_int)]


# mode: default is blocking mode 0x0000
#   SND_CTL_NOBLOCK  0x0001: Non blocking mode  (flag for open mode)
#   SND_CTL_ASYNC    0x0002: Async notification (flag for open mode)
#   SND_CTL_READONLY 0x0004: Read only          (flag for open mode)
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
    return args[0]


snd_ctl_open.errcheck = errcheck_snd_ctl_open

if __name__ == "__main__":
    print(__file__)

    print(f"ALSA sound library version: {bytes(snd_asoundlib_version()).decode()}")

    cards_index = list()
    card_index = CAS2.c_int(0)

    while card_index.value != -1:
        cards_index.append(card_index.value)
        snd_card_next(CAS2.byref(card_index))

    for ci in cards_index:
        if int(snd_card_load(CAS2.c_int(ci))) == 1:
            d_present = "present"
        else:
            d_present = "not present"

        sname = snd_card_get_name(card=CAS2.c_int(ci)).value
        lname = snd_card_get_longname(card=CAS2.c_int(ci)).value
        print(
            f"index {ci}: driver is {d_present}: name {sname.decode()}/{lname.decode()}"
        )

    print("|iface|NAME|DECS|IOID|")
    print("|---|---|---|---|")
    ifaces: list[str] = ["ctl", "pcm", "rawmidi", "timer", "seq"]
    for iface in ifaces:
        hints = snd_device_name_hint(card=CAS2.c_int(1), iface=iface.encode())
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

    ctlp = snd_ctl_open(name=b"hw:CARD=S", mode=0)
    print(ctlp)
