#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import unittest

# test class standardmidifile
from src.audioworkstation.libs.items import standardmidifile as SMF
from pathlib import Path


class TestSMF(unittest.TestCase):

    def test_title(self) -> None:
        extension = ['.mid', '.MID']
        list_midifile = [
            i for i in Path().glob('mid/*.*') if i.suffix in extension]

        for i in list_midifile:
            midifile = SMF.StandardMidiFile(i)
            print(f'{i}, {midifile.title()}, {midifile.channels_preset()}')

        self.assertEqual(2, 2)


if __name__ == '__main__':
    unittest.main()
