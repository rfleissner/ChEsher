import sys
from cx_Freeze import setup, Executable

# Use of the file to create a msi-installer:
# python setup_cx_freeze.py bdist_msi

# Dependencies are automatically detected, but it might need fine tuning.
includefiles = ['geos_c.dll', 'examples/', 'documentation/', 'AC1018.dxf',
                'examples/example_01/output/',
                'examples/example_02/output/',
                'examples/example_03/output/',
                'examples/example_04/output/',
                'examples/example_05/output/',
                'examples/example_06/output/',
                'examples/example_07/output/',
                'examples/example_08/output/',
                'examples/example_09/output/',
                'examples/example_10/output/']

build_exe_options = {"compressed":True, "packages": ["os"], "include_files":includefiles, 

    "excludes": [   "collections.sys",
                    "collections._weakref",
                    "tkinter", 
                    "tk", 
                    "tcl"
                ], 
                
    "includes": [   "shapely",
                    "shapely.geos",
                    "shapely.geometry",
                    "shapely.coords", 
                    "scipy.special._ufuncs_cxx", 
                    "scipy", 
                    "scipy.integrate" ,
                    "scipy.sparse", 
                    "scipy.sparse.csgraph._validation", 
                    "scipy.integrate.vode", 
                    "scipy.integrate.lsoda",
                    "dxfwrite"
                ]}

# GUI applications require a different base on Windows (the default is for a
# console application).

base = None

if sys.platform == "win32":
    setup(  name = "ChEsher",
        version = "1.1",
        author = "Fleissner Reinhard",
        options = {"build_exe": build_exe_options},
        executables = [Executable("ChEsher.py", icon="resource/icon.ico", base="Win32GUI")])

if sys.platform == "win64":
 	setup(  name = "ChEsher",
        version = "1.1",
        author = "Fleissner Reinhard",
        options = {"build_exe": build_exe_options},
        executables = [Executable("ChEsher.py", icon="resource/icon.ico", base="Win64GUI")])
