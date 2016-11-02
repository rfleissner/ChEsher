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
from uiDXF2BK import Ui_DXF2BK
import uiHandler as uih
import fileHandler as fh

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class WrapDXF2BK():
    """Wrapper for module DXF2BK"""

    def __init__(self, dir):
        """Constructor."""

        self.directory = dir

        # setup user interface
        self.widget = QtGui.QWidget()
        self.ui = Ui_DXF2BK()
        self.ui.setupUi(self.widget)

# module DXF2BK

        self.callbackOpenDXFFile = functools.partial(uih.getOpenFileName, "Open DXF-file", "Drawing Interchange File (*.dxf)", self.ui.lineEditInput, self.directory, self.widget)
        QtCore.QObject.connect(self.ui.pushButtonInput, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackOpenDXFFile)

        QtCore.QObject.connect(self.ui.pushButtonAdd, QtCore.SIGNAL(_fromUtf8("clicked()")), self.addLayer)
        QtCore.QObject.connect(self.ui.pushButtonDelete, QtCore.SIGNAL(_fromUtf8("clicked()")), self.deleteLayer)

        QtCore.QObject.connect(self.ui.pushButtonOpen, QtCore.SIGNAL(_fromUtf8("clicked()")), self.getSaveLayerName)
        QtCore.QObject.connect(self.ui.pushButtonRefresh, QtCore.SIGNAL("clicked()"), self.refreshDXF)
        QtCore.QObject.connect(self.ui.pushButtonCreate, QtCore.SIGNAL("clicked()"), self.create)

        header = self.ui.tableWidget.horizontalHeader()
        header.setStretchLastSection(True)

    def setDir(self, directory):
        self.directory = directory
        print "set", self.directory
    
    def addLayer(self):
        dropdownLayer = QtGui.QComboBox(self.widget)
        
        rows = self.ui.tableWidget.rowCount()

        self.ui.tableWidget.insertRow(rows)
        self.ui.tableWidget.setCellWidget(rows, 0, dropdownLayer)
        item = QtGui.QTableWidgetItem()
        item.setText("")
        self.ui.tableWidget.setItem(rows, 1, item)

    def deleteLayer(self):
        row = self.ui.tableWidget.currentRow()
        self.ui.tableWidget.removeRow(row)
        
    def refreshDXF(self):
        
        filename = self.ui.lineEditInput.text()
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
        rows = self.ui.tableWidget.rowCount()
        if rows > 0:
            for row in range(rows):
                combobox = self.ui.tableWidget.cellWidget(row, 0)
                temp = u"{0}".format(combobox.itemText(combobox.currentIndex()))
                combobox.clear()
                combobox.setInsertPolicy(6)
                combobox.addItems(sorted_layers)
                if temp in sorted_layers:
                    combobox.setCurrentIndex(sorted_layers.index(temp))
                else:
                    combobox.setCurrentIndex(combobox.findText("0"))
                self.ui.tableWidget.setCellWidget(rows, 0, combobox)
                
    def create(self):
        
        info = ""
        rows = self.ui.tableWidget.rowCount()
        if rows > 0:
            for row in range(rows):
                combobox = self.ui.tableWidget.cellWidget(row, 0)

                filename = self.ui.tableWidget.item(row, 1).text()
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
                        QMessageBox.critical(self.widget, "Module DXF2BK", 'Type *.i2s: ' + str(e))
                elif type == "i3s":
                    try:
                        nodes, strings = fh.readDXF(self.dxf, layer)
                        fh.writeI3S(nodes, strings, filename)
                        info += " - {0} object(s) from type *.i3s converted to file \n\t{1}\n".format(len(strings), filename)
                    except Exception, e:
                        QMessageBox.critical(self.widget, "Module DXF2BK", 'Type *.i3s: ' + str(e))
                elif type == "xyz":
                    try:
                        nodes, strings = fh.readDXF(self.dxf, layer)
                        fh.writeXYZ(nodes, filename)
                        info += " - {0} object(s) from type *.xyz converted to file \n\t{1}\n".format(len(nodes), filename)
                    except Exception, e:
                        QMessageBox.critical(self.widget, "Module DXF2BK", 'Type *.xyz: ' + str(e))
                else:
                    continue                
        QMessageBox.information(self.widget, "Module DXF2BK", info)

    def getFileName(self):
        row = self.ui.tableWidget.currentRow()
        filetype = ("2D T3 Scalar Mesh (ASCII SingleFrame) (*.t3s)")
        filename = QFileDialog.getOpenFileName(self.widget, "Open T3S-file", self.directory, filetype)

        if filename != "":
            item = QtGui.QTableWidgetItem()
            item.setText(filename)
            self.ui.tableWidget.setItem(row, 0, item)
        
    def openDXFFile(self, title, fileFormat, lineEdit):
        
        filename = QFileDialog.getOpenFileName(self, title, self.directory, fileFormat)
        if filename == "": return
        lineEdit.setText(filename)
        self.refreshDXF()

    def getSaveLayerName(self):
        print "dir", self.directory
        row = self.ui.tableWidget.currentRow()
        filetype = ("2D Line Set (*.i2s);;3D Line Set (*.i3s);;Point Set (*.xyz)")
        filename = QFileDialog.getSaveFileName(self.widget, "Save Layer As", self.directory, filetype)

        if filename != "":
            item = QtGui.QTableWidgetItem()
            item.setText(filename)
            self.ui.tableWidget.setItem(row, 1, item)
    
    def initialize(self):
        
        import os
        abs_path = os.path.abspath('.')
        dir = os.path.join(abs_path, 'examples/').replace('\\', '/')
         
        ###   ~   module DXF2BK   ~   ###
        
        self.ui.tableWidget.setRowCount(0)
        self.ui.lineEditInput.setText(dir + "example_01/geometry.dxf")
        self.addLayer()
        self.addLayer()
        self.addLayer()
        self.addLayer()
        self.refreshDXF()
        
        rows = self.ui.tableWidget.rowCount()

        indices = [1, 2, 3, 4]
        files = [dir + "example_01/output/2D_POLYLINE.i2s",
                dir + "example_01/output/3D_POLYLINE.i3s",
                dir + "example_01/output/LINE.i2s",
                dir + "example_01/output/POINT.xyz"]

        for row in range(rows):
            combobox = self.ui.tableWidget.cellWidget(row, 0)
            combobox.setCurrentIndex(indices[row])
            item3 = QtGui.QTableWidgetItem()
            item3.setText(files[row])
            self.ui.tableWidget.setItem(row, 1, item3)      