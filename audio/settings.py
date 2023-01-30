#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import fluidsynth as FS
import ctypes as C
from json import dump

'''Create a 'json file' containing the initial settings for fluidsynth.
After editing, the settings can be changed by loading the 'json file'.
'''

# test foreach settings


@FS.FLUID_SETTINGS_FOREACH_T
def settings_types(data, name, type):
    settings_names[bytes(name).decode()] = {
        "type": type,
        "options": None,
        "range": None,
        "default": None,
        "value": None}


@FS.FLUID_SETTINGS_FOREACH_OPTION_T
def settings_option(data, name, option):
    global option_list
    option_list += [bytes(option).decode()]


def verify_settings():
    global settings_names, option_list
    settings_names = dict()
    hints_id = C.c_int()

    settings = FS.new_fluid_settings()
    FS.fluid_settings_foreach(settings, None, settings_types)

    for name in settings_names:
        if FS.FLUID_TYPE(settings_names[name]['type']) == FS.FLUID_TYPE.NUM:
            buffer = C.c_double()
            FS.fluid_settings_getnum_default(
                settings, name.encode(), C.byref(buffer))
            settings_names[name]['default'] = buffer.value
            FS.fluid_settings_get_hints(
                settings, name.encode(), C.byref(hints_id))
            if hints_id.value == FS.FLUID_HINT.RANGE:
                min = C.c_double()
                max = C.c_double()
                FS.fluid_settings_getnum_range(
                    settings, name.encode(), C.byref(min), C.byref(max))
                settings_names[name]['range'] = [min.value, max.value]
        elif FS.FLUID_TYPE(settings_names[name]['type']) == FS.FLUID_TYPE.INT:
            buffer = C.c_int()
            FS.fluid_settings_getint_default(
                settings, name.encode(), C.byref(buffer))
            settings_names[name]['default'] = buffer.value
            FS.fluid_settings_get_hints(
                settings, name.encode(), C.byref(hints_id))
            if hints_id.value in [FS.FLUID_HINT.RANGE, FS.FLUID_HINT.ON_OFF]:
                min = C.c_int()
                max = C.c_int()
                FS.fluid_settings_getint_range(
                    settings, name.encode(), C.byref(min), C.byref(max))
                settings_names[name]['range'] = [min.value, max.value]
        elif FS.FLUID_TYPE(settings_names[name]['type']) == FS.FLUID_TYPE.STR:
            FS.fluid_settings_get_hints(
                settings, name.encode(), C.byref(hints_id))
            buffer = C.c_char_p()
            FS.fluid_settings_getstr_default(
                settings, name.encode(), C.byref(buffer))
            settings_names[name]['default'] \
                = buffer.value.decode() if buffer.value else None
            if hints_id.value == 0x02:
                option_list = list()
                FS.fluid_settings_foreach_option(
                    settings, name.encode(), None, settings_option)
                settings_names[name]["options"] = option_list
        else:
            pass

    with open('audio/settings.default.json', 'w') as fw:
        dump(settings_names, fw, indent=4)
    return (True)


if __name__ == '__main__':
    verify_settings()
