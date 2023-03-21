#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path

from audioworkstation.setup import fluidsynth_settings as FSSET
from audioworkstation.setup import audioworkstation_settings as APSET
from audioworkstation.setup import fluidsynth_router_rule as FSRULE


def makedirs():
    Path("config").mkdir(exist_ok=True)
    Path("logs").mkdir(exist_ok=True)
    Path("mid").mkdir(exist_ok=True)
    Path("sf2").mkdir(exist_ok=True)
    Path("sf2/FluidR3_GM.sf2").symlink_to("/usr/share/sounds/sf2/FluidR3_GM.sf2")
    Path("sf3").mkdir(exist_ok=True)


def main():
    makedirs()
    FSSET.extract_default()
    FSSET.customize()
    APSET.player()
    APSET.metronome()
    APSET.keyboard()
    APSET.gmsounset()
    FSRULE.case_study()


if __name__ == "__main__":
    print(__file__)
