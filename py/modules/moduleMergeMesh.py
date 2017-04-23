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
__date__ ="$23.04.2017 00:18:42$"

import os
import functools
import sys
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QFileDialog, QMessageBox, QColor

# modules and classes
from uiMergeMesh import Ui_MergeMesh
import uiHandler as uih
import fileHandler as fh

import numpy as np
from shapely.geometry import LineString, Point, MultiPolygon

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class WrapMergeMesh():
    """Wrapper for module MergeMesh"""

    def __init__(self):
        """Constructor."""

        # setup user interface
        self.widget = QtGui.QWidget()
        self.ui = Ui_MergeMesh()
        self.ui.setupUi(self.widget)
        self.directory = os.path.abspath('.')
        
# module MergeMesh

        self.callbackOpenInputMesh = functools.partial(self.getOpenFileName, "Open T3S-file", "2D T3 Scalar Mesh (ASCII SingleFrame) (*.t3s)", self.ui.lineEditInputMesh)
        QtCore.QObject.connect(self.ui.pushButtonInputMesh, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackOpenInputMesh)

        QtCore.QObject.connect(self.ui.pushButtonAdd, QtCore.SIGNAL(_fromUtf8("clicked()")), self.add)
        QtCore.QObject.connect(self.ui.pushButtonDelete, QtCore.SIGNAL(_fromUtf8("clicked()")), self.delete)
        QtCore.QObject.connect(self.ui.pushButtonUp, QtCore.SIGNAL(_fromUtf8("clicked()")), self.moveUp)
        QtCore.QObject.connect(self.ui.pushButtonDown, QtCore.SIGNAL(_fromUtf8("clicked()")), self.moveDown)
        
        QtCore.QObject.connect(self.ui.pushButtonInputSubmesh, QtCore.SIGNAL(_fromUtf8("clicked()")), self.getFileName)
        
        self.callbackTotalMesh = functools.partial(uih.setEnabled, self.ui.checkBoxOutputTotalMesh, self.ui.pushButtonOutputTotalMesh, self.ui.lineEditOutputTotalMesh)
        QtCore.QObject.connect(self.ui.checkBoxOutputTotalMesh, QtCore.SIGNAL("clicked()"), self.callbackTotalMesh)

        self.callbackIntersectionMesh = functools.partial(uih.setEnabled, self.ui.checkBoxOutputIntersectionMesh, self.ui.pushButtonOutputIntersectionMesh, self.ui.lineEditOutputIntersectionMesh)
        QtCore.QObject.connect(self.ui.checkBoxOutputIntersectionMesh, QtCore.SIGNAL("clicked()"), self.callbackIntersectionMesh)
        
        self.callbackOuterMesh = functools.partial(uih.setEnabled, self.ui.checkBoxOutputOuterMesh, self.ui.pushButtonOutputOuterMesh, self.ui.lineEditOutputOuterMesh)
        QtCore.QObject.connect(self.ui.checkBoxOutputOuterMesh, QtCore.SIGNAL("clicked()"), self.callbackOuterMesh)
        
        self.callbackSaveTotalMesh = functools.partial(self.getSaveFileName, "Save Mesh As", "2D T3 Mesh (*.t3s)", self.ui.lineEditOutputTotalMesh)
        QtCore.QObject.connect(self.ui.pushButtonOutputTotalMesh, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackSaveTotalMesh)
        
        self.callbackSaveIntersectionMesh = functools.partial(self.getSaveFileName, "Save Mesh As", "2D T3 Mesh (*.t3s)", self.ui.lineEditOutputIntersectionMesh)
        QtCore.QObject.connect(self.ui.pushButtonOutputIntersectionMesh, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackSaveIntersectionMesh)
        
        self.callbackSaveOuterMesh = functools.partial(self.getSaveFileName, "Save Mesh As", "2D T3 Mesh (*.t3s)", self.ui.lineEditOutputOuterMesh)
        QtCore.QObject.connect(self.ui.pushButtonOutputOuterMesh, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackSaveOuterMesh)

        QtCore.QObject.connect(self.ui.pushButtonCreate, QtCore.SIGNAL("clicked()"), self.create)
    
    def getFileName(self):
        row = self.ui.tableWidget.currentRow()
        filetype = ("2D T3 Scalar Mesh (ASCII SingleFrame) (*.t3s)")
        filename = QFileDialog.getOpenFileName(self.widget, "Open T3S-file", self.directory, filetype)

        if filename != "":
            item = QtGui.QTableWidgetItem()
            item.setText(filename)
            self.ui.tableWidget.setItem(row, 0, item)
            
    def setDir(self, dir):
        self.directory = dir

    def create(self):
    
        info = "Input data:\n"

        try:
            self.nodProfiles, self.proProfiles = fh.readI2S(self.ui.lineEditInputProfiles.text())
            info += " - Profiles:\t\t\t{0}\n".format(len(self.proProfiles))
        except Exception, e:
            QMessageBox.critical(self.widget, "Error", "Not able to load profiles file!\nCheck filename or content!" + "\n\n" + str(e))
            return
        try:
            self.nodReach = fh.readI2S(self.ui.lineEditInputReach.text())[0]
            info += " - Reach nodes:\t\t{0}\n".format(len(self.nodReach))
        except Exception, e:
            QMessageBox.critical(self.widget, "Error", "Not able to load reach file!\nCheck filename or content!" + "\n\n" + str(e))
            return
        try:
            rows = self.ui.tableWidget.rowCount()
            for row in range(rows):
                self.ui.tableWidget.item(row, 0).text()
                self.ui.tableWidget.item(row, 1).text()
                str(self.ui.tableWidget.item(row, 2).text()).split(",")[2]
            info += " - Water surface results:\t{0}\n".format(rows)
        except Exception, e:
            QMessageBox.critical(self.widget, "Error", "Check filename, surface name and colour!" + "\n\n" + str(e))
            return            
                
        self.proArranged, self.reachStation, self.profileStation, direction = po.determineFlowDirection(self.nodReach, self.nodProfiles, self.proProfiles)

        info += "\nFlow direction:\n"
        for pID_Arranged in direction:
            info += ' - Profile {0}:\t{1}\n'.format(pID_Arranged, direction[pID_Arranged])

        # create bottom cross sections
        try:
            bottom, index = fh.readT3StoShapely(self.ui.lineEditInputBottom.text())
            bottomCrossSections = self.getCrossSections(bottom, index)
        except Exception, e:
            QMessageBox.critical(self.widget, "Error", "Not able to interpolate bottom profile!" + "\n\n" + str(e))
            return
        
        # create water surface cross sections
        try:        
            rows = self.ui.tableWidget.rowCount()
            wsCrossSections = {}
            colRGB = {}
            if rows > 0:
                for row in range(rows):
                    filename = self.ui.tableWidget.item(row, 0).text()
                    name = self.ui.tableWidget.item(row, 1).text()
                    watersurface, index = fh.readT3StoShapely(filename)
                    wsCrossSections[name] = self.getCrossSections(watersurface, index)
                    col = Colour(str(self.ui.tableWidget.item(row, 2).text()).split(","))
                    col.create()
                    colRGB[name] = col.getRGB()
        except Exception, e:
            QMessageBox.critical(self.widget, "Error", "Not able to interpolate water surface profiles!" + "\n\n" + str(e))
            return
        
        scale = self.ui.spinBoxScale.value()
        superelevation = self.ui.doubleSpinBoxSuperelevation.value()
        
        info += "\nOutput data:\n"
        
        if self.ui.checkBoxOutputProfiles.isChecked():             
            try:        
                cs = ProfileWriter(self.ui.lineEditOutputProfiles.text(),\
                    bottomCrossSections,
                    self.reachStation,
                    self.profileStation,
                    scale,
                    superelevation,
                    self.settings,
                    self.ui.lineEditInputReachName.text())

                cs.drawBottom()
                cs.drawWaterSurface(wsCrossSections, colRGB)
                cs.saveDXF()

                info += " - DXF file written to {0}.\n".format(self.ui.lineEditOutputProfiles.text())
            except:
                info += " - ERROR: Not able to write profiles!"
                info += "\n"
                info += str(sys.exc_info())
                info += "\n"

        QMessageBox.information(self.widget, "Module ProfilesDXF", info)     

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

    def moveUp(self):
        row = self.ui.tableWidget.currentRow()
        upper_row = row - 1
        if row > 0:
            content_row = self.ui.tableWidget.item(row, 0).text()
            content_upper_row = self.ui.tableWidget.item(upper_row, 0).text()
            
            item1 = QtGui.QTableWidgetItem()
            item1.setText(content_upper_row)
            self.ui.tableWidget.setItem(row, 0, item1)            

            item2 = QtGui.QTableWidgetItem()
            item2.setText(content_row)
            self.ui.tableWidget.setItem(upper_row, 0, item2)       
            
            self.ui.tableWidget.setCurrentCell(upper_row, 0)

    def moveDown(self):
        rows = self.ui.tableWidget.rowCount()
        row = self.ui.tableWidget.currentRow()
        lower_row = row + 1
        if row < rows-1 and row != -1:
            content_row = self.ui.tableWidget.item(row, 0).text()
            content_lower_row = self.ui.tableWidget.item(lower_row, 0).text()
            
            item1 = QtGui.QTableWidgetItem()
            item1.setText(content_lower_row)
            self.ui.tableWidget.setItem(row, 0, item1)            

            item2 = QtGui.QTableWidgetItem()
            item2.setText(content_row)
            self.ui.tableWidget.setItem(lower_row, 0, item2)    

            self.ui.tableWidget.setCurrentCell(lower_row, 0)
            
    def getFileName(self):
        row = self.ui.tableWidget.currentRow()
        filetype = ("2D T3 Scalar Mesh (ASCII SingleFrame) (*.t3s)")
        filename = QFileDialog.getOpenFileName(self.widget, "Open T3S-file", self.directory, filetype)

        if filename != "":
            item = QtGui.QTableWidgetItem()
            item.setText(filename)
            self.ui.tableWidget.setItem(row, 0, item)
        
    def initialize(self):

