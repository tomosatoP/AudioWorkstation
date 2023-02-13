#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

# test amixer
from src.audioworkstation import amixer as Master


class TestMaster(unittest.TestCase):

    def test_start(self):
        self.assertTrue(Master.start())

    def test_volume(self) -> None:
        arg = '50%,50%'
        self.assertEqual(Master.volume(arg), arg)


if __name__ == '__main__':
    unittest.main()
