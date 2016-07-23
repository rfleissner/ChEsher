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

import os.path as pth
ezdxf.options.template_dir = pth.abspath('.')

def writeProfile(fname, bottom, reachStation, profileStation, wsNames=None, wsElevations=None, levees=None):
    """
    bottom = {1: [[di], [zi]], ..., nOfProfiles:[[di],[zi]]}
    """
    
    layer = "0"

    nOfProfiles = len(bottom)
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

    for pID in bottom:

        off_z = pID*dz
        z = bottom[pID][2]
        d = bottom[pID][3]

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
        text_pTitle = msp.add_text("Profil-Nr. {0}".format(nOfProfiles-pID+1), dxfattribs={'height': textheight_bandtitle*1.5})
        text_pTitle.set_pos((xmin-off_band_x, off_z+zmax+textheight_bandtitle*1.5), align='BOTTOM_LEFT')
        text_pKm = msp.add_text("km %.3f" % round(reachStation[pID]/1000,3), dxfattribs={'height': textheight_bandtitle})
        text_pKm.set_pos((xmin-off_band_x, off_z+zmax), align='BOTTOM_LEFT')

        # scale factor
        text_M = msp.add_text("M = 1:%i/%i"%(int(scale),int(scale/superelev)), dxfattribs={'height': 0.75*textheight_bandtitle})
        text_M.set_pos((xmin-off_band_x, off_z+zmax-1.5*textheight_bandtitle*1.5), align='BOTTOM_LEFT')

        # axis
        if profileStation[pID] >= 0.000001:
            msp.add_line((profileStation[pID], off_z+zmin),(profileStation[pID],off_z+zmax), dxfattribs={'layer': 'axis', 'color':1})

        # band elevation
        msp.add_line((xmin-off_band_x, off_z+zmin-off_band_z),(xmax,off_z+zmin-off_band_z), dxfattribs={'layer': 'frame'})
        msp.add_line((xmin-off_band_x, off_z+zmin-off_band_z-h_band),(xmax,off_z+zmin-off_band_z-h_band), dxfattribs={'layer': 'frame'})
        msp.add_line((xmin-off_band_x, off_z+zmin-off_band_z),(xmin-off_band_x,off_z+zmin-off_band_z-h_band), dxfattribs={'layer': 'frame'})
#            msp.add_line((xmin, off_z+zmin-off_band_z),(xmin,off_z+zmin-off_band_z-h_band), dxfattribs={'layer': 'frame'})
#            msp.add_line((xmax, off_z+zmin-off_band_z),(xmax,off_z+zmin-off_band_z-h_band), dxfattribs={'layer': 'frame'})
        title_height = msp.add_text("Hoehe [m]", dxfattribs={'height': textheight_bandtitle})
        title_height.set_pos((xmin-off_band_x+h_band/2.0, off_z+zmin-off_band_z-h_band/2.0), align='MIDDLE_LEFT')

        # band stationing
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
        for nID in range(len(d)):
            x1 = d[nID]
            z1 = off_z+z[nID]*superelev

            p1 = (x1, z1)
            profilepoints.append(p1)

            # marker
            mx.append(x1)
            if nID != 0 and nID != len(d)-1:
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
            text_stationing = msp.add_text("%.{0}f".format(dec)%(x1-profileStation[pID]), dxfattribs={'height': textheight_band, 'rotation': 90.0})
            text_stationing.set_pos((mx[nID], off_z+zmin-off_band_z-3*h_band/2.0), align='MIDDLE')
            text_height = msp.add_text("%.{0}f".format(dec)%z[nID], dxfattribs={'height': textheight_band, 'rotation': 90.0})
            text_height.set_pos((mx[nID], off_z+zmin-off_band_z-h_band/2.0), align='MIDDLE')

        # print bottom line
        msp.add_polyline2d(profilepoints, dxfattribs={'layer': 'profile'})

        # print water elevation
        if wsNames is not None:

            for wID in range(len(wsElevations[pID])):

                wsElevation = wsElevations[pID][wID]
                layerName = wsNames[wID]
                layerColor = 4
                
                tup = tuple([(xmin-1.0,off_z+zmax*superelev)] + profilepoints + [(xmax+1.0,off_z+zmax*superelev)])
                bottomLine = Polygon(tup)
                wsLine = LineString([(xmin, off_z+wsElevation*superelev), (xmax, off_z+wsElevation*superelev)])
                inters = bottomLine.intersection(wsLine)

                if inters.geom_type == "LineString":
                    msp.add_line((inters.coords[:][0][0], off_z+wsElevation*superelev), (inters.coords[:][1][0], off_z+wsElevation*superelev),  dxfattribs={'layer': layerName, 'color':layerColor})

                if inters.geom_type == "MultiLineString":     
                    for i in range(len(inters)):
                        ls = inters[i]
                        msp.add_line((ls.coords[:][0][0], off_z+wsElevation*superelev), (ls.coords[:][1][0], off_z+wsElevation*superelev),  dxfattribs={'layer': layerName, 'color':layerColor})

        # print levees
        if levees is not None:
            if pID in levees:
                for lID in range(len(levees[pID])):
                    levee_x = levees[pID][lID][0]*xmax
                    levee_z = levees[pID][lID][1]
                    bottomLine = LineString(tup)
                    levee = LineString([(levee_x, off_z+zmin), (levee_x, off_z+zmax)])
                    inters = bottomLine.intersection(levee)
                    print inters
                    msp.add_line((levee_x, inters.y), (levee_x, off_z+levee_z*superelev),  dxfattribs={'layer': 'levee', 'color':1})

    dwg.saveas(str(fname))