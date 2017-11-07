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
sys.path.append('C:/ChEsher/py/modules')

import fileHandler as fh
from calcMesh_new import CalcMesh

filename_input_reach = "./input/AXIS.i2s"
filename_input_LBO = "./input/LEFT_BOUNDARY.i3s"
filename_input_profiles = "./input/PROFILES.i3s"
filename_input_RBO = "./input/RIGHT_BOUNDARY.i3s"
filename_input_HOLE = "./input/HOLE.i2s"

filename_output_mesh_triangulation = "./output/MESH_TRIANGULATION.t3s"
filename_output_mesh_elevation = "./output/MESH_ELEVATION.t3s"

print "read mesh"
nodRaw, proRaw = fh.readI3S(filename_input_profiles)

print "read reach"
nodReach = fh.readI2S(filename_input_reach)[0]

print "read LBO"
nodLBO = fh.readI3S(filename_input_LBO)[0]

print "read RBO"
nodRBO = fh.readI3S(filename_input_RBO)[0]

print "read hole"
nodHole = fh.readI2S(filename_input_HOLE)[0]

print nodHole

nnL = None
nnC = 5
nnR = None
length = 2.0
nodLBL = None
nodRBL = None
delta = 2.0

mesh = CalcMesh(nodRaw, proRaw, nodReach, nnC, length, nodLBL, nodRBL, nodLBO, nodRBO, nnL, nnR, nodHole, delta)

mesh.determineFlowDirection()
mesh.normalizeProfiles()
mesh.interpolateChannel()
mesh.applySegments()

t = triangle.triangulate(mesh.geometry, 'pa')

# plot triangulation using matplotlib
plt.figure(1)
ax1 = plt.subplot(111, aspect='equal')
triangle.plot.plot(ax1, **t)
plt.show()
        




print "\n~+~ FINISH ~+~\n"


pass


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
innermesh = []
outermesh = []
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
        innermesh.append(mesh[tID])
    # if triangle does not intersect boundary mesh, append triangle to outer mesh
    else:
        outermesh.append(mesh[tID])

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
fh.writeT3Slist(x_mesh, y_mesh, z_mesh, outermesh, filename_output_outer)

# write inner mesh
fh.writeT3Slist(x_mesh, y_mesh, z_mesh, innermesh, filename_output_inner)

# write intersection mesh
x_intersectionmesh = []
y_intersectionmesh = []
z_intersectionmesh = []

for i in range(len(t["vertices"])):
    x_intersectionmesh.append(t["vertices"][i][0])
    y_intersectionmesh.append(t["vertices"][i][1])
    z_intersectionmesh.append(0.0)
    
intersectionmesh = t["triangles"]

fh.writeT3Slist(x_intersectionmesh, y_intersectionmesh, z_intersectionmesh, intersectionmesh, filename_output_intersection)

# apply submesh to total mesh
x_totalmesh = x_mesh
y_totalmesh = y_mesh
z_totalmesh = z_mesh
totalmesh = outermesh
n_vertices = len(x_mesh)

for i in range(len(x_submesh)):
    x_totalmesh.append(x_submesh[i])
    y_totalmesh.append(y_submesh[i])
    z_totalmesh.append(z_submesh[i])
for i in range(len(submesh)):    
    totalmesh.append([submesh[i][0]+n_vertices, submesh[i][1]+n_vertices, submesh[i][2]+n_vertices])

# apply intersection mesh to total mesh
# find ids from intersection mesh vertices in total mesh
a = np.array([x_totalmesh, y_totalmesh])
b = np.reshape(a, (2*len(x_totalmesh)), order='F')
mesh_coords = np.reshape(b, (len(x_totalmesh), 2))

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
    totalmesh.append([id1, id2, id3])

# write total mesh
fh.writeT3Slist(x_totalmesh, y_totalmesh, z_totalmesh, totalmesh, filename_output_total)

print("Time for intersecting triangles: " + str(timeit.default_timer() - start_time))
print("Time total: " + str(timeit.default_timer() - start_time_total))

