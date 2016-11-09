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

import functools
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QFileDialog, QMessageBox, QDialog, QColor

# modules and classes
from uiProfilesDXF import Ui_ProfilesDXF
from profileSettings import WrapProfileSettings
from colourHandler import Colour
from matplotlib import colors
import uiHandler as uih
import fileHandler as fh
import profileOrganizer as po
#import profileWriter as pw
from profileWriter import ProfileWriter
import numpy as np
import copy
from shapely.geometry import LineString, Point

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

        self.settings = {}
        self.settings["Frame"] = True
        self.settings["Band"] = True
        self.settings["ProfileName"] = "Cross section "
        self.settings["ReachStation"] = "km "
        self.settings["ScaleFactor"] = "Scale = "
        self.settings["ReferenceLevel"] = "RL = "
        self.settings["BandTitleStationing"] = "Station [m]"
        self.settings["BandTitleElevation"] = "Elevation [m]"
        self.settings["DecimalPlaces"] = 2
        self.settings["doubleSpinBoxOffsetX"] = 75.0
        self.settings["doubleSpinBoxOffsetZ"] = 2.5
        self.settings["doubleSpinBoxBandHeight"] = 15.0
        self.settings["doubleSpinBoxTextSizeBandTitle"] = 4.0
        self.settings["doubleSpinBoxTextSizeBand"] = 1.5
        self.settings["doubleSpinBoxMarkerSize"] = 1.5
        self.settings["doubleSpinBoxCleanValues"] = 0.0
        
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
        
        defaults = ["Template A", "Template B", "Template C"]
        self.ui.comboBoxDefault.addItems(defaults)        
        QtCore.QObject.connect(self.ui.pushButtonDefault, QtCore.SIGNAL(_fromUtf8("clicked()")), self.setDefault)
        
        QtCore.QObject.connect(self.ui.pushButtonProfileSettings, QtCore.SIGNAL("clicked()"), self.setSettings)
        
        QtCore.QObject.connect(self.ui.pushButtonCreate, QtCore.SIGNAL("clicked()"), self.create)

    def setDir(self, directory):
        self.directory = copy.copy(directory)
    
    def applyDefaults(self, dataSets, colHexRGB):

        nLevels = len(dataSets)-1

        self.ui.tableWidget.setRowCount(nLevels)
        print "apply", self.directory
        for row in range(nLevels):
            item1 = QtGui.QTableWidgetItem()
            item1.setText(self.directory + str(dataSets[row]))
            self.ui.tableWidget.setItem(row, 0, item1)
            
            item2 = QtGui.QTableWidgetItem()
            item2.setText(str(dataSets[row]))
            self.ui.tableWidget.setItem(row, 1, item2)

            col = colors.hex2color(colHexRGB[row])
            colPy = QColor(int(col[0]*255),int(col[1]*255),int(col[2]*255))
            item3 = QtGui.QTableWidgetItem()
            item3.setBackground(colPy)
            item3.setFlags(QtCore.Qt.ItemIsEnabled)
            item3.setText(str(colPy.red()) + ", " + str(colPy.green()) + ", " + str(colPy.blue()))
            self.ui.tableWidget.setItem(row, 2, item3)
            
    def setDefault(self):
        
        def RGB2HEX(RGB):
            
            HEX = []
            for i in range(len(RGB)):
                col = Colour(str(RGB[i]).split(","))
                col.create()
                HEX.append(col.getHexRGB())
                
            return HEX
        
        template = self.ui.comboBoxDefault.currentIndex()

        # Template A
        if template == 0:

            dataSets = ["HQ30 IST", "HQ30 ZUK", "HQ100 IST", "HQ100 ZUK", "HQ300 IST", "HQ300 ZUK"]
            col_RGB = ["190,232,255","116,179,255","55,141,255","18,107,238","0,77,168","232,190,255"]
            col_HEX = RGB2HEX(col_RGB)
            
            self.applyDefaults(dataSets, col_HEX)

            self.settings = {}
            self.settings["Frame"] = True
            self.settings["Band"] = True
            self.settings["ProfileName"] = "Profil Nr. "
            self.settings["ReachStation"] = "km "
            self.settings["ScaleFactor"] = "Massstab = "
            self.settings["ReferenceLevel"] = "VE = "
            self.settings["BandTitleStationing"] = "Stationierung [m]"
            self.settings["BandTitleElevation"] = "Gelaendehoehe [m]"
            self.settings["DecimalPlaces"] = 2
            self.settings["doubleSpinBoxOffsetX"] = 75.0
            self.settings["doubleSpinBoxOffsetZ"] = 2.5
            self.settings["doubleSpinBoxBandHeight"] = 15.0
            self.settings["doubleSpinBoxTextSizeBandTitle"] = 4.0
            self.settings["doubleSpinBoxTextSizeBand"] = 1.5
            self.settings["doubleSpinBoxMarkerSize"] = 1.5
            self.settings["doubleSpinBoxCleanValues"] = 0.0
        
        # Template B
        if template == 1:

            dataSets = ["HQ30", "HQ100"]
            col_RGB = ["190,232,255","116,179,255"]
            col_HEX = RGB2HEX(col_RGB)
            
            self.applyDefaults(dataSets, col_HEX)

            self.settings["Frame"] = True
            self.settings["Band"] = True
            self.settings["ProfileName"] = "Cross section "
            self.settings["ReachStation"] = "km "
            self.settings["ScaleFactor"] = "Scale = "
            self.settings["ReferenceLevel"] = "RL = "
            self.settings["BandTitleStationing"] = "Station [m]"
            self.settings["BandTitleElevation"] = "Elevation [m]"
            self.settings["DecimalPlaces"] = 2
            self.settings["doubleSpinBoxOffsetX"] = 75.0
            self.settings["doubleSpinBoxOffsetZ"] = 2.5
            self.settings["doubleSpinBoxBandHeight"] = 15.0
            self.settings["doubleSpinBoxTextSizeBandTitle"] = 4.0
            self.settings["doubleSpinBoxTextSizeBand"] = 1.5
            self.settings["doubleSpinBoxMarkerSize"] = 1.5
            self.settings["doubleSpinBoxCleanValues"] = 0.0

            
    def getCrossSections(self, mesh):

        crossSections = dict((key, np.array([])) for key in self.proArranged)

        for pID in self.proArranged:
            
            nodes = []
            for nID in range(len(self.proArranged[pID])):
                node = self.nodProfiles[self.proArranged[pID][nID]]
                nodes.append(node)

            crossSection = LineString(nodes)

            intersection = mesh.intersection(crossSection)

            values = []
            for p in range(len(intersection)):
                intersection_ = intersection[p]

                if intersection_.geom_type == "Point":
                    inters = crossSection.project(intersection_)
                    values.append([intersection_.x, intersection_.y, intersection_.z, inters])
                elif intersection_.geom_type == "LineString":
                    for i in range(len(intersection_.coords)):
                        pt = Point(intersection_.coords[i])
                        inters = crossSection.project(pt)             
                        values.append([pt.x, pt.y, pt.z, inters])

            arr = np.array(values)
            arr = arr[arr[:,3].argsort()]
            arr.reshape((arr.size/4,4))

            x = arr[:,0]
            y = arr[:,1]
            z = arr[:,2]
            d = arr[:,3]

            crossSections[pID] = [x,y,z,d]
            print "cross section", pID, "done"
        return crossSections
    
    
    def setSettings(self):

        settings = WrapProfileSettings(self.settings)
        settings.setSettings()
    
        if settings.exec_():
            self.settings = settings.getSettings()
            print "settings set"
            print self.settings

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
        try:
            rows = self.ui.tableWidget.rowCount()
            for row in range(rows):
                self.ui.tableWidget.item(row, 0).text()
                self.ui.tableWidget.item(row, 1).text()
                str(self.ui.tableWidget.item(row, 2).text()).split(",")[2]
        except:
            QMessageBox.critical(self.widget, "Error", "Check filename, surface name and colour!")
            return            
                
        self.proArranged, self.reachStation, self.profileStation, direction = po.determineFlowDirection(self.nodReach, self.nodProfiles, self.proProfiles)
        
