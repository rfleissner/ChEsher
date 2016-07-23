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
        print "create profilesDXF"
        
        
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
        

#        try:
#            self.nodProfiles, self.proProfiles = fh.readI2S(self.ui.lineEditInputProfiles.text())
#            info += " - Profiles:\t\t\t{0}\n".format(len(self.proProfiles))
#        except:
#            QMessageBox.critical(self.widget, "Error", "Not able to load profiles file!\nCheck filename or content!")
#            return
#        try:
#            self.nodReach = fh.readI2S(self.ui.lineEditInputReach.text())[0]
#            info += " - Reach nodes:\t\t{0}\n".format(len(self.nodReach))
#        except:
#            QMessageBox.critical(self.widget, "Error", "Not able to load reach file!\nCheck filename or content!")
#            return
#        try:
#            self.points = fh.readXYZ(self.ui.lineEditInputPoints.text())
#            info += " - Points:\t\t{0}\n".format(len(self.points))
#        except:
#            QMessageBox.critical(self.widget, "Error", "Not able to load points file!\nCheck filename or content!")
#            return
#
#        self.proArranged, self.reachStation, self.profileStation, direction = po.determineFlowDirection(self.nodReach, self.nodProfiles, self.proProfiles)
#
#        info += "\nFlow direction:\n"
#        for pID_Arranged in direction:
#            info += ' - Profile {0}:\t{1}\n'.format(pID_Arranged, direction[pID_Arranged])
#
#        self.pointsNormalized, self.segmentStation = self.normalizeProfiles()
#
#        if self.ui.checkBoxOutputTextfile.isChecked():
#            self.writeTXT()
##            try:
##                self.writeTXT()
##                info += " - Textfile created with {0} profiles and {1} points.\n".format(len(self.pointsNormalized), np.size(self.pointsNormalized)) 
##            except:
##                info += " - ERROR: Not able to write textfile!\n"
#
#        if self.ui.checkBoxOutputDXF.isChecked():
##            self.writeDXF()
#            pw.writeProfile(self.ui.lineEditOutputDXF.text(),\
#                self.pointsNormalized,
#                self.reachStation,
#                self.profileStation
#            )
#            
##            try:
##                self.writeDXF()
##                info += " - DXF file created.\n"
##            except:
##                info += " - ERROR: Not able to write DXF file!\n"
#
#        if self.ui.checkBoxOutputHECRAS.isChecked():
#            self.writeGEO()
##            try:
##                self.writeGEO()
##                info += " - GEO file created with {0} profiles and {1} points.\n".format(len(self.pointsNormalized), np.size(self.pointsNormalized)) 
##            except:
##                info += " - ERROR: Not able to write geo file!\n"
#
#        print "finish"
#
#    def normalizeProfiles(self):
#
#        tempDist = dict([(key+1, []) for key in range(len(self.points))])
#        tempProfileID = dict([(key+1, []) for key in range(len(self.points))])
#        tempProfileSegmentID = dict([(key+1, []) for key in range(len(self.points))])
#        tempP = dict([(key+1, []) for key in range(len(self.points))])
#        tempOnsegment = dict([(key+1, []) for key in range(len(self.points))])
#        tempStation = dict([(key+1, []) for key in range(len(self.points))])
#        segmentStation = dict([(key, []) for key in self.proArranged])
#
#        # loop over profiles
#        for pID in self.proArranged:
#            
#            # loop over profile segments
#            for pnID in range(len(self.proArranged[pID])-1):
#                nID_i = self.proArranged[pID][pnID]
#                nID_j = self.proArranged[pID][pnID+1]
#                a = self.nodProfiles[nID_i][0:2]
#                b = self.nodProfiles[nID_j][0:2]
#                ab = math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)
#                segmentStation[pID].append(ab)
#                
#                # loop over points
#                for nID in self.points:
#        
#                    # determine orthogonal projection to profile segment
#                    u = np.subtract(b, a)
#                    x = self.points[nID][0:2]
#                    P = a + np.dot(np.subtract(x, a), u)/np.dot(u, u)*u
#                    distance = np.linalg.norm(np.array(x)-np.array(P))
#                    
#                    aP = math.sqrt((a[0]-P[0])**2 + (a[1]-P[1])**2)
#                    bP = math.sqrt((b[0]-P[0])**2 + (b[1]-P[1])**2)
#
#                    # check if point is on profile segment or not
#                    onsegment = False              
#                    if abs(aP + bP - ab) < 0.0000001:
#                        onsegment = True
#                    else:
#                        onsegment = False
#                
#                    tempDist[nID].append(distance)
#                    tempProfileID[nID].append(pID)
#                    tempProfileSegmentID[nID].append(pnID)
#                    tempP[nID].append(np.append(P,self.points[nID][2]))
#                    tempOnsegment[nID].append(onsegment)
#                    tempStation[nID].append(aP)
#        
#        tempPointsNormalized = {}
#        tempPointsStation = {}
#        tempPointsProfileID = {}
#        tempPointsProfileSegmentID = {}
#
#        nodecounter = 0
#        for nID in tempDist:
#            while True:
#                ID = tempDist[nID].index(min(tempDist[nID]))
#                if tempOnsegment[nID][ID] is True:
#                    nodecounter += 1
#                    pID = tempProfileID[nID][ID]
#                    tempPointsProfileID[nodecounter] = tempProfileID[nID][ID]
#                    tempPointsNormalized[nodecounter] = tempP[nID][ID]
#                    tempPointsProfileSegmentID[nodecounter] = tempProfileSegmentID[nID][ID]
#                    
#                    station = tempStation[nID][ID]
#                    if tempPointsProfileSegmentID[nodecounter] > 0:
#                        for i in range(tempProfileSegmentID[nID][ID]):
#                            station += segmentStation[pID][i]
#                            
#                    tempPointsStation[nodecounter] = station
#                    break
#                else:
#                    del tempDist[nID][ID]
#                    del tempProfileID[nID][ID]
#                    del tempProfileSegmentID[nID][ID]
#                    del tempP[nID][ID]
#                    del tempOnsegment[nID][ID]
#                    del tempStation[nID][ID]
#        
#        # sort normalized points
#        pointsNormalized = dict((key, np.array([])) for key in self.proArranged)
#        for key in tempPointsNormalized:
#            arr1 = np.array(tempPointsNormalized[key])
#            arr2 = np.array([tempPointsStation[key]])
#            arr = np.append(arr1, arr2)
#            pointsNormalized[tempPointsProfileID[key]] = np.append(pointsNormalized[tempPointsProfileID[key]], arr)
#        
#        # arrange normalized points for each profile
#        profile = {}
#        for key in pointsNormalized:
#            length = len(pointsNormalized[key])
#            pointsNormalized[key] = pointsNormalized[key].reshape((length/4,4))
#            
#            # sort points by increasing stationing
#            pointsNormalized[key] = pointsNormalized[key][pointsNormalized[key][:,3].argsort()]
#
#            x = pointsNormalized[key].transpose()[0]
#            y = pointsNormalized[key].transpose()[1]
#            z = pointsNormalized[key].transpose()[2]
#            d = pointsNormalized[key].transpose()[3]
#            
#            profile[key] = [x,y,z,d]
#
#        return profile, segmentStation
#    
#    def writeTXT(self):
#        
#        fname = self.ui.lineEditOutputTextfile.text()
#        file = open(fname, 'w')
#        
#        dec = self.ui.spinBoxDecimal.value()
#        
#        for pID in self.pointsNormalized:
#            file.write(str(len(self.pointsNormalized[pID][0])) + '\n')
#            for nID in range(len(self.pointsNormalized[pID][0])):
##                for i in range(len(self.pointsNormalized[pID][nID])):
#                file.write(str(round(self.pointsNormalized[pID][3][nID]-self.profileStation[pID],dec)) + '\t' + str(round(self.pointsNormalized[pID][2][nID],dec)) + '\n')
#        file.close()
#        
#    def writeGEO(self):
#    
#        fname = self.ui.lineEditOutputHECRAS.text()
#        file = open(fname, 'w')
#        
#        dec = self.ui.spinBoxDecimal.value()
#        
#        rivername = self.ui.lineEditInputRiverName.text()
#        if self.ui.lineEditInputRiverName.text() == "":
#            rivername = "river"
#            
#        reachname = self.ui.lineEditInputReachName.text()
#        if self.ui.lineEditInputReachName.text() == "":
#            reachname = "reach"
#
#        file.write(rivername + '\n\n')
#        file.write('BEGIN HEADER:\n\n')
#        file.write('NUMBER OF REACHES: 1\n')
#        file.write('NUMBER OF CROSS SECTIONS:'+str(len(self.proArranged))+'\n')
#        file.write('UNITS: Meters\n\n')
#        file.write('END HEADER:\n\n')
#        
#        file.write('BEGIN STREAM NETWORK:\n')
#        for nID in self.nodReach:
#            file.write('Endpoint: '+str(round(self.nodReach[nID][0],dec))+', '+str(round(self.nodReach[nID][1],dec))+', 0.0, '+str(nID)+'\n')
#            
#        file.write('\nREACH:\n\n')
#        file.write('STREAM ID: ' + rivername + '\n')
#        file.write('REACH ID: ' + reachname + '\n')
#        file.write('FROM POINT: 1\n')
#        file.write('TO POINT: '+str(len(self.nodReach))+'\n\n')
#        file.write('CENTERLINE:\n')
#        for nID in self.nodReach:
#            file.write(str(round(self.nodReach[nID][0],dec))+', '+str(round(self.nodReach[nID][1],dec))+', 0.0, '+str(round(self.reachStation[nID],dec))+'\n')
#        file.write('END:\n\n')
#        file.write('END STREAM NETWORK:\n\n\n')
#        file.write('BEGIN CROSS-SECTIONS:\n\n\n')
#
#        for pID in self.pointsNormalized:
#            file.write('CROSS-SECTION:\n\n')
#
#            file.write('STREAM ID: ' + rivername + '\n')
#            file.write('REACH ID: ' + reachname + '\n')
#            file.write('STATION: '+str(round(self.reachStation[pID],dec))+'\n')
#            if pID < len(self.pointsNormalized):
#                reachlength = self.reachStation[pID]-self.reachStation[pID+1]
#            else:
#                reachlength = self.reachStation[pID]
#                
#            file.write('REACH LENGTHS: '+str(round(reachlength,dec))+', '+str(round(reachlength,dec))+', '+str(round(reachlength,dec))+'\n\n')
#
#            file.write('CUT LINE: \n')
#            for nID in self.proArranged[pID]:
#                file.write(str(round(self.nodProfiles[nID][0],dec)) + ', '+str(round(self.nodProfiles[nID][1],dec)) + '\n')   
#                    
#            file.write('\nSURFACE LINE:\n')
#            for nID in range(len(self.pointsNormalized[pID][0])):
#                file.write(str(round(self.pointsNormalized[pID][0][nID],dec))+ ', ' + str(round(self.pointsNormalized[pID][1][nID],dec))+ ', ' + str(round(self.pointsNormalized[pID][2][nID],dec)) + '\n')        
#            file.write('\nEND:\n\n')
#            
#        file.close()
#        