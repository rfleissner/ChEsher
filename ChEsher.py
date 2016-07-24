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

"""Main module"""

__author__="Reinhard Fleissner"
__date__ ="$31.03.2015 18:21:40$"

import sys
import platform
import functools
import dxfgrabber
import os
from math import ceil, floor
import matplotlib
matplotlib.use("Agg")
import matplotlib.tri as tri
from matplotlib import colors
import matplotlib.pyplot as plt


from moduleHyDesign import WrapHyDesign
from moduleProfiles import WrapProfiles
from moduleHEC2DXF import WrapHEC2DXF
from moduleXYZ2DXF import WrapXYZ2DXF
from moduleProfilesDXF import WrapProfilesDXF

import triangle
import triangle.plot
import numpy as np
import webbrowser 
from random import uniform
from shapely.geometry import LinearRing, Polygon, Point

# libraries
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QFileDialog, QAction, QMessageBox, QIcon, QMessageBox, QColor
from PyQt4.QtCore import PYQT_VERSION_STR, QT_VERSION_STR, Qt, SIGNAL

# modules and classes

import fileHandler as fh
import macro as mc
import ewsEnSim as ws
from calcMesh import CalcMesh
from uiChEsher import Ui_MainWindow
from resource_rc import *

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class ChEsher(QtGui.QMainWindow):
    """Main class.

    Create menubar, toolbar, actions.
    Translate the application.
    Switch between module ENGINEERING and EDUCATION.

    """
    def __init__(self, app, parent=None):
        """Constructor for main class.

        Keyword arguments:
        app -- the application

        """
        super(ChEsher, self).__init__(parent)
        self._app = app
        # setup user interface of main window
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # variables
        self.directory = ""
        self.filenameProfiles = ""
        self.filenameReach = ""
        self.filenameLBL = ""
        self.filenameRBL = ""
        self.filenameLBO = ""
        self.filenameRBO = ""
        self.length = 0.0
        self.nnC = 2
        self.nnL = 2
        self.nnR = 2

        self.dxf = None
        self.layers = ()

        self.mesh = None

        self.logcounter = 0
        
        # setup instance of module HyDesign
        self.moduleHyDesign = WrapHyDesign()
        self.widgetHyDesign = self.moduleHyDesign.widget
        self.ui.stackedWidget.insertWidget(11,self.widgetHyDesign)

        # setup instance of module Profiles
        self.moduleProfiles = WrapProfiles(self.directory)
        self.widgetProfiles = self.moduleProfiles.widget
        self.ui.stackedWidget.insertWidget(12,self.widgetProfiles)    
        
        # setup instance of module HEC2DXF
        self.moduleHEC2DXF = WrapHEC2DXF(self.directory)
        self.widgetHEC2DXF = self.moduleHEC2DXF.widget
        self.ui.stackedWidget.insertWidget(13,self.widgetHEC2DXF)  
        
        # setup instance of module XYZ2DXF
        self.moduleXYZ2DXF = WrapXYZ2DXF(self.directory)
        self.widgetXYZ2DXF = self.moduleXYZ2DXF.widget
        self.ui.stackedWidget.insertWidget(14,self.widgetXYZ2DXF)                

        # setup instance of module ProfilesDXF
        self.moduleProfilesDXF = WrapProfilesDXF(self.directory)
        self.widgetProfilesDXF = self.moduleProfilesDXF.widget
        self.ui.stackedWidget.insertWidget(15,self.widgetProfilesDXF)   
        
        # actions in menu
        self.fileSetDirectory = self.createAction("Set working directory", slot=self.setDirectory)
        self.fileQuitAction = self.createAction("Close", slot=self.close, \
            shortcut="Ctrl+Q")
        self.fileSetExamples = self.createAction("Initialize examples", slot=self.initializeModules)
        self.helpAction = self.createAction("Help", slot=self.help, shortcut="F1")
        self.setDXFtoBKAction = self.createAction("DXF2BK", slot=self.setDXF2BK, shortcut="F2")
        self.setBK2DXFAction = self.createAction("BK2DXF", slot=self.setBK2DXF, shortcut="F3")
        self.setMeshAction = self.createAction("Mesh", slot=self.setMesh, shortcut="F4")
        self.setXMLAction = self.createAction("LandXML", slot=self.setLandXML, shortcut="F5")
        self.setScalarAction = self.createAction("ScalarDXF", slot=self.setScalarDXF, shortcut="F6")
        self.setVectorAction = self.createAction("VectorDXF", slot=self.setVectorDXF, shortcut="F7")
        self.setCSAction = self.createAction("CS", slot=self.setCS, shortcut="F8")
        self.set2DMAction = self.createAction("2DM2BK", slot=self.set2DM2BK, shortcut="F9")
        self.setCont2DXFAction = self.createAction("Cont2DXF", slot=self.setCont2DXF, shortcut="F10")
        self.setTubeAction = self.createAction("Tube", slot=self.setTube, shortcut="F11")
        self.setHyDesignAction = self.createAction("HyDesign", slot=self.setHyDesign, shortcut="F12")
        self.setProfilesAction = self.createAction("Profiles", slot=self.setProfiles)
        self.setHEC2DXFAction = self.createAction("HEC2DXF", slot=self.setHEC2DXF)
        self.setXYZ2DXFAction = self.createAction("XYZ2DXF", slot=self.setXYZ2DXF)
        self.setProfilesDXFAction = self.createAction("ProfilesDXF", slot=self.setProfilesDXF)
        
        self.helpAboutAction = self.createAction("&About", \
            self.helpAbout)
        # create menu
        self.fileMenu = self.menuBar().addMenu("ChEsher")
        self.moduleMenu = self.menuBar().addMenu("Module")
        self.helpMenu = self.menuBar().addMenu("Help")
        # add actions to menu
        self.addActions(self.fileMenu, (self.fileSetDirectory, self.fileSetExamples, None, self.fileQuitAction))
        self.addActions(self.moduleMenu, (self.setDXFtoBKAction, self.setBK2DXFAction, self.setMeshAction, self.setXMLAction, self.setScalarAction, self.setVectorAction, self.setCSAction, self.set2DMAction, self.setCont2DXFAction, self.setTubeAction, self.setHyDesignAction, self.setProfilesAction, self.setHEC2DXFAction, self.setXYZ2DXFAction, self.setProfilesDXFAction))
        self.addActions(self.helpMenu, (self.helpAction, None, self.helpAboutAction))


# module DXF2BK
        self.callbackOpenDXFFile = functools.partial(self.openDXFFile, "Open DXF-file", "Drawing Interchange File (*.dxf)", self.ui.lineEditDXF2BKInput)
        QtCore.QObject.connect(self.ui.pushButtonDXF2BKInput, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackOpenDXFFile)

        QtCore.QObject.connect(self.ui.pushButtonAdd, QtCore.SIGNAL(_fromUtf8("clicked()")), self.addLayer)
        QtCore.QObject.connect(self.ui.pushButtonDelete, QtCore.SIGNAL(_fromUtf8("clicked()")), self.deleteLayer)

        QtCore.QObject.connect(self.ui.pushButtonOpen, QtCore.SIGNAL(_fromUtf8("clicked()")), self.getSaveLayerName)
        QtCore.QObject.connect(self.ui.pushButtonRefresh, QtCore.SIGNAL("clicked()"), self.refreshDXF)
        QtCore.QObject.connect(self.ui.pushButtonDXF2BKConvert, QtCore.SIGNAL("clicked()"), self.createDXF2BK)

        header = self.ui.tableWidgetDXF2BK.horizontalHeader()
        header.setStretchLastSection(True)

# module BK2DXF

        self.callbackBK2DXFOpenMeshFile = functools.partial(self.getOpenFileName, "Open T3S-file", "2D T3 Scalar Mesh (ASCII SingleFrame) (*.t3s)", self.ui.lineEditBK2DXFInputMesh)
        QtCore.QObject.connect(self.ui.pushButtonBK2DXFInputMesh, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackBK2DXFOpenMeshFile)

        self.callbackBK2DXFOpenLineSetFile = functools.partial(self.getOpenFileName, "Open Line Set", "Line Sets (*.i2s *.i3s)", self.ui.lineEditBK2DXFInputLineSet)
        QtCore.QObject.connect(self.ui.pushButtonBK2DXFInputLineSet, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackBK2DXFOpenLineSetFile)
        

        self.callbackBK2DXFOutMesh = functools.partial(self.getSaveFileName, "Save Mesh As", "Drawing Interchange File (*.dxf)", self.ui.lineEditBK2DXFOutputMesh)
        QtCore.QObject.connect(self.ui.pushButtonBK2DXFOutputMesh, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackBK2DXFOutMesh)

        self.callbackBK2DXFOutLineSet = functools.partial(self.getSaveFileName, "Save Line Set As", "Drawing Interchange File (*.dxf)", self.ui.lineEditBK2DXFOutputLineSet)
        QtCore.QObject.connect(self.ui.pushButtonBK2DXFOutputLineSet, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackBK2DXFOutLineSet)

        self.callbackBK2DXFOutCheckMesh = functools.partial(self.setEnabled, self.ui.checkBoxBK2DXFOutputMesh, self.ui.pushButtonBK2DXFOutputMesh, self.ui.lineEditBK2DXFOutputMesh)
        QtCore.QObject.connect(self.ui.checkBoxBK2DXFOutputMesh, QtCore.SIGNAL("clicked()"), self.callbackBK2DXFOutCheckMesh)
        
        self.callbackBK2DXFOutCheckLineSet= functools.partial(self.setEnabled, self.ui.checkBoxBK2DXFOutputLineSet, self.ui.pushButtonBK2DXFOutputLineSet, self.ui.lineEditBK2DXFOutputLineSet)
        QtCore.QObject.connect(self.ui.checkBoxBK2DXFOutputLineSet, QtCore.SIGNAL("clicked()"), self.callbackBK2DXFOutCheckLineSet)
        
        self.typeDXFmesh = 1
        
        self.callback3DFace = functools.partial(self.setTypeDXFmesh, 1)
        QtCore.QObject.connect(self.ui.radioButtonBK2DXF3DFace, QtCore.SIGNAL("clicked()"), self.callback3DFace)
        
        self.callbackPolyline = functools.partial(self.setTypeDXFmesh, 2)
        QtCore.QObject.connect(self.ui.radioButtonBK2DXFPolyline, QtCore.SIGNAL("clicked()"), self.callbackPolyline)
        
        QtCore.QObject.connect(self.ui.pushButtonBK2DXFCreate, QtCore.SIGNAL("clicked()"), self.createBK2DXF)
        
