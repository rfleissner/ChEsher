#!/usr/bin/python -d
#
# Copyright (C) 2016  Reinhard Fleissner
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

"""Wrapper for module Tube"""

__author__="Reinhard Fleissner"
__date__ ="$18.05.2016 22:38:30$"

import functools
import numpy as np

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QMessageBox

# modules and classes
from uiTube import Ui_Tube
import uiHandler as uih
import fileHandler as fh
import copy

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class WrapTube():
    """Wrapper for module Tube"""

    def __init__(self, dir):
        """Constructor."""

        self.directory = dir
        
        # setup user interface
        self.widget = QtGui.QWidget()
        self.ui = Ui_Tube()
        self.ui.setupUi(self.widget)
        
# module Tube

        self.callbackTubeOpenMeshFile = functools.partial(uih.getOpenFileName, "Open T3S-file", "2D T3 Scalar Mesh (ASCII SingleFrame) (*.t3s)", self.ui.lineEditInputMesh, self.directory, self.widget)
        QtCore.QObject.connect(self.ui.pushButtonInputMesh, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackTubeOpenMeshFile)
        
        self.callbackTubeOpenLineSet = functools.partial(uih.getOpenFileName, "Open I2S-file", "Line Sets (*.i2s)", self.ui.lineEditInputLineSet, self.directory, self.widget)
        QtCore.QObject.connect(self.ui.pushButtonInputLineSet, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackTubeOpenLineSet)
        
        self.callbackTubeOutput = functools.partial(uih.getSaveFileName, "Save textfile As", "Normal text file (*.txt)", self.ui.lineEditOutput, self.directory, self.widget)
        QtCore.QObject.connect(self.ui.pushButtonOutput, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackTubeOutput)
        
        QtCore.QObject.connect(self.ui.pushButtonCreate, QtCore.SIGNAL("clicked()"), self.create)

    def setDir(self, dir):
        self.directory = dir
        self.p = copy.copy(dir)
        print "set", self.directory
        
    def initialize(self):
        
        import os
        abs_path = os.path.abspath('.')
        dir = os.path.join(abs_path, 'examples/').replace('\\', '/')
  
        ###   ~   module Tube   ~   ###
        
        self.ui.lineEditInputMesh.setText(dir + "example_10/mesh.t3s")
        self.ui.lineEditInputLineSet.setText(dir + "example_10/tubes.i2s")
        self.ui.lineEditOutput.setText(dir + "example_10/tubes.txt")
        
    def create(self):
        
        print "ffff", self.directory
        
        info = ""
        info += "Input data:\n"
        
        textfile = []
        
        # read input meshes
        try:
            x, y, z, triangles = fh.readT3STriangulation(self.ui.lineEditInputMesh.text())
            info += " - Mesh loaded with {0} nodes and {1} elements.\n".format(len(x), len(triangles))
        except:
            QMessageBox.critical(self, "Error", "Not able to load mesh file!\nCheck filename or content!")
            return        

        try:
            tube_coords, tubes = fh.readI2S(self.ui.lineEditInputLineSet.text())
            info += " - Line Set loaded with {0} lines.\n".format(len(tubes))
        except:
            QMessageBox.critical(self.widget, "Error", "Not able to load *.i2s file!\nCheck filename or content!")
            return

        # reshape coordinates
        a = np.array([x, y])
        b = np.reshape(a, (2*len(x)), order='F')
        mesh_coords = np.reshape(b, (len(x), 2))
        
        Rel = str(self.ui.doubleSpinBoxRel.value())
        Ce1 = str(self.ui.doubleSpinBoxCe1.value())
        Ce2 = str(self.ui.doubleSpinBoxCe2.value())
        Cs1 = str(self.ui.doubleSpinBoxCs1.value())
        Cs2 = str(self.ui.doubleSpinBoxCs2.value())
        Lrg = str(self.ui.doubleSpinBoxLrg.value())
        Hau = str(self.ui.doubleSpinBoxHau.value())
        Clp = str(self.ui.spinBoxClp.value())
        L12 = str(self.ui.doubleSpinBoxL12.value())
        
        textfile.append("Relaxation")
        textfile.append(Rel)
        textfile.append("I1\tI2\tCe1\tCe2\tCs1\tCs2\tLrg\tHau\tClp\tL12\tz1\tz2")
        
        for tID in tubes:
            line = ""
            tube = tubes[tID]
            
            nodes = ""
            z_val = ""
            
            for i in range(2):
                p = tube_coords[tube[i]]
                vert = np.array(p)
                vert = vert.reshape((1,2))
                temp = mesh_coords-p
                norm = np.linalg.norm(temp, axis = 1)
                I = np.argmin(norm)+1
                nodes += str(I)
                nodes += "\t"
                z_val += str(z[I-1])
                z_val += "\t"

            line += nodes
            line += str(Ce1) + "\t"
            line += str(Ce2) + "\t"
            line += str(Cs1) + "\t"
            line += str(Cs2) + "\t"
            line += str(Lrg) + "\t"
            line += str(Hau) + "\t"
            line += str(Clp) + "\t"
            line += str(L12) + "\t"
            line += z_val

            textfile.append(line)

        info += "\nOutput data:\n"
                    
        try:
            fh.writeTextFile(self.ui.lineEditOutput.text(), textfile)
            info += " - Tubes data file written to {0}.\n".format(self.ui.lineEditOutput.text())
        except:
            QMessageBox.critical(self.widget, "Error", "Not able to write tubes data file!")
            return
    
        QMessageBox.information(self.widget, "Module Tube", info)  