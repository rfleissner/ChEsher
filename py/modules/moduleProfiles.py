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
from PyQt4.QtGui import QMessageBox

# modules and classes
from uiProfiles import Ui_Profiles
import uiHandler as uih
import fileHandler as fh
import profileOrganizer as po
from profileWriter import ProfileWriter
import numpy as np

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class WrapProfiles():
    """Wrapper for module Profiles"""

    def __init__(self, dir):
        """Constructor."""

        self.directory = dir

        # setup user interface
        self.widget = QtGui.QWidget()
        self.ui = Ui_Profiles()
        self.ui.setupUi(self.widget)

        # inputs
        self.points = {}
        self.nodReach = {}
        self.nodProfiles = {}
        self.proProfiles = {}

        # results
        self.reachStation = {}
        self.profileStation={}
        self.proArranged = {}
       
        self.pointsNormalized = {}
        self.segmentStation = []

# module Profiles

        self.callbackOpenProfilesFile = functools.partial(uih.getOpenFileName, "Open Profiles File", "Line Sets (*.i2s *.i3s)", self.ui.lineEditInputProfiles, self.directory, self.widget)
        QtCore.QObject.connect(self.ui.pushButtonInputProfiles, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackOpenProfilesFile)
        
        self.callbackOpenReachFile = functools.partial(uih.getOpenFileName, "Open Reach File", "Line Sets (*.i2s *.i3s)", self.ui.lineEditInputReach, self.directory, self.widget)
        QtCore.QObject.connect(self.ui.pushButtonInputReach, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackOpenReachFile)
        
        self.callbackOpenPointsFile = functools.partial(uih.getOpenFileName, "Open Points File", "Point Set (*.xyz)", self.ui.lineEditInputPoints, self.directory, self.widget)
        QtCore.QObject.connect(self.ui.pushButtonInputPoints, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackOpenPointsFile)


        self.callbackTextfile = functools.partial(uih.setEnabled, self.ui.checkBoxOutputTextfile, self.ui.pushButtonOutputTextfile, self.ui.lineEditOutputTextfile)
        QtCore.QObject.connect(self.ui.checkBoxOutputTextfile, QtCore.SIGNAL("clicked()"), self.callbackTextfile)
        
        self.callbackDXFfile = functools.partial(uih.setEnabled, self.ui.checkBoxOutputDXF, self.ui.pushButtonOutputDXF, self.ui.lineEditOutputDXF)
        QtCore.QObject.connect(self.ui.checkBoxOutputDXF, QtCore.SIGNAL("clicked()"), self.callbackDXFfile)
        
        self.callbackHECRAS = functools.partial(uih.setEnabled, self.ui.checkBoxOutputHECRAS, self.ui.pushButtonOutputHECRAS, self.ui.lineEditOutputHECRAS)
        QtCore.QObject.connect(self.ui.checkBoxOutputHECRAS, QtCore.SIGNAL("clicked()"), self.callbackHECRAS)
    
        self.callbackSaveTextfile = functools.partial(uih.getSaveFileName, "Save textfile As", "Normal text file (*.txt)", self.ui.lineEditOutputTextfile, self.directory, self.widget)
        QtCore.QObject.connect(self.ui.pushButtonOutputTextfile, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackSaveTextfile)
        
        self.callbackSaveDXFfile = functools.partial(uih.getSaveFileName, "Save DXF-file As", "Drawing Interchange File (*.dxf)", self.ui.lineEditOutputDXF, self.directory, self.widget)
        QtCore.QObject.connect(self.ui.pushButtonOutputDXF, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackSaveDXFfile)
        
        self.callbackSaveHECRAS = functools.partial(uih.getSaveFileName, "Save GIS Format data file As", "GIS Format data file (*.geo)", self.ui.lineEditOutputHECRAS, self.directory, self.widget)
        QtCore.QObject.connect(self.ui.pushButtonOutputHECRAS, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackSaveHECRAS)

        QtCore.QObject.connect(self.ui.pushButtonCreate, QtCore.SIGNAL("clicked()"), self.create)
        
    def setDir(self, directory):
        self.directory = directory
        
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
            self.points = fh.readXYZ(self.ui.lineEditInputPoints.text())
            info += " - Points:\t\t{0}\n".format(len(self.points))
        except:
            QMessageBox.critical(self.widget, "Error", "Not able to load points file!\nCheck filename or content!")
            return

        self.proArranged, self.reachStation, self.profileStation, direction = po.determineFlowDirection(self.nodReach, self.nodProfiles, self.proProfiles)

        info += "\nFlow direction:\n"
        for pID_Arranged in direction:
            info += ' - Profile {0}:\t{1}\n'.format(pID_Arranged, direction[pID_Arranged])

        self.pointsNormalized, self.segmentStation = self.normalizeProfiles()

        if self.ui.checkBoxOutputTextfile.isChecked():
            self.writeTXT()
