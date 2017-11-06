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

"""Create mesh"""

__author__="Reinhard Fleissner"
__date__ ="$29.08.2014 18:21:40$"

import numpy as np
import macro as mc


class CalcMesh(object):
    """Create mesh.

    """

    def __init__(   self, nodRaw, proRaw, nodReach, nnC, length,
                    nodLBL=None, nodRBL=None, nodLBO=None, nodRBO=None, nnL=None, nnR=None):
        """Constructor for load case.

        Keyword arguments:
        nodRaw -- raw nodes
        proRaw -- raw profiles
        ...

        """

        # inputs
        self.nodRaw = nodRaw
        self.proRaw = proRaw
        self.nodReach = nodReach
        self.nodLBL = nodLBL
        self.nodRBL = nodRBL
        self.nodLBO = nodLBO
        self.nodRBO = nodRBO
        self.nnL = nnL

        if nnL is not None:
            self.nnL = int(nnL)
        self.nnC = int(nnC)
        self.nnR = nnR
        if nnR is not None:
            self.nnR = int(nnR)
        self.length = length

        # results
        self.nnS = {}
        self.LBLInterp = {}
        self.RBLInterp = {}
        self.LBOInterp = {}
        self.RBOInterp = {}
        self.proArranged = {}
        self.nodInterp = {}
        self.proInterp = {}
        self.nodMesh = {}
        self.proMesh = {}
        self.mesh = {}

        self.geometry = {}
        self.geometry["vertices"] = []
        self.geometry["segments"] = []
        #self.geometry["holes"] = []
        
    def determineFlowDirection(self):

        profilecounter = 1
        direction = {}
        
        # loop over reach nodes
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
            closestnode = mc.getClosestNode(self.nodReach[nID_reach], self.nodRaw.keys(), self.nodRaw)

            # determine profile that inherits closest profile node
            for pID_raw in self.proRaw:

                for nID_raw in range(len(self.proRaw[pID_raw])):
                    if closestnode == self.proRaw[pID_raw][nID_raw]:

                        startnode = self.proRaw[pID_raw][0]
                        endnode = self.proRaw[pID_raw][-1]

                        if direction[profilecounter] == 'N':
                            if self.nodRaw[startnode][0] > self.nodRaw[endnode][0]:
                                self.proRaw[pID_raw].reverse()
                        elif direction[profilecounter] == 'E':
                            if self.nodRaw[startnode][1] < self.nodRaw[endnode][1]:
                                self.proRaw[pID_raw].reverse()
                        elif direction[profilecounter] == 'S':
                            if self.nodRaw[startnode][0] < self.nodRaw[endnode][0]:
                                self.proRaw[pID_raw].reverse()
                        elif direction[profilecounter] == 'W':
                            if self.nodRaw[startnode][1] > self.nodRaw[endnode][1]:
                                self.proRaw[pID_raw].reverse()

                        self.proArranged[profilecounter] = self.proRaw[pID_raw]
                        profilecounter += 1
                        break

        info = "\nFlow direction:\n"
        for pID_Arranged in direction:
            info += ' - Profile {0}:\t{1}\n'.format(pID_Arranged, direction[pID_Arranged])

        return info

    def normalizeProfiles(self):

        def normalize(nID_a, nID_b, nodes):

            nID_i = 0
            nID_j = 0
            up = False
            if nID_a < nID_b:
                nID_i = nID_a
                nID_j = nID_b
                up = True
            else:
                nID_i = nID_b
                nID_j = nID_a
                up = False
            nodesTempNormalized = {}

            for i in range(nID_j - nID_i + 1):
                nID = 0
                if up is True:
                    nID = nID_i + i
                else:
                    nID = nID_j - i
                nID = nID_i + i

                nodesTempNormalized[nID] = nodes[nID][0:3]
            return nodesTempNormalized

        def getXYZ(_range, nodes, profiles, id):
            x = []
            y = []
            z = []
            for i in range(_range):
                x.append(nodes[profiles[pID][i+id]][0])
                y.append(nodes[profiles[pID][i+id]][1])
                z.append(nodes[profiles[pID][i+id]][2])
            return x, y, z

        nodesNormalized = {}
        startkey = 1

        # loop over arranged profiles
        for pID in self.proArranged:
            nIDs = self.proArranged[pID]
            if self.nnL is not None and self.nnR is None:
                leftNode = mc.getClosestNodeFromIntersection(self.nodLBL, self.proArranged[pID], self.nodRaw)

                # left
                tempNodesLeft = normalize(nIDs[0], nIDs[leftNode], self.nodRaw)
                nodesNormalized.update(tempNodesLeft)
                x, y, z = getXYZ(leftNode+1, nodesNormalized, self.proArranged, 0)
                tempNodesLeftInterp = mc.interpolateXYZ(x, y, z, self.nnL, startkey)
                startkey += len(tempNodesLeftInterp)-1
                self.nodInterp.update(tempNodesLeftInterp)

                # channel
                tempNodesChannel = normalize(nIDs[leftNode], nIDs[-1], self.nodRaw)
                nodesNormalized.update(tempNodesChannel)
                x, y, z = getXYZ(len(self.proArranged[pID])-leftNode, nodesNormalized, self.proArranged, leftNode)
                tempNodesChannelInterp = mc.interpolateXYZ(x, y, z, self.nnC, startkey)
                startkey += len(tempNodesChannelInterp)
                self.nodInterp.update(tempNodesChannelInterp)

                self.proInterp[pID] = range(startkey-self.nnL-self.nnC+1, startkey)

            elif self.nnL is None and self.nnR is not None:
                rightNode = mc.getClosestNodeFromIntersection(self.nodRBL, self.proArranged[pID], self.nodRaw)

                # channel
                tempNodesChannel = normalize(nIDs[0], nIDs[rightNode], self.nodRaw)
                nodesNormalized.update(tempNodesChannel)
                x, y, z = getXYZ(rightNode+1, nodesNormalized, self.proArranged, 0)
                tempNodesChannelInterp = mc.interpolateXYZ(x, y, z, self.nnC, startkey)
                startkey += len(tempNodesChannelInterp)-1
                self.nodInterp.update(tempNodesChannelInterp)

                # right
                tempNodesRight = normalize(nIDs[rightNode], nIDs[-1], self.nodRaw)
                nodesNormalized.update(tempNodesRight)
                x, y, z = getXYZ(len(self.proArranged[pID])-rightNode, nodesNormalized, self.proArranged, rightNode)
                tempNodesRightInterp = mc.interpolateXYZ(x, y, z, self.nnR, startkey)
                startkey += len(tempNodesRightInterp)
                self.nodInterp.update(tempNodesRightInterp)

                self.proInterp[pID] = range(startkey-self.nnC-self.nnR+1, startkey)

            elif self.nnL is not None and self.nnR is not None:
                leftNode = mc.getClosestNodeFromIntersection(self.nodLBL, self.proArranged[pID], self.nodRaw)
                rightNode = mc.getClosestNodeFromIntersection(self.nodRBL, self.proArranged[pID], self.nodRaw)

                # left
                tempNodesLeft = normalize(nIDs[0], nIDs[leftNode], self.nodRaw)
                nodesNormalized.update(tempNodesLeft)
                x, y, z = getXYZ(leftNode+1, nodesNormalized, self.proArranged, 0)
                tempNodesLeftInterp = mc.interpolateXYZ(x, y, z, self.nnL, startkey)
                startkey += len(tempNodesLeftInterp)-1
                self.nodInterp.update(tempNodesLeftInterp)

                # channel
                tempNodesChannel = normalize(nIDs[leftNode], nIDs[rightNode], self.nodRaw)
                nodesNormalized.update(tempNodesChannel)
                x, y, z = getXYZ(rightNode-leftNode+1, nodesNormalized, self.proArranged, leftNode)
                tempNodesChannelInterp = mc.interpolateXYZ(x, y, z, self.nnC, startkey)
                startkey += len(tempNodesChannelInterp)-1
                self.nodInterp.update(tempNodesChannelInterp)

                # right
                tempNodesRight = normalize(nIDs[rightNode], nIDs[-1], self.nodRaw)
                nodesNormalized.update(tempNodesRight)
                x, y, z = getXYZ(len(self.proArranged[pID])-rightNode, nodesNormalized, self.proArranged, rightNode)
                tempNodesRightInterp = mc.interpolateXYZ(x, y, z, self.nnR, startkey)
                startkey += len(tempNodesRightInterp)
                self.nodInterp.update(tempNodesRightInterp)

                self.proInterp[pID] = range(startkey-self.nnL-self.nnC-self.nnR+2, startkey)

            else:
                # channel
                tempNodesChannel = normalize(nIDs[0], nIDs[-1], self.nodRaw)
                nodesNormalized.update(tempNodesChannel)
                x, y, z = getXYZ(len(self.proArranged[pID]), nodesNormalized, self.proArranged, 0)
                tempNodesChannelInterp = mc.interpolateXYZ(x, y, z, self.nnC, startkey)
                startkey += len(tempNodesChannelInterp)
                self.nodInterp.update(tempNodesChannelInterp)

                self.proInterp[pID] = range(startkey-self.nnC, startkey)

        return "\nProfiles normalized."

    def getNumberOfSegmentNodes(self, node_i, node_j, length):
        tempLength = np.linalg.norm(np.subtract(node_j, node_i))
        num = int(tempLength / length)+1
        if num < 2:
            return 2
        else:
            return num
        
    def getNodes(self, nodeString):
        x = []
        y = []
        for nID in nodeString:
            x.append(nodeString[nID][0])
            y.append(nodeString[nID][1])
        return x, y
    
    def interpolateChannel(self):

        nodecounter = 0
        nodecounter_triangle = 0
        nodecounter_triangle_old = 0
        profilecounter = 0
        
        if self.nodLBO is None:
            self.nodLBO = self.getNodesLeft(self.nodInterp, self.proInterp)
        if self.nodRBO is None:
            self.nodRBO = self.getNodesRight(self.nodInterp, self.proInterp)

        for i in range(len(self.proInterp)-1):
            pID = i+1

            tempLeftBreaklineInterp = {}
            tempRightBreaklineInterp = {}
            tempLeftBoundaryInterp = {}
            tempRightBoundaryInterp = {}

            tempLeftBoundary = {}
            tempLeftBreakline = {}
            tempRightBreakline = {}
            tempRightBoundary = {}

            id_i = 0
            id_j = 0

            if self.nnL is None:
                id_i = 0
                id_j = self.nnC-1
            else:
                id_i = self.nnL-1
                id_j = self.nnL+self.nnC-2
            if self.nnR is None:
                id_j = 0
            else:
                id_j = self.nnR-1
            if self.nnL is None and self.nnR is None:
                id_i = 0
                id_j = -1

            nodeCount = self.getNumberOfSegmentNodes(self.nodReach[pID], self.nodReach[pID+1], self.length)

            self.nnS[pID] = nodeCount

            tempLeftBoundary = mc.getPartOfNodeString(self.nodLBO,
                                                    self.nodInterp[self.proInterp[pID][0]],
                                                    self.nodInterp[self.proInterp[pID+1][0]]
                                                    )
            tempRightBoundary = mc.getPartOfNodeString(self.nodRBO,
                                                    self.nodInterp[self.proInterp[pID][-1]],
                                                    self.nodInterp[self.proInterp[pID+1][-1]]
                                                    )
            # left boundary
            zVec = []
            if len(tempLeftBoundary[1]) == 2:
            # boundary is *.i2s, interpolate z values linear between profiles
                zVec = np.linspace(self.nodInterp[self.proInterp[pID][0]][2], self.nodInterp[self.proInterp[pID+1][0]][2], num=nodeCount)
                tempLeftBoundaryInterp = mc.interpolateNodeString2d(tempLeftBoundary, nodeCount)
                for key in tempLeftBoundaryInterp:
                    tempLeftBoundaryInterp[key][2] = zVec[key-1]
            else:
            # boundary is *.i3s
                tempLeftBoundaryInterp = mc.interpolateNodeString3d(tempLeftBoundary, nodeCount)

            # right boundary
            zVec = []
            if len(tempRightBoundary[1]) == 2:
                zVec = np.linspace(self.nodInterp[self.proInterp[pID][-1]][2], self.nodInterp[self.proInterp[pID+1][-1]][2], num=nodeCount)
                tempRightBoundaryInterp = mc.interpolateNodeString2d(tempRightBoundary, nodeCount)
                for key in tempRightBoundaryInterp:
                    tempRightBoundaryInterp[key][2] = zVec[key-1]
            else:
                tempRightBoundaryInterp = mc.interpolateNodeString3d(tempRightBoundary, nodeCount)
            
            # apply temporary interpolated left boundary (between two profiles) to total left boundary
            for nID in range(len(tempLeftBoundaryInterp)-1):
                self.LBOInterp[len(self.LBOInterp)+1] = tempLeftBoundaryInterp[nID+1]
            if pID == len(self.proInterp)-1:
                self.LBOInterp[len(self.LBOInterp)+1] = tempLeftBoundaryInterp[len(tempLeftBoundaryInterp)]
            # apply temporary interpolated right boundary (between two profiles) to total right boundary
            for nID in range(len(tempRightBoundaryInterp)-1):
                self.RBOInterp[len(self.RBOInterp)+1] = tempRightBoundaryInterp[nID+1]
            if pID == len(self.proInterp)-1:
                self.RBOInterp[len(self.RBOInterp)+1] = tempRightBoundaryInterp[len(tempRightBoundaryInterp)]

            if self.nnL is None and self.nnR is None:
                pass
            else:
                if self.nnL is not None:
                    tempLeftBreakline = mc.getPartOfNodeString(self.nodLBL,
                                                            self.nodInterp[self.proInterp[pID][id_i]],
                                                            self.nodInterp[self.proInterp[pID+1][id_i]]
                                                            )

                    zVec = []
                    if len(tempLeftBreakline[1]) == 2:
                        zVec = np.linspace(self.nodInterp[self.proInterp[pID][id_i]][2], self.nodInterp[self.proInterp[pID+1][id_i]][2], num=nodeCount)
                        tempLeftBreaklineInterp = mc.interpolateNodeString2d(tempLeftBreakline, nodeCount)
                        for key in tempLeftBreaklineInterp:
                            tempLeftBreaklineInterp[key][2] = zVec[key-1]
                    else:
                        tempLeftBreaklineInterp = mc.interpolateNodeString3d(tempLeftBreakline, nodeCount)

                    for nID in range(len(tempLeftBreaklineInterp)-1):
                        self.LBLInterp[len(self.LBLInterp)+1] = tempLeftBreaklineInterp[nID+1]
                    if pID == len(self.proInterp)-1:
                        self.LBLInterp[len(self.LBLInterp)+1] = tempLeftBreaklineInterp[len(tempLeftBreaklineInterp)]
                    
                if self.nnR is not None:

                    tempRightBreakline = mc.getPartOfNodeString(self.nodRBL,
                                                             self.nodInterp[self.proInterp[pID][id_j]],
                                                             self.nodInterp[self.proInterp[pID+1][id_j]]
                                                             )

                    zVec = []
                    if len(tempRightBreakline[1]) == 2:
                        zVec = np.linspace(self.nodInterp[self.proInterp[pID][id_j]][2], self.nodInterp[self.proInterp[pID+1][id_j]][2], num=nodeCount)
                        tempRightBreaklineInterp = mc.interpolateNodeString2d(tempRightBreakline, nodeCount)
                        for key in tempRightBreaklineInterp:
                            tempRightBreaklineInterp[key][2] = zVec[key-1]
                    else:
                        tempRightBreaklineInterp = mc.interpolateNodeString3d(tempRightBreakline, nodeCount)

                    for nID in range(len(tempRightBreaklineInterp)-1):
                        self.RBLInterp[len(self.RBLInterp)+1] = tempRightBreaklineInterp[nID+1]
                    if pID == len(self.proInterp)-1:
                        self.RBLInterp[len(self.RBLInterp)+1] = tempRightBreaklineInterp[len(tempRightBreaklineInterp)]

            # interpolate channel from left boundary over left and right breakline to right boundary
            elementsInSegment = 0
            if i == (len(self.proInterp)-2):
                elementsInSegment = len(tempLeftBoundaryInterp)
            else:
                elementsInSegment = len(tempLeftBoundaryInterp)-1

            
