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

import os
import sys
import platform
import webbrowser

lib_modules = os.path.abspath(os.path.join('py/modules'))
lib_ui = os.path.abspath(os.path.join('py/ui'))
lib_py = os.path.abspath(os.path.join('py/py'))

sys.path.append(lib_modules)
sys.path.append(lib_ui)
sys.path.append(lib_py)

from moduleDXF2BK import WrapDXF2BK
from moduleBK2DXF import WrapBK2DXF
from moduleMesh import WrapMesh
from moduleLandXML import WrapLandXML
from moduleScalarDXF import WrapScalarDXF
from moduleVectorDXF import WrapVectorDXF
from moduleCS import WrapCS
from module2DM2BK import Wrap2DM2BK
from moduleCont2DXF import WrapCont2DXF
from moduleTube import WrapTube
from moduleHyDesign import WrapHyDesign
from moduleXYZ2Profiles import WrapXYZ2Profiles
from moduleHEC2DXF import WrapHEC2DXF
from moduleXYZ2DXF import WrapXYZ2DXF
from moduleProfilesDXF import WrapProfilesDXF
from moduleMergeMesh import WrapMergeMesh

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QFileDialog, QAction, QMessageBox, QIcon, QMessageBox
from PyQt4.QtCore import PYQT_VERSION_STR, QT_VERSION_STR, Qt, SIGNAL

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

        # setup instance of module DXF2BK
        self.moduleDXF2BK = WrapDXF2BK()
        self.widgetDXF2BK = self.moduleDXF2BK.widget
        self.ui.stackedWidget.insertWidget(0, self.widgetDXF2BK)        

        # setup instance of module BK2DXF
        self.moduleBK2DXF = WrapBK2DXF()
        self.widgetBK2DXF = self.moduleBK2DXF.widget
        self.ui.stackedWidget.insertWidget(1, self.widgetBK2DXF)   

        # setup instance of module Mesh
        self.moduleMesh = WrapMesh()
        self.widgetMesh = self.moduleMesh.widget
        self.ui.stackedWidget.insertWidget(2, self.widgetMesh)   

        # setup instance of module LandXML
        self.moduleLandXML = WrapLandXML()
        self.widgetLandXML = self.moduleLandXML.widget
        self.ui.stackedWidget.insertWidget(3, self.widgetLandXML)   
        
        # setup instance of module ScalarDXF
        self.moduleScalarDXF = WrapScalarDXF()
        self.widgetScalarDXF = self.moduleScalarDXF.widget
        self.ui.stackedWidget.insertWidget(4, self.widgetScalarDXF)  

        # setup instance of module VectorDXF
        self.moduleVectorDXF = WrapVectorDXF()
        self.widgetVectorDXF = self.moduleVectorDXF.widget
        self.ui.stackedWidget.insertWidget(5, self.widgetVectorDXF)  

        # setup instance of module CS
        self.moduleCS = WrapCS()
        self.widgetCS = self.moduleCS.widget
        self.ui.stackedWidget.insertWidget(6, self.widgetCS)  

        # setup instance of module 2DM2BK
        self.module2DM2BK = Wrap2DM2BK()
        self.widget2DM2BK = self.module2DM2BK.widget
        self.ui.stackedWidget.insertWidget(7, self.widget2DM2BK)  

        # setup instance of module Cont2DXF
        self.moduleCont2DXF = WrapCont2DXF()
        self.widgetCont2DXF = self.moduleCont2DXF.widget
        self.ui.stackedWidget.insertWidget(8, self.widgetCont2DXF)  
        
        # setup instance of module Tube
        self.moduleTube = WrapTube()
        self.widgetTube = self.moduleTube.widget
        self.ui.stackedWidget.insertWidget(9, self.widgetTube)  

        # setup instance of module XYZ2Profiles
        self.moduleXYZ2Profiles = WrapXYZ2Profiles()
        self.widgetXYZ2Profiles = self.moduleXYZ2Profiles.widget
        self.ui.stackedWidget.insertWidget(10, self.widgetXYZ2Profiles)    

        # setup instance of module ProfilesDXF
        self.moduleProfilesDXF = WrapProfilesDXF()
        self.widgetProfilesDXF = self.moduleProfilesDXF.widget
        self.ui.stackedWidget.insertWidget(11, self.widgetProfilesDXF)   
        
        # setup instance of module HEC2DXF
        self.moduleHEC2DXF = WrapHEC2DXF()
        self.widgetHEC2DXF = self.moduleHEC2DXF.widget
        self.ui.stackedWidget.insertWidget(12, self.widgetHEC2DXF)  
        
        # setup instance of module XYZ2DXF
        self.moduleXYZ2DXF = WrapXYZ2DXF()
        self.widgetXYZ2DXF = self.moduleXYZ2DXF.widget
        self.ui.stackedWidget.insertWidget(13, self.widgetXYZ2DXF)                

        # setup instance of module HyDesign
        self.moduleMergeMesh = WrapMergeMesh()
        self.widgetMergeMesh = self.moduleMergeMesh.widget
        self.ui.stackedWidget.insertWidget(14, self.widgetMergeMesh)
        
        # setup instance of module HyDesign
        self.moduleHyDesign = WrapHyDesign()
        self.widgetHyDesign = self.moduleHyDesign.widget
        self.ui.stackedWidget.insertWidget(15, self.widgetHyDesign)
        
        # actions in menu
        self.fileSetDirectory = self.createAction("Set working directory", slot=self.setDirectory)
        self.fileQuitAction = self.createAction("Close", slot=self.close, \
            shortcut="Ctrl+Q")
        self.fileSetExamples = self.createAction("Initialize examples", slot=self.initializeModules)
        self.helpAction = self.createAction("Help", slot=self.help, shortcut="F1")
        # modules
        self.setDXFtoBKAction = self.createAction("1 DXF2BK", slot=self.setDXF2BK)
        self.setBK2DXFAction = self.createAction("2 BK2DXF", slot=self.setBK2DXF)
        self.setMeshAction = self.createAction("3 Mesh", slot=self.setMesh)
        self.setXMLAction = self.createAction("4 LandXML", slot=self.setLandXML)
        self.setScalarAction = self.createAction("5 ScalarDXF", slot=self.setScalarDXF)
        self.setVectorAction = self.createAction("6 VectorDXF", slot=self.setVectorDXF)
        self.setCSAction = self.createAction("7 CS", slot=self.setCS)
        self.set2DMAction = self.createAction("8 2DM2BK", slot=self.set2DM2BK)
        self.setCont2DXFAction = self.createAction("9 Cont2DXF", slot=self.setCont2DXF)
        self.setTubeAction = self.createAction("10 Tube", slot=self.setTube)
        self.setProfilesAction = self.createAction("11 XYZ2Profiles", slot=self.setXYZ2Profiles)
        self.setProfilesDXFAction = self.createAction("12 ProfilesDXF", slot=self.setProfilesDXF)
        self.setHEC2DXFAction = self.createAction("13 HEC2DXF", slot=self.setHEC2DXF)
        self.setXYZ2DXFAction = self.createAction("14 XYZ2DXF", slot=self.setXYZ2DXF) 
        self.setMergeMeshAction = self.createAction("15 MergeMesh", slot=self.setMergeMesh)
        # tools
        self.setHyDesignAction = self.createAction("1 HyDesign", slot=self.setHyDesign)
        # help
        self.helpAboutAction = self.createAction("&About", \
            self.helpAbout)
        
        # create menu
        self.fileMenu = self.menuBar().addMenu("ChEsher")
        self.modulesMenu = self.menuBar().addMenu("Modules")
        self.toolsMenu = self.menuBar().addMenu("Tools")
        self.helpMenu = self.menuBar().addMenu("Help")
        
        # add actions to menu
        self.addActions(self.fileMenu, ( \
            self.fileSetDirectory, 
            self.fileSetExamples, 
            None, 
            self.fileQuitAction
            ))
            
        self.addActions(self.modulesMenu, ( \
            self.setDXFtoBKAction, \
            self.setBK2DXFAction,
            self.setMeshAction, 
            self.setXMLAction, 
            self.setScalarAction, 
            self.setVectorAction, 
            self.setCSAction, 
            self.set2DMAction,
            self.setCont2DXFAction,
            self.setTubeAction,
            self.setProfilesAction,
            self.setProfilesDXFAction,
            self.setHEC2DXFAction,
            self.setXYZ2DXFAction,
            self.setMergeMeshAction
            ))

        self.addActions(self.toolsMenu, ( \
            self.setHyDesignAction,
            ))
            
        self.addActions(self.helpMenu, (self.helpAction, None, self.helpAboutAction))

