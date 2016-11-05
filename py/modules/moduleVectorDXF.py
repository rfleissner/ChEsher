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

"""Wrapper for module VectorDXF"""

__author__="Reinhard Fleissner"
__date__ ="$18.05.2016 22:38:30$"

import functools
from math import ceil, floor
import numpy as np

import matplotlib
matplotlib.use("Agg")
import matplotlib.tri as tri

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QMessageBox

# modules and classes
from uiVectorDXF import Ui_VectorDXF
import uiHandler as uih
import fileHandler as fh

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class WrapVectorDXF():
    """Wrapper for module VectorDXF"""

    def __init__(self, dir):
        """Constructor."""

        self.directory = dir

        # setup user interface
        self.widget = QtGui.QWidget()
        self.ui = Ui_VectorDXF()
        self.ui.setupUi(self.widget)
        
# module VectorDXF

        self.callbackOpenVectorInput = functools.partial(uih.getOpenFileName, "Open 2D T3 Vector Mesh", "2D T3 Vector Mesh (ASCIISingleFrame) (*.t3v)", self.ui.lineEditInput, self.directory, self.widget)
        QtCore.QObject.connect(self.ui.pushButtonInput, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackOpenVectorInput)
        
        self.callbackScalarVector = functools.partial(uih.getSaveFileName, "Save DXF-file As", "Drawing Interchange File (*.dxf)", self.ui.lineEditOutput, self.directory, self.widget)
        QtCore.QObject.connect(self.ui.pushButtonOutput, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackScalarVector)    
        
        QtCore.QObject.connect(self.ui.pushButtonCreate, QtCore.SIGNAL("clicked()"), self.create)

    def setDir(self, directory):
        self.directory = directory
        print "set", self.directory
    
    def initialize(self):
        
        import os
        abs_path = os.path.abspath('.')
        dir = os.path.join(abs_path, 'examples/').replace('\\', '/')
  
        ###   ~   module VectorDXF   ~   ###
        
        self.ui.lineEditInput.setText(dir + "example_06/VELOCITY UV_S161_Case_A.t3v")
        self.ui.doubleSpinBoxDX.setValue(25.0)
        self.ui.doubleSpinBoxDY.setValue(25.0)
        self.ui.doubleSpinBoxScale.setValue(40)
        
        self.ui.lineEditOutput.setText(dir + "example_06/output/velocity.dxf")         

    def create(self):

        info = ""
        
        dx = self.ui.doubleSpinBoxDX.value()
        dy = self.ui.doubleSpinBoxDY.value()
        
        VMin = self.ui.doubleSpinBoxVMin.value()
        VMax = self.ui.doubleSpinBoxVMax.value()
        
        scale = self.ui.doubleSpinBoxScale.value()
        
        eps = self.ui.doubleSpinBoxLessThan.value()
        
        # read input meshes
        try:
            x, y, u, v, triangles = fh.readT3VTriangulation(self.ui.lineEditInput.text())
        except:
            QMessageBox.critical(self.widget, "Error", "Not able to load mesh file!\nCheck filename or content!")
            return
        
        vectorNodes = {}
        sCounter = 0
        
        xMin = min(x)
        xMax = max(x)
        yMin = min(y)
        yMax = max(y)       
        
        triang = tri.Triangulation(x, y, triangles)
        
        # Interpolate to regularly-spaced quad grid.

        # origin of scalar
        x0 = floor(xMin/dx)*dx
        y0 = floor(yMin/dy)*dy

        # number of nodes in x- and y-direction
        nx = int(ceil(xMax/dx) - floor(xMin/dx))
        ny = int(ceil(yMax/dy) - floor(yMin/dy))

        xGrid, yGrid = np.meshgrid(np.linspace(x0, x0+nx*dx, nx+1), np.linspace(y0, y0+ny*dy, ny+1))
        info += " - Grid created with {0} x {1} points:\n\t- dx = {2}\n\t- dy = {3}\n\t- x(min) = {4}\n\t- y(min) = {5}\n\t- x(max) = {6}\n\t- y(max) = {7}\n".format(nx, ny, dx, dy, x0, y0, x0+nx*dx, y0+ny*dy)

        interpLinU = tri.LinearTriInterpolator(triang, u)
        zGridU = interpLinU(xGrid, yGrid)

        interpLinV = tri.LinearTriInterpolator(triang, v)
        zGridV = interpLinV(xGrid, yGrid)

        for iy in range(len(xGrid)):
            for ix in range(len(xGrid[0])):
                vectorNodes[sCounter] = [xGrid[iy][ix], yGrid[iy][ix], zGridU[iy][ix], zGridV[iy][ix]]
                sCounter += 1
   
        try:
            fname = self.ui.lineEditOutput.text()
            info += "\n - Number of interpolated values: {0}".format(len(vectorNodes))
            nOfVectors= fh.writeVectorDXF(vectorNodes, VMin, VMax, eps, scale, fname)
            info += "\n - {0} values written to {1}".format(nOfVectors, fname)
        except:
            QMessageBox.critical(self.widget, "Error", "Not able to write DXF file!")
            return   
        
        QMessageBox.information(self.widget, "Module VectorDXF", info)
        
        