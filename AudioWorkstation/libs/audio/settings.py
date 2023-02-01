#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import fluidsynth as FS
import ctypes as C
from typing import Any
from json import dump

'''Create a 'json file' containing the initial settings for fluidsynth.
After editing, the settings can be changed by loading the 'json file'.
'''

# test foreach settings
parts_settings: dict[str, dict[str, Any]] = dict()


@FS.FLUID_SETTINGS_FOREACH_T
def settings_types(data, name, type):
    parts_settings[bytes(name).decode()] = {
        "type": type,
        "options": None,
        "range": None,
        "default": None,
        "value": None}


@FS.FLUID_SETTINGS_FOREACH_OPTION_T
def settings_option(data, name, option):
    global option_list
    option_list += [bytes(option).decode()]


def verify_settings() -> bool:
    global parts_settings, option_list
    hints_id = C.c_int()

    settings = FS.new_fluid_settings()
    FS.fluid_settings_foreach(settings=settings,
                              data=None,
                              func=settings_types)

    for name, part in parts_settings.items():
        type = part['type']
        if type == FS.FLUID_TYPE.NUM:
            buffer = C.c_double()
            FS.fluid_settings_getnum_default(
                settings=settings,
                name=name.encode(),
                val=C.byref(buffer))
            part['default'] = buffer.value

            FS.fluid_settings_get_hints(
                settings=settings,
                name=name.encode(),
                hints=C.byref(hints_id))
            if hints_id.value == FS.FLUID_HINT.RANGE:
                min = C.c_double()
                max = C.c_double()
                FS.fluid_settings_getnum_range(
                    settings=settings,
                    name=name.encode(),
                    min=C.byref(min),
                    max=C.byref(max))
                part['range'] = [min.value, max.value]
        elif type == FS.FLUID_TYPE.INT:
            buffer = C.c_int()
            FS.fluid_settings_getint_default(
                settings=settings,
                name=name.encode(),
                val=C.byref(buffer))
            part['default'] = buffer.value

            FS.fluid_settings_get_hints(
                settings=settings,
                name=name.encode(),
                hints=C.byref(hints_id))
            if hints_id.value in [FS.FLUID_HINT.RANGE, FS.FLUID_HINT.ON_OFF]:
                min = C.c_int()
                max = C.c_int()
                FS.fluid_settings_getint_range(
                    settings=settings,
                    name=name.encode(),
                    min=C.byref(min),
                    max=C.byref(max))
                part['range'] = [min.value, max.value]
        elif type == FS.FLUID_TYPE.STR:
            buffer = C.c_char_p()
            FS.fluid_settings_getstr_default(
                settings=settings,
                name=name.encode(),
                str=C.byref(buffer))
            part['default'] = buffer.value.decode() if buffer.value else None

            FS.fluid_settings_get_hints(
                settings=settings,
                name=name.encode(),
                hints=C.byref(hints_id))
            if hints_id.value == FS.FLUID_HINT_OPTIONLIST:
                option_list = list()
                FS.fluid_settings_foreach_option(
                    settings=settings,
                    name=name.encode(),
                    data=None,
                    func=settings_option)
                part["options"] = option_list
        else:
            pass

    with open('audio/settings.default.json', 'w') as fw:
        dump(parts_settings, fw, indent=4)
    return (True)


if __name__ == '__main__':
    verify_settings()
