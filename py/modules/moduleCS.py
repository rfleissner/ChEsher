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

"""Wrapper for module CS"""

__author__="Reinhard Fleissner"
__date__ ="$18.05.2016 22:38:30$"

import functools

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QMessageBox

# modules and classes
from uiCS import Ui_CS
import uiHandler as uih
import fileHandler as fh

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class WrapCS():
    """Wrapper for module CS"""

    def __init__(self, dir):
        """Constructor."""

        self.directory = dir

        # setup user interface
        self.widget = QtGui.QWidget()
        self.ui = Ui_CS()
        self.ui.setupUi(self.widget)
        
# module CS

        self.callbackCSOpenMeshFile = functools.partial(uih.getOpenFileName, "Open T3S-file", "2D T3 Scalar Mesh (ASCII SingleFrame) (*.t3s)", self.ui.lineEditInputMesh, self.directory, self.widget)
        QtCore.QObject.connect(self.ui.pushButtonInputMesh, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackCSOpenMeshFile)

        self.callbackCSOpenDefinition = functools.partial(uih.getOpenFileName, "Open Control Sections Definition File", "Normal text file (*.txt)", self.ui.lineEditInputDefinition, self.directory, self.widget)
        QtCore.QObject.connect(self.ui.pushButtonInputDefinition, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackCSOpenDefinition)

        self.callbackCSOpenResults = functools.partial(uih.getOpenFileName, "Open Control Sections Results File", "Normal text file (*.txt)", self.ui.lineEditInputResults, self.directory, self.widget)
        QtCore.QObject.connect(self.ui.pushButtonInputResults, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackCSOpenResults)

        self.callbacCSOutCheckFormatted = functools.partial(uih.setEnabled, self.ui.checkBoxOutputFormatted, self.ui.pushButtonOutputFormatted, self.ui.lineEditOutputFormatted)
        QtCore.QObject.connect(self.ui.checkBoxOutputFormatted, QtCore.SIGNAL("clicked()"), self.callbacCSOutCheckFormatted)
        
        self.callbacCSOutFormatted = functools.partial(uih.getSaveFileName, "Save Data File As", "Normal text file (*.txt)", self.ui.lineEditOutputFormatted, self.directory, self.widget)
        QtCore.QObject.connect(self.ui.pushButtonOutputFormatted, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbacCSOutFormatted)

        QtCore.QObject.connect(self.ui.checkBoxOutputCS, QtCore.SIGNAL("clicked()"), self.setEnabledCS)
        
        self.callbacCSOutCS = functools.partial(uih.getSaveFileName, "Save Control Sections As", "Drawing Interchange File (*.dxf)", self.ui.lineEditOutputCS, self.directory, self.widget)
        QtCore.QObject.connect(self.ui.pushButtonOutputCS, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbacCSOutCS)

        QtCore.QObject.connect(self.ui.pushButtonCreate, QtCore.SIGNAL("clicked()"), self.create)
        
