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
        print(f"FSError: {args}")


def errcheck(result: Any, cfunc: Callable, args: tuple) -> Any:
    if result == -1:
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
snd_asoundlib_version.errcheck = errcheck

snd_card_load = prototype(CAS2.c_int, "snd_card_load", (CAS2.c_int, 1, "card"))
snd_card_load.errcheck = errcheck

snd_card_get_name = prototype(
    CAS2.c_int,
    "snd_card_get_name",
    (CAS2.c_int, 1, "card"),
    (CAS2.POINTER(CAS2.c_char_p), 3, "name"),
)

snd_card_get_longname = prototype(
    CAS2.c_int,
    "snd_card_get_longname",
    (CAS2.c_int, 1, "card"),
    (CAS2.POINTER(CAS2.c_char_p), 3, "name"),
)

snd_card_get_index = prototype(
    CAS2.c_int, "snd_card_get_index", (CAS2.c_char_p, 1, "string")
)

snd_card_next = prototype(
    CAS2.c_int, "snd_card_next", (CAS2.POINTER(CAS2.c_int), 1, "rcard")
)

if __name__ == "__main__":
    print(__file__)

    print(bytes(snd_asoundlib_version()).decode())
    for i in range(5):
        print(f"index - {i}: {int(snd_card_load(CAS2.c_int(i)))}")

    for j in range(5):
        sname: CAS2.c_char_p = CAS2.c_char_p()
        lname: CAS2.c_char_p = CAS2.c_char_p()

        snd_card_get_name(card=CAS2.c_int(j), name=CAS2.byref(sname))
        snd_card_get_longname(card=CAS2.c_int(j), name=CAS2.byref(lname))
        print(f"index - {j}: name - {sname.value.decode()}/{lname.value.decode()}")

    for s in [b"Headphones", b"fmidi", b"S", b"vc4hdmi0", b"vc4hdmi1"]:
        print(f"{s.decode()}: index {int(snd_card_get_index(s))}")
