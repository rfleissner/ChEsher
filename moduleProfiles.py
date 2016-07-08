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
import ezdxf
from shapely.geometry import LineString

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
        self.profileStation = {}
        self.reachStation = {}
        self.profileIntersectingStation={}
        self.pointsNormalized = []
        self.segmentStation = []
        self.proArranged = {}

# module Mesh

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
        
#        print self.nodProfiles
#        print self.proProfiles
#        print self.nodReach
#        print self.points

        self.determineFlowDirection()
        self.pointsNormalized, self.segmentStation = self.normalizeProfiles()
        
        if self.ui.checkBoxOutputTextfile.isChecked():
            self.writeTXT()
#            try:
#                self.writeTXT()
#                info += " - Textfile created with {0} profiles and {1} points.\n".format(len(self.pointsNormalized), np.size(self.pointsNormalized)) 
#            except:
#                info += " - ERROR: Not able to write textfile!\n"

        if self.ui.checkBoxOutputDXF.isChecked():
            self.writeDXF()
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
        
    def determineFlowDirection(self):

        station_reach = 0.0
        profilecounter = 1
        direction = {}
        
        # get total length of reach
        reachlength = 0.0
        for nID_reach in range(len(self.nodReach)-1):
            nID_reach += 1
            nID_i = nID_reach
            nID_j = nID_reach+1
        
            xa = self.nodReach[nID_i][0]
            ya = self.nodReach[nID_i][1]
            xe = self.nodReach[nID_j][0]
            ye = self.nodReach[nID_j][1]
            
            reach_line = LineString([(xa, ya), (xe, ye)])            
            reachlength += reach_line.length
 
        # get total length of profiles
        profileLength = {}
        for pID in self.proProfiles:
            totLen = 0.0
            # loop over profile points
            for nID in range(len(self.proProfiles[pID])-1):
                ri = self.nodProfiles[self.proProfiles[pID][nID]][0]
                rj = self.nodProfiles[self.proProfiles[pID][nID]][1]
                si = self.nodProfiles[self.proProfiles[pID][nID+1]][0]
                sj = self.nodProfiles[self.proProfiles[pID][nID+1]][1]

                profile_line = LineString([(ri, rj), (si, sj)])
                totLen += profile_line.length
            profileLength[pID] = totLen
        
        # loop over reach points
        for nID_reach in range(len(self.nodReach)-1):
            nID_reach += 1
            nID_i = nID_reach
            nID_j = nID_reach+1
            
            xa = self.nodReach[nID_i][0]
            ya = self.nodReach[nID_i][1]
            xe = self.nodReach[nID_j][0]
            ye = self.nodReach[nID_j][1]
            
            reach_line = LineString([(xa, ya), (xe, ye)])
            
            # reach point station (zero on last point)
            self.reachStation[nID_reach] = reachlength-station_reach
            station_reach += reach_line.length
                    
            # loop over profiles
            for pID in self.proProfiles:
                cutStat = 0.0
 
                # loop over profile points
                for nID in range(len(self.proProfiles[pID])-1):

                    ri = self.nodProfiles[self.proProfiles[pID][nID]][0]
                    rj = self.nodProfiles[self.proProfiles[pID][nID]][1]
                    si = self.nodProfiles[self.proProfiles[pID][nID+1]][0]
                    sj = self.nodProfiles[self.proProfiles[pID][nID+1]][1]

                    profile_line = LineString([(ri, rj), (si, sj)])
                    
                    # if intersection between reach segment and profile segment?
                    if reach_line.intersects(profile_line) is True:
                        intersection = reach_line.intersection(profile_line)

                        # profile station
                        delta_reach = LineString([(intersection.x,intersection.y), (xe, ye)]).length
                        self.profileStation[profilecounter] = reachlength - station_reach + delta_reach
                        
                        # intersecting station of profile
                        delta_profile = LineString([(intersection.x,intersection.y), (ri, rj)]).length
                        cutStat+=delta_profile
                        profileIntersectingStation = cutStat
                        
                        # get flow direction of profile
                        dx = xa - xe
                        dy = ya - ye
                        if dx >=0.0 and dy >= 0.0 and abs(dx) <= abs(dy):
                            direction[profilecounter] = 'S'
                        elif dx <=0.0 and dy >= 0.0 and abs(dx) <= abs(dy):
                            direction[profilecounter] = 'S'
                        elif dx <=0.0 and dy >= 0.0 and abs(dx) >= abs(dy):
                            direction[profilecounter] = 'E'
                        elif dx <=0.0 and dy <= 0.0 and abs(dx) >= abs(dy):
                            direction[profilecounter] = 'E'
                        elif dx <=0.0 and dy <= 0.0 and abs(dx) <= abs(dy):
                            direction[profilecounter] = 'N'
                        elif dx >=0.0 and dy <= 0.0 and abs(dx) <= abs(dy):
                            direction[profilecounter] = 'N'
                        elif dx >=0.0 and dy <= 0.0 and abs(dx) >= abs(dy):
                            direction[profilecounter] = 'W'
                        elif dx >=0.0 and dy >= 0.0 and abs(dx) >= abs(dy):
                            direction[profilecounter] = 'W'                        
                        
                        startnode = self.proProfiles[pID][0]
                        endnode = self.proProfiles[pID][-1]

                        # reverse profile, if flow direction shows against reach direction
                        if direction[profilecounter] == 'N':
                            if self.nodProfiles[startnode][0] > self.nodProfiles[endnode][0]:
                                self.proProfiles[pID].reverse()
                                profileIntersectingStation = profileLength[pID] - profileIntersectingStation
                        elif direction[profilecounter] == 'E':
                            if self.nodProfiles[startnode][1] < self.nodProfiles[endnode][1]:
                                self.proProfiles[pID].reverse()
                                profileIntersectingStation = profileLength[pID] - profileIntersectingStation
                        elif direction[profilecounter] == 'S':
                            if self.nodProfiles[startnode][0] < self.nodProfiles[endnode][0]:
                                self.proProfiles[pID].reverse()
                                profileIntersectingStation = profileLength[pID] - profileIntersectingStation
                        elif direction[profilecounter] == 'W':
                            if self.nodProfiles[startnode][1] > self.nodProfiles[endnode][1]:
                                self.proProfiles[pID].reverse()
                                profileIntersectingStation = profileLength[pID] - profileIntersectingStation
 
                        self.proArranged[profilecounter] = self.proProfiles[pID]
                        self.profileIntersectingStation[profilecounter] = profileIntersectingStation
                        profilecounter += 1

                    else:
                        cutStat += profile_line.length
          
        self.reachStation[len(self.reachStation)+1] = station_reach

        info = "\nFlow direction:\n"
        for pID_Arranged in direction:
            info += ' - Profile {0}:\t{1}\n'.format(pID_Arranged, direction[pID_Arranged])

        return info

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
        for key in pointsNormalized:
            length = len(pointsNormalized[key])
            pointsNormalized[key] = pointsNormalized[key].reshape((length/4,4))
            
            # sort points by increasing stationing
            pointsNormalized[key] = pointsNormalized[key][pointsNormalized[key][:,3].argsort()]

        return pointsNormalized, segmentStation
    
    def writeTXT(self):
        
        fname = self.ui.lineEditOutputTextfile.text()
        file = open(fname, 'w')
        
        dec = self.ui.spinBoxDecimal.value()
        
        for pID in self.pointsNormalized:
            file.write(str(len(self.pointsNormalized[pID])) + '\n')
            for nID in range(len(self.pointsNormalized[pID])):
