#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from standardmidifile import *

# test class standardmidifile
def verify():
    extension = ['.mid','.MID']
    list_midifile = [i for i in Path().glob('mid/*.*') if i.suffix in extension]
    for i in list_midifile:
        midifile = StandardMidiFile(i)
        print(f'{i}, {midifile.title()}, {midifile.channels_preset()}')

if __name__ == '__main__':
    print('midi file list')
    verify()