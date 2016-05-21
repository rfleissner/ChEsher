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
import macro as mc
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
        self.proArranged = {}
        self.proNormalized = {}
        self.nodNormalized = {}

# module Mesh

        self.callbackOpenProfilesFile = functools.partial(uih.getOpenFileName, "Open Profiles File", "Line Sets (*.i2s *.i3s)", self.ui.lineEditInputProfiles, self.directory, self.widget)
        QtCore.QObject.connect(self.ui.pushButtonInputProfiles, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackOpenProfilesFile)
        
        self.callbackOpenReachFile = functools.partial(uih.getOpenFileName, "Open Reach File", "Line Sets (*.i2s *.i3s)", self.ui.lineEditInputReach, self.directory, self.widget)
        QtCore.QObject.connect(self.ui.pushButtonInputReach, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackOpenReachFile)
        
        self.callbackOpenPointsFile = functools.partial(uih.getOpenFileName, "Open Points File", "Point Set (*.xyz)", self.ui.lineEditInputPoints, self.directory, self.widget)
        QtCore.QObject.connect(self.ui.pushButtonInputPoints, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackOpenPointsFile)

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
        
        print self.nodProfiles
        print self.proProfiles
        print self.nodReach
        print self.points

        self.determineFlowDirection()
        self.normalizeProfiles()
        
    def determineFlowDirection(self):

        profilecounter = 1
        direction = {}

        for nID_reach in range(len(self.nodReach)):
            nID_reach += 1

            # determine flow direction of reach segments
            if nID_reach <= len(self.nodReach)-1:
                xa = self.nodReach[nID_reach][0]
                xe = self.nodReach[nID_reach+1][0]
                ya = self.nodReach[nID_reach][1]
                ye = self.nodReach[nID_reach+1][1]
                dx = xa - xe
                dy = ya - ye
                if dx >=0.0 and dy >= 0.0 and abs(dx) <= abs(dy):
                    direction[nID_reach] = 'S'
                elif dx <=0.0 and dy >= 0.0 and abs(dx) <= abs(dy):
                    direction[nID_reach] = 'S'
                elif dx <=0.0 and dy >= 0.0 and abs(dx) >= abs(dy):
                    direction[nID_reach] = 'E'
                elif dx <=0.0 and dy <= 0.0 and abs(dx) >= abs(dy):
                    direction[nID_reach] = 'E'
                elif dx <=0.0 and dy <= 0.0 and abs(dx) <= abs(dy):
                    direction[nID_reach] = 'N'
                elif dx >=0.0 and dy <= 0.0 and abs(dx) <= abs(dy):
                    direction[nID_reach] = 'N'
                elif dx >=0.0 and dy <= 0.0 and abs(dx) >= abs(dy):
                    direction[nID_reach] = 'W'
                elif dx >=0.0 and dy >= 0.0 and abs(dx) >= abs(dy):
                    direction[nID_reach] = 'W'
            else:
                direction[nID_reach] = direction[nID_reach-1]

            # determine closest profile node to current reach node
            closestnode = mc.getClosestNode(self.nodReach[nID_reach], self.nodProfiles.keys(), self.nodProfiles)

            # determine profile that inherits closest profile node
            for pID_raw in self.proProfiles:

                for nID_raw in range(len(self.proProfiles[pID_raw])):
                    if closestnode == self.proProfiles[pID_raw][nID_raw]:

                        startnode = self.proProfiles[pID_raw][0]
                        endnode = self.proProfiles[pID_raw][-1]

                        if direction[profilecounter] == 'N':
                            if self.nodProfiles[startnode][0] > self.nodProfiles[endnode][0]:
                                self.proProfiles[pID_raw].reverse()
                        elif direction[profilecounter] == 'E':
                            if self.nodProfiles[startnode][1] < self.nodProfiles[endnode][1]:
                                self.proProfiles[pID_raw].reverse()
                        elif direction[profilecounter] == 'S':
                            if self.nodProfiles[startnode][0] < self.nodProfiles[endnode][0]:
                                self.proProfiles[pID_raw].reverse()
                        elif direction[profilecounter] == 'W':
                            if self.nodProfiles[startnode][1] > self.nodProfiles[endnode][1]:
                                self.proProfiles[pID_raw].reverse()

                        self.proArranged[profilecounter] = self.proProfiles[pID_raw]
                        profilecounter += 1
                        break

        info = "\nFlow direction:\n"
        for pID_Arranged in direction:
            info += ' - Profile {0}:\t{1}\n'.format(pID_Arranged, direction[pID_Arranged])
            
        return info
        
    def normalizeProfiles(self):

        # 
        tempDist = dict([(key+1, []) for key in range(len(self.points))])
        tempProfileID = dict([(key+1, []) for key in range(len(self.points))])
        tempProfileSegmentID = dict([(key+1, []) for key in range(len(self.points))])
        tempP = dict([(key+1, []) for key in range(len(self.points))])
        tempOnsegment = dict([(key+1, []) for key in range(len(self.points))])
        tempStation = dict([(key+1, []) for key in range(len(self.points))])
        segmentStation = dict([(key, []) for key in self.proArranged])

        # loop over profiles
        for pID in self.proArranged:
            s = 0.0
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
        
        pointsNormalized = {}
        pointsStation = {}
        pointsProfileID = {}
        pointsProfileSegmentID = {}

        
        nodecounter = 0
        for nID in tempDist:
            while True:
                ID = tempDist[nID].index(min(tempDist[nID]))
                if tempOnsegment[nID][ID] is True:
                    nodecounter += 1
                    pID = tempProfileID[nID][ID]
                    pointsProfileID[nodecounter] = tempProfileID[nID][ID]
                    pointsNormalized[nodecounter] = tempP[nID][ID]
                    pointsProfileSegmentID[nodecounter] = tempProfileSegmentID[nID][ID]
                    
                    station = tempStation[nID][ID]
                    if pointsProfileSegmentID[nodecounter] > 0:
                        for i in range(tempProfileSegmentID[nID][ID]):
                            station += segmentStation[pID][i]
                            
                    pointsStation[nodecounter] = station
                    break
                else:
                    del tempDist[nID][ID]
                    del tempProfileID[nID][ID]
                    del tempProfileSegmentID[nID][ID]
                    del tempP[nID][ID]
                    del tempOnsegment[nID][ID]
                    del tempStation[nID][ID]
        
        # sort normalized points
        tempPro = dict((key, np.array([])) for key in self.proArranged)

        for key in pointsNormalized:
            print pointsNormalized[key], pointsStation[key], pointsProfileID[key], pointsProfileSegmentID[key]
            arr1 = np.array(pointsNormalized[key])
            arr2 = np.array([pointsStation[key]])
            arr = np.append(arr1, arr2)
            tempPro[pointsProfileID[key]] = np.append(tempPro[pointsProfileID[key]], arr)
        
        for key in tempPro:
            length = len(tempPro[key])
            tempPro[key] = tempPro[key].reshape((length/4,4))
            print tempPro[key]
            
#            
#            # loop over profile segments
#            for pnID in range(len(self.proArranged[pID])-1):
#                nID_i = self.proArranged[pID][pnID]
#                nID_j = self.proArranged[pID][pnID+1]
#                
#                # loop over normalized points
#                for nID in pointsNormalized[pID]:
#                    
#                    # determine orthogonal projection to profile segment
#                    a = self.nodProfiles[nID_i][0:2]
#                    b = self.nodProfiles[nID_j][0:2]
#                    
#                    ab = math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)
#                    aP = math.sqrt((a[0]-P[0])**2 + (a[1]-P[1])**2)
#                    bP = math.sqrt((b[0]-P[0])**2 + (b[1]-P[1])**2)
                    
                    
                    
                    
        # loop ueber profile
        #   
        # loop ueber profile
        #   loop ueber punkte, ordne punkte zu profilen zu (ueber kuerzesten orthogonalabstand)
        # loop ueber profile 
        #   ordne normalisierte punkte von links nach rechts
