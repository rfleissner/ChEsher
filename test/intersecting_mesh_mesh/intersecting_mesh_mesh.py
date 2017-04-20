import sys
import timeit
import numpy as np
from shapely.geometry import LineString, MultiLineString, Point, Polygon, MultiPolygon, LinearRing
from shapely.ops import cascaded_union
from rtree import index
import triangle
import triangle.plot
import matplotlib.pyplot as plt
from random import uniform

sys.path.append('C:/ChEsher/py/py')

import fileHandler as fh
import profileOrganizer as po


start_time_total = timeit.default_timer()


start_time_read_input = timeit.default_timer()

print "read mesh"
x_mesh, y_mesh, z_mesh, mesh, boundaries_mesh = fh.readT3STriangulation("./input/mesh.t3s")

print "read submesh"
x_submesh, y_submesh, z_submesh, submesh, boundaries_submesh = fh.readT3STriangulation("./input/submesh.t3s")
    
print("Time for reading input: " + str(timeit.default_timer() - start_time_read_input))

# sort boundary edge points to ordered sequence (necesarry for using shapely's Polygon)
boundaries_sorted = []
boundaries_sorted.append(boundaries_submesh[0])
for i in range(len(boundaries_submesh)-1):
    for j in range(len(boundaries_submesh)):
        if boundaries_submesh[j][0] == boundaries_sorted[-1][1]:
            boundaries_sorted.append(boundaries_submesh[j])
            break

# create Polygon of submesh boundary
coords = []
for i in range(len(boundaries_sorted)):
    coords.append((x_submesh[boundaries_sorted[i][0]], y_submesh[boundaries_sorted[i][0]]))
    coords.append((x_submesh[boundaries_sorted[i][1]], y_submesh[boundaries_sorted[i][1]]))
coords.append((x_submesh[boundaries_sorted[0][1]], y_submesh[boundaries_sorted[0][1]]))
boundary_submesh = Polygon(coords)

# check if triangle of mesh intersects polygon submesh
nodes_inner_mesh = []
nodes_outer_mesh = []
edges_inner_mesh = []
for tID in range(len(mesh)):
    # collect coordinates from actual triangle
    coords_triangle = []
    coords_triangle.append((x_mesh[mesh[tID][0]], y_mesh[mesh[tID][0]]))
    coords_triangle.append((x_mesh[mesh[tID][1]], y_mesh[mesh[tID][1]]))
    coords_triangle.append((x_mesh[mesh[tID][2]], y_mesh[mesh[tID][2]]))
    coords_triangle.append((x_mesh[mesh[tID][0]], y_mesh[mesh[tID][0]]))
    # create polygon out of triangle
    triang = Polygon(coords_triangle)
    # cjeck intersection between triangle and boundary polygon of submesh
    inters = boundary_submesh.intersects(triang)
    if inters is True:
        
        # write node-ids of intersecting triangles to list
        e1 = [mesh[tID][0], mesh[tID][1]]
        e2 = [mesh[tID][1], mesh[tID][2]]
        e3 = [mesh[tID][2], mesh[tID][0]]
        
        if e1[::-1] in edges_inner_mesh:
            del edges_inner_mesh[edges_inner_mesh.index(e1[::-1])]
        else:
            edges_inner_mesh.append(e1)
        if e2[::-1] in edges_inner_mesh:
            del edges_inner_mesh[edges_inner_mesh.index(e2[::-1])]
        else:
            edges_inner_mesh.append(e2)
        if e3[::-1] in edges_inner_mesh:
            del edges_inner_mesh[edges_inner_mesh.index(e3[::-1])]
        else:
            edges_inner_mesh.append(e3)
        
        nodes_inner_mesh.append(mesh[tID])
    else:
        nodes_outer_mesh.append(mesh[tID])

# triangulate mesh between submesh and outer mesh
# instantiate the dictionary for the triangulation
geometry = {}
geometry["vertices"] = []
geometry["segments"] = []
geometry["holes"] = []

vert_counter = 0

# get vertices and segments from inner mesh
nIDs = []
for i in range(len(edges_inner_mesh)):
    s1 = 0
    s2 = 0
    if edges_inner_mesh[i][0] not in nIDs:
        vertex = [x_mesh[edges_inner_mesh[i][0]], y_mesh[edges_inner_mesh[i][0]]]
        nIDs.append(edges_inner_mesh[i][0])
        geometry["vertices"].append(vertex)
        s1 = vert_counter
        vert_counter += 1
    else:
        s1 = nIDs.index(edges_inner_mesh[i][0])
    if edges_inner_mesh[i][1] not in nIDs:
        vertex = [x_mesh[edges_inner_mesh[i][1]], y_mesh[edges_inner_mesh[i][1]]]
        nIDs.append(edges_inner_mesh[i][1])
        geometry["vertices"].append(vertex)
        s2 = vert_counter
        vert_counter += 1
    else:
        s2 = nIDs.index(edges_inner_mesh[i][1])        

    geometry["segments"].append([s1,s2])

# get vertices and segments from submesh
for i in range(len(boundaries_submesh)):
    s1 = 0
    s2 = 0
    if boundaries_submesh[i][0] not in nIDs:
        vertex = [x_submesh[boundaries_submesh[i][0]], y_submesh[boundaries_submesh[i][0]]]
        nIDs.append(boundaries_submesh[i][0])
        geometry["vertices"].append(vertex)
        s1 = vert_counter
        vert_counter += 1
    else:
        s1 = nIDs.index(boundaries_submesh[i][0])
    if boundaries_submesh[i][1] not in nIDs:
        vertex = [x_submesh[boundaries_submesh[i][1]], y_submesh[boundaries_submesh[i][1]]]
        nIDs.append(boundaries_submesh[i][1])
        geometry["vertices"].append(vertex)
        s2 = vert_counter
        vert_counter += 1
    else:
        s2 = nIDs.index(boundaries_submesh[i][1])
        
    geometry["segments"].append([s1,s2])

# get hole of submesh
bounds = boundary_submesh.bounds
while True:
    randX = uniform(bounds[0], bounds[2])
    randY = uniform(bounds[1], bounds[3])
    randPoint = Point(randX,randY)
    if randPoint.within(boundary_submesh):
        geometry["holes"].append([randX,randY])
        break

t = triangle.triangulate(geometry, 'p')

# plot triangulation using matplotlib
plt.figure(1)
ax1 = plt.subplot(111, aspect='equal')
triangle.plot.plot(ax1, **t)
plt.show()

# write outer mesh
fh.writeT3Slist(x_mesh, y_mesh, z_mesh, nodes_outer_mesh, "./output/BOTTOM.t3s")

# write between mesh
x = []
y = []
z = []

for i in range(len(t["vertices"])):
    x.append(t["vertices"][i][0])
    y.append(t["vertices"][i][1])
    z.append(0.0)
    
fh.writeT3Slist(x, y, z, t["triangles"], "./output/BOTTOM_DIFF.t3s")

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
#getIntersection(mesh, idx, submesh)
print("Time for intersecting triangles: " + str(timeit.default_timer() - start_time))
print("Time total: " + str(timeit.default_timer() - start_time_total))

