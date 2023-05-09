#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""unittest libs/audio/asound.py and libs/audio/btaudiosink.py"""

import unittest

from audioworkstation.libs.audio import asound as Master


class TestMaster(unittest.TestCase):
    def test_start(self):
        self.assertTrue(Master.start_jackserver())

    def test_volume(self) -> None:
        Master.set_volume("default", "Master", 50)
        self.assertEqual(Master.get_volume("default", "Master"), 50)


if __name__ == "__main__":
    unittest.main()
