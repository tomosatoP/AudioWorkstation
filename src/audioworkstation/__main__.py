#!/usr/bin/env python3
# -*- coding: utf-8 -*-


if __name__ == "__main__":

    from pathlib import Path
    from kivy.config import Config

    # Kivy
    log_dir = str(Path().absolute()) + "/logs"

    Config.set("kivy", "log_dir", log_dir)
    Config.set("kivy", "log_level", "debug")
    Config.set("graphics", "fullscreen", 0)

    # Kivy: Using Official RPi touch display
    Config.set("input", "mouse", "mouse")
    # Config.set('input', 'mtdev_%(name)s', 'probesysfs,provider=mtdev')
    Config.set("input", "hid_%(name)s", "probesysfs,provider=hidinput")

    from .libs.audio import amixer

    # Jackd2 and amixer
    amixer.start()
    amixer.volume("50%,50%")

    # from . metronome import Metronome
    from .player import Player

    # Metronome().run()
    Player().run()
