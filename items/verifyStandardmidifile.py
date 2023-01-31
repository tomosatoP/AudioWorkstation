#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# test class standardmidifile
import standardmidifile as SMF
from pathlib import Path


def verify() -> bool:
    extension = ['.mid', '.MID']
    list_midifile = [i for i in Path().glob(
        'mid/*.*') if i.suffix in extension]
    for i in list_midifile:
        midifile = SMF.StandardMidiFile(i)
        print(f'{i}, {midifile.title()}, {midifile.channels_preset()}')

    return (True)


if __name__ == '__main__':
    print('midi file list')
    verify()
