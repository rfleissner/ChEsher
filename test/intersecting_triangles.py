import sys
import timeit
import numpy as np
from shapely.geometry import LineString, MultiLineString, Point, MultiPolygon
from shapely.ops import cascaded_union
#from rtree import index

sys.path.append('C:/ChEsher/py/py')

import fileHandler as fh
import profileOrganizer as po

start_time_total = timeit.default_timer()

start_time_read_input = timeit.default_timer()

print "read profiles"
nodProfiles, proProfiles = fh.readI2S("./profiles.i2s")

print "read reach"
nodReach = fh.readI2S("./reach.i2s")[0]

print "read bottom"
bottom, idx = fh.readT3StoShapely("./BOTTOM.t3s")

print("Time for reading input: " + str(timeit.default_timer() - start_time_read_input))

proArranged, reachStation, profileStation, direction = po.determineFlowDirection(nodReach, nodProfiles, proProfiles)


def getCrossSectionsOld(mesh):
    crossSections = dict((key, np.array([])) for key in proArranged)

    for pID in proArranged:
            
        nodes = []
        for nID in range(len(proArranged[pID])):
            node = nodProfiles[proArranged[pID][nID]]
            nodes.append(node)

        crossSection = LineString(nodes)

        intersection = mesh.intersection(crossSection)

        values = []
        for p in range(len(intersection)):
            intersection_ = intersection[p]

            if intersection_.geom_type == "Point":
                inters = crossSection.project(intersection_)
                values.append([intersection_.x, intersection_.y, intersection_.z, inters])
            elif intersection_.geom_type == "LineString":
                for i in range(len(intersection_.coords)):
                    pt = Point(intersection_.coords[i])
                    inters = crossSection.project(pt)             
                    values.append([pt.x, pt.y, pt.z, inters])

        arr = np.array(values)
        arr = arr[arr[:,3].argsort()]
        arr.reshape((arr.size/4,4))

        x = arr[:,0]
        y = arr[:,1]
        z = arr[:,2]
        d = arr[:,3]

        crossSections[pID] = [x,y,z,d]

    return crossSections

def getCrossSectionsNew(mesh, idx):
    # intersection between triangular mesh and linestrings using Rtree
    
    crossSections = dict((key, np.array([])) for key in proArranged)

    for pID in proArranged:
            
        nodes = []
        for nID in range(len(proArranged[pID])):
            node = nodProfiles[proArranged[pID][nID]]
            nodes.append(node)

        crossSection = LineString(nodes)
        
        # Merge triangles to multipolygon
        triangles = MultiPolygon([mesh[int(pos)] for pos in list(idx.intersection(crossSection.bounds))])

        # Now do actual intersection
        intersection = triangles.intersection(crossSection)

        values = []
        for p in range(len(intersection)):
            intersection_ = intersection[p]

            if intersection_.geom_type == "Point":
                inters = crossSection.project(intersection_)
                values.append([intersection_.x, intersection_.y, intersection_.z, inters])
            elif intersection_.geom_type == "LineString":
                for i in range(len(intersection_.coords)):
                    pt = Point(intersection_.coords[i])
                    inters = crossSection.project(pt)             
                    values.append([pt.x, pt.y, pt.z, inters])

        arr = np.array(values)
        arr = arr[arr[:,3].argsort()]
        arr.reshape((arr.size/4,4))

        x = arr[:,0]
        y = arr[:,1]
        z = arr[:,2]
        d = arr[:,3]

        crossSections[pID] = [x,y,z,d]

    return crossSections
        
##start_time = timeit.default_timer()
##crossSectionsOld = getCrossSectionsOld(bottom)
##print("Time for interpolating cross sections: " + str(timeit.default_timer() - start_time))

start_time = timeit.default_timer()
crossSectionsNew = getCrossSectionsNew(bottom, idx)
print("Time for interpolating cross sections: " + str(timeit.default_timer() - start_time))

#print crossSectionsOld
#print
#print crossSectionsNew

print("Time total: " + str(timeit.default_timer() - start_time_total))