#        print self.proArranged
#        print self.nodProfiles
#        print self.reachStation
#        print self.profileStation
#        print direction

        info += "\nFlow direction:\n"
        for pID_Arranged in direction:
            info += ' - Profile {0}:\t{1}\n'.format(pID_Arranged, direction[pID_Arranged])

        # create bottom cross sections
        bottom = fh.readT3StoShapely(self.ui.lineEditInputBottom.text())
        bottomCrossSections = self.getCrossSections(bottom)
        
        # create water surface cross sections
        rows = self.ui.tableWidget.rowCount()
        wsCrossSections = {}
        colRGB = {}
        if rows > 0:
            for row in range(rows):
                filename = self.ui.tableWidget.item(row, 0).text()
                name = self.ui.tableWidget.item(row, 1).text()
                watersurface = fh.readT3StoShapely(filename)
                wsCrossSections[name] = self.getCrossSections(watersurface)
                col = Colour(str(self.ui.tableWidget.item(row, 2).text()).split(","))
                col.create()
                colRGB[name] = col.getRGB()

        print wsCrossSections
        
        scale = self.ui.spinBoxScale.value()
        superelevation = self.ui.doubleSpinBoxSuperelevation.value()
        
        if self.ui.checkBoxOutputProfiles.isChecked():
            cs = ProfileWriter(self.ui.lineEditOutputProfiles.text(),\
                bottomCrossSections,
                self.reachStation,
                self.profileStation,
                scale,
                superelevation,
                self.settings)
            
            cs.drawBottom()
            cs.drawWaterSurface(wsCrossSections, colRGB)
            cs.saveDXF()
            
