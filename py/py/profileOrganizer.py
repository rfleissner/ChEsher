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

"""Module with functins for organizing cross sections along a reach."""

__author__="Reinhard Fleissner"
__date__ ="$16.07.2016 18:21:40$"

from shapely.geometry import LineString

def determineFlowDirection(nodReach, nodProfiles, proProfiles):
    """
    Adjust cross sections along flow direction defined by reach. A reach 
    is defined in flow direction. The cross sections are adjusted in flow
    direction from left to right.
    
    Input:
    nodReach        ... Nodes of reach
    nodProfiles     ... Nodes of cross sections
    proProfiles     ... IDs of cross section nodes
    
    Output:
    reachStation    ... reach stations of crossing cross sections 
    profileStation  ... profile stations of crossing reach
    proArranged     ... IDs of adjusted cross section nodes
    """
         
    reachStation = {}
    proArranged = {}
    profileStation = {}
    
    station_reach = 0.0
    profilecounter = 1
    direction = {}

    # get total length of reach
    reachlength = 0.0
    for nID_reach in range(len(nodReach)-1):
        nID_reach += 1
        nID_i = nID_reach
        nID_j = nID_reach+1

        xa = nodReach[nID_i][0]
        ya = nodReach[nID_i][1]
        xe = nodReach[nID_j][0]
        ye = nodReach[nID_j][1]

        reach_line = LineString([(xa, ya), (xe, ye)])            
        reachlength += reach_line.length
        
    # get total length of profiles
    profileLength = {}
    for pID in proProfiles:
        totLen = 0.0
        # loop over profile points
        for nID in range(len(proProfiles[pID])-1):
            ri = nodProfiles[proProfiles[pID][nID]][0]
            rj = nodProfiles[proProfiles[pID][nID]][1]
            si = nodProfiles[proProfiles[pID][nID+1]][0]
            sj = nodProfiles[proProfiles[pID][nID+1]][1]

            profile_line = LineString([(ri, rj), (si, sj)])
            totLen += profile_line.length
        profileLength[pID] = totLen
        
    # loop over reach points
    for nID_reach in range(len(nodReach)-1):
        nID_reach += 1
        nID_i = nID_reach
        nID_j = nID_reach+1

        xa = nodReach[nID_i][0]
        ya = nodReach[nID_i][1]
        xe = nodReach[nID_j][0]
        ye = nodReach[nID_j][1]

        reach_line = LineString([(xa, ya), (xe, ye)])
        
        # reach point station (zero on last point)
        reachStation[nID_reach] = reachlength-station_reach
        station_reach += reach_line.length

        # loop over profiles
        for pID in proProfiles:
            cutStat = 0.0

            # loop over profile points
            for nID in range(len(proProfiles[pID])-1):

                ri = nodProfiles[proProfiles[pID][nID]][0]
                rj = nodProfiles[proProfiles[pID][nID]][1]
                si = nodProfiles[proProfiles[pID][nID+1]][0]
                sj = nodProfiles[proProfiles[pID][nID+1]][1]

                profile_line = LineString([(ri, rj), (si, sj)])

                # if intersection between reach segment and profile segment
                if reach_line.intersects(profile_line) is True:
                    intersection = reach_line.intersection(profile_line)

                    # profile station
                    delta_reach = LineString([(intersection.x,intersection.y), (xe, ye)]).length
                    reachStation[profilecounter] = reachlength - station_reach + delta_reach

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

                    startnode = proProfiles[pID][0]
                    endnode = proProfiles[pID][-1]

                    # reverse profile, if flow direction shows against reach direction
                    if direction[profilecounter] == 'N':
                        if nodProfiles[startnode][0] > nodProfiles[endnode][0]:
                            proProfiles[pID].reverse()
                            profileIntersectingStation = profileLength[pID] - profileIntersectingStation
                    elif direction[profilecounter] == 'E':
                        if nodProfiles[startnode][1] < nodProfiles[endnode][1]:
                            proProfiles[pID].reverse()
                            profileIntersectingStation = profileLength[pID] - profileIntersectingStation
                    elif direction[profilecounter] == 'S':
                        if nodProfiles[startnode][0] < nodProfiles[endnode][0]:
                            proProfiles[pID].reverse()
                            profileIntersectingStation = profileLength[pID] - profileIntersectingStation
                    elif direction[profilecounter] == 'W':
                        if nodProfiles[startnode][1] > nodProfiles[endnode][1]:
                            proProfiles[pID].reverse()
                            profileIntersectingStation = profileLength[pID] - profileIntersectingStation

                    proArranged[profilecounter] = proProfiles[pID]
                    profileStation[profilecounter] = profileIntersectingStation
                    profilecounter += 1

                else:
                    cutStat += profile_line.length

    reachStation[len(reachStation)+1] = station_reach

    return proArranged, reachStation, profileStation, direction