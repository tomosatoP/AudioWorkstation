#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Connect to jack server and set MASTER volume"""

import subprocess
from typing import Optional

# Master Volume (PulseAudio)
_amixer_master = ['amixer', 'sset', 'Master', '50%,50%', '-M', 'unmute']

# If using S (USB-Audio - Sharkoon Gmaing DAC Pro S/ latency 4ms)
_using_S = [
    ['jack_control', 'stop'],
    ['jack_control', 'exit'],
    ['jack_control', 'ds', 'alsa'],
    ['jack_control', 'eps', 'realtime', 'True'],
    ['jack_control', 'dps', 'duplex', 'True'],
    ['jack_control', 'dps', 'device', 'hw:S'],
    ['jack_control', 'dps', 'playback', 'hw:S'],
    ['jack_control', 'dps', 'rate', '96000'],
    ['jack_control', 'dps', 'nperiods', '3'],
    ['jack_control', 'dps', 'period', '128'],
    ['jack_control', 'dps', 'outchannels', '2'],
    ['jack_control', 'start'],
    ['amixer', '-c', 'S', 'sset', 'PCM', '100%', '-M', 'unmute']
]

# If using Headphones (bcm2835 Headphones/ latency 21.3ms)
_using_Headphones = [
    ['jack_control', 'stop'],
    ['jack_control', 'exit'],
    ['jack_control', 'ds', 'alsa'],
    ['jack_control', 'eps', 'realtime', 'True'],
    ['jack_control', 'dps', 'duplex', 'True'],
    ['jack_control', 'dps', 'device', 'hw:Headphones'],
    ['jack_control', 'dps', 'playback', 'hw:Headphones'],
    ['jack_control', 'dps', 'rate', '96000'],
    ['jack_control', 'dps', 'nperiods', '2'],
    ['jack_control', 'dps', 'period', '1024'],
    ['jack_control', 'dps', 'outchannels', '2'],
    ['jack_control', 'start'],
    ['amixer', '-c', 'Headphones', 'sset', 'Headphone', '100%', '-M', 'unmute']
]


def volume(percentage: Optional[str] = None) -> str:
    '''Usage
    - volume()
    - volume('100%,100%')
    - volume('10%+,10%+')
    - volume('10%-,10%-')
    '''

    if percentage is None:
        ''' jackd server and playback volume settings '''
        result = filter(lambda i: subprocess.run(i).returncode != 0, _using_S)
        print('start jack server') if len(list(result)) == 0 \
            else print('Error: Failed to open jack server')
    else:
        ''' master playback volume settings '''
        _amixer_master[3] = percentage

    result = subprocess.run(_amixer_master, capture_output=True, text=True)
    dict_master = dict()
    for line_buffer in result.stdout.splitlines():
        listb = line_buffer.strip().split(':')
        if len(listb) > 1:
            dict_master[listb[0]] = listb[1].strip()

    l_vol = dict_master['Front Left'].split()[2].strip('[]')
    r_vol = dict_master['Front Right'].split()[2].strip('[]')

    return (f'{l_vol},{r_vol}')


if __name__ == '__main__':
    print('amixer')