# module Mesh

        self.callbackOpenProfilesFile = functools.partial(self.getOpenFileName, "Open Profiles File", "Line Sets (*.i3s)", self.ui.lineEditProfiles)
        QtCore.QObject.connect(self.ui.pushButtonProfiles, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackOpenProfilesFile)

        self.callbackOpenReachFile = functools.partial(self.getOpenFileName, "Open Reach File", "Line Sets (*.i2s *.i3s)", self.ui.lineEditReach)
        QtCore.QObject.connect(self.ui.pushButtonReach, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackOpenReachFile)

        self.callbackOpenLBLFile = functools.partial(self.getOpenFileName, "Open Left Breakline File", "Line Sets (*.i2s *.i3s)", self.ui.lineEditLBL)
        QtCore.QObject.connect(self.ui.pushButtonLBL, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackOpenLBLFile)

        self.callbackOpenRBLFile = functools.partial(self.getOpenFileName, "Open Right Breakline File", "Line Sets (*.i2s *.i3s)", self.ui.lineEditRBL)
        QtCore.QObject.connect(self.ui.pushButtonRBL, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackOpenRBLFile)

        self.callbackOpenLBOFile = functools.partial(self.getOpenFileName, "Open Left Boundary File", "Line Sets (*.i2s *.i3s)", self.ui.lineEditLBO)
        QtCore.QObject.connect(self.ui.pushButtonLBO, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackOpenLBOFile)

        self.callbackOpenRBOFile = functools.partial(self.getOpenFileName, "Open Right Boundary File", "Line Sets (*.i2s *.i3s)", self.ui.lineEditRBO)
        QtCore.QObject.connect(self.ui.pushButtonRBO, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackOpenRBOFile)

        self.callbackSaveMeshFile = functools.partial(self.getSaveFileName, "Save Mesh As", "2D T3 Mesh (*.t3s)", self.ui.lineEditMesh)
        QtCore.QObject.connect(self.ui.pushButtonMesh, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackSaveMeshFile)

        self.callbackSaveIPFile = functools.partial(self.getSaveFileName, "Save Interpolated Profiles As", "Line Sets (*.i3s)", self.ui.lineEditIP)
        QtCore.QObject.connect(self.ui.pushButtonIP, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackSaveIPFile)

        self.callbackSaveLEFile = functools.partial(self.getSaveFileName, "Save Left Edge As", "Line Sets (*.i3s)", self.ui.lineEditLE)
        QtCore.QObject.connect(self.ui.pushButtonLE, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackSaveLEFile)

        self.callbackSaveREFile = functools.partial(self.getSaveFileName, "Save Right Edge As", "Line Sets (*.i3s)", self.ui.lineEditRE)
        QtCore.QObject.connect(self.ui.pushButtonRE, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackSaveREFile)

        self.callbackSaveOLFile = functools.partial(self.getSaveFileName, "Save Outline As", "Line Sets (*.i3s)", self.ui.lineEditOL)
        QtCore.QObject.connect(self.ui.pushButtonOL, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackSaveOLFile)

        self.callbackSaveWSFile = functools.partial(self.getSaveFileName, "Save Workspace As", "EnSim WorkSpace File (*.ews)", self.ui.lineEditWS)
        QtCore.QObject.connect(self.ui.pushButtonWS, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackSaveWSFile)

        self.callbackLBL = functools.partial(self.setEnabledBL, self.ui.checkBoxLBL, self.ui.pushButtonLBL, self.ui.lineEditLBL, self.ui.spinBoxNNL)
        QtCore.QObject.connect(self.ui.checkBoxLBL, QtCore.SIGNAL("clicked()"), self.callbackLBL)

        self.callbackRBL = functools.partial(self.setEnabledBL, self.ui.checkBoxRBL, self.ui.pushButtonRBL, self.ui.lineEditRBL, self.ui.spinBoxNNR)
        QtCore.QObject.connect(self.ui.checkBoxRBL, QtCore.SIGNAL("clicked()"), self.callbackRBL)

        self.callbackLBO = functools.partial(self.setEnabled, self.ui.checkBoxLBO, self.ui.pushButtonLBO, self.ui.lineEditLBO)
        QtCore.QObject.connect(self.ui.checkBoxLBO, QtCore.SIGNAL("clicked()"), self.callbackLBO)

        self.callbackRBO = functools.partial(self.setEnabled, self.ui.checkBoxRBO, self.ui.pushButtonRBO, self.ui.lineEditRBO)
        QtCore.QObject.connect(self.ui.checkBoxRBO, QtCore.SIGNAL("clicked()"), self.callbackRBO)

        self.callbackMesh = functools.partial(self.setEnabled, self.ui.checkBoxMesh, self.ui.pushButtonMesh, self.ui.lineEditMesh)
        QtCore.QObject.connect(self.ui.checkBoxMesh, QtCore.SIGNAL("clicked()"), self.callbackMesh)

        self.callbackIP = functools.partial(self.setEnabled, self.ui.checkBoxIP, self.ui.pushButtonIP, self.ui.lineEditIP)
        QtCore.QObject.connect(self.ui.checkBoxIP, QtCore.SIGNAL("clicked()"), self.callbackIP)

        self.callbackLE = functools.partial(self.setEnabled, self.ui.checkBoxLE, self.ui.pushButtonLE, self.ui.lineEditLE)
        QtCore.QObject.connect(self.ui.checkBoxLE, QtCore.SIGNAL("clicked()"), self.callbackLE)

        self.callbackRE = functools.partial(self.setEnabled, self.ui.checkBoxRE, self.ui.pushButtonRE, self.ui.lineEditRE)
        QtCore.QObject.connect(self.ui.checkBoxRE, QtCore.SIGNAL("clicked()"), self.callbackRE)

        self.callbackOL = functools.partial(self.setEnabled, self.ui.checkBoxOL, self.ui.pushButtonOL, self.ui.lineEditOL)
        QtCore.QObject.connect(self.ui.checkBoxOL, QtCore.SIGNAL("clicked()"), self.callbackOL)

        self.callbackWS = functools.partial(self.setEnabled, self.ui.checkBoxWS, self.ui.pushButtonWS, self.ui.lineEditWS)
        QtCore.QObject.connect(self.ui.checkBoxWS, QtCore.SIGNAL("clicked()"), self.callbackWS)

        QtCore.QObject.connect(self.ui.pushButtonCreate, QtCore.SIGNAL("clicked()"), self.createMesh)
                
# module XML
        self.callbackOpenMeshFile = functools.partial(self.getOpenFileName, "Open T3S-file", "2D T3 Scalar Mesh (ASCII SingleFrame) (*.t3s)", self.ui.lineEditLandXMLInputMesh)
        QtCore.QObject.connect(self.ui.pushButtonLandXMLInputMesh, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackOpenMeshFile)

        self.callbackSaveXMLFile = functools.partial(self.getSaveFileName, "Save Mesh As", "LandXML (*.xml)", self.ui.lineEditLandXMLOutput)
        QtCore.QObject.connect(self.ui.pushButtonLandXMLOutput, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackSaveXMLFile)

        QtCore.QObject.connect(self.ui.pushButtonLandXMLCreate, QtCore.SIGNAL("clicked()"), self.createLandXML)

# module ScalarDXF

        self.callbackOpenScalarInputT3SMajor = functools.partial(self.getOpenFileName, "Open 2D T3 Scalar Mesh", "2D T3 Scalar Mesh (ASCIISingleFrame) (*.t3s)", self.ui.lineEditScalarDXFInputT3SMajor)
        QtCore.QObject.connect(self.ui.pushButtonScalarDXFInputT3SMajor, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackOpenScalarInputT3SMajor)

        self.callbackOpenScalarInputT3SMinor = functools.partial(self.getOpenFileName, "Open 2D T3 Scalar Mesh", "2D T3 Scalar Mesh (ASCIISingleFrame) (*.t3s)", self.ui.lineEditScalarDXFInputT3SMinor)
        QtCore.QObject.connect(self.ui.pushButtonScalarDXFInputT3SMinor, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackOpenScalarInputT3SMinor)

        self.callbackScalarScalar = functools.partial(self.getSaveFileName, "Save DXF-file As", "Drawing Interchange File (*.dxf)", self.ui.lineEditScalarDXFOutput)
        QtCore.QObject.connect(self.ui.pushButtonScalarDXFOutput, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackScalarScalar)
        
        self.scalarSymbol = 0
        
        self.callbackCircle = functools.partial(self.setSymbol, 0)
        QtCore.QObject.connect(self.ui.radioButtonScalarDXFCircle, QtCore.SIGNAL("clicked()"), self.callbackCircle)
        self.callbackCross = functools.partial(self.setSymbol, 1)
        QtCore.QObject.connect(self.ui.radioButtonScalarDXFCross, QtCore.SIGNAL("clicked()"), self.callbackCross)
        self.callbackCrosshairs = functools.partial(self.setSymbol, 2)
        QtCore.QObject.connect(self.ui.radioButtonScalarDXFCrosshairs, QtCore.SIGNAL("clicked()"), self.callbackCrosshairs)
        self.callbackNone = functools.partial(self.setSymbol, 3)
        QtCore.QObject.connect(self.ui.radioButtonScalarDXFNone, QtCore.SIGNAL("clicked()"), self.callbackNone)

        QtCore.QObject.connect(self.ui.pushButtonScalarDXFCreate, QtCore.SIGNAL("clicked()"), self.createScalarDXF)

# module VectorDXF

        self.callbackOpenVectorInput = functools.partial(self.getOpenFileName, "Open 2D T3 Vector Mesh", "2D T3 Vector Mesh (ASCIISingleFrame) (*.t3v)", self.ui.lineEditVectorDXFInput)
        QtCore.QObject.connect(self.ui.pushButtonVectorDXFInput, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackOpenVectorInput)
        
        self.callbackScalarVector = functools.partial(self.getSaveFileName, "Save DXF-file As", "Drawing Interchange File (*.dxf)", self.ui.lineEditVectorDXFOutput)
        QtCore.QObject.connect(self.ui.pushButtonVectorDXFOutput, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackScalarVector)    
        
        QtCore.QObject.connect(self.ui.pushButtonVectorDXFCreate, QtCore.SIGNAL("clicked()"), self.createVectorDXF)
        
# module CS

        self.callbackCSOpenMeshFile = functools.partial(self.getOpenFileName, "Open T3S-file", "2D T3 Scalar Mesh (ASCII SingleFrame) (*.t3s)", self.ui.lineEditCSInputMesh)
        QtCore.QObject.connect(self.ui.pushButtonCSInputMesh, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackCSOpenMeshFile)

        self.callbackCSOpenDefinition = functools.partial(self.getOpenFileName, "Open Control Sections Definition File", "Normal text file (*.txt)", self.ui.lineEditCSInputDefinition)
        QtCore.QObject.connect(self.ui.pushButtonCSInputDefinition, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackCSOpenDefinition)

        self.callbackCSOpenResults = functools.partial(self.getOpenFileName, "Open Control Sections Results File", "Normal text file (*.txt)", self.ui.lineEditCSInputResults)
        QtCore.QObject.connect(self.ui.pushButtonCSInputResults, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackCSOpenResults)

        self.callbacCSOutCheckFormatted = functools.partial(self.setEnabled, self.ui.checkBoxCSOutputFormatted, self.ui.pushButtonCSOutputFormatted, self.ui.lineEditCSOutputFormatted)
        QtCore.QObject.connect(self.ui.checkBoxCSOutputFormatted, QtCore.SIGNAL("clicked()"), self.callbacCSOutCheckFormatted)
        
        self.callbacCSOutFormatted = functools.partial(self.getSaveFileName, "Save Data File As", "Normal text file (*.txt)", self.ui.lineEditCSOutputFormatted)
        QtCore.QObject.connect(self.ui.pushButtonCSOutputFormatted, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbacCSOutFormatted)

        QtCore.QObject.connect(self.ui.checkBoxCSOutputCS, QtCore.SIGNAL("clicked()"), self.setEnabledCS)
        
        self.callbacCSOutCS = functools.partial(self.getSaveFileName, "Save Control Sections As", "Drawing Interchange File (*.dxf)", self.ui.lineEditCSOutputCS)
        QtCore.QObject.connect(self.ui.pushButtonCSOutputCS, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbacCSOutCS)

        QtCore.QObject.connect(self.ui.pushButtonCSCreate, QtCore.SIGNAL("clicked()"), self.createCS)
        