#                for i in range(len(self.pointsNormalized[pID][nID])):
                file.write(str(round(self.pointsNormalized[pID][nID][3],dec)) + '\t' + str(round(self.pointsNormalized[pID][nID][2],dec)) + '\n')
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
            file.write('STATION: '+str(round(self.profileStation[pID],dec))+'\n')
            if pID < len(self.pointsNormalized):
                reachlength = self.profileStation[pID]-self.profileStation[pID+1]
            else:
                reachlength = self.profileStation[pID]
                
            file.write('REACH LENGTHS: '+str(round(reachlength,dec))+', '+str(round(reachlength,dec))+', '+str(round(reachlength,dec))+'\n\n')

            file.write('CUT LINE: \n')
            for nID in self.proArranged[pID]:
                file.write(str(round(self.nodProfiles[nID][0],dec)) + ', '+str(round(self.nodProfiles[nID][1],dec)) + '\n')   
                    
            file.write('\nSURFACE LINE:\n')
            for nID in range(len(self.pointsNormalized[pID])):
                file.write(str(round(self.pointsNormalized[pID][nID][0],dec))+ ', ' + str(round(self.pointsNormalized[pID][nID][1],dec))+ ', ' + str(round(self.pointsNormalized[pID][nID][2],dec)) + '\n')        
            file.write('\nEND:\n\n')
            
        file.close()
        
    def writeDXF(self):
        
        fname = self.ui.lineEditOutputDXF.text()
        file = open(fname, 'w')
        
        layer = "0"

        dec = 2
        dz = -25.0
        superelev = 1.0
        scale = 100.0
        scale_mm = scale/1000.0
        off_band_x = 75.0*scale_mm
        off_band_z = 2.5*scale_mm
        h_band = 15*scale_mm
        textheight_bandtitle = 4.0*scale_mm
        textheight_band = 1.5*scale_mm
        markerlength = 2.5*scale_mm
        
        dwg = ezdxf.new(dxfversion='AC1018')

        msp = dwg.modelspace()
        
        for pID in self.pointsNormalized:
            
            off_z = pID*dz
            
            x = self.pointsNormalized[pID].transpose()[0]
            y = self.pointsNormalized[pID].transpose()[1]
            z = self.pointsNormalized[pID].transpose()[2]
            d = self.pointsNormalized[pID].transpose()[3]
            
            xmin = min(d)
            xmax = max(d)
            zmin = math.floor(min(z*superelev))
            zmax = math.ceil(max(z*superelev))

            # frame
            msp.add_line((xmin, off_z+zmin),(xmax,off_z+zmin), dxfattribs={'layer': 'frame'})
            msp.add_line((xmax,off_z+zmin),(xmax,off_z+zmax), dxfattribs={'layer': 'frame'})
            msp.add_line((xmin, off_z+zmin),(xmin,off_z+zmax), dxfattribs={'layer': 'frame'})
            
            # title
            text_frame = msp.add_text("NN = %.1f m" % round(math.floor(min(z)), 2), dxfattribs={'height': textheight_bandtitle})
            text_frame.set_pos((xmin-off_band_x+h_band/2.0, off_z+zmin), align='BOTTOM_LEFT')
