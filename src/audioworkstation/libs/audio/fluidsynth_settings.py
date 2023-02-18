#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Create configuration file for fluidsynth.

Create a 'json file' containing the initial settings for fluidsynth.
After editing, the settings can be changed by loading the 'json file'.
"""

import ctypes as C
from typing import Any
from json import dump

import fluidsynth as FS


# test foreach settings
all_settings: dict[str, dict[str, Any]] = dict()
option_list: list = list()


@FS.FLUID_SETTINGS_FOREACH_T
def settings_types(data, name, type):
    all_settings[bytes(name).decode()] = {
        "type": type,
        "options": None,
        "range": None,
        "default": None,
        "value": None,
    }


@FS.FLUID_SETTINGS_FOREACH_OPTION_T
def settings_option(data, name, option):
    global option_list
    option_list += [bytes(option).decode()]


def fetch_default() -> bool:
    global all_settings, option_list
    hints_id = C.c_int()

    settings = FS.new_fluid_settings()
    FS.fluid_settings_foreach(settings=settings, data=None, func=settings_types)

    for name, part in all_settings.items():
        type = part["type"]
        if type == FS.FLUID_TYPE.NUM:
            d_default = C.c_double()
            FS.fluid_settings_getnum_default(
                settings=settings, name=name.encode(), val=C.byref(d_default)
            )
            part["default"] = d_default.value

            FS.fluid_settings_get_hints(
                settings=settings, name=name.encode(), hints=C.byref(hints_id)
            )
            if hints_id.value == FS.FLUID_HINT.RANGE:
                d_min = C.c_double()
                d_max = C.c_double()
                FS.fluid_settings_getnum_range(
                    settings=settings,
                    name=name.encode(),
                    min=C.byref(d_min),
                    max=C.byref(d_max),
                )
                part["range"] = [d_min.value, d_max.value]
        elif type == FS.FLUID_TYPE.INT:
            i_default = C.c_int()
            FS.fluid_settings_getint_default(
                settings=settings, name=name.encode(), val=C.byref(i_default)
            )
            part["default"] = i_default.value

            FS.fluid_settings_get_hints(
                settings=settings, name=name.encode(), hints=C.byref(hints_id)
            )
            if hints_id.value in [FS.FLUID_HINT.RANGE, FS.FLUID_HINT.ON_OFF]:
                i_min = C.c_int()
                i_max = C.c_int()
                FS.fluid_settings_getint_range(
                    settings=settings,
                    name=name.encode(),
                    min=C.byref(i_min),
                    max=C.byref(i_max),
                )
                part["range"] = [i_min.value, i_max.value]
        elif type == FS.FLUID_TYPE.STR:
            c_default = C.c_char_p()
            FS.fluid_settings_getstr_default(
                settings=settings, name=name.encode(), str=C.byref(c_default)
            )
            part["default"] = c_default.value.decode() if c_default.value else None

            FS.fluid_settings_get_hints(
                settings=settings, name=name.encode(), hints=C.byref(hints_id)
            )
            if hints_id.value == FS.FLUID_HINT_OPTIONLIST:
                option_list = list()
                FS.fluid_settings_foreach_option(
                    settings=settings,
                    name=name.encode(),
                    data=None,
                    func=settings_option,
                )
                part["options"] = option_list
        else:
            pass

    with open("config/settings.default.json", "w") as fw:
        dump(all_settings, fw, indent=4)
    return True


if __name__ == "__main__":
    fetch_default()