# module 2DM

        self.callbackOpen2dmInput = functools.partial(self.getOpenFileName, "Open 2D Mesh File", "SMS 2d Mesh File (*.2dm)", self.ui.lineEdit2dmInput)
        QtCore.QObject.connect(self.ui.pushButton2dmInput, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackOpen2dmInput)

        self.callbackOpen2dmInputData = functools.partial(self.getOpenFileName, "Open Dataset File", "ASCII Dataset Files (*.dat)", self.ui.lineEdit2dmInputData)
        QtCore.QObject.connect(self.ui.pushButton2dmInputData, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackOpen2dmInputData)

        self.callback2dmImpermeable = functools.partial(self.setEnabled, self.ui.checkBox2dmImpermeable, self.ui.spinBox2dmImpermeable, self.ui.spinBox2dmImpermeable)
        QtCore.QObject.connect(self.ui.checkBox2dmImpermeable, QtCore.SIGNAL("clicked()"), self.callback2dmImpermeable)

        
        self.callback2dmBottom = functools.partial(self.setEnabled, self.ui.checkBox2dmBottom, self.ui.pushButton2dmBottom, self.ui.lineEdit2dmBottom)
        QtCore.QObject.connect(self.ui.checkBox2dmBottom, QtCore.SIGNAL("clicked()"), self.callback2dmBottom)

        self.callback2dmBottomFriction = functools.partial(self.setEnabled, self.ui.checkBox2dmBottomFriction, self.ui.pushButton2dmBottomFriction, self.ui.lineEdit2dmBottomFriction)
        QtCore.QObject.connect(self.ui.checkBox2dmBottomFriction, QtCore.SIGNAL("clicked()"), self.callback2dmBottomFriction)

        self.callback2dmWaterSurface = functools.partial(self.setEnabled, self.ui.checkBox2dmWaterSurface, self.ui.pushButton2dmWaterSurface, self.ui.lineEdit2dmWaterSurface)
        QtCore.QObject.connect(self.ui.checkBox2dmWaterSurface, QtCore.SIGNAL("clicked()"), self.callback2dmWaterSurface)

        self.callback2dmWaterDepth = functools.partial(self.setEnabled, self.ui.checkBox2dmWaterDepth, self.ui.pushButton2dmWaterDepth, self.ui.lineEdit2dmWaterDepth)
        QtCore.QObject.connect(self.ui.checkBox2dmWaterDepth, QtCore.SIGNAL("clicked()"), self.callback2dmWaterDepth)

        self.callback2dmCulvertHeight = functools.partial(self.setEnabled, self.ui.checkBox2dmCulvertHeight, self.ui.pushButton2dmCulvertHeight, self.ui.lineEdit2dmCulvertHeight)
        QtCore.QObject.connect(self.ui.checkBox2dmCulvertHeight, QtCore.SIGNAL("clicked()"), self.callback2dmCulvertHeight)

        self.callback2dmNS1 = functools.partial(self.setEnabled, self.ui.checkBox2dmNS1, self.ui.pushButton2dmNS1, self.ui.lineEdit2dmNS1)
        QtCore.QObject.connect(self.ui.checkBox2dmNS1, QtCore.SIGNAL("clicked()"), self.callback2dmNS1)

        self.callback2dmNS2 = functools.partial(self.setEnabled, self.ui.checkBox2dmNS2, self.ui.pushButton2dmNS2, self.ui.lineEdit2dmNS2)
        QtCore.QObject.connect(self.ui.checkBox2dmNS2, QtCore.SIGNAL("clicked()"), self.callback2dmNS2)

        self.callback2dmNS3 = functools.partial(self.setEnabled, self.ui.checkBox2dmNS3, self.ui.pushButton2dmNS3, self.ui.lineEdit2dmNS3)
        QtCore.QObject.connect(self.ui.checkBox2dmNS3, QtCore.SIGNAL("clicked()"), self.callback2dmNS3)

        self.callback2dmNS4 = functools.partial(self.setEnabled, self.ui.checkBox2dmNS4, self.ui.pushButton2dmNS4, self.ui.lineEdit2dmNS4)
        QtCore.QObject.connect(self.ui.checkBox2dmNS4, QtCore.SIGNAL("clicked()"), self.callback2dmNS4)

        self.callback2dmNS5 = functools.partial(self.setEnabled, self.ui.checkBox2dmNS5, self.ui.pushButton2dmNS5, self.ui.lineEdit2dmNS5)
        QtCore.QObject.connect(self.ui.checkBox2dmNS5, QtCore.SIGNAL("clicked()"), self.callback2dmNS5)

        self.callback2dmNS6 = functools.partial(self.setEnabled, self.ui.checkBox2dmNS6, self.ui.pushButton2dmNS6, self.ui.lineEdit2dmNS6)
        QtCore.QObject.connect(self.ui.checkBox2dmNS6, QtCore.SIGNAL("clicked()"), self.callback2dmNS6)

        self.callback2dmNS7 = functools.partial(self.setEnabled, self.ui.checkBox2dmNS7, self.ui.pushButton2dmNS7, self.ui.lineEdit2dmNS7)
        QtCore.QObject.connect(self.ui.checkBox2dmNS7, QtCore.SIGNAL("clicked()"), self.callback2dmNS7)

        self.callbackSave2dmBottom = functools.partial(self.getSaveFileName, "Save Bottom As", "2D T3 Mesh (*.t3s)", self.ui.lineEdit2dmBottom)
        QtCore.QObject.connect(self.ui.pushButton2dmBottom, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackSave2dmBottom)

        self.callbackSave2dmBottomFriction = functools.partial(self.getSaveFileName, "Save Bottom Friction As", "2D T3 Mesh (*.t3s)", self.ui.lineEdit2dmBottomFriction)
        QtCore.QObject.connect(self.ui.pushButton2dmBottomFriction, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackSave2dmBottomFriction)

        self.callbackSave2dmWaterSurface = functools.partial(self.getSaveFileName, "Save Water Surface As", "2D T3 Mesh (*.t3s)", self.ui.lineEdit2dmWaterSurface)
        QtCore.QObject.connect(self.ui.pushButton2dmWaterSurface, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackSave2dmWaterSurface)

        self.callbackSave2dmWaterDepth = functools.partial(self.getSaveFileName, "Save Water Depth As", "2D T3 Mesh (*.t3s)", self.ui.lineEdit2dmWaterDepth)
        QtCore.QObject.connect(self.ui.pushButton2dmWaterDepth, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackSave2dmWaterDepth)
        
        self.callbackSave2dmCulvertHeight = functools.partial(self.getSaveFileName, "Save Culvert Height As", "Point Set (*.xyz)", self.ui.lineEdit2dmCulvertHeight)
        QtCore.QObject.connect(self.ui.pushButton2dmCulvertHeight, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackSave2dmCulvertHeight)

        self.callbackSave2dmNS1 = functools.partial(self.getSaveFileName, "Save Node String As", "Line Sets (*.i2s)", self.ui.lineEdit2dmNS1)
        QtCore.QObject.connect(self.ui.pushButton2dmNS1, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackSave2dmNS1)

        self.callbackSave2dmNS2 = functools.partial(self.getSaveFileName, "Save Node String As", "Line Sets (*.i2s)", self.ui.lineEdit2dmNS2)
        QtCore.QObject.connect(self.ui.pushButton2dmNS2, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackSave2dmNS2)

        self.callbackSave2dmNS3 = functools.partial(self.getSaveFileName, "Save Node String As", "Line Sets (*.i2s)", self.ui.lineEdit2dmNS3)
        QtCore.QObject.connect(self.ui.pushButton2dmNS3, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackSave2dmNS3)

        self.callbackSave2dmNS4 = functools.partial(self.getSaveFileName, "Save Node String As", "Line Sets (*.i2s)", self.ui.lineEdit2dmNS4)
        QtCore.QObject.connect(self.ui.pushButton2dmNS4, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackSave2dmNS4)

        self.callbackSave2dmNS5 = functools.partial(self.getSaveFileName, "Save Node String As", "Line Sets (*.i2s)", self.ui.lineEdit2dmNS5)
        QtCore.QObject.connect(self.ui.pushButton2dmNS5, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackSave2dmNS5)

        self.callbackSave2dmNS6 = functools.partial(self.getSaveFileName, "Save Node String As", "Line Sets (*.i2s)", self.ui.lineEdit2dmNS6)
        QtCore.QObject.connect(self.ui.pushButton2dmNS6, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackSave2dmNS6)

        self.callbackSave2dmNS7 = functools.partial(self.getSaveFileName, "Save Node String As", "Line Sets (*.i2s)", self.ui.lineEdit2dmNS7)
        QtCore.QObject.connect(self.ui.pushButton2dmNS7, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackSave2dmNS7)

        QtCore.QObject.connect(self.ui.pushButton2dmConvert, QtCore.SIGNAL("clicked()"), self.create2DM2BK)

# module Cont2DXF

        self.callbackCont2DXFOpenMeshFile = functools.partial(self.getOpenFileName, "Open T3S-file", "2D T3 Scalar Mesh (ASCII SingleFrame) (*.t3s)", self.ui.lineEditCont2DXFInput)
        QtCore.QObject.connect(self.ui.pushButtonCont2DXFInput, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackCont2DXFOpenMeshFile)

        QtCore.QObject.connect(self.ui.pushButtonCont2DXFAdd, QtCore.SIGNAL(_fromUtf8("clicked()")), self.addLevel)
        QtCore.QObject.connect(self.ui.pushButtonCont2DXFDelete, QtCore.SIGNAL(_fromUtf8("clicked()")), self.deleteLevel)
        QtCore.QObject.connect(self.ui.pushButtonCont2DXFColour, QtCore.SIGNAL(_fromUtf8("clicked()")), self.setColour)
        QtCore.QObject.connect(self.ui.pushButtonCont2DXFLoad, QtCore.SIGNAL(_fromUtf8("clicked()")), self.loadLegend)
        QtCore.QObject.connect(self.ui.pushButtonCont2DXFSave, QtCore.SIGNAL(_fromUtf8("clicked()")), self.saveLegend)
        QtCore.QObject.connect(self.ui.pushButtonCont2DXFDefault, QtCore.SIGNAL(_fromUtf8("clicked()")), self.defaultLegend)
        
        self.callbackCont2DXFSolid = functools.partial(self.setEnabled, self.ui.checkBoxCont2DXFOutputSolid, self.ui.pushButtonCont2DXFOutputSolid, self.ui.lineEditCont2DXFOutputSolid)
        QtCore.QObject.connect(self.ui.checkBoxCont2DXFOutputSolid, QtCore.SIGNAL("clicked()"), self.callbackCont2DXFSolid)
 
        self.callbackCont2DXFLine = functools.partial(self.setEnabled, self.ui.checkBoxCont2DXFOutputLine, self.ui.pushButtonCont2DXFOutputLine, self.ui.lineEditCont2DXFOutputLine)
        QtCore.QObject.connect(self.ui.checkBoxCont2DXFOutputLine, QtCore.SIGNAL("clicked()"), self.callbackCont2DXFLine)
        
        legends = ["water depth", "water surface difference", "flow velocity", "bottom shear stress"]
        self.ui.comboBoxCont2DXF.addItems(legends)
        
        QtCore.QObject.connect(self.ui.checkBoxCont2DXFOutputLegend, QtCore.SIGNAL("clicked()"), self.setEnabledLegend)
        
        self.callbackCont2DXFOut = functools.partial(self.getSaveFileName, "Save Control Sections As", "Drawing Interchange File (*.dxf)", self.ui.lineEditCont2DXFOutputSolid)
        QtCore.QObject.connect(self.ui.pushButtonCont2DXFOutputSolid, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackCont2DXFOut)

        QtCore.QObject.connect(self.ui.pushButtonCont2DXFCreate, QtCore.SIGNAL("clicked()"), self.createCont2DXF)

        header = self.ui.tableWidgetCont2DXF.horizontalHeader()
        header.setStretchLastSection(True)

# module Tube

        self.callbackTubeOpenMeshFile = functools.partial(self.getOpenFileName, "Open T3S-file", "2D T3 Scalar Mesh (ASCII SingleFrame) (*.t3s)", self.ui.lineEditTubeInputMesh)
        QtCore.QObject.connect(self.ui.pushButtonTubeInputMesh, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackTubeOpenMeshFile)
        
        self.callbackTubeOpenLineSet = functools.partial(self.getOpenFileName, "Open I2S-file", "Line Sets (*.i2s)", self.ui.lineEditTubeInputLineSet)
        QtCore.QObject.connect(self.ui.pushButtonTubeInputLineSet, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackTubeOpenLineSet)
        
        self.callbackTubeOutput = functools.partial(self.getSaveFileName, "Save textfile As", "Normal text file (*.txt)", self.ui.lineEditTubeOutput)
        QtCore.QObject.connect(self.ui.pushButtonTubeOutput, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackTubeOutput)
        
        QtCore.QObject.connect(self.ui.pushButtonTubeCreate, QtCore.SIGNAL("clicked()"), self.createTube)


#        self.setDXF2BK()
#        self.setCont2DXF()
#        self.setHEC2DXF()
#        self.setProfiles()
        self.setProfilesDXF()
        self.initialize()

        
    def setType(self):
        self.calcDischarge()
        self.updateUi()
        
    def setSymbol(self, i):
        self.scalarSymbol = i
        
    def setTypeDXFmesh(self, i):
        self.typeDXFmesh = i
        
    def createLandXML(self):
        nodes, mesh = fh.readT3S(self.ui.lineEditLandXMLInputMesh.text())

        try:
            fh.writeXML(nodes, mesh, self.ui.lineEditLandXMLSurfaceName.text(), self.ui.lineEditLandXMLOutput.text())
            info = "LandXML surface created with:\n"
            info += " - {0} nodes\n - {1} elements".format(len(nodes), len(mesh))            
            QMessageBox.information(self, "LandXML", info)
        except:
            QMessageBox.critical(self, "Error", "Not able to write LandXML!")
            return

    def create2DM2BK(self):
    
#        try:
        SMS_elements, \
            SMS_nodes,\
            SMS_strings,\
            SMS_materials,\
            SMS_bc_nodes,\
            SMS_bc_strings_1,\
            SMS_bc_strings_2,\
            SMS_bc_strings_3,\
            SMS_bc_strings_4,\
            SMS_bc_strings_5,\
            SMS_bc_strings_6,\
            SMS_bc_strings_7 = fh.read2DM(self.ui.lineEdit2dmInput.text())