#            try:
#                self.writeTXT()
#                info += " - Textfile created with {0} profiles and {1} points.\n".format(len(self.pointsNormalized), np.size(self.pointsNormalized)) 
#            except:
#                info += " - ERROR: Not able to write textfile!\n"

        if self.ui.checkBoxOutputDXF.isChecked():

            scale = 100.0
            superelevation = 1.0
            
            settings = {}
            settings["Frame"] = True
            settings["Band"] = True
            settings["ProfileName"] = "Cross section "
            settings["ReachStation"] = "km "
            settings["ScaleFactor"] = "Scale = "
            settings["ReferenceLevel"] = "RL = "
            settings["BandTitleStationing"] = "Station [m]"
            settings["BandTitleElevation"] = "Elevation [m]"
            settings["DecimalPlaces"] = 2
            settings["doubleSpinBoxOffsetX"] = 75.0
            settings["doubleSpinBoxOffsetZ"] = 2.5
            settings["doubleSpinBoxBandHeight"] = 15.0
            settings["doubleSpinBoxTextSizeBandTitle"] = 4.0
            settings["doubleSpinBoxTextSizeBand"] = 1.5
            settings["doubleSpinBoxMarkerSize"] = 1.5
            settings["doubleSpinBoxCleanValues"] = 0.0
            
            cs = ProfileWriter(self.ui.lineEditOutputDXF.text(),\
                self.pointsNormalized,
                self.reachStation,
                self.profileStation,
                scale,
                superelevation,
                settings)
            
            cs.drawBottom()
            cs.saveDXF()

#            pw.writeProfile(self.ui.lineEditOutputDXF.text(),\
#                self.pointsNormalized,
#                self.reachStation,
#                self.profileStation
#            )
            
#            try:
#                self.writeDXF()
#                info += " - DXF file created.\n"
#            except:
#                info += " - ERROR: Not able to write DXF file!\n"

        if self.ui.checkBoxOutputHECRAS.isChecked():
            self.writeGEO()
