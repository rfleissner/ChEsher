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
        self.reachStation = []
        self.nodProfiles = {}
        self.proProfiles = {}

        # results
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
        
        self.callbackSaveDXFfile = functools.partial(uih.getSaveFileName, "Save textfile As", "Normal text file (*.txt)", self.ui.lineEditOutputDXF, self.directory, self.widget)
        QtCore.QObject.connect(self.ui.pushButtonOutputDXF, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackSaveDXFfile)
        
        self.callbackSaveHECRAS = functools.partial(uih.getSaveFileName, "Save textfile As", "Normal text file (*.txt)", self.ui.lineEditOutputHECRAS, self.directory, self.widget)
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
        
        print self.nodProfiles
        print self.proProfiles
        print self.nodReach
        print self.points

        self.determineFlowDirection()
        self.pointsNormalized, self.segmentStation = self.normalizeProfiles()
        self.writeTXT()
#        if self.ui.checkBoxOutputTextfile.isChecked():
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
                
    def determineFlowDirection(self):


        profilecounter = 1
        direction = {}
        self.reachStation.append(0.0)
        
        for nID_reach in range(len(self.nodReach)-1):
            nID_reach += 1
            nID_i = nID_reach
            nID_j = nID_reach+1
            
            xi = self.nodReach[nID_i][0]
            yi = self.nodReach[nID_i][1]
            xj = self.nodReach[nID_j][0]
            yj = self.nodReach[nID_j][1]
            
            reach_line = LineString([(xi, yi), (xj, yj)])
            
            for pID in self.proProfiles:
                for nID in range(len(self.proProfiles[pID])-1):

                    ri = self.nodProfiles[self.proProfiles[pID][nID]][0]
                    rj = self.nodProfiles[self.proProfiles[pID][nID]][1]
                    si = self.nodProfiles[self.proProfiles[pID][nID+1]][0]
                    sj = self.nodProfiles[self.proProfiles[pID][nID+1]][1]

                    profile_line = LineString([(ri, rj), (si, sj)])

                    print reach_line.intersection(profile_line)

            # erstelle mit i und j ein linestring R
            # loop ueber alle profile
            #   erstelle linestring und verschneide mit linestring R
            #   ermittle stationierung von profil
            #   bring profil in reihenfolge
            
            
#            if nID_reach < len(self.nodReach):
#                nID_i = nID_reach
#                nID_j = nID_reach+1
#                a = self.nodReach[nID_i][0:2]
#                b = self.nodReach[nID_j][0:2]
#                ab = math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)
#                self.reachStation.append(ab)
            
            
        for nID_reach in range(len(self.nodReach)):
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
#            print tempPointsNormalized[key], tempPointsStation[key], tempPointsProfileID[key], tempPointsProfileSegmentID[key]
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
            
#            print pointsNormalized[key]
        
        return pointsNormalized, segmentStation
    
#    def writeTXT(self):
#
#        fname = self.ui.lineEditOutputTextfile.text()
#        file = open(fname, 'w')
#        
#        for pID in self.pointsNormalized:
#            file.write(str(len(self.pointsNormalized[pID])) + '\n')
#            for nID in range(len(self.pointsNormalized[pID])):
##                for i in range(len(self.pointsNormalized[pID][nID])):
#                file.write(str(self.pointsNormalized[pID][nID][3]) + '\t' + str(self.pointsNormalized[pID][nID][2]) + '\n')
#        file.close()
        
    def writeTXT(self):

        fname = self.ui.lineEditOutputTextfile.text()
        file = open(fname, 'w')
        file.write('river\n\n')
        file.write('BEGIN HEADER:\n\n')
        file.write('NUMBER OF REACHES: 1\n')
        file.write('NUMBER OF CROSS SECTIONS:'+str(len(self.proArranged))+'\n')
        file.write('UNITS: Meters\n\n')
        file.write('END HEADER:\n\n')
        
        file.write('BEGIN STREAM NETWORK:\n')
        for nID in self.nodReach:
            file.write('Endpoint: '+str(self.nodReach[nID][0])+', '+str(self.nodReach[nID][1])+', 0.0, '+str(nID)+'\n')
            
        file.write('\nREACH:\n\n')
        file.write('STREAM ID: river\n')
        file.write('REACH ID: reach\n')
        file.write('FROM POINT: 1\n')
        file.write('TO POINT: '+str(len(self.nodReach))+'\n\n')
        file.write('CENTERLINE:\n')
        station = 0.0
        for nID in self.nodReach:
            station += self.reachStation[nID-1]
            file.write(str(self.nodReach[nID][0])+', '+str(self.nodReach[nID][1])+', 0.0, '+str(station)+'\n')
        file.write('END:\n\n')
        file.write('END STREAM NETWORK:\n\n\n')
        file.write('BEGIN CROSS-SECTIONS:\n\n\n')
        station = 0.0
        for pID in self.pointsNormalized:
            file.write('CROSS-SECTION:\n\n')

            file.write('STREAM ID: river\n')
            file.write('REACH ID: reach\n')
            file.write('STATION: '+str(station)+'\n')
            station += self.reachStation[pID]
            file.write('REACH LENGTHS: '+str(self.reachStation[pID])+', '+str(self.reachStation[pID])+', '+str(self.reachStation[pID])+'\n\n')

            file.write('CUT LINE: \n')
            for nID in self.proArranged[pID]:
                file.write(str(self.nodProfiles[nID][0]) + ', '+str(self.nodProfiles[nID][1]) + '\n')   
                    
            file.write('\nSURFACE LINE:\n')
            for nID in range(len(self.pointsNormalized[pID])):
                file.write(str(self.pointsNormalized[pID][nID][0])+ ', ' + str(self.pointsNormalized[pID][nID][1])+ ', ' + str(self.pointsNormalized[pID][nID][2]) + '\n')        
            file.write('\nEND:\n\n')
            
        file.close()
        
    def writeDXF(self):
        
        fname = self.ui.lineEditOutputDXF.text()
        file = open(fname, 'w')
        
        layer = "0"
        
        dwg = ezdxf.new(dxfversion='AC1018')

        msp = dwg.modelspace()

#        pointsNormalized, 
        for pID in self.pointsNormalized:
            

            x = self.pointsNormalized[pID].transpose()[0]
            y = self.pointsNormalized[pID].transpose()[1]
            z = self.pointsNormalized[pID].transpose()[2]
            d = self.pointsNormalized[pID].transpose()[3]
            
            xmax = max(d)
            zmin = min(z)
            zmax = max(z)
            
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