#        except:
#            QMessageBox.critical(self, "Error", "Not able to load file!\nCheck filename or content!")
#            return

        # BK_materials = {BK_node_id: strickler's value}
        BK_materials = {}
        
        # MAP_node_id = {SMS_node_id: BK_node_id}
        MAP_node_id = {}
        
        # BK_nodes = {BK_node_id: [x, y, z]}
        BK_nodes = {}        
        
        # BK_elements = {element_id: [BK_node_id, BK_node_id, BK_node_id (, BK_node_id), SMS_material_id]}
        BK_elements = {}
        
        # map BK nodes to SMS nodes
        i = 0
        for key in SMS_nodes:
            i += 1
            BK_nodes[i] = SMS_nodes[key]
            MAP_node_id[key] = i

        # convert SMS mesh to BK mesh
        i = 0
        impermeableMaterialID = self.ui.spinBox2dmImpermeable.value()
        material_added = False

        for key in SMS_elements:
            if len(SMS_elements[key]) == 4:
                node_0 = SMS_elements[key][0]
                node_1 = SMS_elements[key][1]
                node_2 = SMS_elements[key][2]
                material = SMS_elements[key][3]
                
                if material_added is False:
                    if material not in SMS_materials:
                        SMS_materials[material] = 0.0
                        material_added = True
                    
                BK_materials[MAP_node_id[node_0]] = SMS_materials[material]
                BK_materials[MAP_node_id[node_1]] = SMS_materials[material]
                BK_materials[MAP_node_id[node_2]] = SMS_materials[material]
                
                if self.ui.checkBox2dmImpermeable.isChecked():
                    if material != impermeableMaterialID:
                        i += 1
                        BK_elements[i] = [MAP_node_id[node_0], MAP_node_id[node_1], MAP_node_id[node_2]]
                else:
                    i += 1
                    BK_elements[i] = [MAP_node_id[node_0], MAP_node_id[node_1], MAP_node_id[node_2]]
                        
            elif len(SMS_elements[key]) == 5:
                node_0 = SMS_elements[key][0]
                node_1 = SMS_elements[key][1]
                node_2 = SMS_elements[key][2]
                node_3 = SMS_elements[key][3]
                material = SMS_elements[key][4]
                
                if material_added is False:
                    if material not in SMS_materials:
                        SMS_materials[material] = 0.0
                        material_added = True
                        
                BK_materials[MAP_node_id[node_0]] = SMS_materials[material]
                BK_materials[MAP_node_id[node_1]] = SMS_materials[material]
                BK_materials[MAP_node_id[node_2]] = SMS_materials[material]
                BK_materials[MAP_node_id[node_3]] = SMS_materials[material]
                
                if self.ui.checkBox2dmImpermeable.isChecked():
                    if material != impermeableMaterialID:
                        i += 1
                        BK_elements[i] = [MAP_node_id[node_0], MAP_node_id[node_1], MAP_node_id[node_2]]
                        i += 1
                        BK_elements[i] = [MAP_node_id[node_0], MAP_node_id[node_2], MAP_node_id[node_3]]
                else:
                    i += 1
                    BK_elements[i] = [MAP_node_id[node_0], MAP_node_id[node_1], MAP_node_id[node_2]]
                    i += 1
                    BK_elements[i] = [MAP_node_id[node_0], MAP_node_id[node_2], MAP_node_id[node_3]]
                        
        def getStrings(allstrings, strings):
            i = 1
            profiles = {}
            bk_profiles = {}
            for key in strings:
                profiles[i] = allstrings[key]
                bk_profiles[i] = []
                i += 1
            for pID in profiles:
                for nID in profiles[pID]:
                    bk_profiles[pID].append(MAP_node_id[nID])

            return bk_profiles
        
        info = ""
    
        if self.ui.checkBox2dmBottom.isChecked():
            try:
                fh.writeT3S(BK_nodes, BK_elements, self.ui.lineEdit2dmBottom.text())
                info += " - Bottom mesh created with {0} nodes and {1} elements.\n".format(len(BK_nodes), len(BK_elements)) 
            except:
                info += " - ERROR: Not able to write bottom mesh!\n"

        if self.ui.lineEdit2dmInputData.text() != "":
            SMS_wsf = fh.readDAT(self.ui.lineEdit2dmInputData.text())
            BK_nodes_wsf = {}
            BK_nodes_dpth = {}
            for key in SMS_nodes:
                wsf = 0.0
                if SMS_wsf[MAP_node_id[key]] <= 0.000001:
                    wsf = SMS_nodes[key][2]
                else:
                    wsf = SMS_wsf[MAP_node_id[key]]
                BK_nodes_wsf[key] = [SMS_nodes[key][0], SMS_nodes[key][1], wsf]    
                BK_nodes_dpth[key] = [SMS_nodes[key][0], SMS_nodes[key][1], wsf-SMS_nodes[key][2]] 
            try:
                fh.writeT3S(BK_nodes_wsf, BK_elements, self.ui.lineEdit2dmWaterSurface.text())
                info += " - Water surface mesh created with {0} nodes and {1} elements.\n".format(len(BK_nodes_wsf), len(BK_elements)) 
            except:
                info += " - ERROR: Not able to write water surface mesh!\n"
  
            try:
                fh.writeT3S(BK_nodes_dpth, BK_elements, self.ui.lineEdit2dmWaterDepth.text())
                info += " - Water depth mesh created with {0} nodes and {1} elements.\n".format(len(BK_nodes_dpth), len(BK_elements)) 
            except:
                info += " - ERROR: Not able to write water depth mesh!\n"
                  
        if self.ui.checkBox2dmBottomFriction.isChecked():
            BK_nodes_mat = {}
            for key in BK_nodes:
                if key in BK_materials:
                    BK_nodes_mat[key] = [BK_nodes[key][0], BK_nodes[key][1], BK_materials[key]]
                else:
                    BK_nodes_mat[key] = [BK_nodes[key][0], BK_nodes[key][1], 0.0]                    
            try:
                fh.writeT3S(BK_nodes_mat, BK_elements, self.ui.lineEdit2dmBottomFriction.text())
                info += " - Bottom friction mesh created with {0} nodes and {1} elements.\n".format(len(BK_nodes_mat), len(BK_elements)) 
            except:
                info += " - ERROR: Not able to write bottom friction mesh!\n"

        if self.ui.checkBox2dmCulvertHeight.isChecked():
            # convert SMS boundary condition nodes to BK points
            BK_bcNodes = {}
            for key in SMS_bc_nodes:
                height = SMS_bc_nodes[key] - SMS_nodes[key][2]
                BK_bcNodes[key] = [SMS_nodes[key][0], SMS_nodes[key][1], height]

            try:
                fh.writeXYZ(BK_bcNodes, self.ui.lineEdit2dmCulvertHeight.text())
                info += " - Culverts created with {0} nodes.\n".format(len(BK_bcNodes))
            except:
                info += " - ERROR: Not able to write culvert nodes!\n"
                                                                                        
        if self.ui.checkBox2dmNS1.isChecked():
            profiles = getStrings(SMS_strings, SMS_bc_strings_1)
            try:
                fh.writeI2S(BK_nodes, profiles, self.ui.lineEdit2dmNS1.text())
                info += " - Node string 1 created with {0} strings.\n".format(len(profiles)) 
            except:
                info += " - ERROR: Not able to write node string 1!\n"

        if self.ui.checkBox2dmNS2.isChecked():
            profiles = getStrings(SMS_strings, SMS_bc_strings_2)
            try:
                fh.writeI2S(BK_nodes, profiles, self.ui.lineEdit2dmNS2.text())
                info += " - Node string 2 created with {0} strings.\n".format(len(profiles)) 
            except:
                info += " - ERROR: Not able to write node string 2!\n"                               

        if self.ui.checkBox2dmNS3.isChecked():
            profiles = getStrings(SMS_strings, SMS_bc_strings_3)
            try:
                fh.writeI2S(BK_nodes, profiles, self.ui.lineEdit2dmNS3.text())
                info += " - Node string 3 created with {0} strings.\n".format(len(profiles)) 
            except:
                info += " - ERROR: Not able to write node string 3!\n"
                
        if self.ui.checkBox2dmNS4.isChecked():
            profiles = getStrings(SMS_strings, SMS_bc_strings_4)
            try:
                fh.writeI2S(BK_nodes, profiles, self.ui.lineEdit2dmNS4.text())
                info += " - Node string 4 created with {0} strings.\n".format(len(profiles)) 
            except:
                info += " - ERROR: Not able to write node string 4!\n"

        if self.ui.checkBox2dmNS5.isChecked():
            profiles = getStrings(SMS_strings, SMS_bc_strings_5)
            try:
                fh.writeI2S(BK_nodes, profiles, self.ui.lineEdit2dmNS5.text())
                info += " - Node string 5 created with {0} strings.\n".format(len(profiles)) 
            except:
                info += " - ERROR: Not able to write node string 5!\n"
                
        if self.ui.checkBox2dmNS6.isChecked():
            profiles = getStrings(SMS_strings, SMS_bc_strings_6)
            try:
                fh.writeI2S(BK_nodes, profiles, self.ui.lineEdit2dmNS6.text())
                info += " - Node string 6 created with {0} strings.\n".format(len(profiles)) 
            except:
                info += " - ERROR: Not able to write node string 6!\n"
                         
        if self.ui.checkBox2dmNS7.isChecked():
            profiles = getStrings(SMS_strings, SMS_bc_strings_7)
            try:
                fh.writeI2S(BK_nodes, profiles, self.ui.lineEdit2dmNS7.text())
                info += " - Node string 7 created with {0} strings.\n".format(len(profiles)) 
            except:
                info += " - ERROR: Not able to write node string 7!\n"

        QMessageBox.information(self, "Module 2DM2BK", info)
        
    def createDXF2BK(self):
        info = ""
        rows = self.ui.tableWidgetDXF2BK.rowCount()
        if rows > 0:
            for row in range(rows):
                combobox = self.ui.tableWidgetDXF2BK.cellWidget(row, 0)

                filename = self.ui.tableWidgetDXF2BK.item(row, 1).text()
                layer = combobox.itemText(combobox.currentIndex())
                type = filename.split(".")[-1]

                nodes = {}
                strings = {}

                if type == "i2s":
                    try:
                        nodes, strings = fh.readDXF(self.dxf, layer)
                        fh.writeI2S(nodes, strings, filename)
                        info += " - {0} object(s) from type *.i2s converted to file \n\t{1}\n".format(len(strings), filename)
                    except Exception, e:
                        QMessageBox.critical(self, "Module DXF2BK", 'Type *.i2s: ' + str(e))
                elif type == "i3s":
                    try:
                        nodes, strings = fh.readDXF(self.dxf, layer)
                        fh.writeI3S(nodes, strings, filename)
                        info += " - {0} object(s) from type *.i3s converted to file \n\t{1}\n".format(len(strings), filename)
                    except Exception, e:
                        QMessageBox.critical(self, "Module DXF2BK", 'Type *.i3s: ' + str(e))
                elif type == "xyz":
                    try:
                        nodes, strings = fh.readDXF(self.dxf, layer)
                        fh.writeXYZ(nodes, filename)
                        info += " - {0} object(s) from type *.xyz converted to file \n\t{1}\n".format(len(nodes), filename)
                    except Exception, e:
                        QMessageBox.critical(self, "Module DXF2BK", 'Type *.xyz: ' + str(e))
                else:
                    continue                
        QMessageBox.information(self, "Module DXF2BK", info)
    
    def getLevels(self):
        levels = []
        colHEX_RGB = []
        colHEX_BGR = []
        colRGB = []
        colBGR = []
        level_ok = True
        col_ok = True
        
        rows = self.ui.tableWidgetCont2DXF.rowCount()
        
        if rows > 0:
            for row in range(rows):
                try:
                    levels.append(float(self.ui.tableWidgetCont2DXF.item(row, 0).text()))
                    float(self.ui.tableWidgetCont2DXF.item(row, 1).text())
                except:
                    return [], False, [], [], True
                try:
                    col = str(self.ui.tableWidgetCont2DXF.item(row, 2).text()).split(",")

                    colFloat_RGB = (float(col[0])/255.0, float(col[1])/255.0, float(col[2])/255.0)
                    colFloat_BGR = (float(col[2])/255.0, float(col[1])/255.0, float(col[0])/255.0)
                    colRGB.append([float(col[0]), float(col[1]), float(col[2])])
                    colBGR.append([float(col[2]), float(col[1]), float(col[0])])
