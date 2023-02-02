#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''Add project folders to the search path.'''

import os
import sys

sys.path.insert(0, os.path.abspath('.'))


def check():
    '''To avoid Flake8(F401).'''
    pass


if __name__ == '__main__':
    print(__file__)
