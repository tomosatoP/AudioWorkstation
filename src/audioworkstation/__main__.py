#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
from kivy.config import Config

# Kivy
log_dir = str(Path().absolute()) + "/logs"


Config.set("kivy", "log_dir", log_dir)
Config.set("kivy", "log_level", "debug")

Config.set("graphics", "borderless", 1)  # 0, 1
Config.set("graphics", "fullscreen", 0)  # 0, 1, "auto", "fake"
Config.set("graphics", "width", 800)  # not used if fullscreen is set to "auto".
Config.set("graphics", "height", 480)  # not used if fullscreen is set to "auto".

# Kivy: Using Official RPi touch display
Config.set("input", "mouse", "mouse")
Config.set("input", "%(name)s", "")
# Config.set("input", "mtdev_%(name)s", "probesysfs,provider=mtdev")
Config.set("input", "hid_%(name)s", "probesysfs,provider=hidinput")


if __name__ == "__main__":
    # To use japanese font in Kivy
    from kivy.core.text import LabelBase, DEFAULT_FONT
    from kivy.resources import resource_add_path

    from .libs.audio import asound as AS

    # To use japanese font in Kivy
    resource_add_path("/usr/share/fonts/opentype/ipaexfont-gothic")
    LabelBase.register(DEFAULT_FONT, "ipaexg.ttf")

    # Jackd2 and amixer
    AS.set_volume("default", "Master", 100)
    devicename, devicecontrolname = AS.start_jackserver()
    AS.set_volume(devicename, devicecontrolname, 50)

    from .menubar import MenubarApp

    MenubarApp().run()