#                    colHex = colors.rgb2hex(colFloat_RGB)
                    colHEX_RGB.append(colors.rgb2hex(colFloat_RGB))
                    colHEX_BGR.append(colors.rgb2hex(colFloat_BGR))
                except:
                    return [], True, [], [], False
         
            # check if level ranges are in ascending order
            for row in range(rows-1):
                
                level_ai = round(float(self.ui.tableWidgetCont2DXF.item(row, 0).text()), 6)
                level_aj = round(float(self.ui.tableWidgetCont2DXF.item(row, 1).text()), 6)
                level_bi = round(float(self.ui.tableWidgetCont2DXF.item(row+1, 0).text()), 6)
                
                if level_aj != level_bi:
                    level_ok = False
                if level_aj <= level_ai:
                    level_ok = False
                    
            level_1i = float(self.ui.tableWidgetCont2DXF.item(0, 0).text())
            level_1j = float(self.ui.tableWidgetCont2DXF.item(0, 1).text())
            
            if level_1j <= level_1i:
                level_ok = False

            level_Ni = float(self.ui.tableWidgetCont2DXF.item(rows-1, 0).text())
            level_Nj = float(self.ui.tableWidgetCont2DXF.item(rows-1, 1).text())
            
            if level_Nj <= level_Ni:
                level_ok = False
            
            levels.append(float(self.ui.tableWidgetCont2DXF.item(rows-1, 1).text()))
            
        return levels, level_ok, colHEX_RGB, colRGB, colHEX_BGR, colBGR, col_ok
    
    def createCont2DXF(self):
        
        def hole(polycoord):
            """Polygon is a hole, if the vertices are defined clockwise."""
            
            ring = LinearRing(polycoord)
            if ring.is_ccw is False:
                return True
            else:
                return False
                
        def getHole(polycoord):
            """Create random point inside polygon."""
            
            polygon = Polygon(polycoord)
            bounds = polygon.bounds
            
            while True:
                randX = uniform(bounds[0], bounds[2])
                randY = uniform(bounds[1], bounds[3])
                randPoint = Point(randX,randY)

                if randPoint.within(polygon):
                    break
            return [randX, randY]
        
        info = ""

        # get levels and colours
        try:
            levels, levels_ok, coloursHEX_RGB, coloursRGB, coloursHEX_BGR, coloursBGR, col_ok = self.getLevels()
        except:
            QMessageBox.critical(self, "Error", "Check level inputs!")
            return
        
        if not levels_ok:
            QMessageBox.critical(self, "Error", "Check level ranges!")
            return
        if not col_ok:
            QMessageBox.critical(self, "Error", "Check colours!")
            return
        
        # read input meshes
        try:
            x, y, z, triangles = fh.readT3STriangulation(self.ui.lineEditCont2DXFInput.text())
            triang = tri.Triangulation(x, y, triangles)
        except:
            QMessageBox.critical(self, "Error", "Not able to load mesh file!\nCheck filename or content!")
            return

        contours = []
        
        # loop over contour levels
        for level in range(len(levels)-1):

            # create contour plot with matplotlib.pyplot.tricontourf
            cs = plt.tricontourf(triang, z, levels=[levels[level], levels[level+1]], colors=coloursHEX_RGB[level])

            # instantiate the dictionary for the triangulation
            geometry = {}
            geometry["vertices"] = []
            geometry["segments"] = []
            geometry["holes"] = []

            # nodecounter for level
            nodeID = 0
            
            # loop over matplotlib collection
            for cc in cs.collections:
                for pp in cc.get_paths():
                    
                    # paths to polygons
                    polys = pp.to_polygons()

                    eps = 0.000001
                    polys_ = []
                    
                    # loop over polygons
                    for pID in range(len(polys)):
                        poly = polys[pID]
                        nodeIDs = []
                        
                        if len(poly) > 1:
                            
                            # add random point if polygon defines a hole
                            if hole(poly):
                                geometry["holes"].append(getHole(poly))
                            
                            # nodecounter for polygon
                            counter = 0
                            
                            # add vertices and segments
                            # triangle crashes, if vertices are too close to each other,
                            # which would result in zero area triangles
                            for vID in range(len(poly)):
                                vert = np.array(poly[vID])
                                vert = vert.reshape((1,2))
                                
                                # first vertice in polygon
                                if len(geometry["vertices"]) == 0:
                                    geometry["vertices"] = np.array(vert)
                                    nodeIDs.append(nodeID)
                                    counter += 1
                                    nodeID += 1
                                else:
                                    # subtract actual vertice from array of vertices
                                    vertices_ = geometry["vertices"] - vert
                                    
                                    # calculate the length of the vectors
                                    norm = np.linalg.norm(vertices_, axis = 1)
                                    
                                    # get smallest vector norm
                                    min_norm = norm.min()

                                    # if smallest vector norm is greater than a defined value, apply vertice
                                    if min_norm > eps:
                                        counter += 1
                                        geometry["vertices"] = np.concatenate((geometry["vertices"], vert))
                                        nodeIDs.append(nodeID)
                                        nodeID += 1
                                    # else get index of smallest vector norm and apply node-ID
                                    else:
                                        min_index = np.argmin(norm)
                                        # print "comparison: ", min_index, geometry["vertices"][min_index], vID, poly[vID]
                                        nodeIDs.append(min_index)

                            # close polygon by adding id from first vertice
                            nodeIDs.append(nodeID-counter)

                        polys_.append(nodeIDs)

                    # create segments
                    for pID in range(len(polys_)):
                        for nID in range(len(polys_[pID])-1):
                            geometry["segments"].append([polys_[pID][nID], polys_[pID][nID+1]])

            # delete holes from dictionary, if no holes exist
            if len(geometry["holes"]) == 0:
                del geometry["holes"]
            if len(geometry["vertices"]) >= 3:
                t = triangle.triangulate(geometry, 'p')
                contours.append(t)
            else:
                contours.append(None)
                
