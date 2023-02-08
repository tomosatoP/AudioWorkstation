#!/usr/bin/env python3
# -*- coding: utf-8 -*-


if __name__ == '__main__':
    from . import introduction as Intro
    # from . metronome import Metronome
    from . player import Player

    Intro.start()
    # Metronome().run()
    Player().run()
