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

"""Module with functins for geometry manipulation."""


__author__="Reinhard Fleissner"
__date__ ="$29.08.2014 18:21:40$"

import scipy.interpolate as sp
import numpy as np
#import shapely.geometry as sh

from shapely.geometry import LineString

def interpolateXYZ(xx, yy, zz, nodeCount, startkey=1):
#    print "x", xx
#    print "y", yy
#    print "z", zz
    
    ss = getRasterXYZ(xx, yy, np.zeros(len(xx)))
#    print ss
    vec = np.linspace(ss[0], ss[-1], nodeCount)

    f1 = sp.interp1d(ss, xx, kind='linear')
    f2 = sp.interp1d(ss, yy, kind='linear')
    f3 = sp.interp1d(ss, zz, kind='linear')

    xInterp = f1(vec)
    yInterp = f2(vec)
    zInterp = f3(vec)

    nodeStringInterp = getNodeString3d(xInterp, yInterp, zInterp, startkey)

    return nodeStringInterp

def interpolateNodeString3d(nodeString, nodeCount, startkey=1):

    xx = []
    yy = []
    zz = []

    xx, yy, zz = getXYZ(nodeString)

    nodeStringInterp = interpolateXYZ(xx, yy, zz, nodeCount, startkey)

    return nodeStringInterp

def interpolateNodeString2d(nodeString, nodeCount, startkey=1):

    xx = []
    yy = []

    xx, yy = getXY(nodeString)
    zz = np.zeros(len(xx))
    nodeStringInterp = interpolateXYZ(xx, yy, zz, nodeCount, startkey)

    return nodeStringInterp

def getPartOfNodeString(nodesString, queryNode_i, queryNode_j):
    temp = {}
    counter = 1
    nID_i = getClosestNode(queryNode_i, None, nodesString)
    nID_j = getClosestNode(queryNode_j, None, nodesString)
    for key in range(nID_i, nID_j+1):
        temp[counter] = nodesString[key]
        counter += 1
    return temp

def getNodeString3d(x, y, z, startkey):
    nodeString = {}
    for i in range(len(x)):
        nodeString[startkey+i] = [x[i], y[i], z[i]]
    return nodeString

def getNodeString2d(x, y, startkey):
    nodeString = {}
    for i in range(len(x)):
        nodeString[startkey+i] = [x[i], y[i]]
    return nodeString

def getXYZ(nodeString):
    x, y = getXY(nodeString)
    z = []
    for nID in nodeString:
        z.append(nodeString[nID][2])
    return x, y, z

def getXY(nodeString):
    x = []
    y = []
    for nID in nodeString:
        x.append(nodeString[nID][0])
        y.append(nodeString[nID][1])
    return x, y

def getRasterXYZ(x, y, z):
    s = np.zeros(len(x), dtype=float)
#    print "x", x
#    print "y", y
#    print "z", z
    for i in range(len(x)):
        dx = x[i] - x[i-1]
        dy = y[i] - y[i-1]
        dz = z[i] - z[i-1]
        vec = np.array([dx, dy, dz])
#        print "vec", vec
        s[i] = s[i-1] + np.linalg.norm(vec, 2)
#        print "norm", np.linalg.norm(vec)
    return s

def getClosestNode(querynode, nIDs, nodes):
    distance = []
    nIDs_ = []
    if nIDs is None:
        for key in nodes:
            nIDs_.append(key)
    else:
        nIDs_ = nIDs
    for nID in nIDs_:
        b = nodes[nID][0:2]
        distance.append(np.linalg.norm(np.subtract(b, querynode[0:2])))
    if nIDs is None:
        closestnode = distance.index(min(distance))+1
    else:
        closestnode = distance.index(min(distance))

    return closestnode

def getClosestNodeFromIntersection(querynodes, nIDs, nodes):
    nIDs_ = []
    if nIDs is None:
        for key in nodes:
            nIDs_.append(key)
    else:
        nIDs_ = nIDs

    # create nodestrings
    nodestring = []
    for nID in querynodes:
        nodestring.append(querynodes[nID])
    profile = []
    for nID in nIDs_:
        profile.append(nodes[nID][0:2])

    # extend nodestring at first and last point
    dxa = nodestring[0][0] - nodestring[1][0]
    dya = nodestring[0][1] - nodestring[1][1]
    nodestring[0] = [nodestring[0][0]+dxa*100.0, nodestring[0][1]+dya*100.0]

    dxe = nodestring[-1][0] - nodestring[-2][0]
    dye = nodestring[-1][1] - nodestring[-2][1]
    nodestring[-1] = [nodestring[-1][0]+dxe*100.0, nodestring[-1][1]+dye*100.0]

    # find intersection from nodestring with profile
    ns1 = LineString(nodestring)
    ns2 = LineString(profile)

    querynode = [ns1.intersection(ns2).x, ns1.intersection(ns2).y]

    # find nearest node to intersection
    distance = []
    for nID in nIDs_:
        b = nodes[nID][0:2]
        distance.append(np.linalg.norm(np.subtract(b, querynode)))
    closestnode = distance.index(min(distance))

    return closestnode

def getX(xi, yi, xj, yj, Y):
    """Linear interpolation. Return unknown X value.

    Keyword arguments:
    xi -- lower x value
    yi -- lower y value
    xj -- higher x value
    yj -- higer y value
    Y -- y value in between

    """
    dx = xj - xi
    dy = yj - yi
    X = dx/dy * (Y - yi) + xi
    return X

def getY(xi, yi, xj, yj, X):
    """Linear interpolation. Return unknown Y value.

    Keyword arguments:
    xi -- lower x value
    yi -- lower y value
    xj -- higher x value
    yj -- higer y value
    X -- x value in between

    """
    dx = xj - xi
    dy = yj - yi
    Y = dy/dx * (X - xi) + yi
    return Y

def getNodeIDsLeft(profiles):
    nodeIDs = []
    for pID in range(len(profiles)):
        nodeIDs.append(profiles[pID+1][0])
    return nodeIDs

def getNodeIDsRight(profiles):
    nodeIDs = []
    for pID in range(len(profiles)):
        nodeIDs.append(profiles[pID+1][-1])
    return nodeIDs

def getNodeIDsOutline(profiles):
    nodeIDs = []
    nodeIDs.extend(getNodeIDsLeft(profiles))
    nodeIDs.extend(profiles[len(profiles)][1:])
    right = getNodeIDsRight(profiles)[:]
    right.reverse()
    nodeIDs.extend(right[1:])
    up = profiles[1][:]
    up = up[::-1]
    nodeIDs.extend(up[1:])
    return nodeIDs
