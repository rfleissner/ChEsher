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

"""Wrapper for module ScalarDXF"""

__author__="Reinhard Fleissner"
__date__ ="$18.05.2016 22:38:30$"

import os
import functools
from math import ceil, floor
import numpy as np

import matplotlib
matplotlib.use("Agg")
import matplotlib.tri as tri

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QMessageBox, QFileDialog

# modules and classes
from uiScalarDXF import Ui_ScalarDXF
import fileHandler as fh

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class WrapScalarDXF():
    """Wrapper for module ScalarDXF"""

    def __init__(self):
        """Constructor."""

        # setup user interface
        self.widget = QtGui.QWidget()
        self.ui = Ui_ScalarDXF()
        self.ui.setupUi(self.widget)
        self.directory = os.path.abspath('.')
        
# module ScalarDXF

        self.callbackOpenScalarInputT3SMajor = functools.partial(self.getOpenFileName, "Open 2D T3 Scalar Mesh", "2D T3 Scalar Mesh (ASCIISingleFrame) (*.t3s)", self.ui.lineEditInputT3SMajor)
        QtCore.QObject.connect(self.ui.pushButtonInputT3SMajor, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackOpenScalarInputT3SMajor)

        self.callbackOpenScalarInputT3SMinor = functools.partial(self.getOpenFileName, "Open 2D T3 Scalar Mesh", "2D T3 Scalar Mesh (ASCIISingleFrame) (*.t3s)", self.ui.lineEditInputT3SMinor)
        QtCore.QObject.connect(self.ui.pushButtonInputT3SMinor, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackOpenScalarInputT3SMinor)

        self.callbackScalarScalar = functools.partial(self.getSaveFileName, "Save DXF-file As", "Drawing Interchange File (*.dxf)", self.ui.lineEditOutput)
        QtCore.QObject.connect(self.ui.pushButtonOutput, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackScalarScalar)
        
        self.ui.spinBoxScale.valueChanged.connect(self.setScale)
                
        self.scalarSymbol = 0
        
        self.callbackCircle = functools.partial(self.setSymbol, 0)
        QtCore.QObject.connect(self.ui.radioButtonCircle, QtCore.SIGNAL("clicked()"), self.callbackCircle)
        self.callbackCross = functools.partial(self.setSymbol, 1)
        QtCore.QObject.connect(self.ui.radioButtonCross, QtCore.SIGNAL("clicked()"), self.callbackCross)
        self.callbackCrosshairs = functools.partial(self.setSymbol, 2)
        QtCore.QObject.connect(self.ui.radioButtonCrosshairs, QtCore.SIGNAL("clicked()"), self.callbackCrosshairs)
        self.callbackNone = functools.partial(self.setSymbol, 3)
        QtCore.QObject.connect(self.ui.radioButtonNone, QtCore.SIGNAL("clicked()"), self.callbackNone)

        QtCore.QObject.connect(self.ui.pushButtonCreate, QtCore.SIGNAL("clicked()"), self.create)

    def setDir(self, directory):
        self.directory = directory
        print "set", self.directory
    
    def initialize(self):
        
        import os
        abs_path = os.path.abspath('.')
        dir = os.path.join(abs_path, 'examples/').replace('\\', '/')
  
        ###   ~   module ScalarDXF   ~   ###

        self.ui.lineEditInputT3SMajor.setText(dir + "example_05/WATER DEPTH_S161_Case_A.t3s")
        self.ui.lineEditInputT3SMinor.setText(dir + "example_05/WATER DEPTH_S161_Case_B.t3s")
        self.ui.doubleSpinBoxDX.setValue(50.0)
        self.ui.doubleSpinBoxDY.setValue(50.0)
        self.ui.doubleSpinBoxSizeFactor.setValue(7.5)
        
        self.ui.checkBoxMonochrome.setChecked(True)
        self.ui.radioButtonCircle.setChecked(False)
        self.ui.radioButtonCrosshairs.setChecked(True)
        self.setSymbol(2)
        
        self.ui.lineEditOutput.setText(dir + "example_05/output/water_depth.dxf")        

    def create(self):
        
        info = ""
        
        dx = self.ui.doubleSpinBoxDX.value()
        dy = self.ui.doubleSpinBoxDY.value()
        
        SMin = self.ui.doubleSpinBoxSMin.value()
        SMax = self.ui.doubleSpinBoxSMax.value()
        
        scale = self.ui.doubleSpinBoxSizeFactor.value()
        
        eps = self.ui.doubleSpinBoxLessThan.value()
        
        # read input meshes
        
        try:
            x, y, zMajor, triangles = fh.readT3STriangulation(self.ui.lineEditInputT3SMajor.text())
        except Exception, e:
            QMessageBox.critical(self, "Error", "Not able to load mesh file!\nCheck filename or content!" + "\n\n" + str(e))
            return
        
        minor = False
        if self.ui.lineEditInputT3SMinor.text() != "":
            minor = True
            try:
                x, y, zMinor, triangles = fh.readT3STriangulation(self.ui.lineEditInputT3SMinor.text())
            except Exception, e:
                QMessageBox.critical(self.widget, "Error", "Not able to load mesh file!\nCheck filename or content!" + "\n\n" + str(e))
                return            
            
        scalarNodes = {}
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

        interpLinMajor = tri.LinearTriInterpolator(triang, zMajor)
        zGridMaj = interpLinMajor(xGrid, yGrid)

        zGridMin = []
        if minor is True:
            interpLinMinor = tri.LinearTriInterpolator(triang, zMinor)
            zGridMin = interpLinMinor(xGrid, yGrid)
            
        for iy in range(len(xGrid)):
            for ix in range(len(xGrid[0])):
                if minor is True:
                    scalarNodes[sCounter] = [xGrid[iy][ix], yGrid[iy][ix], zGridMaj[iy][ix], zGridMin[iy][ix]]
                    sCounter += 1
                else:
                    scalarNodes[sCounter] = [xGrid[iy][ix], yGrid[iy][ix], zGridMaj[iy][ix], None]
                    sCounter += 1                    

        useMono = self.ui.checkBoxMonochrome.isChecked()
        fname = self.ui.lineEditOutput.text()
        info += "\n - Number of interpolated values: {0}".format(len(scalarNodes))

        try:
            nOfValues = fh.writeScalarDXF(scalarNodes, SMin, SMax, eps, scale, self.scalarSymbol, useMono, fname)
            info += "\n - {0} values written to {1}".format(nOfValues, fname)
        except Exception, e:
            QMessageBox.critical(self.widget, "Error", "Not able to write DXF file!" + "\n\n" + str(e))
            return

        QMessageBox.information(self.widget, "Module ScalarDXF", info)  

    def setSymbol(self, i):
        self.scalarSymbol = i

    def setScale(self):

        scale = self.ui.spinBoxScale.value()
        d = scale/100.0
        size_factor = scale*3.0/2000.0
        
        self.ui.doubleSpinBoxDX.setValue(d)
        self.ui.doubleSpinBoxDY.setValue(d)
                
        self.ui.doubleSpinBoxSizeFactor.setValue(size_factor)
        
    def getOpenFileName(self, title, fileFormat, lineEdit):
        filename = QFileDialog.getOpenFileName(self.widget, title, self.directory, fileFormat)
        if filename != "":
            lineEdit.setText(filename)

    def getSaveFileName(self, title, fileFormat, lineEdit):
        filename = QFileDialog.getSaveFileName(self.widget, title, self.directory, fileFormat)
        if filename != "":
            lineEdit.setText(filename)