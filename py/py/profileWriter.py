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


"""Module for writing cross section to dxf file."""

__author__="Reinhard Fleissner"
__date__ ="$15.07.2016 18:21:40$"

import ezdxf
import math

from shapely.geometry import LineString, Polygon 
from scipy import interpolate

import os.path as pth
ezdxf.options.template_dir = pth.abspath('.')


class ProfileWriter():
    """Writing cross sections to dxf file format"""

    def __init__(self, fname, bottom, reachStation, profileStation, scale, superelevation, settings, reachName):
        """Constructor."""
        
        self.fname = fname
        self.bottom = bottom
        self.reachStation = reachStation
        self.profileStation = profileStation
        self.scale = scale
        self.superelev = superelevation
        self.settings = settings
        self.reachName = reachName
        self.nOfProfiles = len(self.bottom)
        
        # 1d hydraulic entities
        self.ws1dNames = None
        self.ws1dElevations = None
        self.levees = None

        # user defined parameters
        
        scale_mm = self.scale/1000.0        

        self.drawFrame = self.settings["Frame"]
        self.drawBand = self.settings["Band"]
        self.ProfileName = self.settings["ProfileName"]
        self.ReachStationPrefix = self.settings["ReachStation"]
        self.ScaleFactorPrefix = self.settings["ScaleFactor"]
        self.ReferenceLevelPrefix = self.settings["ReferenceLevel"]
        self.BandTitleStationing = self.settings["BandTitleStationing"]
        self.BandTitleElevation = self.settings["BandTitleElevation"]
        self.dec = self.settings["DecimalPlaces"]
        self.off_band_x = self.settings["doubleSpinBoxOffsetX"] * scale_mm
        self.off_band_z = self.settings["doubleSpinBoxOffsetZ"] * scale_mm
        self.h_band = self.settings["doubleSpinBoxBandHeight"] * scale_mm
        self.textheight_bandtitle = self.settings["doubleSpinBoxTextSizeBandTitle"]*scale_mm
        self.textheight_band = self.settings["doubleSpinBoxTextSizeBand"] * scale_mm
        self.markerlength = self.settings["doubleSpinBoxMarkerSize"] * scale_mm
        self.bereinig = self.settings["doubleSpinBoxCleanValues"]

        self.offVE = 0.0
        self.off_band = 0.0 * self.h_band
        self.off_raster = 0.0

#        self.dec = 2
#        self.superelev = 1.0
#        self.scale = 100.0
#        
#        scale_mm = self.scale/1000.0
#        self.drawBand = True
#        self.drawFrame = True
#        self.bereinig = 2.0
#        self.off_band_x = 75.0*scale_mm
#        self.off_band_z = 2.5*scale_mm
#        self.h_band = 15*scale_mm
#        self.textheight_bandtitle = 4.0*scale_mm
#        self.textheight_band = 1.5*scale_mm
#        self.markerlength = 1.5*scale_mm
#    
#        self.offVE = 0.0
#        self.off_band = 0.0 * self.h_band
#        self.off_raster = 0.0        
        
        # parameters
        
        self.dz = -self.scale/5.0
        
        self.dwg = ezdxf.new(dxfversion='AC1018')
        self.msp = self.dwg.modelspace()

        self.xmin = {}
        self.xmax = {}
        self.zmin = {}
        self.zmax = {}
        self.bottompoints = {}
        
    def drawBottom(self):

        for pID in self.bottom:

            off_z = pID*self.dz
            
            z = self.bottom[pID][2]
            d = self.bottom[pID][3]

            xmin = min(d)
            xmax = max(d)
            zmin = math.floor(min(z*self.superelev)-self.offVE)-1.0
            zmax = math.ceil(max(z*self.superelev))

            self.xmin[pID] = xmin
            self.xmax[pID] = xmax
            self.zmin[pID] = zmin
            self.zmax[pID] = zmax
            
            # frame
            if self.drawFrame:
                self.msp.add_line((xmax,off_z+zmin),(xmax,off_z+zmax), dxfattribs={'layer': 'frame'})
                self.msp.add_line((xmin, off_z+zmin),(xmin,off_z+zmax), dxfattribs={'layer': 'frame'})
            self.msp.add_line((xmin, off_z+zmin),(xmax,off_z+zmin), dxfattribs={'layer': 'frame'})
            print zmin, self.superelev, zmin/self.superelev
            # title
