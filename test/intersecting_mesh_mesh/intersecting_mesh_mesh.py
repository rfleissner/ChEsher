import sys
import timeit
import numpy as np
from shapely.geometry import LineString, MultiLineString, Point, Polygon, MultiPolygon
from shapely.ops import cascaded_union
from rtree import index

# 1. erstelle index von mesh
# 2. read submesh
# 3. erstelle rand von submesh -> ueber node ids
# 4. check, ob triangle von mesh im rand liegt.
#    wenn ja, loesche es
#    sonst
#      check, ob triangle den rand schneidet
#      wenn ja, check wie viel punkte im rand liegen
#        wenn 1 punkt im rand liegt, erstelle segment aus anderen zwei punkten
#    trianguliere zwischennetz aus rand und segments
#    schreibe netz und zwischennetz


sys.path.append('C:/ChEsher/py/py')

import fileHandler as fh
import profileOrganizer as po


start_time_total = timeit.default_timer()


start_time_read_input = timeit.default_timer()

print "read mesh"
mesh, idx = fh.readT3StoShapely("./input/mesh.t3s")


print "read submesh"
x, y, z, submesh, boundaries = fh.readT3STriangulation("./input/submesh.t3s")

# create MultiLineString
coords = []
for i in range(len(boundaries)):
    coords.append(((x[boundaries[i][0]], y[boundaries[i][0]]),(x[boundaries[i][1]], y[boundaries[i][1]])))
    
#    print boundaries[i]
boundary = MultiLineString(coords)
#print boundary

for t in range(len(mesh)):
    inters = mesh[t].intersects(boundary)
    if inters is True:
        print mesh[t]
    
print("Time for reading input: " + str(timeit.default_timer() - start_time_read_input))

def getIntersection(mesh, idx, submesh):
    # intersection between triangular mesh and triangles using Rtree

    for tID in range(len(submesh)):

        submesh_triangle = submesh[tID]
       # print submesh_triangle.exterior.coords
        t = MultiLineString([submesh_triangle.exterior.coords])

        #t = Polygon([p1, p2, p3])
        # Merge triangles from index to multipolygon
        mesh_triangles = MultiPolygon([mesh[int(pos)] for pos in list(idx.intersection(t.bounds))])

        # Now do actual intersection
        intersection = mesh_triangles.intersects(t)
      #  print intersection
        
##        values = []
##        for p in range(len(intersection)):
##            intersection_ = intersection[p]
##
##            if intersection_.geom_type == "Point":
##                inters = crossSection.project(intersection_)
##                values.append([intersection_.x, intersection_.y, intersection_.z, inters])
##            elif intersection_.geom_type == "LineString":
##                for i in range(len(intersection_.coords)):
##                    pt = Point(intersection_.coords[i])
##                    inters = crossSection.project(pt)             
##                    values.append([pt.x, pt.y, pt.z, inters])
##
##        arr = np.array(values)
##        arr = arr[arr[:,3].argsort()]
##        arr.reshape((arr.size/4,4))
##
##        x = arr[:,0]
##        y = arr[:,1]
##        z = arr[:,2]
##        d = arr[:,3]
##
##        crossSections[pID] = [x,y,z,d]


start_time = timeit.default_timer()
getIntersection(mesh, idx, submesh)
print("Time for intersecting triangles: " + str(timeit.default_timer() - start_time))


print("Time total: " + str(timeit.default_timer() - start_time_total))