#            frame = msp.add_line((xmin, off_z+zmax),(xmax,off_z+zmax), dxfattribs={'layer': 'frame'})
            text_pTitle = msp.add_text("Profil-Nr. {0}".format(len(self.pointsNormalized)-pID+1), dxfattribs={'height': textheight_bandtitle*1.5})
            text_pTitle.set_pos((xmin-off_band_x, off_z+zmax+textheight_bandtitle*1.5), align='BOTTOM_LEFT')
            text_pKm = msp.add_text("km %.3f" % round(self.profileStation[pID]/1000,3), dxfattribs={'height': textheight_bandtitle})
            text_pKm.set_pos((xmin-off_band_x, off_z+zmax), align='BOTTOM_LEFT')
            
            # scale factor
            text_M = msp.add_text("M = 1:%i/%i"%(int(scale),int(scale/superelev)), dxfattribs={'height': 0.75*textheight_bandtitle})
            text_M.set_pos((xmin-off_band_x, off_z+zmax-1.5*textheight_bandtitle*1.5), align='BOTTOM_LEFT')

            
            # axis 
            msp.add_line((self.profileIntersectingStation[pID], off_z+zmin),(self.profileIntersectingStation[pID],off_z+zmax), dxfattribs={'layer': 'axis', 'color':1})
            
            # band Hoehe
            msp.add_line((xmin-off_band_x, off_z+zmin-off_band_z),(xmax,off_z+zmin-off_band_z), dxfattribs={'layer': 'frame'})
            msp.add_line((xmin-off_band_x, off_z+zmin-off_band_z-h_band),(xmax,off_z+zmin-off_band_z-h_band), dxfattribs={'layer': 'frame'})
            msp.add_line((xmin-off_band_x, off_z+zmin-off_band_z),(xmin-off_band_x,off_z+zmin-off_band_z-h_band), dxfattribs={'layer': 'frame'})