#        dir = "C:/opentelemac/simulation/sulz/Profile/"
#  
#        ###   ~   module ProfilesDXF   ~   ###
#
#        self.ui.lineEditInputProfiles.setText(dir + "profiles.i2s")
#        self.ui.lineEditInputReach.setText(dir + "reach.i2s")
#        self.ui.lineEditInputBottom.setText(dir + "BOTTOM(Subset).t3s")
#        self.ui.lineEditInputReachName.setText("Glawoggenbach")
#        self.ui.spinBoxScale.setValue(200)
#        self.ui.doubleSpinBoxSuperelevation.setValue(2.0)
#        
#        self.ui.tableWidget.setRowCount(0)
#        self.add()
#        self.add()
#        
#        item1 = QtGui.QTableWidgetItem()
#        item1.setText(dir + "S_HQ30_IST(Subset).t3s")
#        self.ui.tableWidget.setItem(0, 0, item1)
#        
#        item2 = QtGui.QTableWidgetItem()
#        item2.setText("HQ30 IST [m]")
#        self.ui.tableWidget.setItem(0, 1, item2)
#
#        item3 = QtGui.QTableWidgetItem()
#        item3.setText(dir + "S_HQ100_IST(Subset).t3s")
#        self.ui.tableWidget.setItem(1, 0, item3)
#
#        item4 = QtGui.QTableWidgetItem()
#        item4.setText("HQ100 IST [m]")
#        self.ui.tableWidget.setItem(1, 1, item4)
#
#        initCol = item2.backgroundColor()
#        initCol.setRed(255)
#        initCol.setGreen(127)
#        initCol.setBlue(223)
#        item5 = QtGui.QTableWidgetItem()
#        item5.setBackground(initCol)
#        item5.setFlags(QtCore.Qt.ItemIsEnabled)
#        item5.setText(str(initCol.red()) + ", " + str(initCol.green()) + ", " + str(initCol.blue()))
#        self.ui.tableWidget.setItem(0, 2, item5)
#
#        initCol = item4.backgroundColor()
#        initCol.setRed(0)
#        initCol.setGreen(191)
#        initCol.setBlue(255)
#        item6 = QtGui.QTableWidgetItem()
#        item6.setBackground(initCol)
#        item6.setFlags(QtCore.Qt.ItemIsEnabled)
#        item6.setText(str(initCol.red()) + ", " + str(initCol.green()) + ", " + str(initCol.blue()))
#        self.ui.tableWidget.setItem(1, 2, item6)
#        
#        uih.setEnabledInitialize(self.ui.checkBoxOutputProfiles, self.ui.pushButtonOutputProfiles, self.ui.lineEditOutputProfiles)
#        self.ui.lineEditOutputProfiles.setText(dir + "profiles.dxf")
#        
        
        import os
        abs_path = os.path.abspath('.')
        dir = os.path.join(abs_path, 'examples/').replace('\\', '/')
  
        ###   ~   module ProfilesDXF   ~   ###

        self.ui.lineEditInputMesh.setText(dir + "example_16/mesh.t3s")

        self.ui.tableWidget.setRowCount(0)
        self.add()
        self.add()
        
        item1 = QtGui.QTableWidgetItem()
        item1.setText(dir + "example_16/submesh_1.t3s")
        self.ui.tableWidget.setItem(0, 0, item1)

        item2 = QtGui.QTableWidgetItem()
        item2.setText(dir + "example_16/submesh_2.t3s")
        self.ui.tableWidget.setItem(1, 0, item2)

        uih.setEnabledInitialize(self.ui.checkBoxOutputTotalMesh, self.ui.pushButtonOutputTotalMesh, self.ui.lineEditOutputTotalMesh)
        self.ui.lineEditOutputTotalMesh.setText(dir + "example_16/output/mesh_total.t3s")

        uih.setEnabledInitialize(self.ui.checkBoxOutputIntersectionMesh, self.ui.pushButtonOutputIntersectionMesh, self.ui.lineEditOutputIntersectionMesh)
        self.ui.lineEditOutputIntersectionMesh.setText(dir + "example_16/output/mesh_intersection.t3s")
        
        uih.setEnabledInitialize(self.ui.checkBoxOutputOuterMesh, self.ui.pushButtonOutputOuterMesh, self.ui.lineEditOutputOuterMesh)
        self.ui.lineEditOutputOuterMesh.setText(dir + "example_16/output/mesh_outer.t3s")
        
    def getOpenFileName(self, title, fileFormat, lineEdit):
        filename = QFileDialog.getOpenFileName(self.widget, title, self.directory, fileFormat)
        if filename != "":
            lineEdit.setText(filename)

    def getSaveFileName(self, title, fileFormat, lineEdit):
        filename = QFileDialog.getSaveFileName(self.widget, title, self.directory, fileFormat)
        if filename != "":
            lineEdit.setText(filename)