#            text_frame = self.msp.add_text(self.ReferenceLevelPrefix + "%.1f m" % round(math.floor(min(z-self.offVE)), 2), dxfattribs={'height': self.textheight_bandtitle})
            text_frame = self.msp.add_text(self.ReferenceLevelPrefix + "%.1f m" % float(zmin/self.superelev), dxfattribs={'height': self.textheight_bandtitle})
            text_frame.set_pos((xmin-self.off_band_x+self.h_band/2.0, off_z+zmin), align='BOTTOM_LEFT')
            text_pTitle = self.msp.add_text("{0}{1}".format(self.ProfileName, self.nOfProfiles-pID+1), dxfattribs={'height': self.textheight_bandtitle*1.5})
            text_pTitle.set_pos((xmin-self.off_band_x, off_z+zmax+self.textheight_bandtitle*1.5), align='BOTTOM_LEFT')
            text_pKm = self.msp.add_text(self.ReachStationPrefix + "%.3f" % round(self.reachStation[pID]/1000,3), dxfattribs={'height': self.textheight_bandtitle})
            text_pKm.set_pos((xmin-self.off_band_x, off_z+zmax), align='BOTTOM_LEFT')

            # scale factor
            text_M = self.msp.add_text(self.ScaleFactorPrefix + "1:%i/%i"%(int(self.scale),int(self.scale/self.superelev)), dxfattribs={'height': 0.75*self.textheight_bandtitle})
            text_M.set_pos((xmin-self.off_band_x, off_z+zmax-1.5*self.textheight_bandtitle*1.5), align='BOTTOM_LEFT')

            # axis
            if self.profileStation[pID] >= 0.0001:
                self.msp.add_line((self.profileStation[pID], off_z+zmin),(self.profileStation[pID],off_z+zmax), dxfattribs={'layer': 'axis', 'color':1})
                text_axis = self.msp.add_text(self.reachName, dxfattribs={'height': self.textheight_bandtitle, 'color':1})
                text_axis.set_pos((self.profileStation[pID], off_z+zmax), align='BOTTOM_CENTER')
                
            # band
            if self.drawBand:
                # elevation
                self.msp.add_line((xmin-self.off_band_x, off_z+zmin-self.off_band_z+self.off_band),(xmax,off_z+zmin-self.off_band_z+self.off_band), dxfattribs={'layer': 'frame'})
                self.msp.add_line((xmin-self.off_band_x, off_z+zmin-self.off_band_z-self.h_band+self.off_band),(xmax,off_z+zmin-self.off_band_z-self.h_band+self.off_band), dxfattribs={'layer': 'frame'})
                self.msp.add_line((xmin-self.off_band_x, off_z+zmin-self.off_band_z+self.off_band),(xmin-self.off_band_x,off_z+zmin-self.off_band_z-self.h_band+self.off_band), dxfattribs={'layer': 'frame'})
                title_height = self.msp.add_text(self.BandTitleStationing, dxfattribs={'height': self.textheight_bandtitle})
                title_height.set_pos((xmin-self.off_band_x+self.h_band/2.0, off_z+zmin-self.off_band_z-self.h_band/2.0+self.off_band), align='MIDDLE_LEFT')

                # stationing
                self.msp.add_line((xmin-self.off_band_x, off_z+zmin-self.off_band_z-2*self.h_band+self.off_band),(xmax,off_z+zmin-self.off_band_z-2*self.h_band+self.off_band), dxfattribs={'layer': 'frame'})
                self.msp.add_line((xmin-self.off_band_x, off_z+zmin-self.off_band_z-self.h_band+self.off_band),(xmin-self.off_band_x,off_z+zmin-self.off_band_z-2*self.h_band+self.off_band), dxfattribs={'layer': 'frame'})
                title_stationing = self.msp.add_text(self.BandTitleElevation, dxfattribs={'height': self.textheight_bandtitle})
                title_stationing.set_pos((xmin-self.off_band_x+self.h_band/2.0, off_z+zmin-self.off_band_z-3*self.h_band/2.0+self.off_band), align='MIDDLE_LEFT')

            bottompoints = []
            mx = []
            x0 = -1000000.0
            mxcounter = -1
            for nID in range(len(d)):
                x1 = d[nID]
                z1 = off_z+z[nID]*self.superelev

                p1 = (x1, z1)
                bottompoints.append(p1)

                # marker
                if self.drawBand:

                    if (abs(x1 - x0) >= self.bereinig) or (len(mx) == 0):
                        mx.append(x1)
                        mxcounter+=1

                        if len(mx) > 1 and nID != len(d)-1: 
                            self.msp.add_line(p1,(x1,off_z+zmin+self.off_raster), dxfattribs={'layer': 'marker', 'color':253})
                        
                        if len(mx) > 1:    
                            if mx[mxcounter]-mx[mxcounter-1] < 1.5*self.textheight_band:
                                mx[mxcounter] = mx[mxcounter-1] + 1.5*self.textheight_band
                                self.msp.add_line((x1,off_z+zmin+self.off_raster),(mx[mxcounter],off_z+zmin-self.off_band_z), dxfattribs={'layer': 'marker', 'color':253})
                            else:
                                self.msp.add_line((x1,off_z+zmin+self.off_raster),(x1,off_z+zmin-self.off_band_z), dxfattribs={'layer': 'marker', 'color':253})
                        else:
                            self.msp.add_line((x1,off_z+zmin+self.off_raster),(x1,off_z+zmin-self.off_band_z), dxfattribs={'layer': 'marker', 'color':253})
                    
                        # band
                        self.msp.add_line((mx[mxcounter], off_z+zmin-self.off_band_z+self.off_band), (mx[mxcounter], off_z+zmin-self.off_band_z-self.markerlength+self.off_band),  dxfattribs={'layer': 'band'})   
                        self.msp.add_line((mx[mxcounter], off_z+zmin-self.off_band_z-self.h_band+self.off_band), (mx[mxcounter], off_z+zmin-self.off_band_z-self.h_band+self.markerlength+self.off_band),  dxfattribs={'layer': 'band'})
                        self.msp.add_line((mx[mxcounter], off_z+zmin-self.off_band_z-self.h_band+self.off_band), (mx[mxcounter], off_z+zmin-self.off_band_z-self.h_band-self.markerlength+self.off_band),  dxfattribs={'layer': 'band'})   
                        self.msp.add_line((mx[mxcounter], off_z+zmin-self.off_band_z-2*self.h_band+self.off_band), (mx[mxcounter], off_z+zmin-self.off_band_z-2*self.h_band+self.markerlength+self.off_band),  dxfattribs={'layer': 'band'})
                        text_stationing = self.msp.add_text("%.{0}f".format(self.dec)%(x1-self.profileStation[pID]), dxfattribs={'height': self.textheight_band, 'rotation': 90.0})
                        text_stationing.set_pos((mx[mxcounter], off_z+zmin-self.off_band_z-self.h_band/2.0+self.off_band), align='MIDDLE')
                        text_height = self.msp.add_text("%.{0}f".format(self.dec)%z[nID], dxfattribs={'height': self.textheight_band, 'rotation': 90.0})
                        text_height.set_pos((mx[mxcounter], off_z+zmin-self.off_band_z-3*self.h_band/2.0+self.off_band), align='MIDDLE')
                        x0 = x1
            self.bottompoints[pID] = bottompoints
            # draw bottom line
            self.msp.add_polyline2d(bottompoints, dxfattribs={'layer': 'profile'})

    def drawWaterSurface(self, ws, col):
        
        wsCounter = 0

        for name in ws:
            wsCounter += 1
            for pID in ws[name]:

                p = ws[name][pID]
                off_z = pID*self.dz
                z = p[2]
                d = p[3]

                z_bottom = self.bottom[pID][2]
                d_bottom = self.bottom[pID][3]
            
                f = interpolate.interp1d(d_bottom, z_bottom)

                xmin = self.xmin[pID]
                xmax = self.xmax[pID]
                zmin = self.zmin[pID]
                zmax = self.zmax[pID]

                # band
                if self.drawBand:
                    # stationing
                    self.msp.add_line((xmin-self.off_band_x, off_z+zmin-self.off_band_z-(2+wsCounter)*self.h_band),(xmax,off_z+zmin-self.off_band_z-(2+wsCounter)*self.h_band), dxfattribs={'layer': 'frame'})
                    self.msp.add_line((xmin-self.off_band_x, off_z+zmin-self.off_band_z-self.h_band),(xmin-self.off_band_x,off_z+zmin-self.off_band_z-(2+wsCounter)*self.h_band), dxfattribs={'layer': 'frame'})
                    title_height = self.msp.add_text(name, dxfattribs={'height': self.textheight_bandtitle})
                    title_height.set_pos((xmin-self.off_band_x+self.h_band/2.0, off_z+zmin-self.off_band_z-(2+wsCounter-1./2.)*self.h_band), align='MIDDLE_LEFT')
                    title_height.rgb = col[name]
                cou = 1
                profilepoints = {}
                profilepoint = []

                mx = []
                x0 = -1000000.0
                mxcounter = -1
                
                for nID in range(len(d)):

                    x1 = d[nID]
                    z1 = off_z+z[nID]*self.superelev

                    z_interp = f(x1)
                    
                    # print water surface, if the water depth is greater than 0.01
                    zeroWS = True
                    if z[nID] - z_interp >= 0.01:
                        zeroWS = False
                        p1 = (x1, z1)
                        profilepoint.append(p1)
                    else:
                        if len(profilepoint)>0:
                            profilepoints[cou] = profilepoint
                            cou += 1
                            profilepoint = []

                    # marker
                    if self.drawBand:

                        if (abs(x1 - x0) >= self.bereinig) or (len(mx) == 0):
                            mx.append(x1)
                            mxcounter+=1

                            if len(mx) > 1:    
                                if mx[mxcounter]-mx[mxcounter-1] < 1.5*self.textheight_band:
                                    mx[mxcounter] = mx[mxcounter-1] + 1.5*self.textheight_band

                            # band
                            if not zeroWS:
                                self.msp.add_line((mx[mxcounter], off_z+zmin-self.off_band_z-(1+wsCounter)*self.h_band), (mx[mxcounter], off_z+zmin-self.off_band_z-(1+wsCounter)*self.h_band-self.markerlength),  dxfattribs={'layer': 'band'})   
                                self.msp.add_line((mx[mxcounter], off_z+zmin-self.off_band_z-(2+wsCounter)*self.h_band), (mx[mxcounter], off_z+zmin-self.off_band_z-(2+wsCounter)*self.h_band+self.markerlength),  dxfattribs={'layer': 'band'})
                                text_height = self.msp.add_text("%.{0}f".format(self.dec)%z[nID], dxfattribs={'height': self.textheight_band, 'rotation': 90.0})
                                text_height.set_pos((mx[mxcounter], off_z+zmin-self.off_band_z-(2+wsCounter-1./2.)*self.h_band), align='MIDDLE')
                                text_height.rgb = col[name]
                                x0 = x1
                        
                # draw water surface
                if len(profilepoint)>0:
                    profilepoints[cou] = profilepoint
                    
                for key in profilepoints:
                    poly = self.msp.add_polyline2d(profilepoints[key], dxfattribs={'layer': 'profile'})
                    poly.rgb = col[name]

    def draw1dResults(self, ws1dNames, ws1dElevations, levees):

        # print 1d water elevation
        for pID in range(len(ws1dElevations)):
            pID+=1
            off_z = pID*self.dz
            
            xmin = self.xmin[pID]
            xmax = self.xmax[pID]
            zmin = self.zmin[pID]
            zmax = self.zmax[pID]
            profilepoints = self.bottompoints[pID]
            
            #legend
            n = len(ws1dElevations[pID])
            h = (n+1.0+(n-1)*0.5)*0.75*self.textheight_bandtitle
            dh = 0.75*self.textheight_bandtitle
            
            self.msp.add_line((xmin+dh, off_z+zmin+dh),(xmin+dh, off_z+zmin+h+dh), dxfattribs={'layer': 'frame'})
            self.msp.add_line((xmin+self.off_band_x+dh, off_z+zmin+dh),(xmin+self.off_band_x+dh, off_z+zmin+h+dh), dxfattribs={'layer': 'frame'})
            self.msp.add_line((xmin+dh, off_z+zmin+dh),(xmin+self.off_band_x+dh, off_z+zmin+dh), dxfattribs={'layer': 'frame'})
            self.msp.add_line((xmin+dh, off_z+zmin+h+dh),(xmin+self.off_band_x+dh, off_z+zmin+h+dh), dxfattribs={'layer': 'frame'})
                
            for wID in range(len(ws1dElevations[pID])):

                wsElevation = ws1dElevations[pID][wID]
                layerName = ws1dNames[wID]
                layerColor = 2+wID
                
                # legend
                self.msp.add_line((xmin+dh+dh, off_z+zmin+h-(wID+1+wID*0.5)*dh+dh),(xmin+dh+h+dh, off_z+zmin+h-(wID+1+wID*0.5)*dh+dh), dxfattribs={'layer': layerName, 'color':layerColor})
                text_M = self.msp.add_text(ws1dNames[wID] +" = %.{0}f m".format(self.dec)%wsElevation, dxfattribs={'height': 0.75*self.textheight_bandtitle})
                text_M.set_pos((xmin+dh+h+dh+dh, off_z+zmin+h-(wID+1+wID*0.5)*dh+dh), align='MIDDLE_LEFT')
                
                tup = tuple([(xmin-1.0,off_z+zmax*self.superelev)] + profilepoints + [(xmax+1.0,off_z+zmax*self.superelev)])
                bottomLine = Polygon(tup)
                wsLine = LineString([(xmin, off_z+wsElevation*self.superelev), (xmax, off_z+wsElevation*self.superelev)])
                inters = bottomLine.intersection(wsLine)

                if inters.geom_type == "LineString":
                    self.msp.add_line((inters.coords[:][0][0], off_z+wsElevation*self.superelev), (inters.coords[:][1][0], off_z+wsElevation*self.superelev),  dxfattribs={'layer': layerName, 'color':layerColor})

                if inters.geom_type == "MultiLineString":     
                    for i in range(len(inters)):
                        ls = inters[i]
                        self.msp.add_line((ls.coords[:][0][0], off_z+wsElevation*self.superelev), (ls.coords[:][1][0], off_z+wsElevation*self.superelev),  dxfattribs={'layer': layerName, 'color':layerColor})

            # print levees
            if pID in levees:
                for lID in range(len(levees[pID])):
                    levee_x = levees[pID][lID][0]*xmax
                    levee_z = levees[pID][lID][1]
                    bottomLine = LineString(tup)
                    levee = LineString([(levee_x, off_z+zmin), (levee_x, off_z+zmax)])
                    inters = bottomLine.intersection(levee)

                    self.msp.add_line((levee_x, inters.y), (levee_x, off_z+levee_z*self.superelev),  dxfattribs={'layer': 'levee', 'color':1})
            
    def saveDXF(self):
        self.dwg.saveas(str(self.fname))
























