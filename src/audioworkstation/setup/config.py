#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Configure the folder for settings."""


def makedirs() -> None:
    """Create a folder for settings."""

    print("mkdir ...")

    from pathlib import Path

    homedir: str = str(Path.home())

    Path("config").mkdir(exist_ok=True)
    Path("example").mkdir(exist_ok=True)
    Path("logs").mkdir(exist_ok=True)
    Path("mid").mkdir(exist_ok=True)
    Path("sf2").mkdir(exist_ok=True)
    Path("sf3").mkdir(exist_ok=True)
    Path(f"{homedir}/.icons").mkdir(exist_ok=True)

    print("Link 'FluidR3_GM.sf2' ...")

    if not Path("sf2/FluidR3_GM.sf2").is_file():
        Path("sf2/FluidR3_GM.sf2").symlink_to("/usr/share/sounds/sf2/FluidR3_GM.sf2")


def makefiles() -> None:
    """Create various configuration files."""

    from ..setup import fluidsynth_settings as FSSET
    from ..setup import audioworkstation_settings as AKSET
    from ..setup import jack_settings as JASET
    from ..setup import fluidsynth_router_rule as FSRRULE
    from ..setup import compile as COM
    from ..setup import middata as MID

    FSSET.extract_default()
    FSSET.customize()
    AKSET.screens()
    AKSET.gmsounset()
    AKSET.desktop()
    JASET.jacks()
    FSRRULE.router_rule_example()
    COM.purepython()
    MID.midfile()


def main() -> None:
    """Initialize."""

    makedirs()
    makefiles()


if __name__ == "__main__":
    print(__file__)