# plot triangulation using matplotlib
#            plt.figure(1)
#            ax1 = plt.subplot(111, aspect='equal')
#            triangle.plot.plot(ax1, **t)
#            plt.show()

        xLeg = max(x)
        yLeg = min(y)
        origin = (xLeg, yLeg)
        
        title = self.ui.lineEditCont2DXFOutputLegendTitle.text()
        subtitle = self.ui.lineEditCont2DXFOutputLegendSubtitle.text()

        if self.ui.checkBoxCont2DXFOutputSolid.isChecked():
            try:
                fh.writeContSolidDXF(
                    self.ui.lineEditCont2DXFOutputSolid.text(), 
                    contours,
                    levels,
                    coloursRGB, 
                    self.ui.lineEditCont2DXFOutputLayer.text(),
                    self.ui.checkBoxCont2DXFOutputLegend.isChecked(),
                    title,
                    subtitle,
                    origin,
                    self.ui.lineEditCont2DXFOutputLegendSeparator.text(),
                    self.ui.checkBoxCont2DXFOutputLegendReverse.isChecked()
                )
                info += "Contours:\n"
                info += " - Contours created with {0} levels.\n".format(len(levels)) 
                if self.ui.checkBoxCont2DXFOutputLegend.isChecked():
                    info += " - Legend created.\n"
                info += " - DXF written to {0}.\n\n".format(self.ui.lineEditCont2DXFOutputSolid.text())
            except:
                info += " - ERROR: Not able to write contour to dxf!\n"
            
        if self.ui.checkBoxCont2DXFOutputLine.isChecked():
            try:
                fh.writeContIsoLineDXF(
                self.ui.lineEditCont2DXFOutputLine.text(), 
                contours, 
                levels,
                coloursRGB, 
                self.ui.lineEditCont2DXFOutputLayer.text(),
                self.ui.checkBoxCont2DXFOutputLegend.isChecked(),
                title,
                subtitle,
                origin,
                self.ui.lineEditCont2DXFOutputLegendSeparator.text(),
                self.ui.checkBoxCont2DXFOutputLegendReverse.isChecked()
                )
                info += "Isolines:\n"
                info += " - Isolines created with {0} levels.\n".format(len(levels))
                if self.ui.checkBoxCont2DXFOutputLegend.isChecked():
                    info += " - Legend created.\n"
                info += " - DXF written to {0}.\n".format(self.ui.lineEditCont2DXFOutputLine.text())
            except:
                info += " - ERROR: Not able to write isolines to dxf!\n"            

        QMessageBox.information(self, "Module Cont2DXF", info)

    def getSaveLayerName(self):
        row = self.ui.tableWidgetDXF2BK.currentRow()
        filetype = ("2D Line Set (*.i2s);;3D Line Set (*.i3s);;Point Set (*.xyz)")
        filename = QFileDialog.getSaveFileName(self, "Save Layer As", self.directory, filetype)

        if filename != "":
            item = QtGui.QTableWidgetItem()
            item.setText(filename)
            self.ui.tableWidgetDXF2BK.setItem(row, 1, item)
        
    def addLayer(self):
        dropdownLayer = QtGui.QComboBox(self)
        
        rows = self.ui.tableWidgetDXF2BK.rowCount()

        self.ui.tableWidgetDXF2BK.insertRow(rows)
        self.ui.tableWidgetDXF2BK.setCellWidget(rows, 0, dropdownLayer)
        item = QtGui.QTableWidgetItem()
        item.setText("")
        self.ui.tableWidgetDXF2BK.setItem(rows, 1, item)

    def addLevel(self):
        row = self.ui.tableWidgetCont2DXF.currentRow()
        item = QtGui.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        if row == -1:
            row = 0
        self.ui.tableWidgetCont2DXF.insertRow(row)
        self.ui.tableWidgetCont2DXF.setItem(row, 2, item)
        
    def deleteLayer(self):
        row = self.ui.tableWidgetDXF2BK.currentRow()
        self.ui.tableWidgetDXF2BK.removeRow(row)

    def deleteLevel(self):
        row = self.ui.tableWidgetCont2DXF.currentRow()
        self.ui.tableWidgetCont2DXF.removeRow(row)
  
    def initializeModules(self):
        answer = QMessageBox.question(self, "Initialize examples", "Do you really want to overwrite all inputs to initialize examples?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        if answer == QtGui.QMessageBox.Yes:
            self.initialize()
        elif answer == QtGui.QMessageBox.No:
            return
        
    def initialize(self):
        def setEnabled(checkBox, pushButton, lineEdit):
            checkBox.setChecked(True)
            pushButton.setEnabled(True)
            lineEdit.setEnabled(True)
            
        def makedir(dir):
            if not os.path.exists(dir):
                os.makedirs(dir)
        
#        self.directory = "C:/ChEsher/"
        abs_path = os.path.abspath('.')
        self.directory = os.path.join(abs_path, 'examples/').replace('\\', '/')

        makedir(self.directory + "example_01/output/")
        makedir(self.directory + "example_02/output/")  
        makedir(self.directory + "example_03/output/")
        makedir(self.directory + "example_04/output/")
        makedir(self.directory + "example_05/output/")
        makedir(self.directory + "example_06/output/")
        makedir(self.directory + "example_07/output/")
        makedir(self.directory + "example_08/output/")
        makedir(self.directory + "example_09/output/")
        makedir(self.directory + "example_10/output/")
        makedir(self.directory + "example_12/output/")
        makedir(self.directory + "example_13/output/")
        
        ###   ~   module DXF2BK   ~   ###
        
        self.ui.tableWidgetDXF2BK.setRowCount(0)
        self.ui.lineEditDXF2BKInput.setText(self.directory + "example_01/geometry.dxf")
        self.addLayer()
        self.addLayer()
        self.addLayer()
        self.addLayer()
        self.refreshDXF()
        
        rows = self.ui.tableWidgetDXF2BK.rowCount()

        indices = [1, 2, 3, 4]
        files = [self.directory + "example_01/output/2D_POLYLINE.i2s",
                self.directory + "example_01/output/3D_POLYLINE.i3s",
                self.directory + "example_01/output/LINE.i2s",
                self.directory + "example_01/output/POINT.xyz"]

        for row in range(rows):
            combobox = self.ui.tableWidgetDXF2BK.cellWidget(row, 0)
            combobox.setCurrentIndex(indices[row])
            item3 = QtGui.QTableWidgetItem()
            item3.setText(files[row])
            self.ui.tableWidgetDXF2BK.setItem(row, 1, item3)

        ###   ~   module BK2DXF   ~   ###
        
        self.ui.lineEditBK2DXFInputMesh.setText(self.directory + "example_02/WATER DEPTH_S161_Case_A.t3s")
        self.ui.lineEditBK2DXFInputLineSet.setText(self.directory + "example_02/WATER DEPTH_S161_Case_A(IsoLine).i2s")        
        setEnabled(self.ui.checkBoxBK2DXFOutputMesh, self.ui.pushButtonBK2DXFOutputMesh, self.ui.lineEditBK2DXFOutputMesh)
        setEnabled(self.ui.checkBoxBK2DXFOutputLineSet, self.ui.pushButtonBK2DXFOutputLineSet, self.ui.lineEditBK2DXFOutputLineSet)
        
        self.ui.lineEditBK2DXFOutputMesh.setText(self.directory + "example_02/output/mesh.dxf")        
        self.ui.lineEditBK2DXFOutputLineSet.setText(self.directory + "example_02/output/contour.dxf")        
        
        ###   ~   module Mesh   ~   ###
        
        self.ui.lineEditProfiles.setText(self.directory + "example_03/PROFILES.i3s")
        self.ui.lineEditReach.setText(self.directory + "example_03/AXIS.i2s")        
        
        setEnabled(self.ui.checkBoxLBO, self.ui.pushButtonLBO, self.ui.lineEditLBO)
        self.ui.lineEditLBO.setText(self.directory + "example_03/LEFT_BOUNDARY.i3s")        

        setEnabled(self.ui.checkBoxRBO, self.ui.pushButtonRBO, self.ui.lineEditRBO)
        self.ui.lineEditRBO.setText(self.directory + "example_03/RIGHT_BOUNDARY.i3s")    
        
        self.ui.checkBoxEC.setChecked(True)
        self.ui.doubleSpinBoxEL.setValue(1.0)
        self.ui.spinBoxNNC.setValue(20)
        
        self.ui.lineEditMesh.setText(self.directory + "example_03/output/MESH.t3s")
        setEnabled(self.ui.checkBoxMesh, self.ui.pushButtonMesh, self.ui.lineEditMesh)
        
        self.ui.lineEditWS.setText(self.directory + "example_03/output/VIEW.ews")
        setEnabled(self.ui.checkBoxWS, self.ui.pushButtonWS, self.ui.lineEditWS)
  
        ###   ~   module LandXML   ~   ###
  
        self.ui.lineEditLandXMLInputMesh.setText(self.directory + "example_04/BOTTOM.t3s")
        self.ui.lineEditLandXMLSurfaceName.setText("BOTTOM")
        self.ui.lineEditLandXMLOutput.setText(self.directory + "example_04/output/BOTTOM.xml")
     
        ###   ~   module ScalarDXF   ~   ###

        self.ui.lineEditScalarDXFInputT3SMajor.setText(self.directory + "example_05/WATER DEPTH_S161_Case_A.t3s")
        self.ui.lineEditScalarDXFInputT3SMinor.setText(self.directory + "example_05/WATER DEPTH_S161_Case_B.t3s")
        self.ui.doubleSpinBoxScalarDXFDX.setValue(50.0)
        self.ui.doubleSpinBoxScalarDXFDY.setValue(50.0)
        self.ui.doubleSpinBoxScalarDXFSizeFactor.setValue(7.5)
        
        self.ui.checkBoxScalarDXFMonochrome.setChecked(True)
        self.ui.radioButtonScalarDXFCircle.setChecked(False)
        self.ui.radioButtonScalarDXFCrosshairs.setChecked(True)
        self.setSymbol(2)
        
        self.ui.lineEditScalarDXFOutput.setText(self.directory + "example_05/output/water_depth.dxf")        

        ###   ~   module VectorDXF   ~   ###

        self.ui.lineEditVectorDXFInput.setText(self.directory + "example_06/VELOCITY UV_S161_Case_A.t3v")
        self.ui.doubleSpinBoxVectorDXFDX.setValue(25.0)
        self.ui.doubleSpinBoxVectorDXFDY.setValue(25.0)
        self.ui.doubleSpinBoxVectorDXFScale.setValue(40)
        
        self.ui.lineEditVectorDXFOutput.setText(self.directory + "example_06/output/velocity.dxf")        

        ###   ~   module CS   ~   ###
        
        self.ui.lineEditCSInputMesh.setText(self.directory + "example_07/BOTTOM_Case_A.t3s")
        self.ui.lineEditCSInputDefinition.setText(self.directory + "example_07/cs_input.txt")
        self.ui.lineEditCSInputResults.setText(self.directory + "example_07/cs_output_donau.txt")
        self.ui.doubleSpinBoxCSSizeFactor.setValue(7.5)
        
        setEnabled(self.ui.checkBoxCSOutputFormatted, self.ui.pushButtonCSOutputFormatted, self.ui.lineEditCSOutputFormatted)
        setEnabled(self.ui.checkBoxCSOutputCS, self.ui.pushButtonCSOutputCS, self.ui.lineEditCSOutputCS)

        self.ui.lineEditCSOutputFormatted.setText(self.directory + "example_07/output/cs_formatted.txt")
        self.ui.lineEditCSOutputCS.setText(self.directory + "example_07/output/cs.dxf")

        ###   ~   module 2DM   ~   ###

        self.ui.lineEdit2dmInput.setText(self.directory + "example_08/input.2dm")
        self.ui.lineEdit2dmInputData.setText(self.directory + "example_08/water_depth.dat")
        
        setEnabled(self.ui.checkBox2dmBottom, self.ui.pushButton2dmBottom, self.ui.lineEdit2dmBottom)
        setEnabled(self.ui.checkBox2dmBottomFriction, self.ui.pushButton2dmBottomFriction, self.ui.lineEdit2dmBottomFriction)
        setEnabled(self.ui.checkBox2dmWaterSurface, self.ui.pushButton2dmWaterSurface, self.ui.lineEdit2dmWaterSurface)
        setEnabled(self.ui.checkBox2dmWaterDepth, self.ui.pushButton2dmWaterDepth, self.ui.lineEdit2dmWaterDepth)                
        setEnabled(self.ui.checkBox2dmCulvertHeight, self.ui.pushButton2dmCulvertHeight, self.ui.lineEdit2dmCulvertHeight)
        setEnabled(self.ui.checkBox2dmNS1, self.ui.pushButton2dmNS1, self.ui.lineEdit2dmNS1)
        setEnabled(self.ui.checkBox2dmNS2, self.ui.pushButton2dmNS2, self.ui.lineEdit2dmNS2)
        setEnabled(self.ui.checkBox2dmNS3, self.ui.pushButton2dmNS3, self.ui.lineEdit2dmNS3)
        setEnabled(self.ui.checkBox2dmNS4, self.ui.pushButton2dmNS4, self.ui.lineEdit2dmNS4)
        setEnabled(self.ui.checkBox2dmNS5, self.ui.pushButton2dmNS5, self.ui.lineEdit2dmNS5)
        setEnabled(self.ui.checkBox2dmNS6, self.ui.pushButton2dmNS6, self.ui.lineEdit2dmNS6)
        setEnabled(self.ui.checkBox2dmNS7, self.ui.pushButton2dmNS7, self.ui.lineEdit2dmNS7)
                                                                                             
        self.ui.lineEdit2dmBottom.setText(self.directory + "example_08/output/BOTTOM.t3s")
        self.ui.lineEdit2dmBottomFriction.setText(self.directory + "example_08/output/BOTTOM FRICTION.t3s")
        self.ui.lineEdit2dmWaterSurface.setText(self.directory + "example_08/output/WATER SURFACE.t3s")
        self.ui.lineEdit2dmWaterDepth.setText(self.directory + "example_08/output/WATER DEPTH.t3s")
        self.ui.lineEdit2dmCulvertHeight.setText(self.directory + "example_08/output/culvert.xyz")
        self.ui.lineEdit2dmNS1.setText(self.directory + "example_08/output/NS1.i2s")
        self.ui.lineEdit2dmNS2.setText(self.directory + "example_08/output/NS2.i2s")
        self.ui.lineEdit2dmNS3.setText(self.directory + "example_08/output/NS3.i2s")
        self.ui.lineEdit2dmNS4.setText(self.directory + "example_08/output/NS4.i2s")
        self.ui.lineEdit2dmNS5.setText(self.directory + "example_08/output/NS5.i2s")
        self.ui.lineEdit2dmNS6.setText(self.directory + "example_08/output/NS6.i2s")
        self.ui.lineEdit2dmNS7.setText(self.directory + "example_08/output/NS7.i2s")

        ###   ~   module Cont2DXF   ~   ###
        
        self.ui.lineEditCont2DXFInput.setText(self.directory + "example_09/WATER DEPTH_S161_Case_A.t3s")
        self.ui.lineEditCont2DXFOutputLayer.setText("HQ100")
        self.ui.lineEditCont2DXFOutputLegendSeparator.setText(" - ")
        self.ui.lineEditCont2DXFOutputSolid.setText(self.directory + "example_09/output/contours_Case_A_water_depth.dxf")
        self.ui.lineEditCont2DXFOutputLine.setText(self.directory + "example_09/output/isolines_Case_A_water_depth.dxf")
        self.ui.checkBoxCont2DXFOutputLegend.setChecked(True)
        self.ui.checkBoxCont2DXFOutputLegendReverse.setChecked(True)
        self.setEnabledLegend()
        
        setEnabled(self.ui.checkBoxCont2DXFOutputSolid, self.ui.pushButtonCont2DXFOutputSolid, self.ui.lineEditCont2DXFOutputSolid)
        setEnabled(self.ui.checkBoxCont2DXFOutputLine, self.ui.pushButtonCont2DXFOutputLine, self.ui.lineEditCont2DXFOutputLine)
        
        self.defaultLegend()
        
        ###   ~   module Tube   ~   ###
        
        self.ui.lineEditTubeInputMesh.setText(self.directory + "example_10/mesh.t3s")
        self.ui.lineEditTubeInputLineSet.setText(self.directory + "example_10/tubes.i2s")
        self.ui.lineEditTubeOutput.setText(self.directory + "example_10/tubes.txt")

        ###   ~   module Profile   ~   ###
        
        self.moduleProfiles.ui.lineEditInputProfiles.setText(self.directory + "example_12/profiles.i2s")
        self.moduleProfiles.ui.lineEditInputReach.setText(self.directory + "example_12/reach.i2s")
        self.moduleProfiles.ui.lineEditInputPoints.setText(self.directory + "example_12/points.xyz")
        
        setEnabled(self.moduleProfiles.ui.checkBoxOutputTextfile, self.moduleProfiles.ui.pushButtonOutputTextfile, self.moduleProfiles.ui.lineEditOutputTextfile)
        self.moduleProfiles.ui.lineEditOutputTextfile.setText(self.directory + "example_12/output/points.txt")
        
        setEnabled(self.moduleProfiles.ui.checkBoxOutputDXF, self.moduleProfiles.ui.pushButtonOutputDXF, self.moduleProfiles.ui.lineEditOutputDXF)
        self.moduleProfiles.ui.lineEditOutputDXF.setText(self.directory + "example_12/output/points.dxf")

        setEnabled(self.moduleProfiles.ui.checkBoxOutputHECRAS, self.moduleProfiles.ui.pushButtonOutputHECRAS, self.moduleProfiles.ui.lineEditOutputHECRAS)
        self.moduleProfiles.ui.lineEditOutputHECRAS.setText(self.directory + "example_12/output/points.geo")       

        ###   ~   module HEC2DXF   ~   ###
        
        self.moduleHEC2DXF.ui.lineEditInputSDF.setText(self.directory + "example_13/results.sdf")
        self.moduleHEC2DXF.ui.lineEditOutputDXF.setText(self.directory + "example_13/output/results.dxf")

        ###   ~   module ProfilesDXF   ~   ###
        
        self.moduleProfilesDXF.ui.lineEditInputProfiles.setText(self.directory + "example_15/profiles.i2s")
        self.moduleProfilesDXF.ui.lineEditInputReach.setText(self.directory + "example_15/reach.i2s")
        self.moduleProfilesDXF.ui.lineEditInputBottom.setText(self.directory + "example_15/BOTTOM_Case_A.t3s")
        self.moduleProfilesDXF.ui.lineEditInputReachName.setText("Donau")

        self.moduleProfilesDXF.ui.tableWidget.setRowCount(0)
        self.moduleProfilesDXF.add()
        
        item1 = QtGui.QTableWidgetItem()
        item1.setText(self.directory + "example_15/FREE SURFACE_S161.t3s")
        self.moduleProfilesDXF.ui.tableWidget.setItem(0, 0, item1)
        
        item2 = QtGui.QTableWidgetItem()
        item2.setText("HQ100")
        self.moduleProfilesDXF.ui.tableWidget.setItem(0, 1, item2)
        
        row = self.moduleProfilesDXF.ui.tableWidget.currentRow()
        item3 = self.moduleProfilesDXF.ui.tableWidget.item(0, 2)
        initCol = item3.backgroundColor()
        initCol.setRed(200)
        initCol.setGreen(200)
        initCol.setBlue(255)
        item3 = QtGui.QTableWidgetItem()
        item3.setBackground(initCol)
        item3.setFlags(QtCore.Qt.ItemIsEnabled)
        item3.setText(str(initCol.red()) + ", " + str(initCol.green()) + ", " + str(initCol.blue()))
        self.moduleProfilesDXF.ui.tableWidget.setItem(0, 2, item3)

        setEnabled(self.moduleProfilesDXF.ui.checkBoxOutputProfiles, self.moduleProfilesDXF.ui.pushButtonOutputProfiles, self.moduleProfilesDXF.ui.lineEditOutputProfiles)
        self.moduleProfilesDXF.ui.lineEditOutputProfiles.setText(self.directory + "example_15/output/profiles.dxf")
        
    def setDXF2BK(self):
        self.ui.labelModule.setText("~   Module DXF2BK   ~")
        self.ui.stackedWidget.setCurrentIndex(0)

    def setBK2DXF(self):
        self.ui.labelModule.setText("~   Module BK2DXF   ~")
        self.ui.stackedWidget.setCurrentIndex(1)

    def setMesh(self):
        self.ui.labelModule.setText("~   Module Mesh   ~")
        self.ui.stackedWidget.setCurrentIndex(2)

    def setLandXML(self):
        self.ui.labelModule.setText("~   Module LandXML   ~")
        self.ui.stackedWidget.setCurrentIndex(3)
        
    def setScalarDXF(self):
        self.ui.labelModule.setText("~   Module ScalarDXF   ~")
        self.ui.stackedWidget.setCurrentIndex(4)
 
    def setVectorDXF(self):
        self.ui.labelModule.setText("~   Module VectorDXF   ~")
        self.ui.stackedWidget.setCurrentIndex(5)
        
    def setCS(self):
        self.ui.labelModule.setText("~   Module CS   ~")
        self.ui.stackedWidget.setCurrentIndex(6)
        
    def set2DM2BK(self):
        self.ui.labelModule.setText("~   Module 2DM2BK   ~")
        self.ui.stackedWidget.setCurrentIndex(7)

    def setCont2DXF(self):
        self.ui.labelModule.setText("~   Module Cont2DXF   ~")
        self.ui.stackedWidget.setCurrentIndex(8)

    def setTube(self):
        self.ui.labelModule.setText("~   Module Tube   ~")
        self.ui.stackedWidget.setCurrentIndex(9)
        
    def setHyDesign(self):
        self.ui.labelModule.setText("~   Module HyDesign   ~")
        self.ui.stackedWidget.setCurrentIndex(10)

    def setProfiles(self):
        self.ui.labelModule.setText("~   Module Profiles   ~")
        self.ui.stackedWidget.setCurrentIndex(11)
        
    def setHEC2DXF(self):
        self.ui.labelModule.setText("~   HEC2DXF   ~")
        self.ui.stackedWidget.setCurrentIndex(12)
        
    def setXYZ2DXF(self):
        self.ui.labelModule.setText("~   XYZ2DXF   ~")
        self.ui.stackedWidget.setCurrentIndex(13)

    def setProfilesDXF(self):
        self.ui.labelModule.setText("~   Module ProfilesDXF   ~")
        self.ui.stackedWidget.setCurrentIndex(14)
        
    def setDirectory(self):
        dir = QFileDialog.getExistingDirectory(self, "Select directory", self.directory)
        self.moduleProfiles.setDir(dir)
        self.moduleHEC2DXF.setDir(dir)
        self.moduleXYZ2DXF.setDir(dir)
        if dir != "":
            self.directory = dir
        else:
            return
            
    def setColour(self):
        row = self.ui.tableWidgetCont2DXF.currentRow()
        item1 = self.ui.tableWidgetCont2DXF.item(row, 2)
        initCol = item1.backgroundColor()
        coldia = QtGui.QColorDialog()
        col = coldia.getColor(initCol)
        if col.isValid():
            item = QtGui.QTableWidgetItem()
            item.setBackground(col)
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            item.setText(str(col.red()) + ", " + str(col.green()) + ", " + str(col.blue()))
            self.ui.tableWidgetCont2DXF.setItem(row, 2, item)
        else:
            return
    
    def interpolatePoint(self, xa, ya, za, xb, yb, zb, xc, yc, zc, xp, yp):
        dot1 = (yb - ya)*(xp - xa) + (-xb + xa)*(yp - ya)
        dot2 = (yc - yb)*(xp - xb) + (-xc + xb)*(yp - yb)
        dot3 = (ya - yc)*(xp - xc) + (-xa + xc)*(yp - yc)

        zp = 0.0
        counter = 0 
        if dot1 <= 0.0 and dot2 <= 0.0 and dot3 <= 0.0:

            #Determine two vectors from the points:
            v1 = [xc - xa, yc - ya, zc - za]
            v2 = [xb - xa, yb - ya, zb - za]

            #Determine the cross product of the two vectors:
            cp = [v1[1] * v2[2] - v1[2] * v2[1],
                  v1[2] * v2[0] - v1[0] * v2[2],
                  v1[0] * v2[1] - v1[1] * v2[0]]

            #A plane can be described using a simple equation ax + by + cz = d. The three coefficients from the cross product are a, b and c, and d can be solved by substituting a known point, for example the first:
            a, b, c = cp
            d = a * xa + b * ya + c * za

            #Determine the z value at x, y. Re-arrange the simple equation, and solve for z:
            zp = (d - a * xp - b * yp) / float(c)            
            counter = 1
        else:
            counter = 0
        return zp, counter
    
    def insideBoundingBox(self, xa, ya, xb, yb, xc, yc, xp, yp):

        xMin = min([xa, xb, xc])
        xMax = max([xa, xb, xc])
        yMin = min([ya, yb, yc])
        yMax = max([ya, yb, yc])

        if xp >= xMin and xp <= xMax and yp >= yMin and yp <= yMax:
            return True
        else:
            return False

    def getTriangles(self, mesh, nodesMajor, nodesMinor):

        x = []
        y = []
        zMajor = []
        zMinor = []
        
        triangles = []
        for nID in nodesMajor:
            x.append(nodesMajor[nID][0])
            y.append(nodesMajor[nID][1])
            zMajor.append(nodesMajor[nID][2])
            if nodesMinor is not None:
                zMinor.append(nodesMinor[nID][2])
 
        for eID in mesh:
            n1 = mesh[eID][0]-1
            n2 = mesh[eID][1]-1
            n3 = mesh[eID][2]-1
            triangles.append([n1,n2,n3])
              
        return x, y, zMajor, zMinor, triangles
    
    def createScalarDXF(self):
        
        info = ""
        
        dx = self.ui.doubleSpinBoxScalarDXFDX.value()
        dy = self.ui.doubleSpinBoxScalarDXFDY.value()
        
        SMin = self.ui.doubleSpinBoxScalarDXFSMin.value()
        SMax = self.ui.doubleSpinBoxScalarDXFSMax.value()
        
        scale = self.ui.doubleSpinBoxScalarDXFSizeFactor.value()
        
        eps = self.ui.doubleSpinBoxScalarDXFLessThan.value()
        
        # read input meshes
        
        try:
            x, y, zMajor, triangles = fh.readT3STriangulation(self.ui.lineEditScalarDXFInputT3SMajor.text())
        except:
            QMessageBox.critical(self, "Error", "Not able to load mesh file!\nCheck filename or content!")
            return
        
        minor = False
        if self.ui.lineEditScalarDXFInputT3SMinor.text() != "":
            minor = True
            try:
                x, y, zMinor, triangles = fh.readT3STriangulation(self.ui.lineEditScalarDXFInputT3SMinor.text())
            except:
                QMessageBox.critical(self, "Error", "Not able to load mesh file!\nCheck filename or content!")
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

        useMono = self.ui.checkBoxScalarDXFMonochrome.isChecked()
        fname = self.ui.lineEditScalarDXFOutput.text()
        info += "\n - Number of interpolated values: {0}".format(len(scalarNodes))

        try:
            nOfValues = fh.writeScalarDXF(scalarNodes, SMin, SMax, eps, scale, self.scalarSymbol, useMono, fname)
            info += "\n - {0} values written to {1}".format(nOfValues, fname)
        except:
            QMessageBox.critical(self, "Error", "Not able to write DXF file!")
            return

        QMessageBox.information(self, "Module ScalarDXF", info)  
        
    def createVectorDXF(self):
        
        info = ""
        
        dx = self.ui.doubleSpinBoxVectorDXFDX.value()
        dy = self.ui.doubleSpinBoxVectorDXFDY.value()
        
        VMin = self.ui.doubleSpinBoxVectorDXFVMin.value()
        VMax = self.ui.doubleSpinBoxVectorDXFVMax.value()
        
        scale = self.ui.doubleSpinBoxVectorDXFScale.value()
        
        eps = self.ui.doubleSpinBoxVectorDXFLessThan.value()
        
        # read input meshes
        try:
            x, y, u, v, triangles = fh.readT3VTriangulation(self.ui.lineEditVectorDXFInput.text())
        except:
            QMessageBox.critical(self, "Error", "Not able to load mesh file!\nCheck filename or content!")
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
            fname = self.ui.lineEditVectorDXFOutput.text()
            info += "\n - Number of interpolated values: {0}".format(len(vectorNodes))
            nOfVectors= fh.writeVectorDXF(vectorNodes, VMin, VMax, eps, scale, fname)
            info += "\n - {0} values written to {1}".format(nOfVectors, fname)
        except:
            QMessageBox.critical(self, "Error", "Not able to write DXF file!")
            return   
        
        QMessageBox.information(self, "Module VectorDXF", info)
        
    def createCS(self):

        info = ""
        info += "Input data:\n"
        
        # read input meshes
        nodes = {}
        mesh = {}
        
        try:
            nodes, mesh = fh.readT3S(self.ui.lineEditCSInputMesh.text())
            info += " - Mesh loaded with {0} nodes and {1} elements.\n".format(len(nodes), len(mesh))
        except:
            QMessageBox.critical(self, "Error", "Not able to load mesh file!\nCheck filename or content!")
            return
    
        # read control sections definition file
        nCS = 0
        nameCS = {}
        nodeIDsCS = {}
        try:
            nCS, nameCS, nodeIDsCS, coordsCS, type = fh.readCSDefinition(self.ui.lineEditCSInputDefinition.text())
            info += " - Control section definition loaded with {0} control sections.\n".format(nCS)
        except:
            QMessageBox.critical(self, "Error", "Not able to load control sections definition file!\nCheck filename or content!")
            return

        # read control sections results file
        time = []
        resultsCS = {}
        try:
            time, resultsCS = fh.readCSResults(self.ui.lineEditCSInputResults.text(), nCS)
            info += " - Control section results loaded with {0} time steps.\n".format(len(time))
        except:
            QMessageBox.critical(self, "Error", "Not able to load control sections results file!\nCheck filename or content!")
            return        
        
        decTime = self.ui.spinBoxCSTime.value()
        decFlow = self.ui.spinBoxCSFlow.value()

        info += "\nOutput data:\n"
                    
        if self.ui.checkBoxCSOutputFormatted.isChecked():
            try:
                fh.writeCSFormatted(self.ui.lineEditCSOutputFormatted.text(), nameCS, time, resultsCS, decTime, decFlow)
                info += " - Formatted control section data file written to {0}.\n".format(self.ui.lineEditCSOutputFormatted.text())
            except:
                QMessageBox.critical(self, "Error", "Not able to write formatted data file!")
                return

        if self.ui.checkBoxCSOutputCS.isChecked():
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

                scale = self.ui.doubleSpinBoxCSSizeFactor.value()
                prefix = self.ui.lineEditCSInputPrefix.text()
                suffix = self.ui.lineEditCSInputSuffix.text()
                fh.writeCSDXF(self.ui.lineEditCSOutputCS.text(), nameCS, nodeIDsCS, nodesCS, valuesCS, decFlow, scale, prefix, suffix)
                info += " - Control sections written to {0}.\n".format(self.ui.lineEditCSOutputCS.text())
                for key in valuesCS:
                    info += "\t{0} to {1} ({2})\n".format(round(valuesCS[key][0], decFlow), round(valuesCS[key][1], decFlow), nameCS[key])
            except:
                QMessageBox.critical(self, "Error", "Not able to write control section file!")
                return               
    
        QMessageBox.information(self, "Module CS", info)
        
    def createTube(self):

        info = ""
        info += "Input data:\n"
        
        textfile = []
        
        # read input meshes
        try:
            x, y, z, triangles = fh.readT3STriangulation(self.ui.lineEditTubeInputMesh.text())
            info += " - Mesh loaded with {0} nodes and {1} elements.\n".format(len(x), len(triangles))
        except:
            QMessageBox.critical(self, "Error", "Not able to load mesh file!\nCheck filename or content!")
            return        

        try:
            tube_coords, tubes = fh.readI2S(self.ui.lineEditTubeInputLineSet.text())
            info += " - Line Set loaded with {0} lines.\n".format(len(tubes))
        except:
            QMessageBox.critical(self, "Error", "Not able to load *.i2s file!\nCheck filename or content!")
            return

        # reshape coordinates
        a = np.array([x, y])
        b = np.reshape(a, (2*len(x)), order='F')
        mesh_coords = np.reshape(b, (len(x), 2))
        
        Rel = str(self.ui.doubleSpinBoxTubeRel.value())
        Ce1 = str(self.ui.doubleSpinBoxTubeCe1.value())
        Ce2 = str(self.ui.doubleSpinBoxTubeCe2.value())
        Cs1 = str(self.ui.doubleSpinBoxTubeCs1.value())
        Cs2 = str(self.ui.doubleSpinBoxTubeCs2.value())
        Lrg = str(self.ui.doubleSpinBoxTubeLrg.value())
        Hau = str(self.ui.doubleSpinBoxTubeHau.value())
        Clp = str(self.ui.spinBoxTubeClp.value())
        L12 = str(self.ui.doubleSpinBoxTubeL12.value())
        
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
            fh.writeTextFile(self.ui.lineEditTubeOutput.text(), textfile)
            info += " - Tubes data file written to {0}.\n".format(self.ui.lineEditTubeOutput.text())
        except:
            QMessageBox.critical(self, "Error", "Not able to write tubes data file!")
            return
    
        QMessageBox.information(self, "Module Tube", info)

    def createBK2DXF(self):

        info = ""
        info += "Input data:\n"
        
        # read input meshes
        nodes = {}
        mesh = {}
        if self.ui.lineEditBK2DXFInputMesh.text() != "":
            try:
                nodes, mesh = fh.readT3S(self.ui.lineEditBK2DXFInputMesh.text())
                info += " - Mesh loaded with {0} nodes and {1} elements.\n".format(len(nodes), len(mesh))
            except:
                QMessageBox.critical(self, "Error", "Not able to load mesh file!\nCheck filename or content!")
                return

        # read input line sets
        linesetNodes = {}
        lineset = {}
        dim = 2
        if self.ui.lineEditBK2DXFInputLineSet.text() != "":
            try:
                if self.ui.lineEditBK2DXFInputLineSet.text().split(".")[-1] == "i2s":
                    linesetNodes, lineset = fh.readI2S(self.ui.lineEditBK2DXFInputLineSet.text())                
                    dim = 2
                else:
                    linesetNodes, lineset = fh.readI3S(self.ui.lineEditBK2DXFInputLineSet.text())
                    dim = 3
                info += " - Line set loaded with {0} lines and {1} nodes.\n".format(len(lineset), len(linesetNodes))
            except:
                QMessageBox.critical(self, "Error", "Not able to load line set!\nCheck filename or content!")
                return

        info += "\nOutput data:\n"
        
        # write mesh
        if self.ui.checkBoxBK2DXFOutputMesh.isChecked() and self.ui.lineEditBK2DXFInputMesh.text() != "":
            try:
                fh.writeMeshDXF(self.ui.lineEditBK2DXFOutputMesh.text(), nodes, mesh, self.typeDXFmesh)
                info += " - Mesh written to {0}.\n".format(self.ui.lineEditBK2DXFOutputMesh.text())
            except:
                QMessageBox.critical(self, "Error", "Not able to write mesh!")
                return
            
        # write line set
        if self.ui.checkBoxBK2DXFOutputLineSet.isChecked() and self.ui.lineEditBK2DXFInputLineSet.text() != "":
            try:
                fh.writeLineSetDXF(self.ui.lineEditBK2DXFOutputLineSet.text(), linesetNodes, lineset, dim)
                info += " - Line set written to {0}.\n".format(self.ui.lineEditBK2DXFOutputLineSet.text())
            except:
                QMessageBox.critical(self, "Error", "Not able to write line sets!")
                return
    
        QMessageBox.information(self, "Module BK2DXF", info)
        
    def createMesh(self):
        info = "Input data:\n"
        try:
            nodRaw, proRaw = fh.readI3S(self.ui.lineEditProfiles.text())
            info += " - Profiles:\t\t\t{0}\n".format(len(proRaw))
        except:
            QMessageBox.critical(self, "Error", "Not able to load profiles file!\nCheck filename or content!")
            return
        try:
            nodReach = fh.readI2S(self.ui.lineEditReach.text())[0]
            info += " - Reach nodes:\t\t{0}\n".format(len(nodReach))
        except:
            QMessageBox.critical(self, "Error", "Not able to load reach file!\nCheck filename or content!")
            return
            
        if len(proRaw) != len(nodReach):
            QMessageBox.critical(self, "Error", "Number of profiles must correspond to number of reach nodes!")
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
                QMessageBox.critical(self, "Error", "Not able to load left breakline file!\nCheck filename or content!")
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
                QMessageBox.critical(self, "Error", "Not able to load right breakline file!\nCheck filename or content!")
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
                QMessageBox.critical(self, "Error", "Not able to load left boundary file!\nCheck filename or content!")
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
                QMessageBox.critical(self, "Error", "Not able to load right boundary file!\nCheck filename or content!")
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
            QMessageBox.critical(self, "Error", "Not able to determine flow direction!\nCheck inputs!")
            return
        
        try:
            info += self.mesh.normalizeProfiles()
        except:
            QMessageBox.critical(self, "Error", "Not able to normalize profiles!\nCheck inputs!")
            return
        
        try:
            info += self.mesh.interpolateChannel()
        except:
            QMessageBox.critical(self, "Error", "Not able to interpolate channel!\nCheck inputs!")
            return
        
        try:
            info += self.mesh.interpolateElevation()
        except:
            QMessageBox.critical(self, "Error", "Not able to interpolate elevation!\nCheck inputs!")
            return
        
        if self.ui.checkBoxEC.isChecked():
            try:
                info += self.mesh.interpolateElevationCorrection()
            except:
                QMessageBox.critical(self, "Error", "Not able to interpolate elevation correction!\nCheck inputs!")
                return
            
        try:
            info += self.mesh.createMesh()
        except:
            QMessageBox.critical(self, "Error", "Not able to create mesh!\nCheck inputs!")
            return
        
#        try:
        self.writeOutput()
#        except:
#            QMessageBox.critical(self, "Error", "Not able to write output!")
#            return
        
        QMessageBox.information(self, "Module Mesh", info)

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

    def getDim(self, lineEdit):
        return lineEdit.text().split('.')[-1][1]

    def getPath(self, lineEdit):
        return lineEdit.text().replace('/', '\\')

    def setEnabledBL(self, checkBox, pushButton, lineEdit, spinBox):
        self.setEnabled(checkBox, pushButton, lineEdit)
        checked = checkBox.isChecked()
        spinBox.setEnabled(checked)

    def setEnabledCS(self):
        checked = self.ui.checkBoxCSOutputCS.isChecked()
        self.ui.doubleSpinBoxCSSizeFactor.setEnabled(checked)
        self.ui.lineEditCSInputPrefix.setEnabled(checked)       
        self.ui.lineEditCSInputSuffix.setEnabled(checked) 
        self.ui.pushButtonCSOutputCS.setEnabled(checked)    
        self.ui.lineEditCSOutputCS.setEnabled(checked)          
        
    def setEnabled(self, checkBox, pushButton, lineEdit):
        checked = checkBox.isChecked()
        pushButton.setEnabled(checked)
        lineEdit.setEnabled(checked)

    def setEnabledLegend(self):
        checked = self.ui.checkBoxCont2DXFOutputLegend.isChecked()
        self.ui.widgetCont2DXFLegend.setEnabled(checked)
        
    def refreshDXF(self):
        
        filename = self.ui.lineEditDXF2BKInput.text()
        self.dxf = None
        self.dxf = dxfgrabber.readfile(str(filename))
        try:
            self.dxf = dxfgrabber.readfile(str(filename))
        except Exception:
            QMessageBox.critical(self, "File error", "File not found!")
            self.ui.lineEditDXF.selectAll()
            self.ui.lineEditDXF.setFocus()
            return

        self.layers = ()
        for layer in self.dxf.layers:
            self.layers = self.layers + (layer.name,)
        sorted_layers = sorted(self.layers)
        rows = self.ui.tableWidgetDXF2BK.rowCount()
        if rows > 0:
            for row in range(rows):
                combobox = self.ui.tableWidgetDXF2BK.cellWidget(row, 0)
                temp = u"{0}".format(combobox.itemText(combobox.currentIndex()))
                combobox.clear()
                combobox.setInsertPolicy(6)
                combobox.addItems(sorted_layers)
                if temp in sorted_layers:
                    combobox.setCurrentIndex(sorted_layers.index(temp))
                else:
                    combobox.setCurrentIndex(combobox.findText("0"))
                self.ui.tableWidgetDXF2BK.setCellWidget(rows, 0, combobox)
                
    def openDXFFile(self, title, fileFormat, lineEdit):
        
        filename = QFileDialog.getOpenFileName(self, title, self.directory, fileFormat)
        if filename == "": return
        lineEdit.setText(filename)
        self.refreshDXF()
        
    def getOpenFileName(self, title, fileFormat, lineEdit):
        filename = QFileDialog.getOpenFileName(self, title, self.directory, fileFormat)
        if filename != "":
            lineEdit.setText(filename)

    def getSaveFileName(self, title, fileFormat, lineEdit):
        filename = QFileDialog.getSaveFileName(self, title, self.directory, fileFormat)
        if filename != "":
            lineEdit.setText(filename)
        
    def applyLegend(self, levels, colHEX_RGB):

        nLevels = len(levels)-1

        self.ui.tableWidgetCont2DXF.setRowCount(nLevels)
        
        for row in range(nLevels):
            item1 = QtGui.QTableWidgetItem()
            item1.setText(str(levels[row]))
            self.ui.tableWidgetCont2DXF.setItem(row, 0, item1)
            
            item2 = QtGui.QTableWidgetItem()
            item2.setText(str(levels[row+1]))
            self.ui.tableWidgetCont2DXF.setItem(row, 1, item2)
            
            col = colors.hex2color(colHEX_RGB[row])
            colPy = QColor(int(col[0]*255),int(col[1]*255),int(col[2]*255))
            item3 = QtGui.QTableWidgetItem()
            item3.setBackground(colPy)
            item3.setFlags(QtCore.Qt.ItemIsEnabled)
            item3.setText(str(colPy.red()) + ", " + str(colPy.green()) + ", " + str(colPy.blue()))
            self.ui.tableWidgetCont2DXF.setItem(row, 2, item3)

    def loadLegend(self):
        filename = QFileDialog.getOpenFileName(self, "Load an EnSim ColourScale definition file", self.directory, "EnSim ColourScale Files (*.cs1)")
        
        if filename != "":
            try:
                levels, colHEX_BGR = fh.readCS1(filename)

                colHEX_RGB = []

                for col in range(len(colHEX_BGR)):
                    colFloat_BGR = colors.hex2color(colHEX_BGR[col])
                    colFloat_RGB = [colFloat_BGR[2], colFloat_BGR[1], colFloat_BGR[0]]
                    colHEX_RGB.append(colors.rgb2hex(colFloat_RGB)) 

                self.applyLegend(levels, colHEX_RGB)

                info = "Legend loaded with {0} levels.".format(len(levels))     
                QMessageBox.information(self, "Legend", info)
            except:
                QMessageBox.critical(self, "Error", "Not able to load legend!")

    def saveLegend(self):
        filename = QFileDialog.getSaveFileName(self, "Save an EnSim ColourScale definition file", self.directory, "EnSim ColourScale Files (*.cs1)")
   
        if filename != "":
            try:
                levels, levels_ok, coloursHEX_RGB, coloursRGB, coloursHEX_BGR, coloursBGR, col_ok = self.getLevels()
            except:
                QMessageBox.critical(self, "Error", "Check level inputs!")
                return        

            if not levels_ok:
                QMessageBox.critical(self, "Error", "Check level ranges!")
                return
            if not col_ok:
                QMessageBox.critical(self, "Error", "Check colours!")
                return

            try:
                fh.writeCS1(filename, levels, coloursHEX_BGR)
                info = "Legend saved with {0} levels.".format(len(levels))     
                QMessageBox.information(self, "Legend", info)
            except:
                QMessageBox.critical(self, "Error", "Not able to save legend!")
                return
        
    def defaultLegend(self):
        
        def RGB2HEX(RGB):
            
            HEX = []
            for i in range(len(RGB)):
                RGB[i]
                colFloat_RGB = (float(RGB[i][0])/255.0, float(RGB[i][1])/255.0, float(RGB[i][2])/255.0)
                HEX.append(colors.rgb2hex(colFloat_RGB))
            return HEX
        
        legend = self.ui.comboBoxCont2DXF.currentIndex()

        # water depth
        if legend == 0:

            levels = [0.0, 0.1, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 4.0, 100.0]
            col_RGB = [[190,232,255],[116,179,255],[55,141,255],[18,107,238],[0,77,168],[232,190,255],[202,123,245],[161,91,137],[130,39,100],[230,0,0]]
            col_HEX = RGB2HEX(col_RGB)
            
            self.applyLegend(levels, col_HEX)
            
            self.ui.lineEditCont2DXFOutputLegendTitle.setText("Water depth")
            self.ui.lineEditCont2DXFOutputLegendSubtitle.setText("[m]")
            
        # water surface difference
        if legend == 1:
            levels = [-100.0, -0.8, -0.6, -0.4, -0.2, -0.1, -0.05, -0.01, 0.01, 0.05, 0.1, 0.2, 0.4, 0.6, 0.8, 100.0]
            col_RGB = [[219,81,216],[255,128,255],[191,128,255],[128,128,255],[128,191,255],[128,255,255],[179,255,255],[255,255,255],[255,255,204],[255,255,128],[255,191,128],[255,128,128],[255,0,0],[202,0,0],[157,0,0]]
            col_HEX = RGB2HEX(col_RGB)
            
            self.applyLegend(levels, col_HEX)

            self.ui.lineEditCont2DXFOutputLegendTitle.setText("Water surface difference")
            self.ui.lineEditCont2DXFOutputLegendSubtitle.setText("[m]")
            
        # velocity
        if legend == 2:
            levels = [0.0, 0.1, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 4.0, 100.0]
            col_RGB = [[211,255,190],[163,255,116],[77,230,0],[55,168,0],[36,116,0],[255,190,190],[255,127,127],[230,0,0],[168,0,0], [116,0,0]]
            col_HEX = RGB2HEX(col_RGB)
            
            self.applyLegend(levels, col_HEX)

            self.ui.lineEditCont2DXFOutputLegendTitle.setText("Flow velocity")
            self.ui.lineEditCont2DXFOutputLegendSubtitle.setText("[m/s]")
            
        # bottom shear stress
        if legend == 3:
            levels = [0.0, 5.0, 12.5, 25.0, 37.5, 50.0, 75.0, 100.0, 150.0, 200.0, 1000.0]
            col_RGB = [[211,255,190],[163,255,116],[77,230,0],[55,168,0],[36,116,0],[255,190,190],[255,127,127],[230,0,0],[168,0,0], [116,0,0]]
            col_HEX = RGB2HEX(col_RGB)
            
            self.applyLegend(levels, col_HEX)

            self.ui.lineEditCont2DXFOutputLegendTitle.setText("Bottom shear stress")
            self.ui.lineEditCont2DXFOutputLegendSubtitle.setText("[N/m2]")
            
    def createAction(self, text="", slot=None, shortcut=None, icon=None,
                     tip=None, checkable=False, signal="triggered()"):
        """Create action out of keyword arguments. Return action.

        Keyword arguments:
        text -- User visible text (default "")
        slot -- function to call (default None)
        shortcut -- Key sequence (default None)
        icon -- Name of icon file (default None)
        tip -- Tooltip (default None)
        checkable -- Should action be checkable (default None)
        signal -- Signal to emit (default "triggered()")

        """
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(":/resource/{0}.png".format(icon)))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            self.connect(action, SIGNAL(signal), slot)
        if checkable:
            action.setCheckable(True)
        return action

    def addActions(self, target, actions):
        """Add action or separator to menu.

        Keyword arguments:
        target -- name of menu
        actions -- tuple with names of actions

        """
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)

    def help(self):
        
        abs_path = os.path.abspath('.')
        filename = os.path.join(abs_path, 'documentation/00_index.html')
        webbrowser.open(filename)

    def helpAbout(self):
        """Setup the About-dialog."""
        msg = u"""<p><b>ChEsher</b> V 1.0</p>
                    <p>Additional tool to <a href="http://www.nrc-cnrc.gc.ca/eng/solutions/advisory/blue_kenue_index.html">Blue Kenue&trade;</a> that is a pre and post processing software for the <a href="http://www.opentelemac.org/">open TELEMAC-MASCARET</a> system - an integrated suite of solvers for use in the field of free-surface flow of hydraulic modeling. </p>
                    <p>Copyright \u00A9 2016 <a href="mailto:reinhard.fleissner@gmail.com?subject=ChEsher">Reinhard Flei\xdfner</a></p>
                    <hr/>
                    <p>Python {0} - Qt {1} - PyQt {2} - {3}</p>""".format(
                    platform.python_version(),
                    QT_VERSION_STR,
                    PYQT_VERSION_STR,
                    platform.system()
                    )
        QMessageBox.about(self, "About ChEsher", msg)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = ChEsher(app)
    myapp.show()
    sys.exit(app.exec_())
