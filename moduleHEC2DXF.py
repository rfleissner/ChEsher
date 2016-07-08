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

"""Wrapper for module HEC2DXF"""

__author__="Reinhard Fleissner"
__date__ ="$18.05.2016 22:38:30$"

import math
import functools
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QMessageBox

# modules and classes
from uiHEC2DXF import Ui_HEC2DXF
import uiHandler as uih
import fileHandler as fh
from dxfwrite import DXFEngine as dxf

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class WrapHEC2DXF():
    """Wrapper for module HEC2DXF"""

    def __init__(self, dir):
        """Constructor."""

        self.directory = dir

        # setup user interface
        self.widget = QtGui.QWidget()
        self.ui = Ui_HEC2DXF()
        self.ui.setupUi(self.widget)

        # inputs
        self.callbackOpenSDFFile = functools.partial(uih.getOpenFileName, "Open Spatial Data Format File", "Spatial Data Format File (*.sdf)", self.ui.lineEditInputSDF, self.directory, self.widget)
        QtCore.QObject.connect(self.ui.pushButtonInputSDF, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackOpenSDFFile)
    
        self.callbackSaveDXFfile = functools.partial(uih.getSaveFileName, "Save DXF-file As", "Drawing Interchange File (*.dxf)", self.ui.lineEditOutputDXF, self.directory, self.widget)
        QtCore.QObject.connect(self.ui.pushButtonOutputDXF, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackSaveDXFfile)
                
        QtCore.QObject.connect(self.ui.pushButtonCreate, QtCore.SIGNAL("clicked()"), self.create)
        
        self.NUMBER_OF_PROFILES = 0
        self. PROFILE_NAMES = []
        self.NUMBER_OF_REACHES = 0
        self.NUMBER_OF_CROSS_SECTIONS = 0
        
    def setDir(self, directory):
        self.directory = directory
        
    def create(self):
        info = "Input data:\n"

        self.readSDF(self.ui.lineEditInputSDF.text())

#        try:
#            self.points = fh.readXYZ(self.ui.lineEditInputPoints.text())
#            info += " - Points:\t\t{0}\n".format(len(self.points))
#        except:
#            QMessageBox.critical(self.widget, "Error", "Not able to load points file!\nCheck filename or content!")
#            return




#        self.writeDXF()
#            try:
#                self.writeDXF()
#                info += " - DXF file created.\n"
#            except:
#                info += " - ERROR: Not able to write DXF file!\n"
    
    def readSDF(self, filename):

        file = open(filename, 'r')
        content = file.readlines()
        file.close()

        for lID in range(len(content)):
            line = content[lID].split()
#            if len(line) > 0:
#                print line
#                if line[0] == ':NUMBER OF PROFILES:':
#                    print content[lID].split()[-1]
            if content[lID].startswith('  NUMBER OF PROFILES:'):
                self.NUMBER_OF_PROFILES = int(content[lID].split()[-1])
            if content[lID].startswith('  PROFILE NAMES:'):
                for i in range(self.NUMBER_OF_PROFILES):
                    lID += 1
                    self.PROFILE_NAMES.append(content[lID].split()[-1] )
            if content[lID].startswith('  NUMBER OF REACHES:'):
                self.NUMBER_OF_REACHES = int(content[lID].split()[-1])
            if content[lID].startswith('  NUMBER OF CROSS-SECTIONS:'):
                self.NUMBER_OF_CROSS_SECTIONS = int(content[lID].split()[-1])                

    
                
                
    #                levels.append(float(content[line].split()[-1]))
    #            elif content[line].startswith(':ScaleColour '):
    #                colHEX_BGR.append(content[line].split()[-1][1:].replace('x', '#'))
    
        self.print_content()
        return    
    
        
    def print_content(self):
        print 'NUMBER OF PROFILES:', self.NUMBER_OF_PROFILES
        print 'PROFILE NAMES:', self.PROFILE_NAMES
        print 'NUMBER OF REACHES:', self.NUMBER_OF_REACHES
        print 'NUMBER OF CROSS SECTIONS:', self.NUMBER_OF_CROSS_SECTIONS

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