#        self.callbackOpenVectorInput = functools.partial(uih.getOpenFileName, "Open 2D T3 Vector Mesh", "2D T3 Vector Mesh (ASCIISingleFrame) (*.t3v)", self.ui.lineEditInput, self.directory, self.widget)
#        QtCore.QObject.connect(self.ui.pushButtonInput, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackOpenVectorInput)
#        
#        self.callbackScalarVector = functools.partial(uih.getSaveFileName, "Save DXF-file As", "Drawing Interchange File (*.dxf)", self.ui.lineEditOutput, self.directory, self.widget)
#        QtCore.QObject.connect(self.ui.pushButtonOutput, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackScalarVector)    
#        
#        QtCore.QObject.connect(self.ui.pushButtonCreate, QtCore.SIGNAL("clicked()"), self.create)

    def setDir(self, directory):
        self.directory = directory
        print "set", self.directory
    
    def initialize(self):
        
        import os
        abs_path = os.path.abspath('.')
        dir = os.path.join(abs_path, 'examples/').replace('\\', '/')
  
        ###   ~   module CS   ~   ###
        
        self.ui.lineEditInputMesh.setText(dir + "example_07/BOTTOM_Case_A.t3s")
        self.ui.lineEditInputDefinition.setText(dir + "example_07/cs_input.txt")
        self.ui.lineEditInputResults.setText(dir + "example_07/cs_output_donau.txt")
        self.ui.doubleSpinBoxSizeFactor.setValue(7.5)
        
        uih.setEnabledInitialize(self.ui.checkBoxOutputFormatted, self.ui.pushButtonOutputFormatted, self.ui.lineEditOutputFormatted)
        uih.setEnabledInitialize(self.ui.checkBoxOutputCS, self.ui.pushButtonOutputCS, self.ui.lineEditOutputCS)

        self.ui.lineEditOutputFormatted.setText(dir + "example_07/output/cs_formatted.txt")
        self.ui.lineEditOutputCS.setText(dir + "example_07/output/cs.dxf")
        
    def setEnabledCS(self):
        checked = self.ui.checkBoxOutputCS.isChecked()
        self.ui.doubleSpinBoxSizeFactor.setEnabled(checked)
        self.ui.lineEditInputPrefix.setEnabled(checked)       
        self.ui.lineEditInputSuffix.setEnabled(checked) 
        self.ui.pushButtonOutputCS.setEnabled(checked)    
        self.ui.lineEditOutputCS.setEnabled(checked)        
        
    def create(self):
        
        info = ""
        info += "Input data:\n"
        
        # read input meshes
        nodes = {}
        mesh = {}
        
        try:
            nodes, mesh = fh.readT3S(self.ui.lineEditInputMesh.text())
            info += " - Mesh loaded with {0} nodes and {1} elements.\n".format(len(nodes), len(mesh))
        except:
            QMessageBox.critical(self.widget, "Error", "Not able to load mesh file!\nCheck filename or content!")
            return
    
        # read control sections definition file
        nCS = 0
        nameCS = {}
        nodeIDsCS = {}
        try:
            nCS, nameCS, nodeIDsCS, coordsCS, type = fh.readCSDefinition(self.ui.lineEditInputDefinition.text())
            info += " - Control section definition loaded with {0} control sections.\n".format(nCS)
        except:
            QMessageBox.critical(self.widget, "Error", "Not able to load control sections definition file!\nCheck filename or content!")
            return

        # read control sections results file
        time = []
        resultsCS = {}
        try:
            time, resultsCS = fh.readCSResults(self.ui.lineEditInputResults.text(), nCS)
            info += " - Control section results loaded with {0} time steps.\n".format(len(time))
        except:
            QMessageBox.critical(self.widget, "Error", "Not able to load control sections results file!\nCheck filename or content!")
            return        
        
        decTime = self.ui.spinBoxTime.value()
        decFlow = self.ui.spinBoxFlow.value()

        info += "\nOutput data:\n"
                    
        if self.ui.checkBoxOutputFormatted.isChecked():
            try:
                fh.writeCSFormatted(self.ui.lineEditOutputFormatted.text(), nameCS, time, resultsCS, decTime, decFlow)
                info += " - Formatted control section data file written to {0}.\n".format(self.ui.lineEditOutputFormatted.text())
            except:
                QMessageBox.critical(self.widget, "Error", "Not able to write formatted data file!")
                return

        if self.ui.checkBoxOutputCS.isChecked():
            try:
                nodesCS = {}
                valuesCS = {}

                if type == "1":
                    nodesCS = coordsCS
                    for nID in nodeIDsCS:
                        valuesCS[nID] = [min(resultsCS[nID]), max(resultsCS[nID])]
                else:
                    for nID in nodeIDsCS:
                        nodesCS[nodeIDsCS[nID][0]] = nodes[nodeIDsCS[nID][0]]
                        nodesCS[nodeIDsCS[nID][1]] = nodes[nodeIDsCS[nID][1]]
                        valuesCS[nID] = [min(resultsCS[nID]), max(resultsCS[nID])]

                scale = self.ui.doubleSpinBoxSizeFactor.value()
                prefix = self.ui.lineEditInputPrefix.text()
                suffix = self.ui.lineEditInputSuffix.text()
                fh.writeCSDXF(self.ui.lineEditOutputCS.text(), nameCS, nodeIDsCS, nodesCS, valuesCS, decFlow, scale, prefix, suffix)
                info += " - Control sections written to {0}.\n".format(self.ui.lineEditOutputCS.text())
                for key in valuesCS:
                    info += "\t{0} to {1} ({2})\n".format(round(valuesCS[key][0], decFlow), round(valuesCS[key][1], decFlow), nameCS[key])
            except:
                QMessageBox.critical(self.widget, "Error", "Not able to write control section file!")
                return               
    
        QMessageBox.information(self.widget, "Module CS", info)