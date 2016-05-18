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


class CalcProfiles(object):
    """Create profiles.

    """

    def __init__(   self, nodRaw, proRaw, nodReach):
        """Constructor for load case.

        Keyword arguments:i
        nodRaw -- raw nodes
        proRaw -- raw profiles
        ...

        """

        # inputs
        self.nodRaw = nodRaw
        self.proRaw = proRaw
        self.nodReach = nodReach

        # results
        self.proNormalized = {}
        self.nodNormalized = {}

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

        for key in profiles:
            node_IDs = profiles[key]
            r0 = nodes[node_IDs[0]][0:2]
            r1 = nodes[node_IDs[-1]][0:2]

            u = numpy.subtract(r1, r0)
            for i in range(len(profiles[key])):
                x = nodes[profiles[key][i]][0:2]
                Pg = r0 + numpy.dot(numpy.subtract(x, r0), u)/numpy.dot(u, u)*u
                nodes_normalized[node_IDs[i]] = Pg
        for key in nodes_normalized:
            print nodes_normalized[key]
        
        return "\nProfiles normalized."