#            try:
#                self.writeGEO()
#                info += " - GEO file created with {0} profiles and {1} points.\n".format(len(self.pointsNormalized), np.size(self.pointsNormalized)) 
#            except:
#                info += " - ERROR: Not able to write geo file!\n"

        print "finish"

    def normalizeProfiles(self):

        tempDist = dict([(key+1, []) for key in range(len(self.points))])
        tempProfileID = dict([(key+1, []) for key in range(len(self.points))])
        tempProfileSegmentID = dict([(key+1, []) for key in range(len(self.points))])
        tempP = dict([(key+1, []) for key in range(len(self.points))])
        tempOnsegment = dict([(key+1, []) for key in range(len(self.points))])
        tempStation = dict([(key+1, []) for key in range(len(self.points))])
        segmentStation = dict([(key, []) for key in self.proArranged])

        # loop over profiles
        for pID in self.proArranged:
            
            # loop over profile segments
            for pnID in range(len(self.proArranged[pID])-1):
                nID_i = self.proArranged[pID][pnID]
                nID_j = self.proArranged[pID][pnID+1]
                a = self.nodProfiles[nID_i][0:2]
                b = self.nodProfiles[nID_j][0:2]
                ab = math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)
                segmentStation[pID].append(ab)
                
                # loop over points
                for nID in self.points:
        
                    # determine orthogonal projection to profile segment
                    u = np.subtract(b, a)
                    x = self.points[nID][0:2]
                    P = a + np.dot(np.subtract(x, a), u)/np.dot(u, u)*u
                    distance = np.linalg.norm(np.array(x)-np.array(P))
                    
                    aP = math.sqrt((a[0]-P[0])**2 + (a[1]-P[1])**2)
                    bP = math.sqrt((b[0]-P[0])**2 + (b[1]-P[1])**2)

                    # check if point is on profile segment or not
                    onsegment = False              
                    if abs(aP + bP - ab) < 0.0000001:
                        onsegment = True
                    else:
                        onsegment = False
                
                    tempDist[nID].append(distance)
                    tempProfileID[nID].append(pID)
                    tempProfileSegmentID[nID].append(pnID)
                    tempP[nID].append(np.append(P,self.points[nID][2]))
                    tempOnsegment[nID].append(onsegment)
                    tempStation[nID].append(aP)
        
        tempPointsNormalized = {}
        tempPointsStation = {}
        tempPointsProfileID = {}
        tempPointsProfileSegmentID = {}

        nodecounter = 0
        for nID in tempDist:
            while True:
                ID = tempDist[nID].index(min(tempDist[nID]))
                if tempOnsegment[nID][ID] is True:
                    nodecounter += 1
                    pID = tempProfileID[nID][ID]
                    tempPointsProfileID[nodecounter] = tempProfileID[nID][ID]
                    tempPointsNormalized[nodecounter] = tempP[nID][ID]
                    tempPointsProfileSegmentID[nodecounter] = tempProfileSegmentID[nID][ID]
                    
                    station = tempStation[nID][ID]
                    if tempPointsProfileSegmentID[nodecounter] > 0:
                        for i in range(tempProfileSegmentID[nID][ID]):
                            station += segmentStation[pID][i]
                            
                    tempPointsStation[nodecounter] = station
                    break
                else:
                    del tempDist[nID][ID]
                    del tempProfileID[nID][ID]
                    del tempProfileSegmentID[nID][ID]
                    del tempP[nID][ID]
                    del tempOnsegment[nID][ID]
                    del tempStation[nID][ID]
        
        # sort normalized points
        pointsNormalized = dict((key, np.array([])) for key in self.proArranged)
        for key in tempPointsNormalized:
            arr1 = np.array(tempPointsNormalized[key])
            arr2 = np.array([tempPointsStation[key]])
            arr = np.append(arr1, arr2)
            pointsNormalized[tempPointsProfileID[key]] = np.append(pointsNormalized[tempPointsProfileID[key]], arr)
        
        # arrange normalized points for each profile
        profiles = {}
        for key in pointsNormalized:
            length = len(pointsNormalized[key])
            pointsNormalized[key] = pointsNormalized[key].reshape((length/4,4))
            
            # sort points by increasing stationing
            pointsNormalized[key] = pointsNormalized[key][pointsNormalized[key][:,3].argsort()]

            x = pointsNormalized[key].transpose()[0]
            y = pointsNormalized[key].transpose()[1]
            z = pointsNormalized[key].transpose()[2]
            d = pointsNormalized[key].transpose()[3]
            
            profiles[key] = [x,y,z,d]

        return profiles, segmentStation
    
    def writeTXT(self):
        
        fname = self.ui.lineEditOutputTextfile.text()
        file = open(fname, 'w')
        
        dec = self.ui.spinBoxDecimal.value()
        
        for pID in self.pointsNormalized:
            file.write(str(len(self.pointsNormalized[pID][0])) + '\n')
            for nID in range(len(self.pointsNormalized[pID][0])):
