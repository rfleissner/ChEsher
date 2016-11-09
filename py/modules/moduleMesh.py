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

"""Wrapper for module Mesh"""

__author__="Reinhard Fleissner"
__date__ ="$18.05.2016 22:38:30$"

import functools
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QMessageBox

# modules and classes
from uiMesh import Ui_Mesh
import uiHandler as uih
import fileHandler as fh
from calcMesh import CalcMesh
import ewsEnSim as ws
import macro as mc

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class WrapMesh():
    """Wrapper for module Mesh"""

    def __init__(self, dir):
        """Constructor."""

        self.directory = dir

        # setup user interface
        self.widget = QtGui.QWidget()
        self.ui = Ui_Mesh()
        self.ui.setupUi(self.widget)

# module Mesh

        self.callbackOpenProfilesFile = functools.partial(uih.getOpenFileName, "Open Profiles File", "Line Sets (*.i3s)", self.ui.lineEditProfiles, self.directory, self.widget)
        QtCore.QObject.connect(self.ui.pushButtonProfiles, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackOpenProfilesFile)

        self.callbackOpenReachFile = functools.partial(uih.getOpenFileName, "Open Reach File", "Line Sets (*.i2s *.i3s)", self.ui.lineEditReach, self.directory, self.widget)
        QtCore.QObject.connect(self.ui.pushButtonReach, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackOpenReachFile)

        self.callbackOpenLBLFile = functools.partial(uih.getOpenFileName, "Open Left Breakline File", "Line Sets (*.i2s *.i3s)", self.ui.lineEditLBL, self.directory, self.widget)
        QtCore.QObject.connect(self.ui.pushButtonLBL, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackOpenLBLFile)

        self.callbackOpenRBLFile = functools.partial(uih.getOpenFileName, "Open Right Breakline File", "Line Sets (*.i2s *.i3s)", self.ui.lineEditRBL, self.directory, self.widget)
        QtCore.QObject.connect(self.ui.pushButtonRBL, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackOpenRBLFile)

        self.callbackOpenLBOFile = functools.partial(uih.getOpenFileName, "Open Left Boundary File", "Line Sets (*.i2s *.i3s)", self.ui.lineEditLBO, self.directory, self.widget)
        QtCore.QObject.connect(self.ui.pushButtonLBO, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackOpenLBOFile)

        self.callbackOpenRBOFile = functools.partial(uih.getOpenFileName, "Open Right Boundary File", "Line Sets (*.i2s *.i3s)", self.ui.lineEditRBO, self.directory, self.widget)
        QtCore.QObject.connect(self.ui.pushButtonRBO, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackOpenRBOFile)

        self.callbackSaveMeshFile = functools.partial(uih.getSaveFileName, "Save Mesh As", "2D T3 Mesh (*.t3s)", self.ui.lineEditMesh, self.directory, self.widget)
        QtCore.QObject.connect(self.ui.pushButtonMesh, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackSaveMeshFile)

        self.callbackSaveIPFile = functools.partial(uih.getSaveFileName, "Save Interpolated Profiles As", "Line Sets (*.i3s)", self.ui.lineEditIP, self.directory, self.widget)
        QtCore.QObject.connect(self.ui.pushButtonIP, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackSaveIPFile)

        self.callbackSaveLEFile = functools.partial(uih.getSaveFileName, "Save Left Edge As", "Line Sets (*.i3s)", self.ui.lineEditLE, self.directory, self.widget)
        QtCore.QObject.connect(self.ui.pushButtonLE, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackSaveLEFile)

        self.callbackSaveREFile = functools.partial(uih.getSaveFileName, "Save Right Edge As", "Line Sets (*.i3s)", self.ui.lineEditRE, self.directory, self.widget)
        QtCore.QObject.connect(self.ui.pushButtonRE, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackSaveREFile)

        self.callbackSaveOLFile = functools.partial(uih.getSaveFileName, "Save Outline As", "Line Sets (*.i3s)", self.ui.lineEditOL, self.directory, self.widget)
        QtCore.QObject.connect(self.ui.pushButtonOL, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackSaveOLFile)

        self.callbackSaveWSFile = functools.partial(uih.getSaveFileName, "Save Workspace As", "EnSim WorkSpace File (*.ews)", self.ui.lineEditWS, self.directory, self.widget)
        QtCore.QObject.connect(self.ui.pushButtonWS, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackSaveWSFile)

        self.callbackLBL = functools.partial(self.setEnabledBL, self.ui.checkBoxLBL, self.ui.pushButtonLBL, self.ui.lineEditLBL, self.ui.spinBoxNNL)
        QtCore.QObject.connect(self.ui.checkBoxLBL, QtCore.SIGNAL("clicked()"), self.callbackLBL)

        self.callbackRBL = functools.partial(self.setEnabledBL, self.ui.checkBoxRBL, self.ui.pushButtonRBL, self.ui.lineEditRBL, self.ui.spinBoxNNR)
        QtCore.QObject.connect(self.ui.checkBoxRBL, QtCore.SIGNAL("clicked()"), self.callbackRBL)

        self.callbackLBO = functools.partial(uih.setEnabled, self.ui.checkBoxLBO, self.ui.pushButtonLBO, self.ui.lineEditLBO)
        QtCore.QObject.connect(self.ui.checkBoxLBO, QtCore.SIGNAL("clicked()"), self.callbackLBO)

        self.callbackRBO = functools.partial(uih.setEnabled, self.ui.checkBoxRBO, self.ui.pushButtonRBO, self.ui.lineEditRBO)
        QtCore.QObject.connect(self.ui.checkBoxRBO, QtCore.SIGNAL("clicked()"), self.callbackRBO)

        self.callbackMesh = functools.partial(uih.setEnabled, self.ui.checkBoxMesh, self.ui.pushButtonMesh, self.ui.lineEditMesh)
        QtCore.QObject.connect(self.ui.checkBoxMesh, QtCore.SIGNAL("clicked()"), self.callbackMesh)

        self.callbackIP = functools.partial(uih.setEnabled, self.ui.checkBoxIP, self.ui.pushButtonIP, self.ui.lineEditIP)
        QtCore.QObject.connect(self.ui.checkBoxIP, QtCore.SIGNAL("clicked()"), self.callbackIP)

        self.callbackLE = functools.partial(uih.setEnabled, self.ui.checkBoxLE, self.ui.pushButtonLE, self.ui.lineEditLE)
        QtCore.QObject.connect(self.ui.checkBoxLE, QtCore.SIGNAL("clicked()"), self.callbackLE)

        self.callbackRE = functools.partial(uih.setEnabled, self.ui.checkBoxRE, self.ui.pushButtonRE, self.ui.lineEditRE)
        QtCore.QObject.connect(self.ui.checkBoxRE, QtCore.SIGNAL("clicked()"), self.callbackRE)

        self.callbackOL = functools.partial(uih.setEnabled, self.ui.checkBoxOL, self.ui.pushButtonOL, self.ui.lineEditOL)
        QtCore.QObject.connect(self.ui.checkBoxOL, QtCore.SIGNAL("clicked()"), self.callbackOL)

        self.callbackWS = functools.partial(uih.setEnabled, self.ui.checkBoxWS, self.ui.pushButtonWS, self.ui.lineEditWS)
        QtCore.QObject.connect(self.ui.checkBoxWS, QtCore.SIGNAL("clicked()"), self.callbackWS)

        QtCore.QObject.connect(self.ui.pushButtonCreate, QtCore.SIGNAL("clicked()"), self.create)

    def setDir(self, directory):
        self.directory = directory
    
    def initialize(self):

        import os
        abs_path = os.path.abspath('.')
        dir = os.path.join(abs_path, 'examples/').replace('\\', '/')
         
        ###   ~   module Mesh   ~   ###

        self.ui.lineEditProfiles.setText(dir + "example_03/PROFILES.i3s")
        self.ui.lineEditReach.setText(dir + "example_03/AXIS.i2s")        
        
        uih.setEnabledInitialize(self.ui.checkBoxLBO, self.ui.pushButtonLBO, self.ui.lineEditLBO)
        self.ui.lineEditLBO.setText(dir + "example_03/LEFT_BOUNDARY.i3s")        

        uih.setEnabledInitialize(self.ui.checkBoxRBO, self.ui.pushButtonRBO, self.ui.lineEditRBO)
        self.ui.lineEditRBO.setText(dir + "example_03/RIGHT_BOUNDARY.i3s")    
        
        self.ui.checkBoxEC.setChecked(True)
        self.ui.doubleSpinBoxEL.setValue(1.0)
        self.ui.spinBoxNNC.setValue(20)
        
        self.ui.lineEditMesh.setText(dir + "example_03/output/MESH.t3s")
        uih.setEnabledInitialize(self.ui.checkBoxMesh, self.ui.pushButtonMesh, self.ui.lineEditMesh)
        
        self.ui.lineEditWS.setText(dir + "example_03/output/VIEW.ews")
        uih.setEnabledInitialize(self.ui.checkBoxWS, self.ui.pushButtonWS, self.ui.lineEditWS)
        
    def create(self):
        info = "Input data:\n"
        try:
            nodRaw, proRaw = fh.readI3S(self.ui.lineEditProfiles.text())
            info += " - Profiles:\t\t\t{0}\n".format(len(proRaw))
        except:
            QMessageBox.critical(self.widget, "Error", "Not able to load profiles file!\nCheck filename or content!")
            return
        try:
            nodReach = fh.readI2S(self.ui.lineEditReach.text())[0]
            info += " - Reach nodes:\t\t{0}\n".format(len(nodReach))
        except:
            QMessageBox.critical(self.widget, "Error", "Not able to load reach file!\nCheck filename or content!")
            return
            
        if len(proRaw) != len(nodReach):
            QMessageBox.critical(self.widget, "Error", "Number of profiles must correspond to number of reach nodes!")
            return
        
        nnC = self.ui.spinBoxNNC.value()
        length = self.ui.doubleSpinBoxEL.value()

        nnL = None
        nodLBL = None
        if self.ui.checkBoxLBL.isChecked():
            nnL = self.ui.spinBoxNNL.value()
            try:
                if self.ui.lineEditLBL.text().split(".")[-1] == "i2s":
                    nodLBL = fh.readI2S(self.ui.lineEditLBL.text())[0]
                else:
                    nodLBL = fh.readI3S(self.ui.lineEditLBL.text())[0]
                info += " - Left breakline nodes:\t{0}\n".format(len(nodLBL))
            except:
                QMessageBox.critical(self.widget, "Error", "Not able to load left breakline file!\nCheck filename or content!")
                return
        else:
            nnL = None
            nodLBL = None

        nnR = None
        nodRBL = None
        if self.ui.checkBoxRBL.isChecked():
            nnR = self.ui.spinBoxNNR.value()
            try:
                if self.ui.lineEditRBL.text().split(".")[-1] == "i2s":
                    nodRBL = fh.readI2S(self.ui.lineEditRBL.text())[0]
                else:
                    nodRBL = fh.readI3S(self.ui.lineEditRBL.text())[0]
                info += " - Right breakline nodes:\t{0}\n".format(len(nodRBL))
            except:
                QMessageBox.critical(self.widget, "Error", "Not able to load right breakline file!\nCheck filename or content!")
                return
        else:
            nnR = None
            nodRBL = None

        nodLBO = None
        if self.ui.checkBoxLBO.isChecked():
            try:
                if self.ui.lineEditLBO.text().split(".")[-1] == "i2s":
                    nodLBO = fh.readI2S(self.ui.lineEditLBO.text())[0]
                else:
                    nodLBO = fh.readI3S(self.ui.lineEditLBO.text())[0]
                info += " - Left boundary nodes:\t{0}\n".format(len(nodLBO))
            except:
                QMessageBox.critical(self.widget, "Error", "Not able to load left boundary file!\nCheck filename or content!")
                return
        else:
            nodLBO = None

        nodRBO = None
        if self.ui.checkBoxRBO.isChecked():
            try:
                if self.ui.lineEditRBO.text().split(".")[-1] == "i2s":
                    nodRBO = fh.readI2S(self.ui.lineEditRBO.text())[0]
                else:
                    nodRBO = fh.readI3S(self.ui.lineEditRBO.text())[0]
                info += " - Right boundary nodes:\t{0}\n".format(len(nodRBO))
            except:
                QMessageBox.critical(self.widget, "Error", "Not able to load right boundary file!\nCheck filename or content!")
                return
        else:
            nodRBO = None
        
        self.mesh = CalcMesh(   nodRaw,
                                proRaw,
                                nodReach,
                                nnC,
                                length,
                                nodLBL,
                                nodRBL,
                                nodLBO,
                                nodRBO,
                                nnL,
                                nnR
                                )

        try:                        
            info += self.mesh.determineFlowDirection()
        except:
            QMessageBox.critical(self.widget, "Error", "Not able to determine flow direction!\nCheck inputs!")
            return
        
        try:
            info += self.mesh.normalizeProfiles()
        except:
            QMessageBox.critical(self.widget, "Error", "Not able to normalize profiles!\nCheck inputs!")
            return
        
        try:
            info += self.mesh.interpolateChannel()
        except:
            QMessageBox.critical(self.widget, "Error", "Not able to interpolate channel!\nCheck inputs!")
            return
        
        try:
            info += self.mesh.interpolateElevation()
        except:
            QMessageBox.critical(self.widget, "Error", "Not able to interpolate elevation!\nCheck inputs!")
            return
        
        if self.ui.checkBoxEC.isChecked():
            try:
                info += self.mesh.interpolateElevationCorrection()
            except:
                QMessageBox.critical(self.widget, "Error", "Not able to interpolate elevation correction!\nCheck inputs!")
                return
            
        try:
            info += self.mesh.createMesh()
        except:
            QMessageBox.critical(self.widget, "Error", "Not able to create mesh!\nCheck inputs!")
            return
        
        try:
            self.writeOutput()
        except:
            QMessageBox.critical(self.widget, "Error", "Not able to write output!")
            return
        
        QMessageBox.information(self.widget, "Module Mesh", info)

    def writeOutput(self):
        if self.ui.checkBoxMesh.isChecked():
            fh.writeT3S(self.mesh.nodMesh, self.mesh.mesh, self.ui.lineEditMesh.text())
        if self.ui.checkBoxIP.isChecked():
            fh.writeI3S(self.mesh.nodInterp, self.mesh.proInterp, self.ui.lineEditIP.text())
        if self.ui.checkBoxLE.isChecked():
            LE = {1:mc.getNodeIDsLeft(self.mesh.proMesh)}
            fh.writeI3S(self.mesh.nodMesh, LE, self.ui.lineEditLE.text())
        if self.ui.checkBoxRE.isChecked():
            RE = {1:mc.getNodeIDsRight(self.mesh.proMesh)}
            fh.writeI3S(self.mesh.nodMesh, RE, self.ui.lineEditRE.text())
        if self.ui.checkBoxOL.isChecked():
            OL = {1:mc.getNodeIDsOutline(self.mesh.proMesh)}
            fh.writeI3S(self.mesh.nodMesh, OL, self.ui.lineEditOL.text())

        if self.ui.checkBoxWS.isChecked():
            view = """"""
            counter = -1
            content = """"""

            content += ws.lineSet.format(self.getDim(self.ui.lineEditProfiles), self.getPath(self.ui.lineEditProfiles), "0xff0000", "raw profiles")
            counter += 1
            view += ":ObjectView {0} 0\n".format(counter)

            content += ws.lineSet.format(self.getDim(self.ui.lineEditReach), self.getPath(self.ui.lineEditReach), "0xffff00", "channel reach")
            counter += 1
            view += ":ObjectView {0} 0\n".format(counter)

            if self.ui.checkBoxLBL.isChecked():
                content += ws.lineSet.format(self.getDim(self.ui.lineEditLBL), self.getPath(self.ui.lineEditLBL), "0x00ff00", "left breakline")
                counter += 1
                view += ":ObjectView {0} 0\n".format(counter)

            if self.ui.checkBoxRBL.isChecked():
                content += ws.lineSet.format(self.getDim(self.ui.lineEditRBL), self.getPath(self.ui.lineEditRBL), "0x00ff00", "right breakline")
                counter += 1
                view += ":ObjectView {0} 0\n".format(counter)

            if self.ui.checkBoxLBO.isChecked():
                content += ws.lineSet.format(self.getDim(self.ui.lineEditLBO), self.getPath(self.ui.lineEditLBO), "0x0000ff", "left boundary")
                counter += 1
                view += ":ObjectView {0} 0\n".format(counter)

            if self.ui.checkBoxRBO.isChecked():
                content += ws.lineSet.format(self.getDim(self.ui.lineEditRBO), self.getPath(self.ui.lineEditRBO), "0x0000ff", "right boundary")
                counter += 1
                view += ":ObjectView {0} 0\n".format(counter)

            content += ws.meshScalar.format(self.getPath(self.ui.lineEditMesh), "0xc0c0c0", "mesh")
            counter += 1
            view += ":ObjectView {0} 0\n".format(counter)


            if self.ui.checkBoxIP.isChecked():
                content += ws.lineSet.format(self.getDim(self.ui.lineEditIP), self.getPath(self.ui.lineEditIP), "0x8000ff", "interpolated profiles")
                counter += 1
                view += ":ObjectView {0} 1\n".format(counter)

            if self.ui.checkBoxLE.isChecked():
                content += ws.lineSet.format(self.getDim(self.ui.lineEditLE), self.getPath(self.ui.lineEditLE), "0x0080ff", "left edge")
                counter += 1
                view += ":ObjectView {0} 1\n".format(counter)

            if self.ui.checkBoxRE.isChecked():
                content += ws.lineSet.format(self.getDim(self.ui.lineEditRE), self.getPath(self.ui.lineEditRE), "0x0080ff", "right edge")
                counter += 1
                view += ":ObjectView {0} 1\n".format(counter)

            if self.ui.checkBoxOL.isChecked():
                content += ws.lineSet.format(self.getDim(self.ui.lineEditOL), self.getPath(self.ui.lineEditOL), "0x800080", "outline")
                counter += 1
                view += ":ObjectView {0} 1\n".format(counter)

            content += ws.meshScalar.format(self.getPath(self.ui.lineEditMesh), "0x808080", "mesh")
            counter += 1
            view += ":ObjectView {0} 1\n".format(counter)

            fh.writeEWS(content, view, self.ui.lineEditWS.text())
            
    def setEnabledBL(self, checkBox, pushButton, lineEdit, spinBox):
        uih.setEnabled(checkBox, pushButton, lineEdit)
        checked = checkBox.isChecked()
        spinBox.setEnabled(checked)
        
    def getDim(self, lineEdit):
        return lineEdit.text().split('.')[-1][1]

    def getPath(self, lineEdit):
        return lineEdit.text().replace('/', '\\')