#            msp.add_line((xmin, off_z+zmin-off_band_z),(xmin,off_z+zmin-off_band_z-h_band), dxfattribs={'layer': 'frame'})
#            msp.add_line((xmax, off_z+zmin-off_band_z),(xmax,off_z+zmin-off_band_z-h_band), dxfattribs={'layer': 'frame'})
            title_height = msp.add_text("Hoehe [m]", dxfattribs={'height': textheight_bandtitle})
            title_height.set_pos((xmin-off_band_x+h_band/2.0, off_z+zmin-off_band_z-h_band/2.0), align='MIDDLE_LEFT')
            
            # band Stationierung
            msp.add_line((xmin-off_band_x, off_z+zmin-off_band_z-2*h_band),(xmax,off_z+zmin-off_band_z-2*h_band), dxfattribs={'layer': 'frame'})
            msp.add_line((xmin-off_band_x, off_z+zmin-off_band_z-h_band),(xmin-off_band_x,off_z+zmin-off_band_z-2*h_band), dxfattribs={'layer': 'frame'})
#            msp.add_line((xmin, off_z+zmin-off_band_z-h_band),(xmin,off_z+zmin-off_band_z-2*h_band), dxfattribs={'layer': 'frame'})
#            msp.add_line((xmax, off_z+zmin-off_band_z-h_band),(xmax,off_z+zmin-off_band_z-2*h_band), dxfattribs={'layer': 'frame'})
            title_stationing = msp.add_text("Stationierung [m]", dxfattribs={'height': textheight_bandtitle})
            title_stationing.set_pos((xmin-off_band_x+h_band/2.0, off_z+zmin-off_band_z-3*h_band/2.0), align='MIDDLE_LEFT')
            
#            frame = msp.add_line((xmax,off_z+zmin),(xmax,off_z+zmax), dxfattribs={'layer': 'frame'})
#            frame = msp.add_line((xmin, off_z+zmin),(xmin,off_z+zmax), dxfattribs={'layer': 'frame'})
#            frame = msp.add_line((xmin, off_z+zmax),(xmax,off_z+zmax), dxfattribs={'layer': 'frame'})            
            
            
            profilepoints = []
            
            mx = []
            for nID in range(len(self.pointsNormalized[pID])):
                x1 = self.pointsNormalized[pID][nID][3]
                z1 = off_z+self.pointsNormalized[pID][nID][2]*superelev
                
                p1 = (x1, z1)
                profilepoints.append(p1)
                            
                # marker
                mx.append(x1)
                if nID != 0 and nID != len(self.pointsNormalized[pID])-1:
                    msp.add_line(p1,(x1,off_z+zmin), dxfattribs={'layer': 'marker', 'color':253})
                    if mx[nID]-mx[nID-1] < 1.5*textheight_band:
                        mx[nID] = mx[nID-1] + 1.5*textheight_band
                        msp.add_line((x1,off_z+zmin),(mx[nID],off_z+zmin-off_band_z), dxfattribs={'layer': 'marker', 'color':253})
                    else:
                        msp.add_line((x1,off_z+zmin),(x1,off_z+zmin-off_band_z), dxfattribs={'layer': 'marker', 'color':253})
                    
                msp.add_line((mx[nID], off_z+zmin-off_band_z), (mx[nID], off_z+zmin-off_band_z-markerlength),  dxfattribs={'layer': 'band'})   
                msp.add_line((mx[nID], off_z+zmin-off_band_z-h_band), (mx[nID], off_z+zmin-off_band_z-h_band+markerlength),  dxfattribs={'layer': 'band'})
                msp.add_line((mx[nID], off_z+zmin-off_band_z-h_band), (mx[nID], off_z+zmin-off_band_z-h_band-markerlength),  dxfattribs={'layer': 'band'})   
                msp.add_line((mx[nID], off_z+zmin-off_band_z-2*h_band), (mx[nID], off_z+zmin-off_band_z-2*h_band+markerlength),  dxfattribs={'layer': 'band'})

                # band text
                text_stationing = msp.add_text("%.{0}f".format(dec)%(x1-self.profileIntersectingStation[pID]), dxfattribs={'height': textheight_band, 'rotation': 90.0})
                text_stationing.set_pos((mx[nID], off_z+zmin-off_band_z-3*h_band/2.0), align='MIDDLE')
                text_height = msp.add_text("%.{0}f".format(dec)%self.pointsNormalized[pID][nID][2], dxfattribs={'height': textheight_band, 'rotation': 90.0})
                text_height.set_pos((mx[nID], off_z+zmin-off_band_z-h_band/2.0), align='MIDDLE')
                                
            profile = msp.add_polyline2d(profilepoints, dxfattribs={'layer': 'profile'})
       
