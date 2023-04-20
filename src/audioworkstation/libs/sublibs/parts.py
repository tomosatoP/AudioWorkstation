#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Miscellaneous Functions."""

from math import pow, log10

# [-4, 100/(4+1)], [-3, 100/(3+1)], [-2, 100/(2+1)]
_min_gain: float = 10**-2
_ratio: float = 100.0 / 3.0


def gain2dB(value: float) -> int:
    """Convert gain to dB-like value.

    :param float value: gain
    :return: dB-like value
    """
    if value < _min_gain:
        value = _min_gain
    return int(_ratio * log10(value / _min_gain))


def dB2gain(value: int) -> float:
    """Convert dB-like value to gain.

    :param int value: dB-like value
    :return: gain
    """
    return _min_gain * pow(10.0, float(value) / _ratio)


if __name__ == "__main__":
    print(__file__)
