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

"""Wrapper for module XYZ2DXF"""

__author__="Reinhard Fleissner"
__date__ ="$18.05.2016 22:38:30$"

import os
import sys
from colourHandler import Colour
import functools
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QMessageBox, QFileDialog, QColor

# modules and classes
from uiXYZ2DXF import Ui_XYZ2DXF
import fileHandler as fh
from dxfwrite import DXFEngine as dxf

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class WrapXYZ2DXF():
    """Wrapper for module XYZ2DXF"""

    def __init__(self):
        """Constructor."""
        
        # setup user interface
        self.widget = QtGui.QWidget()
        self.ui = Ui_XYZ2DXF()
        self.ui.setupUi(self.widget)
        self.directory = os.path.abspath('.')
        
        self.ui.labelSymbolColour.setStyleSheet("QLabel { background-color: rgb(0, 0, 0); }")
        self.ui.labelTextColour.setStyleSheet("QLabel { background-color: rgb(0, 0, 0); }")
        
        # inputs
        self.points = {}
        
# module Mesh

        self.callbackOpenPointsFile = functools.partial(self.getOpenFileName, "Open Points File", "Point Set (*.xyz)", self.ui.lineEditInputXYZ)
        QtCore.QObject.connect(self.ui.pushButtonInputXYZ, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackOpenPointsFile)
    
        self.callbackSaveDXFfile = functools.partial(self.getSaveFileName, "Save DXF-file As", "Drawing Interchange File (*.dxf)", self.ui.lineEditOutputDXF)
        QtCore.QObject.connect(self.ui.pushButtonOutputDXF, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackSaveDXFfile)

        self.callbackSetSymbolColour = functools.partial(self.setColour, self.ui.labelSymbolColour)
        QtCore.QObject.connect(self.ui.pushButtonSymbolColour, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackSetSymbolColour)
        self.callbackSetTextColour = functools.partial(self.setColour, self.ui.labelTextColour)
        QtCore.QObject.connect(self.ui.pushButtonTextColour, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackSetTextColour)
        
        self.scalarSymbol = 0
        
        self.callbackCircle = functools.partial(self.setSymbol, 0)
        QtCore.QObject.connect(self.ui.radioButtonCircle, QtCore.SIGNAL("clicked()"), self.callbackCircle)
        self.callbackCross = functools.partial(self.setSymbol, 1)
        QtCore.QObject.connect(self.ui.radioButtonCross, QtCore.SIGNAL("clicked()"), self.callbackCross)
        self.callbackCrosshairs = functools.partial(self.setSymbol, 2)
        QtCore.QObject.connect(self.ui.radioButtonCrosshairs, QtCore.SIGNAL("clicked()"), self.callbackCrosshairs)
        self.callbackNone = functools.partial(self.setSymbol, 3)
        QtCore.QObject.connect(self.ui.radioButtonNone, QtCore.SIGNAL("clicked()"), self.callbackNone)
        
        QtCore.QObject.connect(self.ui.pushButtonCreate, QtCore.SIGNAL("clicked()"), self.create)
        
    def setDir(self, directory):
        self.directory = directory
        
    def create(self):
        info = "Input data:\n"

        self.points = fh.readXYZ(self.ui.lineEditInputXYZ.text())
#        try:
#            self.points = fh.readXYZ(self.ui.lineEditInputXYZ.text())
#            info += " - Points:\t\t{0}\n".format(len(self.points))
#        except Exception, e:
#            QMessageBox.critical(self.widget, "Error", "Not able to load points file!\nCheck filename or content!" + "\n\n" + str(e))
#            return

        dec = self.ui.spinBoxDecimal.value()
        scale = self.ui.spinBoxScale.value()
        fname = self.ui.lineEditOutputDXF.text()
        blockName = self.ui.lineEditInputBlockName.text()
        attributeName = self.ui.lineEditInputAttributeName.text()
        cs = Colour(self.ui.labelSymbolColour.text().split(","))
        cs.create()
        colRGBSymbol = cs.getRGB()
        ct = Colour(self.ui.labelTextColour.text().split(","))
        ct.create()
        colRGBText = ct.getRGB()        
        fh.writeXYZ2DXF(self.points, dec, scale, self.scalarSymbol, fname, colRGBSymbol, colRGBText, blockName, attributeName)
        
#        try:
#            nOfValues = fh.writeScalarDXF(self.points, -10000, 10000, 0.0, 10.0, self.scalarSymbol, True, fname)
#            info += "\n - {0} values written to {1}".format(nOfValues, fname)
#        except Exception, e:
#            QMessageBox.critical(self.widget, "Error", "Not able to write DXF file!" + "\n\n" + str(e))
#            return
        
        
#        try:
#            self.writeDXF()
#            info += " - DXF file created.\n"
#        except:
#            info += " - ERROR: Not able to write DXF file!\n"
#            info += "\n"
#            info += str(sys.exc_info())
#            info += "\n"
        
    def writeDXF(self):
        
        fname = self.ui.lineEditOutputDXF.text()
        file = open(fname, 'w')
        
        rad = 0.25
        scale = 1.0
        col = 7
        dec = self.ui.spinBoxDecimal.value()
        dwg = dxf.drawing(fname)
           
        # create block
        scalarsymbol = dxf.block(name='symbol')
        scalarsymbol.add( dxf.circle(radius=rad, color=0) )

        # define some attributes
        scalarsymbol.add( dxf.attdef(insert=(1.25, -1.25), tag='VAL1', height=1.25, color=0) )

        # add block definition to the drawing
        dwg.blocks.add(scalarsymbol)

        for nID in self.points:
            x = self.points[nID][0]
            y = self.points[nID][1]
            val1 = self.points[nID][2]
            values = {'VAL1': "%.{0}f".format(dec) % val1}
            
            dwg.add(dxf.insert2(blockdef=scalarsymbol, insert=(x, y),
                                attribs=values,
                                xscale=scale,
                                yscale=scale,
                                layer='0',
                                color = col))

        dwg.save()

    def getOpenFileName(self, title, fileFormat, lineEdit):
        filename = QFileDialog.getOpenFileName(self.widget, title, self.directory, fileFormat)
        if filename != "":
            lineEdit.setText(filename)

    def getSaveFileName(self, title, fileFormat, lineEdit):
        filename = QFileDialog.getSaveFileName(self.widget, title, self.directory, fileFormat)
        if filename != "":
            lineEdit.setText(filename)
            
    def setSymbol(self, i):
        self.scalarSymbol = i
    
    def initialize(self):
        
        abs_path = os.path.abspath('.')
        dir = os.path.join(abs_path, 'examples/').replace('\\', '/')
  
        ###   ~   module ScalarDXF   ~   ###

        self.ui.lineEditInputXYZ.setText(dir + "example_14/points.xyz")
        self.ui.spinBoxScale.setValue(100)
        
        self.ui.radioButtonCircle.setChecked(False)
        self.ui.radioButtonCrosshairs.setChecked(True)
        self.setSymbol(2)
        
        self.ui.lineEditOutputDXF.setText(dir + "example_14/output/points.dxf")        

    def setColour(self, label):

        coldia = QtGui.QColorDialog()
        col = coldia.getColor()
        
        label.setAutoFillBackground(True) # This is important!!

        if col.isValid():
            values = "{r}, {g}, {b}".format(r = col.red(),
                                                 g = col.green(),
                                                 b = col.blue()
                                                 )
                                            
            label.setStyleSheet("QLabel { background-color: rgb(" + values + "); }")
            label.setText(values)
        else:
            return