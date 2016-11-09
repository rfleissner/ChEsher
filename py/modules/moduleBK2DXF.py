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

"""Wrapper for module Profiles"""

__author__="Reinhard Fleissner"
__date__ ="$18.05.2016 22:38:30$"

import dxfgrabber
import functools
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QFileDialog, QMessageBox

# modules and classes
from uiBK2DXF import Ui_BK2DXF
import uiHandler as uih
import fileHandler as fh

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class WrapBK2DXF():
    """Wrapper for module BK2DXF"""

    def __init__(self, dir):
        """Constructor."""

        self.directory = dir

        # setup user interface
        self.widget = QtGui.QWidget()
        self.ui = Ui_BK2DXF()
        self.ui.setupUi(self.widget)

        # module BK2DXF
        
        self.callbackOpenMeshFile = functools.partial(uih.getOpenFileName, "Open T3S-file", "2D T3 Scalar Mesh (ASCII SingleFrame) (*.t3s)", self.ui.lineEditInputMesh, self.directory, self.widget)
        QtCore.QObject.connect(self.ui.pushButtonInputMesh, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackOpenMeshFile)

        self.callbackOpenLineSetFile = functools.partial(uih.getOpenFileName, "Open Line Set", "Line Sets (*.i2s *.i3s)", self.ui.lineEditInputLineSet, self.directory, self.widget)
        QtCore.QObject.connect(self.ui.pushButtonInputLineSet, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackOpenLineSetFile)
        
        self.callbackOutMesh = functools.partial(uih.getSaveFileName, "Save Mesh As", "Drawing Interchange File (*.dxf)", self.ui.lineEditOutputMesh, self.directory, self.widget)
        QtCore.QObject.connect(self.ui.pushButtonOutputMesh, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackOutMesh)

        self.callbackOutLineSet = functools.partial(uih.getSaveFileName, "Save Line Set As", "Drawing Interchange File (*.dxf)", self.ui.lineEditOutputLineSet, self.directory, self.widget)
        QtCore.QObject.connect(self.ui.pushButtonOutputLineSet, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackOutLineSet)

        self.callbackOutCheckMesh = functools.partial(uih.setEnabled, self.ui.checkBoxOutputMesh, self.ui.pushButtonOutputMesh, self.ui.lineEditOutputMesh, self.directory, self.widget)
        QtCore.QObject.connect(self.ui.checkBoxOutputMesh, QtCore.SIGNAL("clicked()"), self.callbackOutCheckMesh)
        
        self.callbackOutCheckLineSet= functools.partial(uih.setEnabled, self.ui.checkBoxOutputLineSet, self.ui.pushButtonOutputLineSet, self.ui.lineEditOutputLineSet, self.directory, self.widget)
        QtCore.QObject.connect(self.ui.checkBoxOutputLineSet, QtCore.SIGNAL("clicked()"), self.callbackOutCheckLineSet)
        
        self.typeDXFmesh = 1
        
        self.callback3DFace = functools.partial(self.setTypeDXFmesh, 1)
        QtCore.QObject.connect(self.ui.radioButton3DFace, QtCore.SIGNAL("clicked()"), self.callback3DFace)
        
        self.callbackPolyline = functools.partial(self.setTypeDXFmesh, 2)
        QtCore.QObject.connect(self.ui.radioButtonPolyline, QtCore.SIGNAL("clicked()"), self.callbackPolyline)
        
        QtCore.QObject.connect(self.ui.pushButtonCreate, QtCore.SIGNAL("clicked()"), self.create)

    def setTypeDXFmesh(self, i):
        self.typeDXFmesh = i
        
    def setDir(self, directory):
        self.directory = directory

    def create(self):

        info = ""
        info += "Input data:\n"
        
        # read input meshes
        nodes = {}
        mesh = {}
        if self.ui.lineEditInputMesh.text() != "":
            try:
                nodes, mesh = fh.readT3S(self.ui.lineEditInputMesh.text())
                info += " - Mesh loaded with {0} nodes and {1} elements.\n".format(len(nodes), len(mesh))
            except:
                QMessageBox.critical(self.widget, "Error", "Not able to load mesh file!\nCheck filename or content!")
                return

        # read input line sets
        linesetNodes = {}
        lineset = {}
        dim = 2
        if self.ui.lineEditInputLineSet.text() != "":
            try:
                if self.ui.lineEditInputLineSet.text().split(".")[-1] == "i2s":
                    linesetNodes, lineset = fh.readI2S(self.ui.lineEditInputLineSet.text())                
                    dim = 2
                else:
                    linesetNodes, lineset = fh.readI3S(self.ui.lineEditInputLineSet.text())
                    dim = 3
                info += " - Line set loaded with {0} lines and {1} nodes.\n".format(len(lineset), len(linesetNodes))
            except:
                QMessageBox.critical(self.widget, "Error", "Not able to load line set!\nCheck filename or content!")
                return

        info += "\nOutput data:\n"
        
        # write mesh
        if self.ui.checkBoxOutputMesh.isChecked() and self.ui.lineEditInputMesh.text() != "":
            try:
                fh.writeMeshDXF(self.ui.lineEditOutputMesh.text(), nodes, mesh, self.typeDXFmesh)
                info += " - Mesh written to {0}.\n".format(self.ui.lineEditOutputMesh.text())
            except:
                QMessageBox.critical(self.widget, "Error", "Not able to write mesh!")
                return
            
        # write line set
        if self.ui.checkBoxOutputLineSet.isChecked() and self.ui.lineEditInputLineSet.text() != "":
            try:
                fh.writeLineSetDXF(self.ui.lineEditOutputLineSet.text(), linesetNodes, lineset, dim)
                info += " - Line set written to {0}.\n".format(self.ui.lineEditOutputLineSet.text())
            except:
                QMessageBox.critical(self.widget, "Error", "Not able to write line sets!")
                return
    
        QMessageBox.information(self.widget, "Module BK2DXF", info)

    
    def initialize(self):
        
        import os
        abs_path = os.path.abspath('.')
        dir = os.path.join(abs_path, 'examples/').replace('\\', '/')
        
        self.ui.lineEditInputMesh.setText(dir + "example_02/WATER DEPTH_S161_Case_A.t3s")
        self.ui.lineEditInputLineSet.setText(dir + "example_02/WATER DEPTH_S161_Case_A(IsoLine).i2s")        
        uih.setEnabledInitialize(self.ui.checkBoxOutputMesh, self.ui.pushButtonOutputMesh, self.ui.lineEditOutputMesh)
        uih.setEnabledInitialize(self.ui.checkBoxOutputLineSet, self.ui.pushButtonOutputLineSet, self.ui.lineEditOutputLineSet)
        
        self.ui.lineEditOutputMesh.setText(dir + "example_02/output/mesh.dxf")        
        self.ui.lineEditOutputLineSet.setText(dir + "example_02/output/contour.dxf")        
