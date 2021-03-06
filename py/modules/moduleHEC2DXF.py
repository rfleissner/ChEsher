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

import os
import sys
import functools
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QMessageBox, QFileDialog

# modules and classes
from uiHEC2DXF import Ui_HEC2DXF
import profileOrganizer as po
from profileWriter import ProfileWriter
from profileSettings import WrapProfileSettings

import numpy as np

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class WrapHEC2DXF():
    """Wrapper for module HEC2DXF"""

    def __init__(self):
        """Constructor."""

        # setup user interface
        self.widget = QtGui.QWidget()
        self.ui = Ui_HEC2DXF()
        self.ui.setupUi(self.widget)
        self.directory = os.path.abspath('.')
        
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
        
        # inputs
        self.callbackOpenSDFFile = functools.partial(self.getOpenFileName, "Open Spatial Data Format File", "Spatial Data Format File (*.sdf)", self.ui.lineEditInputSDF)
        QtCore.QObject.connect(self.ui.pushButtonInputSDF, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackOpenSDFFile)
    
        self.callbackSaveDXFfile = functools.partial(self.getSaveFileName, "Save DXF-file As", "Drawing Interchange File (*.dxf)", self.ui.lineEditOutputDXF)
        QtCore.QObject.connect(self.ui.pushButtonOutputDXF, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackSaveDXFfile)

        defaults = ["Template A", "Template B"]
        self.ui.comboBoxDefault.addItems(defaults)  
        QtCore.QObject.connect(self.ui.pushButtonDefault, QtCore.SIGNAL(_fromUtf8("clicked()")), self.setDefault)
                
        QtCore.QObject.connect(self.ui.pushButtonProfileSettings, QtCore.SIGNAL("clicked()"), self.setSettings)

        QtCore.QObject.connect(self.ui.pushButtonCreate, QtCore.SIGNAL("clicked()"), self.create)
        
        self.NUMBER_OF_PROFILES = 0
        self.PROFILE_NAMES = []
        self.NUMBER_OF_REACHES = 0
        self.NUMBER_OF_CROSS_SECTIONS = 0
        self.STREAM_ID = ""
        self.REACH_ID = ""
        self.CROSS_SECTIONS = {\
            "PROFILE_ID":[],\
            "STREAM_ID":[], \
            "REACH_ID":[],\
            "STATION":[],\
            "NODE_NAME":[],\
            "CUT_LINE":{"x":[], "y":[]},\
            "REACH_LENGTHS":[],\
            "LEVEE_POSITIONS":{},\
            "WATER_ELEVATION":{},\
            "SURFACE_LINE":{"x":[], "y":[], "z":[]}\
            }
            
        self.nodReach = {}
        self.nodProfiles = {}
        self.proProfiles = {}
        self.profileNodes = {}
        
    def setDir(self, directory):
        self.directory = directory
        
    def create(self):
        info = "Input data:\n"
        
        try:
            self.readSDF(self.ui.lineEditInputSDF.text())
            info += " - Reach:\t\t\t\t{0}\n".format(self.REACH_ID)
            info += " - Number of cross sections:\t\t{0}\n".format(self.NUMBER_OF_CROSS_SECTIONS)
            info += " - Number of water surface profiles:\t{0}\n".format(self.NUMBER_OF_PROFILES)
        except Exception, e:
            QMessageBox.critical(self.widget, "Error", "Not able to load GIS data file!\nCheck filename or content!" + "\n\n" + str(e))
            return
        
        from shapely.geometry import LineString
        
        reachStation = {}
        profileStation = {}
        bottom = {}
        
        profileStation_ = po.determineFlowDirection(self.nodReach, self.nodProfiles, self.proProfiles)[2]

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
            profileStation[self.CROSS_SECTIONS["PROFILE_ID"][pID]] = profileStation_[pID+1]
            bottom[self.CROSS_SECTIONS["PROFILE_ID"][pID]] = [x, y, z, d]

        scale = self.ui.spinBoxScale.value()
        superelevation = self.ui.doubleSpinBoxSuperelevation.value()
        
        info += "\nOutput data:\n"
             
        try:
            cs = ProfileWriter(self.ui.lineEditOutputDXF.text(),\
                bottom,
                reachStation,
                profileStation,
                scale,
                superelevation,
                self.settings,
                self.REACH_ID)   

            cs.drawBottom()
            cs.draw1dResults(self.PROFILE_NAMES, self.CROSS_SECTIONS["WATER_ELEVATION"], self.CROSS_SECTIONS["LEVEE_POSITIONS"])
            cs.saveDXF()    
            
            info += " - DXF file written to {0}.\n".format(self.ui.lineEditOutputDXF.text())
    
        except:
            info += " - ERROR: Not able to write profiles!\n"
            info += "\n"
            info += str(sys.exc_info())
            info += "\n"

        QMessageBox.information(self.widget, "Module HEC2DXF", info)        
            
    def readSDF(self, filename):
        
        self.NUMBER_OF_PROFILES = 0
        self.PROFILE_NAMES = []
        self.NUMBER_OF_REACHES = 0
        self.NUMBER_OF_CROSS_SECTIONS = 0
        self.STREAM_ID = ""
        self.REACH_ID = ""
        self.CROSS_SECTIONS = {\
            "PROFILE_ID":[],\
            "STREAM_ID":[], \
            "REACH_ID":[],\
            "STATION":[],\
            "NODE_NAME":[],\
            "CUT_LINE":{"x":[], "y":[]},\
            "REACH_LENGTHS":[],\
            "LEVEE_POSITIONS":{},\
            "WATER_ELEVATION":{},\
            "SURFACE_LINE":{"x":[], "y":[], "z":[]}\
            }
            
        self.nodReach = {}
        self.nodProfiles = {}
        self.proProfiles = {}
        self.profileNodes = {}
        
        file = open(filename, 'r')
        content = file.readlines()
        file.close()
        CS_counter = 0
        cID = 0
        self.nodProfiles = {}
        
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
                nID = 1

                while True:
                    self.nodReach[nID] = [float(content[lID].split(",")[0]), float(content[lID].split(",")[1])]
                    nID += 1
                    lID += 1
                    if content[lID].startswith(' END:'):
                        break

            if content[lID].startswith('  CROSS-SECTION:'):
                CS_counter += 1
                self.CROSS_SECTIONS["PROFILE_ID"].append(CS_counter)
                while True:
                    lID += 1
                    if content[lID].startswith('    STREAM ID:'):
                        self.CROSS_SECTIONS["STREAM_ID"].append(content[lID].split(":")[1].strip())
                        continue
                    if content[lID].startswith('    REACH ID:'):
                        self.CROSS_SECTIONS["REACH_ID"].append(content[lID].split(":")[1].strip())
                        continue
                    if content[lID].startswith('    STATION:'):
                        self.CROSS_SECTIONS["STATION"].append(float(content[lID].split(":")[1].strip()))
                        continue
                    if content[lID].startswith('    NODE NAME:'):
                        self.CROSS_SECTIONS["NODE_NAME"].append(content[lID].split(":")[1].strip())
                        continue
                    if content[lID].startswith('    CUT LINE:'):
                        lID += 1
                        x = []
                        y = []
                        cs = []
                        while True:
                            try:
                                x.append(float(content[lID].split(",")[0]))
                                y.append(float(content[lID].split(",")[1]))
                                cID +=1
                                cs.append(cID)
                                self.nodProfiles[cID] = [float(content[lID].split(",")[0]), float(content[lID].split(",")[1])]
                                lID += 1                            
                            except:
                                self.CROSS_SECTIONS["CUT_LINE"]["x"].append(x)
                                self.CROSS_SECTIONS["CUT_LINE"]["y"].append(y)
                                break
                        self.proProfiles[CS_counter]= cs
                        continue
                    if content[lID].startswith('    REACH LENGTHS:'):
                        self.CROSS_SECTIONS["REACH_LENGTHS"].append([float(content[lID].split(":")[1].split(",")[0]),\
                        float(content[lID].split(":")[1].split(",")[1]),\
                        float(content[lID].split(":")[1].split(",")[2])])
                        continue
                    if content[lID].startswith('    LEVEE POSITIONS:'):
                        lev = []
                        while True:
                            try:
                                lID += 1
                                lev.append([float(content[lID].split(",")[1]),\
                                    float(content[lID].split(",")[2])])
                                
                            except:
                                self.CROSS_SECTIONS["LEVEE_POSITIONS"][CS_counter] = lev
                                lID -= 1
                                break
                        continue
                    if content[lID].startswith('    WATER ELEVATION:'):
                        wel = []
                        for i in range(len(content[lID].split(":")[1].split(","))):
                            wel.append(float(content[lID].split(":")[1].split(",")[i]))
                        self.CROSS_SECTIONS["WATER_ELEVATION"][CS_counter] = wel
                        continue
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
                    if content[lID].startswith('  END:'):
                        break
