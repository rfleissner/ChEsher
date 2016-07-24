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

import math
import functools
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QFileDialog, QMessageBox

# modules and classes
from uiProfilesDXF import Ui_ProfilesDXF
import uiHandler as uih
import fileHandler as fh
import profileOrganizer as po
import profileWriter as pw
import macro as mc
import numpy as np
import ezdxf
from shapely.geometry import MultiLineString, LineString

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class WrapProfilesDXF():
    """Wrapper for module ProfilesDXF"""

    def __init__(self, dir):
        """Constructor."""

        self.directory = dir

        # setup user interface
        self.widget = QtGui.QWidget()
        self.ui = Ui_ProfilesDXF()
        self.ui.setupUi(self.widget)

#        # inputs
#        self.points = {}
#        self.nodReach = {}
#        self.nodProfiles = {}
#        self.proProfiles = {}
#
#        # results
#        self.reachStation = {}
#        self.profileStation={}
#        self.proArranged = {}
#       
#        self.pointsNormalized = {}
#        self.segmentStation = []
#
#    def setDir(self, directory):
#        self.directory = directory
#        

# module ProfilesDXF

        self.callbackOpenProfilesFile = functools.partial(uih.getOpenFileName, "Open Profiles File", "Line Sets (*.i2s *.i3s)", self.ui.lineEditInputProfiles, self.directory, self.widget)
        QtCore.QObject.connect(self.ui.pushButtonInputProfiles, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackOpenProfilesFile)
        
        self.callbackOpenReachFile = functools.partial(uih.getOpenFileName, "Open Reach File", "Line Sets (*.i2s *.i3s)", self.ui.lineEditInputReach, self.directory, self.widget)
        QtCore.QObject.connect(self.ui.pushButtonInputReach, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackOpenReachFile)

        self.callbackOpenBottomFile = functools.partial(uih.getOpenFileName, "Open T3S-file", "2D T3 Scalar Mesh (ASCII SingleFrame) (*.t3s)", self.ui.lineEditInputBottom, self.directory, self.widget)
        QtCore.QObject.connect(self.ui.pushButtonInputBottom, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackOpenBottomFile)

        QtCore.QObject.connect(self.ui.pushButtonAdd, QtCore.SIGNAL(_fromUtf8("clicked()")), self.add)
        QtCore.QObject.connect(self.ui.pushButtonDelete, QtCore.SIGNAL(_fromUtf8("clicked()")), self.delete)
        QtCore.QObject.connect(self.ui.pushButtonColour, QtCore.SIGNAL(_fromUtf8("clicked()")), self.setColour)
        QtCore.QObject.connect(self.ui.pushButtonInputWaterSurface, QtCore.SIGNAL(_fromUtf8("clicked()")), self.getFileName)
        
        self.ui.tableWidget.setColumnWidth(0, 400)
        header = self.ui.tableWidget.horizontalHeader()
        header.setStretchLastSection(True)

        self.callbackProfiles = functools.partial(uih.setEnabled, self.ui.checkBoxOutputProfiles, self.ui.pushButtonOutputProfiles, self.ui.lineEditOutputProfiles)
        QtCore.QObject.connect(self.ui.checkBoxOutputProfiles, QtCore.SIGNAL("clicked()"), self.callbackProfiles)
        
        self.callbackPlan = functools.partial(uih.setEnabled, self.ui.checkBoxOutputPlan, self.ui.pushButtonOutputPlan, self.ui.lineEditOutputPlan)
        QtCore.QObject.connect(self.ui.checkBoxOutputPlan, QtCore.SIGNAL("clicked()"), self.callbackPlan)
        
        self.callbackSaveProfiles = functools.partial(uih.getSaveFileName, "Save DXF-file As", "Drawing Interchange File (*.dxf)", self.ui.lineEditOutputProfiles, self.directory, self.widget)
        QtCore.QObject.connect(self.ui.pushButtonOutputProfiles, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackSaveProfiles)
        
        self.callbackSavePlan = functools.partial(uih.getSaveFileName, "Save DXF-file As", "Drawing Interchange File (*.dxf)", self.ui.lineEditOutputPlan, self.directory, self.widget)
        QtCore.QObject.connect(self.ui.pushButtonOutputPlan, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackSavePlan)

        QtCore.QObject.connect(self.ui.pushButtonCreate, QtCore.SIGNAL("clicked()"), self.create)
        
    def create(self):
        info = "Input data:\n"

        try:
            self.nodProfiles, self.proProfiles = fh.readI2S(self.ui.lineEditInputProfiles.text())
            info += " - Profiles:\t\t\t{0}\n".format(len(self.proProfiles))
        except:
            QMessageBox.critical(self.widget, "Error", "Not able to load profiles file!\nCheck filename or content!")
            return
        try:
            self.nodReach = fh.readI2S(self.ui.lineEditInputReach.text())[0]
            info += " - Reach nodes:\t\t{0}\n".format(len(self.nodReach))
        except:
            QMessageBox.critical(self.widget, "Error", "Not able to load reach file!\nCheck filename or content!")
            return

        self.proArranged, self.reachStation, self.profileStation, direction = po.determineFlowDirection(self.nodReach, self.nodProfiles, self.proProfiles)
        
        print self.proArranged
        print self.nodProfiles
#        print self.reachStation
#        print self.profileStation
#        print direction
        
        
        info += "\nFlow direction:\n"
        for pID_Arranged in direction:
            info += ' - Profile {0}:\t{1}\n'.format(pID_Arranged, direction[pID_Arranged])

        mesh = fh.readT3StoShapely(self.ui.lineEditInputBottom.text())

        crossSections = {}
#        linestrings = []
        for pID in self.proArranged:
            nodes = []
            for nID in range(len(self.proArranged[pID])):
                node = self.nodProfiles[self.proArranged[pID][nID]]
                nodes.append(node)
                
            crossSection = LineString(nodes)
            intersection = mesh.intersection(crossSection)
            linestrings.append(crossSection)
            
            print intersection
            print len(intersection)
            
            for p in range(len(intersection)):
                print intersection[p]
                
            crossSections[pID] = intersection
            
#        mlinestring = MultiLineString(linestrings)
#        inters = mesh.intersection(mlinestring)
#        print len(inters)

    def add(self):
        row = self.ui.tableWidget.currentRow()
        item = QtGui.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        if row == -1:
            row = 0
        self.ui.tableWidget.insertRow(row)
        self.ui.tableWidget.setItem(row, 2, item)

    def delete(self):
        row = self.ui.tableWidget.currentRow()
        self.ui.tableWidget.removeRow(row)
        
    def setColour(self):
        row = self.ui.tableWidget.currentRow()
        item1 = self.ui.tableWidget.item(row, 2)
        initCol = item1.backgroundColor()
        coldia = QtGui.QColorDialog()
        col = coldia.getColor(initCol)
        if col.isValid():
            item = QtGui.QTableWidgetItem()
            item.setBackground(col)
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            item.setText(str(col.red()) + ", " + str(col.green()) + ", " + str(col.blue()))
            self.ui.tableWidget.setItem(row, 2, item)
        else:
            return     
        
    def getFileName(self):
        row = self.ui.tableWidget.currentRow()
        filetype = ("2D T3 Scalar Mesh (ASCII SingleFrame) (*.t3s)")
        filename = QFileDialog.getOpenFileName(self.widget, "Open T3S-file", self.directory, filetype)

        if filename != "":
            item = QtGui.QTableWidgetItem()
            item.setText(filename)
            self.ui.tableWidget.setItem(row, 0, item)
        
