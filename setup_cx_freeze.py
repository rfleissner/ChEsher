#!/usr/bin/python -d
#
# Copyright (C) 2015  Reinhard Fleissner
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.

import sys
from cx_Freeze import setup, Executable

# Use of the file to create a msi-installer:
# python setup_cx_freeze.py bdist_msi


# Dependencies are automatically detected, but it might need fine tuning.
includefiles = ['geos_c.dll']
build_exe_options = {"compressed":True, "packages": ["os"], "include_files":includefiles, "excludes": ["tkinter", "tk", "tcl"], "includes": ["shapely","shapely.geos","shapely.geometry","shapely.coords", "scipy.special._ufuncs_cxx", "scipy", "scipy.integrate" ,"scipy.sparse", "scipy.sparse.csgraph._validation", "scipy.integrate.vode", "scipy.integrate.lsoda"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":

	setup(  name = "ChEsher",
        version = "1.0",
        author = "Fleissner Reinhard",
        options = {"build_exe": build_exe_options},
        executables = [Executable("ChEsher.py", icon="icon_256x256.ico", base="Win32GUI")])

if sys.platform == "win64":

	setup(  name = "ChEsher",
        version = "1.0",
        author = "Fleissner Reinhard",
        options = {"build_exe": build_exe_options},
        executables = [Executable("ChEsher.py", icon="icon_256x256.ico", base="Win64GUI")])