#        self.print_content()

    def print_content(self):
        print 'NUMBER OF PROFILES:', self.NUMBER_OF_PROFILES
        print 'PROFILE NAMES:', self.PROFILE_NAMES
        print 'NUMBER OF REACHES:', self.NUMBER_OF_REACHES
        print 'NUMBER OF CROSS SECTIONS:', self.NUMBER_OF_CROSS_SECTIONS
        print 'CENTERLINE:'
        for nID in self.nodReach:
            print self.nodReach[nID]
        print 'CROSS SECTIONS:'
        for key in self.CROSS_SECTIONS:
            print key, self.CROSS_SECTIONS[key]
    
    def initialize(self):
        
        import os
        abs_path = os.path.abspath('.')
        dir = os.path.join(abs_path, 'examples/').replace('\\', '/')
          
        self.ui.lineEditInputSDF.setText(dir + "example_13/results.sdf")
        self.ui.lineEditOutputDXF.setText(dir + "example_13/output/results.dxf")

    def setSettings(self):

        settings = WrapProfileSettings(self.settings)
        settings.setSettings()
    
        if settings.exec_():
            self.settings = settings.getSettings()

    def setDefault(self):

        ans = QMessageBox.question(self.widget, "Module HEC2DXF", "Do you want do set default settings?", 1, 2)

        if ans != 1:
            return
        else:
            template = self.ui.comboBoxDefault.currentIndex()

            # Template A
            if template == 0:

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
            
    def getOpenFileName(self, title, fileFormat, lineEdit):
        filename = QFileDialog.getOpenFileName(self.widget, title, self.directory, fileFormat)
        if filename != "":
            lineEdit.setText(filename)

    def getSaveFileName(self, title, fileFormat, lineEdit):
        filename = QFileDialog.getSaveFileName(self.widget, title, self.directory, fileFormat)
        if filename != "":
            lineEdit.setText(filename)