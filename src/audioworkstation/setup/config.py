#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Configure the folder for settings."""

from pathlib import Path

from audioworkstation.setup import fluidsynth_settings as FSSET
from audioworkstation.setup import audioworkstation_settings as AKSET
from audioworkstation.setup import jack_settings as JASET
from audioworkstation.setup import fluidsynth_router_rule as FSRRULE


def makedirs() -> None:
    """Create a folder for settings."""

    Path("config").mkdir(exist_ok=True)
    Path("logs").mkdir(exist_ok=True)
    Path("mid").mkdir(exist_ok=True)
    Path("sf2").mkdir(exist_ok=True)
    Path("sf2/FluidR3_GM.sf2").symlink_to("/usr/share/sounds/sf2/FluidR3_GM.sf2")
    Path("sf3").mkdir(exist_ok=True)


def main() -> None:
    """Create various configuration files."""

    makedirs()
    FSSET.extract_default()
    FSSET.customize()
    AKSET.screens()
    AKSET.gmsounset()
    AKSET.desktop()
    JASET.jacks()
    FSRRULE.router_rule_example()


if __name__ == "__main__":
    print(__file__)