#        print self.profileStation
#        print self.reachStation
#        print self.pointsNormalized
#        print self.segmentStation
#        print self.proArranged            

#            frame.rgb = coloursRGB[c]
            
#            print max(self.pointsNormalized[pID][self.pointsNormalized[pID][:,1]])
#            print x
#            print y
#            print z
#            print d
#            print 
#            print "xmax", xmax
#            print "zmin", zmin
#            print "zmax", zmax
            
#            for i in range(len(self.segmentStation[pID])):
#                xmax += self.segmentStation[pID][i]
#            print "xmax", xmax
            
            
            # ermittle ausdehnung in x und z
            # zeichne rahmen
            # zeichne band fuer stationierung, hoehe
            # zeichne profil und marker
#
#            
#            for segment in contour[c]['segments']:
#
#                p1 = contour[c]['vertices'][segment[0]]
#                p2 = contour[c]['vertices'][segment[1]]
#
#                poly = msp.add_line(p1, p2, dxfattribs={'layer': layer})
#                poly.rgb = coloursRGB[c]
#
#        if writelegend:
#
#            b = 75.0
#            ht = 8.0
#            h = 5.0
#            dxc = 5.0
#            bc = 20.0
#
#            legend = dwg.blocks.new(name='LEGEND')
#            legend.add_line([0.0, 0.0], [b, 0.0])
#            legend.add_line([0.0, 0.0], [0.0, -ht])
#            legend.add_line([b, 0.0], [b, -ht])
#            legend.add_line([0.0, -ht], [b, -ht])
#
#            tit = legend.add_text(title, dxfattribs={'insert': [b/2.0, -h/2.0], 'height':4.0/5.0*h, 'halign':1, 'valign':0})
#            tit.set_pos([b/2.0, -ht/2.0], align='MIDDLE_CENTER')
#
#            lc = 1
#            if subtitle != "":
#                legend.add_line([0.0, -ht], [b, -ht])
#                legend.add_line([0.0, -ht], [0.0, -2.0*ht])
#                legend.add_line([b, -ht], [b, -2.0*ht])
#                legend.add_line([0.0, -2.0*ht], [b, -2.0*ht])
#                tit = legend.add_text(subtitle, dxfattribs={'height':4.0/5.0*h})
#                tit.set_pos([b/2.0, -3.0*ht/2.0], align='MIDDLE_CENTER')
#                lc = 2
#            i = 0
#            for l in range(len(coloursRGB)):
#                p1 = [dxc, -lc*ht-l*h-h]
#                p2 = [dxc+bc, -lc*ht-l*h-h]
#                line = legend.add_line(p1, p2)
#                if reverse_order:
#                    i = len(coloursRGB)-l-1
#                else:
#                    i = l
#                line.rgb = coloursRGB[i]
#                ran = str(levels[i]) + separator + str(levels[i+1])
#                lev = legend.add_text(ran, dxfattribs={'height':2.0/5.0*h})
#                lev.set_pos([2*dxc+bc, -lc*ht-l*h-h], align='MIDDLE_LEFT')
#
#            legend.add_line([0, -lc*ht], [0, -lc*ht-len(coloursRGB)*h-h])
#            legend.add_line([b, -lc*ht], [b, -lc*ht-len(coloursRGB)*h-h])
#            legend.add_line([0, -lc*ht-len(coloursRGB)*h-h], [b, -lc*ht-len(coloursRGB)*h-h])
#
#            msp.add_blockref('LEGEND', origin, dxfattribs={
#                'xscale': 1.0,
#                'yscale': 1.0,
#                'rotation': 0.0})
#
        dwg.saveas(str(fname))