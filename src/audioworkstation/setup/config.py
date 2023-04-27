#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Configure the folder for settings."""


def makedirs() -> None:
    """Create a folder for settings."""

    from pathlib import Path

    Path("config").mkdir(exist_ok=True)
    Path("logs").mkdir(exist_ok=True)
    Path("mid").mkdir(exist_ok=True)
    Path("sf2").mkdir(exist_ok=True)
    Path("sf2/FluidR3_GM.sf2").symlink_to("/usr/share/sounds/sf2/FluidR3_GM.sf2")
    Path("sf3").mkdir(exist_ok=True)


def makefiles() -> None:
    """Create various configuration files."""

    from audioworkstation.setup import fluidsynth_settings as FSSET
    from audioworkstation.setup import audioworkstation_settings as AKSET
    from audioworkstation.setup import jack_settings as JASET
    from audioworkstation.setup import fluidsynth_router_rule as FSRRULE

    FSSET.extract_default()
    FSSET.customize()
    AKSET.screens()
    AKSET.gmsounset()
    AKSET.desktop()
    AKSET.cbuild()
    JASET.jacks()
    FSRRULE.router_rule_example()


def main() -> None:
    """Initialize."""

    makedirs()
    makefiles()


if __name__ == "__main__":
    print(__file__)
