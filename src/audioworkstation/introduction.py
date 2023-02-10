#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
from kivy.config import Config


def start():
    log_dir = str(Path().absolute()) + '/logs'

    Config.set('kivy', 'log_dir', log_dir)
    Config.set('kivy', 'log_level', 'debug')
    Config.set('graphics', 'fullscreen', 0)

    # Using Official RPi touch display
    Config.set('input', 'mouse', 'mouse')
    # Config.set('input', 'mtdev_%(name)s', 'probesysfs,provider=mtdev')
    Config.set('input', 'hid_%(name)s', 'probesysfs,provider=hidinput')
