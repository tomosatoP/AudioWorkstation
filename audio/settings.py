#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from fluidsynth import *

# test foreach settings
@FLUID_SETTINGS_FOREACH_T
def settings_types(data: c_void_p, name: c_char_p, type: c_int):
    settings_names[name.decode()] = {
        "type": type,
        "options": None,
        "range": None,
        "default": None,
        "value": None}
 
@FLUID_SETTINGS_FOREACH_OPTION_T
def settings_option(data: c_void_p, name: c_char_p, option: c_char_p):
    global option_list
    option_list += [option.decode()]

def verify_settings():
    global settings_names, option_list
    settings_names = dict()
    hints_id = c_int()

    settings = new_fluid_settings()
    fluid_settings_foreach(settings, None, settings_types)
    for name in settings_names:
        if FLUID_TYPE(settings_names[name]['type']) == FLUID_TYPE.NUM:
            buffer = c_double()
            fluid_settings_getnum_default(settings, name.encode(), byref(buffer))
            settings_names[name]['default'] = buffer.value
            fluid_settings_get_hints(settings, name.encode(), byref(hints_id))
            if hints_id.value == 3:
                min = c_double()
                max = c_double()
                fluid_settings_getnum_range(settings, name.encode(), byref(min), byref(max))
                settings_names[name]['range'] = [min.value, max.value]
        elif FLUID_TYPE(settings_names[name]['type']) == FLUID_TYPE.INT:
            buffer = c_int()
            fluid_settings_getint_default(settings, name.encode(), byref(buffer))
            settings_names[name]['default'] = buffer.value
            fluid_settings_get_hints(settings, name.encode(), byref(hints_id))
            if hints_id.value in [3, 7]:
                min = c_int()
                max = c_int()
                fluid_settings_getint_range(settings, name.encode(), byref(min), byref(max))
                settings_names[name]['range'] = [min.value, max.value]
        elif FLUID_TYPE(settings_names[name]['type']) == FLUID_TYPE.STR:
            fluid_settings_get_hints(settings, name.encode(), byref(hints_id))
            buffer = c_char_p()
            fluid_settings_getstr_default(settings, name.encode(), byref(buffer))
            settings_names[name]['default'] = buffer.value.decode()
            if hints_id.value == 2:
                option_list = list()
                fluid_settings_foreach_option(settings, name.encode(), None, settings_option)
                settings_names[name]["options"] = option_list
        else:
            pass
    
    with open('settings.default.json', 'w') as fw:
        dump(settings_names, fw, indent=4)
    return(True)


if __name__ == '__main__':
    verify_settings()
