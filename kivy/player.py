#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('../AudioWorkstation')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.properties import (BoundedNumericProperty, ObjectProperty)

# To use japanese font in Kivy
from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.resources import resource_add_path
resource_add_path('/usr/share/fonts/opentype/ipaexfont-gothic')
LabelBase.register(DEFAULT_FONT, 'ipaexg.ttf')

class PlayerView(Widget):
    pass

class Player(App):
    def build(self):
        return(PlayerView())

if __name__ == '__main__':
    Player().run()