#        self.setDXF2BK()
        self.setMesh()
#        self.setCont2DXF()
#        self.setTube()
#        self.setHEC2DXF()
#        self.setXYZ2Profiles()
#        self.setProfilesDXF()
#        self.setXYZ2DXF()
        self.initialize()
#        self.setMergeMesh()
#        self.setScalarDXF()

    def setType(self):
        self.calcDischarge()
        self.updateUi()
  
    def initializeModules(self):
        answer = QMessageBox.question(self, "Initialize examples", "Do you really want to overwrite all inputs to initialize examples?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        if answer == QtGui.QMessageBox.Yes:
            self.initialize()
        elif answer == QtGui.QMessageBox.No:
            return
        
    def initialize(self):
        
        def makedir(dir):
            if not os.path.exists(dir):
                os.makedirs(dir)
        
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
        makedir(self.directory + "example_11/output/")
        makedir(self.directory + "example_12/output/")
        makedir(self.directory + "example_13/output/")
        makedir(self.directory + "example_14/output/")
        makedir(self.directory + "example_15/output/")
        
        self.moduleDXF2BK.initialize()
        self.moduleBK2DXF.initialize()
        self.moduleMesh.initialize()
        self.moduleLandXML.initialize()
        self.moduleScalarDXF.initialize()
        self.moduleVectorDXF.initialize()   
        self.moduleCS.initialize()
        self.module2DM2BK.initialize()
        self.moduleCont2DXF.initialize()
        self.moduleTube.initialize()
        self.moduleXYZ2Profiles.initialize()
        self.moduleProfilesDXF.initialize()
        self.moduleHEC2DXF.initialize()
        self.moduleXYZ2DXF.initialize()
        self.moduleMergeMesh.initialize()
        
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

    def setXYZ2Profiles(self):
        self.ui.labelModule.setText("~   Module XYZ2Profiles   ~")
        self.ui.stackedWidget.setCurrentIndex(10)
        
    def setProfilesDXF(self):
        self.ui.labelModule.setText("~   Module ProfilesDXF   ~")
        self.ui.stackedWidget.setCurrentIndex(11)
        
    def setHEC2DXF(self):
        self.ui.labelModule.setText("~   HEC2DXF   ~")
        self.ui.stackedWidget.setCurrentIndex(12)
        
    def setXYZ2DXF(self):
        self.ui.labelModule.setText("~   XYZ2DXF   ~")
        self.ui.stackedWidget.setCurrentIndex(13)
 
    def setMergeMesh(self):
        self.ui.labelModule.setText("~   Module MergeMesh   ~")
        self.ui.stackedWidget.setCurrentIndex(14)
        
    def setHyDesign(self):
        self.ui.labelModule.setText("~   Tool HyDesign   ~")
        self.ui.stackedWidget.setCurrentIndex(15)

    def setDirectory(self):
        
        dir = QFileDialog.getExistingDirectory(self, "Select directory", self.directory)
        
        if dir != "":
            
            self.moduleDXF2BK.setDir(dir)
            self.moduleBK2DXF.setDir(dir)
            self.moduleMesh.setDir(dir)
            self.moduleLandXML.setDir(dir)
            self.moduleScalarDXF.setDir(dir)
            self.moduleVectorDXF.setDir(dir)
            self.moduleCS.setDir(dir)
            self.module2DM2BK.setDir(dir)
            self.moduleCont2DXF.setDir(dir)
            self.moduleTube.setDir(dir)
            self.moduleProfilesDXF.setDir(dir)
            self.moduleHEC2DXF.setDir(dir)
            self.moduleXYZ2DXF.setDir(dir)
            self.moduleXYZ2Profiles.setDir(dir)
            self.moduleMergeMesh.setDir(dir)
            
            self.directory = dir

        else:
            return

#    def interpolatePoint(self, xa, ya, za, xb, yb, zb, xc, yc, zc, xp, yp):
#        dot1 = (yb - ya)*(xp - xa) + (-xb + xa)*(yp - ya)
#        dot2 = (yc - yb)*(xp - xb) + (-xc + xb)*(yp - yb)
#        dot3 = (ya - yc)*(xp - xc) + (-xa + xc)*(yp - yc)
#
#        zp = 0.0
#        counter = 0 
#        if dot1 <= 0.0 and dot2 <= 0.0 and dot3 <= 0.0:
#
#            #Determine two vectors from the points:
#            v1 = [xc - xa, yc - ya, zc - za]
#            v2 = [xb - xa, yb - ya, zb - za]
#
#            #Determine the cross product of the two vectors:
#            cp = [v1[1] * v2[2] - v1[2] * v2[1],
#                  v1[2] * v2[0] - v1[0] * v2[2],
#                  v1[0] * v2[1] - v1[1] * v2[0]]
#
#            #A plane can be described using a simple equation ax + by + cz = d. The three coefficients from the cross product are a, b and c, and d can be solved by substituting a known point, for example the first:
#            a, b, c = cp
#            d = a * xa + b * ya + c * za
#
#            #Determine the z value at x, y. Re-arrange the simple equation, and solve for z:
#            zp = (d - a * xp - b * yp) / float(c)            
#            counter = 1
#        else:
#            counter = 0
#        return zp, counter
#    
#    def insideBoundingBox(self, xa, ya, xb, yb, xc, yc, xp, yp):
#
#        xMin = min([xa, xb, xc])
#        xMax = max([xa, xb, xc])
#        yMin = min([ya, yb, yc])
#        yMax = max([ya, yb, yc])
#
#        if xp >= xMin and xp <= xMax and yp >= yMin and yp <= yMax:
#            return True
#        else:
#            return False
#
#    def getTriangles(self, mesh, nodesMajor, nodesMinor):
#
#        x = []
#        y = []
#        zMajor = []
#        zMinor = []
#        
#        triangles = []
#        for nID in nodesMajor:
#            x.append(nodesMajor[nID][0])
#            y.append(nodesMajor[nID][1])
#            zMajor.append(nodesMajor[nID][2])
#            if nodesMinor is not None:
#                zMinor.append(nodesMinor[nID][2])
# 
#        for eID in mesh:
#            n1 = mesh[eID][0]-1
#            n2 = mesh[eID][1]-1
#            n3 = mesh[eID][2]-1
#            triangles.append([n1,n2,n3])
#              
#        return x, y, zMajor, zMinor, triangles
    
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
        msg = u"""<p><b>ChEsher</b> V 1.1</p>
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
