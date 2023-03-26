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
:param c_int val: CTL element related interface [enum SND_CTL_ELEM_IFACE_T]
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

""" list funcs
int lookup_id(snd_ctl_elem_id_t *id, snd_ctl_t *handle){
    snd_ctl_elem_info_t *info;
    snd_ctl_elem_info_alloca(&info);    マクロ

    snd_ctl_elem_info_set_id(info, id); idをinfoに設定
    snd_ctl_elem_info(handle, info);    handleを持つサウンドカード上の要素を検索
    snd_ctl_elem_info_get_id(info, id); idを完全に埋められたidで更新。
    return 0;
}

int main(){
    snd_ctl_t *handle;
    snd_ctl_elem_id_t *id;
    snd_ctl_elem_value_t *value;

    snd_ctl_elem_id_alloca(&id);
    snd_ctl_elem_value_alloca(&value);

    snd_ctl_open(&handle, "hw:0", 0);

    snd_ctl_elem_id_set_interface(id, SND_CTL_ELEM_IFACE_MIXER);
    snd_ctl_elem_id_set_name(id, "Headphone Playback Volume");

    lookup_id(id, handle);

    snd_ctl_elem_value_set_id(value, id);
    snd_ctl_elem_value_set_integer(value, 0, 55);
    snd_ctl_elem_value_set_integer(value, 1, 77);

    snd_ctl_elem_write(handle, value);

さて、これでコントロールの値が変更されました。
  snd_ctl_elem_value_set_id()      変更するコントロールのidを設定
  snd_ctl_elem_value_set_integer() 実際の値を設定
このコントロールには複数のメンバー(この場合、左右のチャンネル)があるため、
複数の呼び出しがあります。
  snd_ctl_elem_write()             値をコミット

なお、snd_ctl_elem_value_set_integer()が直接呼ばれるのは、
このコントロールが整数であることがわかっているからですが、実際には、
  snd_ctl_elem_type_t snd_ctl_elem_info_get_type(const snd_ctl_elem_info_t* obj)
でどの種類の値が使われるべきかを照会することができます。
整数のスケールもデバイス固有で、
  long snd_ctl_elem_info_get_min(const snd_ctl_elem_info_t* obj)
  long snd_ctl_elem_info_get_max(const snd_ctl_elem_info_t* obj)
  long snd_ctl_elem_info_get_step(const snd_ctl_elem_info_t* obj)
ヘルパーで取得することができる。

    snd_ctl_elem_id_clear(id);
    snd_ctl_elem_id_set_interface(id, SND_CTL_ELEM_IFACE_MIXER);
    snd_ctl_elem_id_set_name(id, "Headphone Playback Switch");
    lookup_id(id, handle);

    snd_ctl_elem_value_clear(value);
    snd_ctl_elem_value_set_id(value, id);
    snd_ctl_elem_value_set_boolean(value, 1, 1);

    snd_ctl_elem_write(handle, value);

これはHeadphone再生の右チャンネルのミュートを解除するもので、今回はブール値です。
もう1つの一般的なエレメントの種類は、列挙型コンテンツ用の
  SND_CTL_ELEM_TYPE_ENUMERATED
enum snd_ctl_elem_type_t{
  SND_CTL_ELEM_TYPE_NONE = 0,
  SND_CTL_ELEM_TYPE_BOOLEAN,
  SND_CTL_ELEM_TYPE_INTEGER,
  SND_CTL_ELEM_TYPE_ENUMERATED,
  SND_CTL_ELEM_TYPE_BYTES,
  SND_CTL_ELEM_TYPE_IEC958,
  SND_CTL_ELEM_TYPE_INTEGER64,
  SND_CTL_ELEM_TYPE_LAST = SND_CTL_ELEM_TYPE_INTEGER64
}
です。
これは、例えばチャンネル多重化や復元値の選択などに使用されます。
選択された項目を設定するには、
    void snd_ctl_elem_value_set_enumerated(
        snd_ctl_elem_value_t* obj,
        unsigned int idx,
        unsigned int val
    )
を使用する必要があります。

  return 0;
}
"""


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
    ncard: int = 4  # if all is -1, otherwise 0 to 3
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

    # "ctl" + "index" で id(hw:CARD=Sなど)リストを取得する

    # 再生音量の取得と設定
    # default(or pulse), Master Playback Volume
    # hw:CARD=Headphones, PCM Playback Volume
    # hw:CARD=S, PCM Playback Volume
    ctl_handler = snd_ctl_open(name=b"hw:CARD=Headphones", mode=0)
    ctl_elem_id = snd_ctl_elem_id_malloc()
    ctl_elem_value = snd_ctl_elem_value_malloc()

    snd_ctl_elem_id_set_interface(ctl_elem_id, CAS2.c_int(SND_CTL_ELEM_IFACE_T.MIXER))
    snd_ctl_elem_id_set_name(ctl_elem_id, b"PCM Playback Volume")

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
    print("Headphones, PCM Playback Volume")

    snd_ctl_elem_value_free(ctl_elem_value)
    snd_ctl_elem_id_free(ctl_elem_id)
    snd_ctl_close(ctl_handler)
