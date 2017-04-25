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

offset = 0.5

filename_input_mesh = "K:/10-051_FA19B_HW_ Heimschuh_Leibnitz-Sulm_Daemme_erhoehen/Wasserbau/Plaene/Heimschuh/2017/Hydraulik/Geometrie/MergeMesh/BOTTOM_8_TOTAL.t3s"
filename_input_submesh = "K:/10-051_FA19B_HW_ Heimschuh_Leibnitz-Sulm_Daemme_erhoehen/Wasserbau/Plaene/Heimschuh/2017/Hydraulik/Geometrie/MergeMesh/Massnahme_7.t3s"

filename_output_outer = "K:/10-051_FA19B_HW_ Heimschuh_Leibnitz-Sulm_Daemme_erhoehen/Wasserbau/Plaene/Heimschuh/2017/Hydraulik/Geometrie/MergeMesh/BOTTOM_9_OUTSIDE.t3s"
filename_output_intersection = "K:/10-051_FA19B_HW_ Heimschuh_Leibnitz-Sulm_Daemme_erhoehen/Wasserbau/Plaene/Heimschuh/2017/Hydraulik/Geometrie/MergeMesh/BOTTOM_9_INTERSECTION.t3s"
filename_output_total = "K:/10-051_FA19B_HW_ Heimschuh_Leibnitz-Sulm_Daemme_erhoehen/Wasserbau/Plaene/Heimschuh/2017/Hydraulik/Geometrie/MergeMesh/BOTTOM_9_TOTAL.t3s"

start_time_total = timeit.default_timer()
start_time_read_input = timeit.default_timer()

print "read mesh"
#x_mesh, y_mesh, z_mesh, mesh, boundaries_mesh = fh.readT3STriangulation("./input/BOTTOM.t3s")
x_mesh, y_mesh, z_mesh, mesh, boundaries_mesh = fh.readT3STriangulation(filename_input_mesh)

print "read submesh"
#x_submesh, y_submesh, z_submesh, submesh, boundaries_submesh = fh.readT3STriangulation("./input/Massnahme_1.t3s")
x_submesh, y_submesh, z_submesh, submesh, boundaries_submesh = fh.readT3STriangulation(filename_input_submesh)
    
print("Time for reading input: " + str(timeit.default_timer() - start_time_read_input))

start_time = timeit.default_timer()

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
boundary_submesh_real = LineString(coords)
boundary_submesh_polygon = Polygon(boundary_submesh_real) # just used for detecting hole point
# apply offset for detecting intersection
boundary_submesh_linestring = boundary_submesh_real.parallel_offset(offset, 'right')
boundary_submesh = Polygon(boundary_submesh_linestring)

# check if triangle of mesh intersects polygon submesh
nodes_inner_mesh = []
nodes_outer_mesh = []
edges_inner_mesh = []

# loop over mesh triangles
for tID in range(len(mesh)):
    
    # collect coordinates from actual triangle
    coords_triangle = []
    coords_triangle.append((x_mesh[mesh[tID][0]], y_mesh[mesh[tID][0]]))
    coords_triangle.append((x_mesh[mesh[tID][1]], y_mesh[mesh[tID][1]]))
    coords_triangle.append((x_mesh[mesh[tID][2]], y_mesh[mesh[tID][2]]))
    coords_triangle.append((x_mesh[mesh[tID][0]], y_mesh[mesh[tID][0]]))
    
    # create polygon out of triangle
    triang = Polygon(coords_triangle)
    
    # check intersection between triangle and boundary polygon of submesh
    inters = boundary_submesh.intersects(triang)

    # if triangle intersects boundary mesh, append triangle to inner mesh
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
    # if triangle does not intersect boundary mesh, append triangle to outer mesh
    else:
        nodes_outer_mesh.append(mesh[tID])

# triangulate mesh between submesh and outer mesh
# instantiate the dictionary for the triangulation with package triangle
geometry = {}
geometry["vertices"] = []
geometry["segments"] = []
geometry["holes"] = []

vert_counter = 0

# get vertices and segments from inner mesh (outer boundary of intersection mesh)
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

# get vertices and segments from submesh (inner boundary of intersection mesh)
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
    if randPoint.within(boundary_submesh_polygon):
        geometry["holes"].append([randX,randY])
        break

# triangulate intersection mesh with package triangle
t = triangle.triangulate(geometry, 'p')

# plot triangulation using matplotlib
plt.figure(1)
ax1 = plt.subplot(111, aspect='equal')
triangle.plot.plot(ax1, **t)
plt.show()

# write outer mesh
fh.writeT3Slist(x_mesh, y_mesh, z_mesh, nodes_outer_mesh, filename_output_outer)

# write intersection mesh
x_intersectionmesh = []
y_intersectionmesh = []
z_intersectionmesh = []

for i in range(len(t["vertices"])):
    x_intersectionmesh.append(t["vertices"][i][0])
    y_intersectionmesh.append(t["vertices"][i][1])
    z_intersectionmesh.append(0.0)
    
fh.writeT3Slist(x_intersectionmesh, y_intersectionmesh, z_intersectionmesh, t["triangles"], filename_output_intersection)

# apply submesh to total mesh
x_tot = x_mesh
y_tot = y_mesh
z_tot = z_mesh
mesh_tot = nodes_outer_mesh
n_vertices = len(x_mesh)

for i in range(len(x_submesh)):
    x_tot.append(x_submesh[i])
    y_tot.append(y_submesh[i])
    z_tot.append(z_submesh[i])
for i in range(len(submesh)):    
    mesh_tot.append([submesh[i][0]+n_vertices, submesh[i][1]+n_vertices, submesh[i][2]+n_vertices])

# apply intersection mesh to total mesh
# find ids from intersection mesh vertices in total mesh
a = np.array([x_tot, y_tot])
b = np.reshape(a, (2*len(x_tot)), order='F')
mesh_coords = np.reshape(b, (len(x_tot), 2))

map_ids = []
for i in range(len(t["vertices"])):
    p = np.array(t["vertices"][i])
    temp = mesh_coords - p
    norm = np.linalg.norm(temp, axis = 1)
    I = np.argmin(norm)+1
    map_ids.append(I)

for i in range(len(t["triangles"])):
    id1 = map_ids[t["triangles"][i][0]]-1
    id2 = map_ids[t["triangles"][i][1]]-1
    id3 = map_ids[t["triangles"][i][2]]-1
    mesh_tot.append([id1, id2, id3])

fh.writeT3Slist(x_tot, y_tot, z_tot, mesh_tot, filename_output_total)

print("Time for intersecting triangles: " + str(timeit.default_timer() - start_time))
print("Time total: " + str(timeit.default_timer() - start_time_total))