#                for i in range(len(self.pointsNormalized[pID][nID])):
                file.write(str(round(self.pointsNormalized[pID][3][nID]-self.profileStation[pID],dec)) + '\t' + str(round(self.pointsNormalized[pID][2][nID],dec)) + '\n')
        file.close()
        
    def writeGEO(self):
    
        fname = self.ui.lineEditOutputHECRAS.text()
        file = open(fname, 'w')
        
        dec = self.ui.spinBoxDecimal.value()
        
        rivername = self.ui.lineEditInputRiverName.text()
        if self.ui.lineEditInputRiverName.text() == "":
            rivername = "river"
            
        reachname = self.ui.lineEditInputReachName.text()
        if self.ui.lineEditInputReachName.text() == "":
            reachname = "reach"

        file.write(rivername + '\n\n')
        file.write('BEGIN HEADER:\n\n')
        file.write('NUMBER OF REACHES: 1\n')
        file.write('NUMBER OF CROSS SECTIONS:'+str(len(self.proArranged))+'\n')
        file.write('UNITS: Meters\n\n')
        file.write('END HEADER:\n\n')
        
        file.write('BEGIN STREAM NETWORK:\n')
        for nID in self.nodReach:
            file.write('Endpoint: '+str(round(self.nodReach[nID][0],dec))+', '+str(round(self.nodReach[nID][1],dec))+', 0.0, '+str(nID)+'\n')
            
        file.write('\nREACH:\n\n')
        file.write('STREAM ID: ' + rivername + '\n')
        file.write('REACH ID: ' + reachname + '\n')
        file.write('FROM POINT: 1\n')
        file.write('TO POINT: '+str(len(self.nodReach))+'\n\n')
        file.write('CENTERLINE:\n')
        for nID in self.nodReach:
            file.write(str(round(self.nodReach[nID][0],dec))+', '+str(round(self.nodReach[nID][1],dec))+', 0.0, '+str(round(self.reachStation[nID],dec))+'\n')
        file.write('END:\n\n')
        file.write('END STREAM NETWORK:\n\n\n')
        file.write('BEGIN CROSS-SECTIONS:\n\n\n')

        for pID in self.pointsNormalized:
            file.write('CROSS-SECTION:\n\n')

            file.write('STREAM ID: ' + rivername + '\n')
            file.write('REACH ID: ' + reachname + '\n')
            file.write('STATION: '+str(round(self.reachStation[pID],dec))+'\n')
            if pID < len(self.pointsNormalized):
                reachlength = self.reachStation[pID]-self.reachStation[pID+1]
            else:
                reachlength = self.reachStation[pID]
                
            file.write('REACH LENGTHS: '+str(round(reachlength,dec))+', '+str(round(reachlength,dec))+', '+str(round(reachlength,dec))+'\n\n')

            file.write('CUT LINE: \n')
            for nID in self.proArranged[pID]:
                file.write(str(round(self.nodProfiles[nID][0],dec)) + ', '+str(round(self.nodProfiles[nID][1],dec)) + '\n')   
                    
            file.write('\nSURFACE LINE:\n')
            for nID in range(len(self.pointsNormalized[pID][0])):
                file.write(str(round(self.pointsNormalized[pID][0][nID],dec))+ ', ' + str(round(self.pointsNormalized[pID][1][nID],dec))+ ', ' + str(round(self.pointsNormalized[pID][2][nID],dec)) + '\n')        
            file.write('\nEND:\n\n')
            
        file.close()
    
    def initialize(self):
        
        import os
        abs_path = os.path.abspath('.')
        dir = os.path.join(abs_path, 'examples/').replace('\\', '/')
  
        ###   ~   module Profiles   ~   ###   
        
        self.ui.lineEditInputProfiles.setText(dir + "example_12/profiles.i2s")
        self.ui.lineEditInputReach.setText(dir + "example_12/reach.i2s")
        self.ui.lineEditInputPoints.setText(dir + "example_12/points.xyz")
        
        uih.setEnabledInitialize(self.ui.checkBoxOutputTextfile, self.ui.pushButtonOutputTextfile, self.ui.lineEditOutputTextfile)
        self.ui.lineEditOutputTextfile.setText(dir + "example_12/output/points.txt")
        
        uih.setEnabledInitialize(self.ui.checkBoxOutputDXF, self.ui.pushButtonOutputDXF, self.ui.lineEditOutputDXF)
        self.ui.lineEditOutputDXF.setText(dir + "example_12/output/points.dxf")

        uih.setEnabledInitialize(self.ui.checkBoxOutputHECRAS, self.ui.pushButtonOutputHECRAS, self.ui.lineEditOutputHECRAS)
        self.ui.lineEditOutputHECRAS.setText(dir + "example_12/output/points.geo")       
