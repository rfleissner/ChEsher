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

"""Wrapper for module LandXML"""

__author__="Reinhard Fleissner"
__date__ ="$18.05.2016 22:38:30$"

import functools
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QMessageBox

# modules and classes
from uiLandXML import Ui_LandXML
import uiHandler as uih
import fileHandler as fh

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class WrapLandXML():
    """Wrapper for module LandXML"""

    def __init__(self, dir):
        """Constructor."""

        self.directory = dir

        # setup user interface
        self.widget = QtGui.QWidget()
        self.ui = Ui_LandXML()
        self.ui.setupUi(self.widget)
        
# module XML
        self.callbackOpenMeshFile = functools.partial(uih.getOpenFileName, "Open T3S-file", "2D T3 Scalar Mesh (ASCII SingleFrame) (*.t3s)", self.ui.lineEditInputMesh, self.directory, self.widget)
        QtCore.QObject.connect(self.ui.pushButtonInputMesh, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackOpenMeshFile)

        self.callbackSaveXMLFile = functools.partial(uih.getSaveFileName, "Save Mesh As", "LandXML (*.xml)", self.ui.lineEditOutput, self.directory, self.widget)
        QtCore.QObject.connect(self.ui.pushButtonOutput, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackSaveXMLFile)

        QtCore.QObject.connect(self.ui.pushButtonCreate, QtCore.SIGNAL("clicked()"), self.create)

    def setDir(self, directory):
        self.directory = directory
        print "set", self.directory
    
    def initialize(self):
        
        import os
        abs_path = os.path.abspath('.')
        dir = os.path.join(abs_path, 'examples/').replace('\\', '/')
  
        ###   ~   module LandXML   ~   ###
        
        self.ui.lineEditInputMesh.setText(dir + "example_04/BOTTOM.t3s")
        self.ui.lineEditSurfaceName.setText("BOTTOM")
        self.ui.lineEditOutput.setText(dir + "example_04/output/BOTTOM.xml")
        
    def create(self):
        nodes, mesh = fh.readT3S(self.ui.lineEditInputMesh.text())

        try:
            fh.writeXML(nodes, mesh, self.ui.lineEditSurfaceName.text(), self.ui.lineEditOutput.text())
            info = "LandXML surface created with:\n"
            info += " - {0} nodes\n - {1} elements".format(len(nodes), len(mesh))            
            QMessageBox.information(self.widget, "LandXML", info)
        except:
            QMessageBox.critical(self.widget, "Error", "Not able to write LandXML!")
            return
   