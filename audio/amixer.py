#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess

# Master Volume (PulseAudio)
'''
amixer sget Master

amixer sset Master 100%,100% -M unmute
amixer sset Master 10%+,10%+ -M unmute
amixer sset Master 10%-,10%- -M unmute
'''
master_volume = ['amixer', 'sset', 'Master', '50%,50%', '-M', 'unmute']

# If using S (USB-Audio - Sharkoon Gmaing DAC Pro S/ latency 4ms)
using_S = [
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
    ['amixer', '-c', 'S', 'sset', 'PCM', '100%', '-M', 'unmute']]

# If using Headphones (bcm2835 Headphones/ latency 21.3ms)
using_Headphones = [
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
    ['amixer', '-c', 'Headphones', 'sset', 'Headphone', '100%', '-M', 'unmute']]

result = filter(lambda i: subprocess.run(i).returncode != 0, using_S)
print('start jack server') if len(list(result)) == 0 \
    else print('Error: Failed to open jack server')

result = subprocess.run(master_volume, capture_output=True, text=True)
a = result.stdout.splitlines()
listc = list()
for b in a:
    listb = list()
    for c in b.strip().split(':'):
        listb += [c.strip()]
    listc.append(listb)

print(listc)
'''
Simple mixer control 'Master',0
 Capabilities: pvolume pswitch pswitch-joined
 playback channels: Front Left - Front Right
 Limits: playback 0 - 65536
 Mono:
 Front Left: Playback 65536 [100%] [on]
 Front Right: Playback 65536 [100%] [on]
'''

