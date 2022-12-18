#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess

result = subprocess.run(['amixer', 'sset', 'Master', '100%,100%', '-M', 'unmute'])
result = subprocess.run(['amixer', 'sset', 'Master', '10%-,10%-', '-M', 'unmute'])
result = subprocess.run(['amixer', 'sset', 'Master', '10%+,10%+', '-M', 'unmute'])
result = subprocess.run(['amixer', '-c', 'S', 'sset', 'PCM', '100%', '-M', 'unmute'])
print(result.returncode)