##      ToDo: interpolate channel dependend on element width
##      replace for example self.nnL by element width
##      save all points to triangulate mesh

            for j in range(elementsInSegment):

                nID = j+1

                xx = []
                yy = []

                if self.nnL is not None and self.nnR is None:
                    tempLeft = {}
                    tempLeft[1] = tempLeftBoundaryInterp[nID]
                    tempLeft[2] = tempLeftBreaklineInterp[nID]
                    nodesInterpLeft = mc.interpolateNodeString2d(tempLeft, self.nnL)
                    xleft, yleft = mc.getXY(nodesInterpLeft)
                    
                    tempChannel = {}
                    tempChannel[1] = tempLeftBreaklineInterp[nID]
                    tempChannel[2] = tempRightBoundaryInterp[nID]
                    nodesInterpChannel = mc.interpolateNodeString2d(tempChannel, self.nnC)
                    xchannel, ychannel = mc.getXY(nodesInterpChannel)

                    xx = np.concatenate([xleft[0:-1], xchannel])
                    yy = np.concatenate([yleft[0:-1], ychannel])

                elif self.nnL is None and self.nnR is not None:
                    tempChannel = {}
                    tempChannel[1] = tempLeftBoundaryInterp[nID]
                    tempChannel[2] = tempRightBreaklineInterp[nID]
                    nodesInterpChannel = mc.interpolateNodeString2d(tempChannel, self.nnC)
                    xchannel, ychannel = mc.getXY(nodesInterpChannel)

                    tempRight = {}
                    tempRight[1] = tempRightBreaklineInterp[nID]
                    tempRight[2] = tempRightBoundaryInterp[nID]
                    nodesInterpRight = mc.interpolateNodeString2d(tempRight, self.nnR)
                    xright, yright = mc.getXY(nodesInterpRight)

                    xx = np.concatenate([xchannel[0:-1], xright])
                    yy = np.concatenate([ychannel[0:-1], yright])

                elif self.nnL is not None and self.nnR is not None:
                    tempLeft = {}
                    tempLeft[1] = tempLeftBoundaryInterp[nID]
                    tempLeft[2] = tempLeftBreaklineInterp[nID]
                    nodesInterpLeft = mc.interpolateNodeString2d(tempLeft, self.nnL)
                    xleft, yleft = mc.getXY(nodesInterpLeft)

                    tempChannel = {}
                    tempChannel[1] = tempLeftBreaklineInterp[nID]
                    tempChannel[2] = tempRightBreaklineInterp[nID]
                    nodesInterpChannel = mc.interpolateNodeString2d(tempChannel, self.nnC)
                    xchannel, ychannel = mc.getXY(nodesInterpChannel)

                    tempRight = {}
                    tempRight[1] = tempRightBreaklineInterp[nID]
                    tempRight[2] = tempRightBoundaryInterp[nID]
                    nodesInterpRight = mc.interpolateNodeString2d(tempRight, self.nnR)
                    xright, yright = mc.getXY(nodesInterpRight)

                    xx = np.concatenate([xleft[0:-1], xchannel[0:-1], xright])
                    yy = np.concatenate([yleft[0:-1], ychannel[0:-1], yright])
                else:
                    temp = {}
                    temp[1] = tempLeftBoundaryInterp[nID]
                    temp[2] = tempRightBoundaryInterp[nID]
                    
                    # calculate length between left and right boundary
                    d1 = np.linalg.norm(np.subtract(temp[1], temp[2]))

                    # element width
                    e = 1.0
                    
                    # number of elements
                    nnC = d1/e
                                        
                    
                    tempNodesInterp = mc.interpolateNodeString2d(temp, self.nnC)
                    xx, yy = mc.getXY(tempNodesInterp)

                    tempNodesInterp_triangle = mc.interpolateNodeString2d(temp, int(nnC)+1)

                    nodes_mesh_triangle = mc.getVertices2d(tempNodesInterp_triangle)


                    self.geometry["vertices"].extend(nodes_mesh_triangle[:])
                    nodecounter_triangle_old_old = nodecounter_triangle_old
                    nodecounter_triangle_old = nodecounter_triangle
                    nodecounter_triangle += len(nodes_mesh_triangle)
                    
                    print nodecounter_triangle_old, nodecounter_triangle
                    print range(nodecounter_triangle_old,nodecounter_triangle)
                    if i == 0 and j == 0:
                        for k in range(nodecounter_triangle_old,nodecounter_triangle-1,1):
                            self.geometry["segments"].append([k, k+1])
                    else:
                        self.geometry["segments"].append([nodecounter_triangle_old-1,nodecounter_triangle-1])
                        self.geometry["segments"].append([nodecounter_triangle_old_old,nodecounter_triangle_old])
                    if i == len(self.proInterp)-2 and j == elementsInSegment-1:
                        for k in range(nodecounter_triangle_old,nodecounter_triangle-1,1):
                            self.geometry["segments"].append([k, k+1])
                        #self.geometry["segments"].append(range(nodecounter_triangle_old,nodecounter_triangle))
                    
                    
                    
                    #print tempNodesInterp
                zz = np.zeros(len(xx))
                nodes = mc.getNodeString3d(xx, yy, zz, nodecounter+1)
                self.nodMesh = dict(self.nodMesh.items() + nodes.items())

                profilecounter = profilecounter + 1
                numberOfNodes = 0
                if self.nnL is None and self.nnR is not None:
                    numberOfNodes = self.nnC+self.nnR-1
                elif self.nnL is not None and self.nnR is None:
                    numberOfNodes = self.nnL+self.nnC-1
                elif self.nnL is None and self.nnR is None:
                    numberOfNodes = self.nnC
                else:
                    numberOfNodes = self.nnL+self.nnC+self.nnR-2
                self.proMesh[profilecounter] = np.arange(nodecounter+1, nodecounter+numberOfNodes+1, 1)
                nodecounter = nodecounter + len(xx)

        #print self.geometry
        #print nodecounter_triangle, len(self.geometry["vertices"])

        return "\nChannel nodes interpolated."
    
    def interpolateElevation(self):

        for i in range(len(self.proInterp[1])):
            zVec = []
            for j in range(len(self.proInterp)-1):
                pID = j+1
                nNodes = self.nnS[pID]
                zi = self.nodInterp[self.proInterp[pID][i]][2]
                zj = self.nodInterp[self.proInterp[pID+1][i]][2]
                zVec = np.append(zVec, np.linspace(zi, zj, num=nNodes)[0:-1])

            zVec = np.append(zVec, zj)

            for k in range(len(zVec)):
                id = k*len(self.proMesh[1])+1+i
                self.nodMesh[id][2] = zVec[k]

        return "\nElevation interpolated."

    def interpolateElevationCorrection(self):

        for pID in self.proMesh:
            dzVec = list()

            if self.nnL is not None and self.nnR is None:

                dzLi = self.LBOInterp[pID][2] - self.nodMesh[(pID-1)*len(self.proMesh[1])+1][2]
                dzLj = self.LBLInterp[pID][2] - self.nodMesh[(pID-1)*len(self.proMesh[1])+self.nnL][2]
                dzLvec = dzLi + np.linspace(0.0, dzLj - dzLi, num=self.nnL)

                dzCi = dzLj
                dzCj = self.RBOInterp[pID][2] - self.nodMesh[(pID-1)*len(self.proMesh[1])+self.nnL+self.nnC-1][2]
                dzCvec = dzCi + np.linspace(0.0, dzCj - dzCi, num=self.nnC)

                dzVec = np.concatenate([dzLvec[0:-1], dzCvec])

                for i in range(len(dzVec)):
                    id = (pID-1)*(self.nnL+self.nnC-1)+i+1
                    self.nodMesh[id][2] += dzVec[i]

            elif self.nnL is None and self.nnR is not None:
                
                dzCi = self.LBOInterp[pID][2] - self.nodMesh[(pID-1)*len(self.proMesh[1])+1][2]
                dzCj = self.RBLInterp[pID][2] - self.nodMesh[(pID-1)*len(self.proMesh[1])+self.nnC][2]
                dzCvec = dzCi + np.linspace(0.0, dzCj - dzCi, num=self.nnC)

                dzRi = dzCj
                dzRj = self.RBOInterp[pID][2] - self.nodMesh[(pID-1)*len(self.proMesh[1])+self.nnC+self.nnR-1][2]
                dzRvec = dzRi + np.linspace(0.0, dzRj - dzRi, num=self.nnR)

                dzVec = np.concatenate([dzCvec[0:-1], dzRvec])

                for i in range(len(dzVec)):
                    id = (pID-1)*(self.nnC+self.nnR-1)+i+1
                    self.nodMesh[id][2] += dzVec[i]

            elif self.nnL is not None and self.nnR is not None:

                dzLi = self.LBOInterp[pID][2] - self.nodMesh[(pID-1)*len(self.proMesh[1])+1][2]
                dzLj = self.LBLInterp[pID][2] - self.nodMesh[(pID-1)*len(self.proMesh[1])+self.nnL][2]
                dzLvec = dzLi + np.linspace(0.0, dzLj - dzLi, num=self.nnL)

                dzCi = dzLj
                dzCj = self.RBLInterp[pID][2] - self.nodMesh[(pID-1)*len(self.proMesh[1])+self.nnL+self.nnC-1][2]
                dzCvec = dzCi + np.linspace(0.0, dzCj - dzCi, num=self.nnC)

                dzRi = dzCj
                dzRj = self.RBOInterp[pID][2] - self.nodMesh[(pID-1)*len(self.proMesh[1])+self.nnL+self.nnC+self.nnR-2][2]
                dzRvec = dzRi + np.linspace(0.0, dzRj - dzRi, num=self.nnR)

                dzVec = np.concatenate([dzLvec[0:-1], dzCvec[0:-1], dzRvec])

                for i in range(len(dzVec)):
                    id = (pID-1)*(self.nnL+self.nnC+self.nnR-2)+i+1
                    self.nodMesh[id][2] += dzVec[i]
            else:
                dzCi = self.LBOInterp[pID][2] - self.nodMesh[(pID-1)*len(self.proMesh[1])+1][2]
                dzCj = self.RBOInterp[pID][2] - self.nodMesh[(pID-1)*len(self.proMesh[1])+self.nnC][2]

                dzVec = dzCi + np.linspace(0.0, dzCj - dzCi, num=self.nnC)

                for i in range(len(dzVec)):
                    id = (pID-1)*(self.nnC)+i+1
                    self.nodMesh[id][2] += dzVec[i]

        return "\nElevation correction interpolated."

    def createMesh(self):

        info = "\n\nChannel mesh:\n"

        eID = 1
        for pID in range(len(self.proMesh)-1):
            pID += 1
            for nID in range(len(self.proMesh[pID])-1):
                a1 = self.proMesh[pID][nID]
                a2 = self.proMesh[pID][nID+1]
                b1 = self.proMesh[pID+1][nID]
                b2 = self.proMesh[pID+1][nID+1]

                d1 = np.linalg.norm(np.subtract(self.nodMesh[b1], self.nodMesh[a2]))
                d2 = np.linalg.norm(np.subtract(self.nodMesh[b2], self.nodMesh[a1]))

                if d1 < d2:
                    self.mesh[eID] = [a1, a2, b1]
                    eID += 1
                    self.mesh[eID] = [b1, a2, b2]
                    eID += 1
                else:
                    self.mesh[eID] = [b1, a1, b2]
                    eID += 1
                    self.mesh[eID] = [b2, a1, a2]
                    eID += 1

        info += " - Nodes:\t{0}\n".format(len(self.nodMesh))
        info += " - Elements:\t{0}\n".format(eID-1)

        return info

    def getNodesRow(self, nodes, profiles, row):
        nodesRow = {}
        for i in range(len(profiles)):
            pID = i+1
            nodesRow[pID] = nodes[profiles[pID][row]]
        return nodesRow

    def getNodesLeft(self, nodes, profiles):
        nodesLeft = {}
        for i in range(len(profiles)):
            pID = i+1
            nodesLeft[pID] = nodes[profiles[pID][0]]
        return nodesLeft

    def getNodesRight(self, nodes, profiles):
        nodesRight = {}
        for i in range(len(profiles)):
            pID = i+1
            nodesRight[pID] = nodes[profiles[pID][-1]]
        return nodesRight

    def getNodeIDsLeft(self, profiles):
        nodes = []
        for pID in range(len(profiles)):
            nodes.append(profiles[pID+1][0])
        return nodes

    def getNodeIDsRight(self, profiles):
        nodes = []
        for pID in range(len(profiles)):
            nodes.append(profiles[pID+1][-1])
        return nodes

    def getNodesOutline(self, profiles):
        nodes = []
        nodes.extend(getNodeIDsLeft(profiles))
        nodes.extend(profiles[len(profiles)][1:])
        right = getNodeIDsRight(profiles)[:]
        right.reverse()
        nodes.extend(right[1:])
        up = profiles[1][:]
        up = up[::-1]
        nodes.extend(up[1:])
        return nodes