#"""Module for writing cross section to dxf file."""
#
#__author__="Reinhard Fleissner"
#__date__ ="$15.07.2016 18:21:40$"
#
#import ezdxf
#import math
#from shapely.geometry import LineString, Polygon 
#
#import os.path as pth
#ezdxf.options.template_dir = pth.abspath('.')
#
#def writeProfile(fname, bottom, reachStation, profileStation, wsNames=None, wsElevations=None, levees=None):
#    """
#    bottom = {1: [[di], [zi]], ..., self.nOfProfiles:[[di],[zi]]}
    #"""
#    
#    layer = "0"
#
#    self.nOfProfiles = len(bottom)
#    dec = 2
#    dz = -25.0
#    superelev = 1.0
#    scale = 200.0
#    scale_mm = scale/1000.0
#    off_band_x = 75.0*scale_mm
#    off_band_z = 2.5*scale_mm
#    h_band = 15*scale_mm
#    textheight_bandtitle = 4.0*scale_mm
#    textheight_band = 1.5*scale_mm
#    markerlength = 2.5*scale_mm
#
#    dwg = ezdxf.new(dxfversion='AC1018')
#
#    msp = dwg.modelspace()
#
#    for pID in bottom:
#
#        off_z = pID*dz
#        z = bottom[pID][2]
#        d = bottom[pID][3]
#
#        xmin = min(d)
#        xmax = max(d)
#        zmin = math.floor(min(z*superelev))
#        zmax = math.ceil(max(z*superelev))
#        
#        # frame
#        msp.add_line((xmin, off_z+zmin),(xmax,off_z+zmin), dxfattribs={'layer': 'frame'})
#        msp.add_line((xmax,off_z+zmin),(xmax,off_z+zmax), dxfattribs={'layer': 'frame'})
#        msp.add_line((xmin, off_z+zmin),(xmin,off_z+zmax), dxfattribs={'layer': 'frame'})
#
#        # title
#        text_frame = msp.add_text("NN = %.1f m" % round(math.floor(min(z)), 2), dxfattribs={'height': textheight_bandtitle})
#        text_frame.set_pos((xmin-off_band_x+h_band/2.0, off_z+zmin), align='BOTTOM_LEFT')
##            frame = msp.add_line((xmin, off_z+zmax),(xmax,off_z+zmax), dxfattribs={'layer': 'frame'})
#        text_pTitle = msp.add_text("Profil-Nr. {0}".format(self.nOfProfiles-pID+1), dxfattribs={'height': textheight_bandtitle*1.5})
#        text_pTitle.set_pos((xmin-off_band_x, off_z+zmax+textheight_bandtitle*1.5), align='BOTTOM_LEFT')
#        text_pKm = msp.add_text("km %.3f" % round(reachStation[pID]/1000,3), dxfattribs={'height': textheight_bandtitle})
#        text_pKm.set_pos((xmin-off_band_x, off_z+zmax), align='BOTTOM_LEFT')
#
#        # scale factor
#        text_M = msp.add_text("M = 1:%i/%i"%(int(scale),int(scale/superelev)), dxfattribs={'height': 0.75*textheight_bandtitle})
#        text_M.set_pos((xmin-off_band_x, off_z+zmax-1.5*textheight_bandtitle*1.5), align='BOTTOM_LEFT')
#
#        # axis
#        if profileStation[pID] >= 0.000001:
#            print profileStation[pID]
#            msp.add_line((profileStation[pID], off_z+zmin),(profileStation[pID],off_z+zmax), dxfattribs={'layer': 'axis', 'color':1})
#
#        # band elevation
#        msp.add_line((xmin-off_band_x, off_z+zmin-off_band_z),(xmax,off_z+zmin-off_band_z), dxfattribs={'layer': 'frame'})
#        msp.add_line((xmin-off_band_x, off_z+zmin-off_band_z-h_band),(xmax,off_z+zmin-off_band_z-h_band), dxfattribs={'layer': 'frame'})
#        msp.add_line((xmin-off_band_x, off_z+zmin-off_band_z),(xmin-off_band_x,off_z+zmin-off_band_z-h_band), dxfattribs={'layer': 'frame'})
##            msp.add_line((xmin, off_z+zmin-off_band_z),(xmin,off_z+zmin-off_band_z-h_band), dxfattribs={'layer': 'frame'})
##            msp.add_line((xmax, off_z+zmin-off_band_z),(xmax,off_z+zmin-off_band_z-h_band), dxfattribs={'layer': 'frame'})
#        title_height = msp.add_text("Hoehe [m]", dxfattribs={'height': textheight_bandtitle})
#        title_height.set_pos((xmin-off_band_x+h_band/2.0, off_z+zmin-off_band_z-h_band/2.0), align='MIDDLE_LEFT')
#
#        # band stationing
#        msp.add_line((xmin-off_band_x, off_z+zmin-off_band_z-2*h_band),(xmax,off_z+zmin-off_band_z-2*h_band), dxfattribs={'layer': 'frame'})
#        msp.add_line((xmin-off_band_x, off_z+zmin-off_band_z-h_band),(xmin-off_band_x,off_z+zmin-off_band_z-2*h_band), dxfattribs={'layer': 'frame'})
##            msp.add_line((xmin, off_z+zmin-off_band_z-h_band),(xmin,off_z+zmin-off_band_z-2*h_band), dxfattribs={'layer': 'frame'})
##            msp.add_line((xmax, off_z+zmin-off_band_z-h_band),(xmax,off_z+zmin-off_band_z-2*h_band), dxfattribs={'layer': 'frame'})
#        title_stationing = msp.add_text("Stationierung [m]", dxfattribs={'height': textheight_bandtitle})
#        title_stationing.set_pos((xmin-off_band_x+h_band/2.0, off_z+zmin-off_band_z-3*h_band/2.0), align='MIDDLE_LEFT')
#
##            frame = msp.add_line((xmax,off_z+zmin),(xmax,off_z+zmax), dxfattribs={'layer': 'frame'})
##            frame = msp.add_line((xmin, off_z+zmin),(xmin,off_z+zmax), dxfattribs={'layer': 'frame'})
##            frame = msp.add_line((xmin, off_z+zmax),(xmax,off_z+zmax), dxfattribs={'layer': 'frame'})            
#
#        profilepoints = []
#        mx = []
#        for nID in range(len(d)):
#            x1 = d[nID]
#            z1 = off_z+z[nID]*superelev
#
#            p1 = (x1, z1)
#            profilepoints.append(p1)
#
#            # marker
#            mx.append(x1)
#            if nID != 0 and nID != len(d)-1:
#                msp.add_line(p1,(x1,off_z+zmin), dxfattribs={'layer': 'marker', 'color':253})
#                if mx[nID]-mx[nID-1] < 1.5*textheight_band:
#                    mx[nID] = mx[nID-1] + 1.5*textheight_band
#                    msp.add_line((x1,off_z+zmin),(mx[nID],off_z+zmin-off_band_z), dxfattribs={'layer': 'marker', 'color':253})
#                else:
#                    msp.add_line((x1,off_z+zmin),(x1,off_z+zmin-off_band_z), dxfattribs={'layer': 'marker', 'color':253})
#
#            msp.add_line((mx[nID], off_z+zmin-off_band_z), (mx[nID], off_z+zmin-off_band_z-markerlength),  dxfattribs={'layer': 'band'})   
#            msp.add_line((mx[nID], off_z+zmin-off_band_z-h_band), (mx[nID], off_z+zmin-off_band_z-h_band+markerlength),  dxfattribs={'layer': 'band'})
#            msp.add_line((mx[nID], off_z+zmin-off_band_z-h_band), (mx[nID], off_z+zmin-off_band_z-h_band-markerlength),  dxfattribs={'layer': 'band'})   
#            msp.add_line((mx[nID], off_z+zmin-off_band_z-2*h_band), (mx[nID], off_z+zmin-off_band_z-2*h_band+markerlength),  dxfattribs={'layer': 'band'})
#
#            # band text
#            text_stationing = msp.add_text("%.{0}f".format(dec)%(x1-profileStation[pID]), dxfattribs={'height': textheight_band, 'rotation': 90.0})
#            text_stationing.set_pos((mx[nID], off_z+zmin-off_band_z-3*h_band/2.0), align='MIDDLE')
#            text_height = msp.add_text("%.{0}f".format(dec)%z[nID], dxfattribs={'height': textheight_band, 'rotation': 90.0})
#            text_height.set_pos((mx[nID], off_z+zmin-off_band_z-h_band/2.0), align='MIDDLE')
#
#        # print bottom line
#        msp.add_polyline2d(profilepoints, dxfattribs={'layer': 'profile'})
#
#        # print 1d water elevation
#        if wsNames is not None:
#
#            for wID in range(len(wsElevations[pID])):
#
#                wsElevation = wsElevations[pID][wID]
#                layerName = wsNames[wID]
#                layerColor = 4
#                
#                tup = tuple([(xmin-1.0,off_z+zmax*superelev)] + profilepoints + [(xmax+1.0,off_z+zmax*superelev)])
#                bottomLine = Polygon(tup)
#                wsLine = LineString([(xmin, off_z+wsElevation*superelev), (xmax, off_z+wsElevation*superelev)])
#                inters = bottomLine.intersection(wsLine)
#
#                if inters.geom_type == "LineString":
#                    msp.add_line((inters.coords[:][0][0], off_z+wsElevation*superelev), (inters.coords[:][1][0], off_z+wsElevation*superelev),  dxfattribs={'layer': layerName, 'color':layerColor})
#
#                if inters.geom_type == "MultiLineString":     
#                    for i in range(len(inters)):
#                        ls = inters[i]
#                        msp.add_line((ls.coords[:][0][0], off_z+wsElevation*superelev), (ls.coords[:][1][0], off_z+wsElevation*superelev),  dxfattribs={'layer': layerName, 'color':layerColor})
#
#        # print levees
#        if levees is not None:
#            if pID in levees:
#                for lID in range(len(levees[pID])):
#                    levee_x = levees[pID][lID][0]*xmax
#                    levee_z = levees[pID][lID][1]
#                    bottomLine = LineString(tup)
#                    levee = LineString([(levee_x, off_z+zmin), (levee_x, off_z+zmax)])
#                    inters = bottomLine.intersection(levee)
#                    print inters
#                    msp.add_line((levee_x, inters.y), (levee_x, off_z+levee_z*superelev),  dxfattribs={'layer': 'levee', 'color':1})
#
#    dwg.saveas(str(fname))