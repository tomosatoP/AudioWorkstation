#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Application Entry

#. Kivy logging starts.
#. Configure hardware settings for Kivy.
#. Start JACK server.
#. Start Application.
"""

from pathlib import Path
from kivy.config import Config

# from . import splashscreen

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

    resource_add_path("/usr/share/fonts/opentype/ipaexfont-gothic")
    LabelBase.register(DEFAULT_FONT, "ipaexg.ttf")

    # Jackd2 and amixer
    from kivy.logger import Logger
    from .libs.audio import asound

    Logger.debug("JACK server: initializing...")
    asound.set_volume("default", "Master", 100)
    mixer: list[str] = asound.start_jackserver()
    asound.set_volume(mixer[2], mixer[3], 50)

    from .menubar import MenubarApp

    MenubarApp().run()
