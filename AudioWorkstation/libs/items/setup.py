#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
To speed up smf(standard midi file) analysis, cython was used.
 ~ $ python3 setup.py build_ext --inplace
'''

from distutils.core import setup, Extension
from Cython.Build import cythonize

ext = Extension("standardmidifile",
                sources=["standardmidifile.py"])
setup(name="standardmidifile",
      ext_modules=cythonize([ext]))