#
#            pw.writeProfile(self.ui.lineEditOutputProfiles.text(),\
#                bottomCrossSections,
#                self.reachStation,
#                self.profileStation
#            )                

        print "finish"

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
        
    def initialize(self):
        
        import os
        abs_path = os.path.abspath('.')
        dir = os.path.join(abs_path, 'examples/').replace('\\', '/')
  
        ###   ~   module ProfilesDXF   ~   ###
        
        self.ui.lineEditInputProfiles.setText(dir + "example_15/profiles.i2s")
        self.ui.lineEditInputReach.setText(dir + "example_15/reach.i2s")
        self.ui.lineEditInputBottom.setText(dir + "example_15/BOTTOM_Case_A.t3s")
        self.ui.lineEditInputReachName.setText("Donau")

        self.ui.tableWidget.setRowCount(0)
        self.add()
        self.add()
        
        item1 = QtGui.QTableWidgetItem()
        item1.setText(self.directory + "example_15/FREE SURFACE_S161_Case_A.t3s")
        self.ui.tableWidget.setItem(0, 0, item1)
        
        item2 = QtGui.QTableWidgetItem()
        item2.setText("HQ100 Case A")
        self.ui.tableWidget.setItem(0, 1, item2)

        item3 = QtGui.QTableWidgetItem()
        item3.setText(self.directory + "example_15/FREE SURFACE_S161_Case_B.t3s")
        self.ui.tableWidget.setItem(1, 0, item3)

        item4 = QtGui.QTableWidgetItem()
        item4.setText("HQ100 Case B")
        self.ui.tableWidget.setItem(1, 1, item4)

        item3 = self.ui.tableWidget.item(0, 2)
        initCol = item3.backgroundColor()
        initCol.setRed(200)
        initCol.setGreen(200)
        initCol.setBlue(255)
        item3 = QtGui.QTableWidgetItem()
        item3.setBackground(initCol)
        item3.setFlags(QtCore.Qt.ItemIsEnabled)
        item3.setText(str(initCol.red()) + ", " + str(initCol.green()) + ", " + str(initCol.blue()))
        self.ui.tableWidget.setItem(0, 2, item3)

        uih.setEnabledInitialize(self.ui.checkBoxOutputProfiles, self.ui.pushButtonOutputProfiles, self.ui.lineEditOutputProfiles)
        self.ui.lineEditOutputProfiles.setText(self.directory + "example_15/output/profiles.dxf")