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
import profileWriter as pw
import numpy as np
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
        self.PROFILE_NAMES = []
        self.NUMBER_OF_REACHES = 0
        self.NUMBER_OF_CROSS_SECTIONS = 0
        self.STREAM_ID = ""
        self.REACH_ID = ""
        self.CENTERLINE = {"x":[], "y":[]}
        self.CROSS_SECTIONS = {\
            "PROFILE_ID":[],\
            "STREAM_ID":[], \
            "REACH_ID":[],\
            "STATION":[],\
            "NODE_NAME":[],\
            "CUT_LINE":{"x":[], "y":[]},\
            "REACH_LENGTHS":[],\
            "WATER_ELEVATION":{},\
            "SURFACE_LINE":{"x":[], "y":[], "z":[]}\
            }
    def setDir(self, directory):
        self.directory = directory
        
    def create(self):
        info = "Input data:\n"

        self.readSDF(self.ui.lineEditInputSDF.text())
        
        from shapely.geometry import LineString
        
        reachStation = {}
        profileStation = {}
        bottom = {}
        for pID in range(len(self.CROSS_SECTIONS["SURFACE_LINE"]["x"])):
            
            d = []
            x_ = []
            y_ = []
            z_ = []
            x_.append(self.CROSS_SECTIONS["SURFACE_LINE"]["x"][pID][0])
            y_.append(self.CROSS_SECTIONS["SURFACE_LINE"]["y"][pID][0])
            z_.append(self.CROSS_SECTIONS["SURFACE_LINE"]["z"][pID][0])            
            d.append(0.0)
            
            totLen = 0.0
            for nID in range(len(self.CROSS_SECTIONS["SURFACE_LINE"]["x"][pID])-1):
                xi = self.CROSS_SECTIONS["SURFACE_LINE"]["x"][pID][nID]
                xj = self.CROSS_SECTIONS["SURFACE_LINE"]["x"][pID][nID+1]
                yi = self.CROSS_SECTIONS["SURFACE_LINE"]["y"][pID][nID]
                yj = self.CROSS_SECTIONS["SURFACE_LINE"]["y"][pID][nID+1]
#                print xi
#                print xj
                profile_line = LineString([(xi, yi), (xj, yj)])
                totLen += profile_line.length
                if profile_line.length >= 0.005:
                    d.append(totLen)
                    x_.append(self.CROSS_SECTIONS["SURFACE_LINE"]["x"][pID][nID+1])
                    y_.append(self.CROSS_SECTIONS["SURFACE_LINE"]["y"][pID][nID+1])
                    z_.append(self.CROSS_SECTIONS["SURFACE_LINE"]["z"][pID][nID+1])

            x = np.array(x_)
            y = np.array(y_)
            z = np.array(z_)
            
            reachStation[self.CROSS_SECTIONS["PROFILE_ID"][pID]] = self.CROSS_SECTIONS["STATION"][pID]
            profileStation[self.CROSS_SECTIONS["PROFILE_ID"][pID]] = 0.0            
            bottom[self.CROSS_SECTIONS["PROFILE_ID"][pID]] = [x, y, z, d]

        print self.CROSS_SECTIONS["WATER_ELEVATION"]
        
        
        pw.writeProfile(self.ui.lineEditOutputDXF.text(),\
            bottom,
            reachStation,
            profileStation,
            self.PROFILE_NAMES,
            self.CROSS_SECTIONS["WATER_ELEVATION"]
        )

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
        print "finish"
        
    def readSDF(self, filename):

        file = open(filename, 'r')
        content = file.readlines()
        file.close()
        CS_counter = 0
        for lID in range(len(content)):
            line = content[lID].split()

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
            if content[lID].startswith('REACH:'):
                lID += 1
                self.STREAM_ID = content[lID].split()[-1]
                lID += 1
                self.REACH_ID = content[lID].split()[-1]
                lID += 4

                while True:
                    self.CENTERLINE["x"].append(float(content[lID].split(",")[0]))
                    self.CENTERLINE["y"].append(float(content[lID].split(",")[1]))
                    lID += 1
                    if content[lID].startswith(' END:'):
                        break

            
            if content[lID].startswith('  CROSS-SECTION:'):
                CS_counter += 1
                self.CROSS_SECTIONS["PROFILE_ID"].append(CS_counter)
                lID += 1
                if content[lID].startswith('    STREAM ID:'):
                    self.CROSS_SECTIONS["STREAM_ID"].append(content[lID].split(":")[1].strip())
                    lID += 1
                if content[lID].startswith('    REACH ID:'):
                    self.CROSS_SECTIONS["REACH_ID"].append(content[lID].split(":")[1].strip())
                    lID += 1
                if content[lID].startswith('    STATION:'):
                    self.CROSS_SECTIONS["STATION"].append(float(content[lID].split(":")[1].strip()))
                    lID += 1
                if content[lID].startswith('    NODE NAME:'):
                    self.CROSS_SECTIONS["NODE_NAME"].append(content[lID].split(":")[1].strip())
                    lID += 1
                if content[lID].startswith('    CUT LINE:'):
                    lID += 1
                    x = []
                    y = []
                    while True:
                        try:
                            x.append(float(content[lID].split(",")[0]))
                            y.append(float(content[lID].split(",")[1]))
                            lID += 1
                        except:
                            self.CROSS_SECTIONS["CUT_LINE"]["x"].append(x)
                            self.CROSS_SECTIONS["CUT_LINE"]["y"].append(y)
                            break
                if content[lID].startswith('    REACH LENGTHS:'):
                    self.CROSS_SECTIONS["REACH_LENGTHS"].append([float(content[lID].split(":")[1].split(",")[0]),\
                    float(content[lID].split(":")[1].split(",")[1]),\
                    float(content[lID].split(":")[1].split(",")[2])])
                    lID += 1
                if content[lID].startswith('    WATER ELEVATION:'):
                    wel = []
                    for i in range(len(content[lID].split(":")[1].split(","))):
                        wel.append(float(content[lID].split(":")[1].split(",")[i]))
                    self.CROSS_SECTIONS["WATER_ELEVATION"][CS_counter] = wel
                    lID += 1
                if content[lID].startswith('    SURFACE LINE:'):
                    lID += 1
                    x = []
                    y = []
                    z = []
                    while True:
                        try:
                            x.append(float(content[lID].split(",")[0]))
                            y.append(float(content[lID].split(",")[1]))
                            z.append(float(content[lID].split(",")[2]))
                            lID += 1
                        except:
                            self.CROSS_SECTIONS["SURFACE_LINE"]["x"].append(x)
                            self.CROSS_SECTIONS["SURFACE_LINE"]["y"].append(y)
                            self.CROSS_SECTIONS["SURFACE_LINE"]["z"].append(z)
                            break
#        self.print_content()
        return    

    def print_content(self):
        print 'NUMBER OF PROFILES:', self.NUMBER_OF_PROFILES
        print 'PROFILE NAMES:', self.PROFILE_NAMES
        print 'NUMBER OF REACHES:', self.NUMBER_OF_REACHES
        print 'NUMBER OF CROSS SECTIONS:', self.NUMBER_OF_CROSS_SECTIONS
        print 'CENTERLINE:'
        for i in range(len(self.CENTERLINE["x"])):
            print self.CENTERLINE["x"][i], self.CENTERLINE["y"][i]
        print 'CROSS SECTIONS:'
        for key in self.CROSS_SECTIONS:
            print key, self.CROSS_SECTIONS[key]

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
