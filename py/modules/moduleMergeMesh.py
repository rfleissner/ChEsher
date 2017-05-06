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

"""Wrapper for module MergeMesh"""

__author__="Reinhard Fleissner"
__date__ ="$23.04.2017 00:18:42$"

import os
import functools
import copy
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QFileDialog, QMessageBox

# modules and classes
from uiMergeMesh import Ui_MergeMesh
import uiHandler as uih
import fileHandler as fh

from random import uniform
import triangle
import triangle.plot
import numpy as np
from shapely.geometry import LineString, Point, Polygon

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class WrapMergeMesh():
    """Wrapper for module MergeMesh"""

    def __init__(self):
        """Constructor."""

        # setup user interface
        self.widget = QtGui.QWidget()
        self.ui = Ui_MergeMesh()
        self.ui.setupUi(self.widget)
        self.directory = os.path.abspath('.')
        
        # module MergeMesh

        self.callbackOpenInputMesh = functools.partial(self.getOpenFileName, "Open T3S-file", "2D T3 Scalar Mesh (ASCII SingleFrame) (*.t3s)", self.ui.lineEditInputMesh)
        QtCore.QObject.connect(self.ui.pushButtonInputMesh, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackOpenInputMesh)

        QtCore.QObject.connect(self.ui.pushButtonAdd, QtCore.SIGNAL(_fromUtf8("clicked()")), self.add)
        QtCore.QObject.connect(self.ui.pushButtonDelete, QtCore.SIGNAL(_fromUtf8("clicked()")), self.delete)
        QtCore.QObject.connect(self.ui.pushButtonUp, QtCore.SIGNAL(_fromUtf8("clicked()")), self.moveUp)
        QtCore.QObject.connect(self.ui.pushButtonDown, QtCore.SIGNAL(_fromUtf8("clicked()")), self.moveDown)
        
        QtCore.QObject.connect(self.ui.pushButtonInputSubmesh, QtCore.SIGNAL(_fromUtf8("clicked()")), self.getFileName)
        
        self.callbackTotalMesh = functools.partial(uih.setEnabled, self.ui.checkBoxOutputTotalMesh, self.ui.pushButtonOutputTotalMesh, self.ui.lineEditOutputTotalMesh)
        QtCore.QObject.connect(self.ui.checkBoxOutputTotalMesh, QtCore.SIGNAL("clicked()"), self.callbackTotalMesh)

        self.callbackIntersectionMesh = functools.partial(uih.setEnabled, self.ui.checkBoxOutputIntersectionMesh, self.ui.pushButtonOutputIntersectionMesh, self.ui.lineEditOutputIntersectionMesh)
        QtCore.QObject.connect(self.ui.checkBoxOutputIntersectionMesh, QtCore.SIGNAL("clicked()"), self.callbackIntersectionMesh)

        self.callbackInnerMesh = functools.partial(uih.setEnabled, self.ui.checkBoxOutputInnerMesh, self.ui.pushButtonOutputInnerMesh, self.ui.lineEditOutputInnerMesh)
        QtCore.QObject.connect(self.ui.checkBoxOutputInnerMesh, QtCore.SIGNAL("clicked()"), self.callbackInnerMesh)
        
        self.callbackOuterMesh = functools.partial(uih.setEnabled, self.ui.checkBoxOutputOuterMesh, self.ui.pushButtonOutputOuterMesh, self.ui.lineEditOutputOuterMesh)
        QtCore.QObject.connect(self.ui.checkBoxOutputOuterMesh, QtCore.SIGNAL("clicked()"), self.callbackOuterMesh)
        
        self.callbackSaveTotalMesh = functools.partial(self.getSaveFileName, "Save Mesh As", "2D T3 Mesh (*.t3s)", self.ui.lineEditOutputTotalMesh)
        QtCore.QObject.connect(self.ui.pushButtonOutputTotalMesh, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackSaveTotalMesh)
        
        self.callbackSaveIntersectionMesh = functools.partial(self.getSaveFileName, "Save Mesh As", "2D T3 Mesh (*.t3s)", self.ui.lineEditOutputIntersectionMesh)
        QtCore.QObject.connect(self.ui.pushButtonOutputIntersectionMesh, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackSaveIntersectionMesh)

        self.callbackSaveInnerMesh = functools.partial(self.getSaveFileName, "Save Mesh As", "2D T3 Mesh (*.t3s)", self.ui.lineEditOutputInnerMesh)
        QtCore.QObject.connect(self.ui.pushButtonOutputInnerMesh, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackSaveInnerMesh)

        self.callbackSaveOuterMesh = functools.partial(self.getSaveFileName, "Save Mesh As", "2D T3 Mesh (*.t3s)", self.ui.lineEditOutputOuterMesh)
        QtCore.QObject.connect(self.ui.pushButtonOutputOuterMesh, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackSaveOuterMesh)

        QtCore.QObject.connect(self.ui.pushButtonCreate, QtCore.SIGNAL("clicked()"), self.create)
    
    def getFileName(self):
        row = self.ui.tableWidget.currentRow()
        filetype = ("2D T3 Scalar Mesh (ASCII SingleFrame) (*.t3s)")
        filename = QFileDialog.getOpenFileName(self.widget, "Open T3S-file", self.directory, filetype)

        if filename != "":
            item = QtGui.QTableWidgetItem()
            item.setText(filename)
            self.ui.tableWidget.setItem(row, 0, item)
            
    def setDir(self, dir):
        self.directory = dir

    def mergeMesh(self, offset, x_mesh, y_mesh, z_mesh, mesh, boundaries_mesh, x_submesh, y_submesh, z_submesh, submesh, boundaries_submesh):

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
        edges_innermesh = []

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

                if e1[::-1] in edges_innermesh:
                    del edges_innermesh[edges_innermesh.index(e1[::-1])]
                else:
                    edges_innermesh.append(e1)
                if e2[::-1] in edges_innermesh:
                    del edges_innermesh[edges_innermesh.index(e2[::-1])]
                else:
                    edges_innermesh.append(e2)
                if e3[::-1] in edges_innermesh:
                    del edges_innermesh[edges_innermesh.index(e3[::-1])]
                else:
                    edges_innermesh.append(e3)
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
        for i in range(len(edges_innermesh)):
            s1 = 0
            s2 = 0

            if edges_innermesh[i][0] not in nIDs:
                vertex = [x_mesh[edges_innermesh[i][0]], y_mesh[edges_innermesh[i][0]]]
                nIDs.append(edges_innermesh[i][0])
                geometry["vertices"].append(vertex)
                s1 = vert_counter
                vert_counter += 1
            else:
                s1 = nIDs.index(edges_innermesh[i][0])
            if edges_innermesh[i][1] not in nIDs:
                vertex = [x_mesh[edges_innermesh[i][1]], y_mesh[edges_innermesh[i][1]]]
                nIDs.append(edges_innermesh[i][1])
                geometry["vertices"].append(vertex)
                s2 = vert_counter
                vert_counter += 1
            else:
                s2 = nIDs.index(edges_innermesh[i][1])        

            geometry["segments"].append([s1,s2])

        n_vert_innermesh = len(edges_innermesh)
        # get vertices and segments from submesh (inner boundary of intersection mesh)
        del nIDs[:]
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
                s1 = nIDs.index(boundaries_submesh[i][0])+n_vert_innermesh
            if boundaries_submesh[i][1] not in nIDs:
                vertex = [x_submesh[boundaries_submesh[i][1]], y_submesh[boundaries_submesh[i][1]]]
                nIDs.append(boundaries_submesh[i][1])
                geometry["vertices"].append(vertex)
                s2 = vert_counter
                vert_counter += 1
            else:
                s2 = nIDs.index(boundaries_submesh[i][1])+n_vert_innermesh

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

        # get intersection mesh
        x_intersectionmesh = []
        y_intersectionmesh = []
        z_intersectionmesh = []

        for i in range(len(t["vertices"])):
            x_intersectionmesh.append(t["vertices"][i][0])
            y_intersectionmesh.append(t["vertices"][i][1])
            z_intersectionmesh.append(0.0)

        intersectionmesh = t["triangles"]     

        # apply submesh to total mesh
        x_totalmesh = copy.copy(x_mesh)
        y_totalmesh = copy.copy(y_mesh)
        z_totalmesh = copy.copy(z_mesh)
        totalmesh = copy.copy(outermesh)
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
        
        return  innermesh,\
                outermesh, \
                x_intersectionmesh, y_intersectionmesh, z_intersectionmesh, intersectionmesh,\
                x_totalmesh, y_totalmesh, z_totalmesh, totalmesh
                
    def create(self):

        info = ""
        
        filename_input_mesh = self.ui.lineEditInputMesh.text()
        try:
            x_mesh, y_mesh, z_mesh, mesh, boundaries_mesh = fh.readT3STriangulation(filename_input_mesh)
            info += " - Mesh loaded with {0} nodes and {1} elements.\n".format(len(x_mesh), len(mesh))
        except Exception, e:
            QMessageBox.critical(self.widget, "Error", "Not able to load mesh!\nCheck filename or content!" + "\n\n" + str(e))
            return
        
        info += "\n"
        
        rows = self.ui.tableWidget.rowCount()
        offset = self.ui.doubleSpinBoxOffset.value()
        for row in range(rows):  
            # read submesh
            try:
                filename_input_submesh = self.ui.tableWidget.item(row, 0).text()
                x_submesh, y_submesh, z_submesh, submesh, boundaries_submesh = fh.readT3STriangulation(filename_input_submesh)
                info += " - Submesh {0} loaded with {1} nodes and {2} elements.\n".format(row+1, len(x_submesh), len(submesh))
            except Exception, e:
                QMessageBox.critical(self.widget, "Error", "Not able to load mesh!\nCheck filename or content!" + "\n\n" + str(e))
                return 
            # do merging
            try:
                innermesh, outermesh, \
                x_intersectionmesh, y_intersectionmesh, z_intersectionmesh, intersectionmesh,\
                x_totalmesh, y_totalmesh, z_totalmesh, totalmesh = self.mergeMesh(offset, x_mesh, y_mesh, z_mesh, mesh, boundaries_mesh, x_submesh, y_submesh, z_submesh, submesh, boundaries_submesh)
                info += " - Merging of mesh and submesh {0} done.\n".format(row+1)
                info += "\n"
            except Exception, e:
                QMessageBox.critical(self.widget, "Error", "Not able to merge mesh and submesh {0}. Check filename or content of files!".format(row+1) + "\n\n" + str(e))
                return

            if self.ui.checkBoxOutputSubmesh.isChecked() is False and row < rows-1:
                x_mesh = x_totalmesh
                y_mesh = y_totalmesh
                z_mesh = z_totalmesh
                mesh = totalmesh
                continue
                
            # write output total mesh
            if self.ui.checkBoxOutputTotalMesh.isChecked():
                try:
                    file = self.ui.lineEditOutputTotalMesh.text().split(".")
                    filename_output_total = file[0]+"_"+str(row+1)+"."+file[1]
                    fh.writeT3Slist(x_totalmesh, y_totalmesh, z_totalmesh, totalmesh, filename_output_total)
                    info += " - Total mesh after merging submesh {0} written to file {1}.\n".format(row+1, filename_output_total)
                except Exception, e:
                    QMessageBox.critical(self.widget, "Error", "Not able to write total mesh!" + "\n\n" + str(e))
            
            # write output intersection mesh
            if self.ui.checkBoxOutputIntersectionMesh.isChecked():
                try:
                    file = self.ui.lineEditOutputIntersectionMesh.text().split(".")
                    filename_output_intersection = file[0]+"_"+str(row+1)+"."+file[1]
                    fh.writeT3Slist(x_intersectionmesh, y_intersectionmesh, z_intersectionmesh, intersectionmesh, filename_output_intersection)
                    info += " - Intersection mesh after merging submesh {0} written to file {1}.\n".format(row+1, filename_output_intersection)
                except Exception, e:
                    QMessageBox.critical(self.widget, "Error", "Not able to write intersection mesh!" + "\n\n" + str(e))
            
            # write output inner mesh
            if self.ui.checkBoxOutputInnerMesh.isChecked():
                try:
                    file = self.ui.lineEditOutputInnerMesh.text().split(".")
                    filename_output_inner = file[0]+"_"+str(row+1)+"."+file[1]
                    fh.writeT3Slist(x_mesh, y_mesh, z_mesh, innermesh, filename_output_inner)
                    info += " - Inner mesh after merging submesh {0} written to file {1}.\n".format(row+1, filename_output_inner)
                except Exception, e:
                    QMessageBox.critical(self.widget, "Error", "Not able to write inner mesh!" + "\n\n" + str(e))
            
            # write output outer mesh
            if self.ui.checkBoxOutputOuterMesh.isChecked():
                try:
                    file = self.ui.lineEditOutputOuterMesh.text().split(".")
                    filename_output_outer = file[0]+"_"+str(row+1)+"."+file[1]
                    fh.writeT3Slist(x_mesh, y_mesh, z_mesh, outermesh, filename_output_outer)
                    info += " - Outer mesh after merging submesh {0} written to file {1}.\n".format(row+1, filename_output_outer)
                except Exception, e:
                    QMessageBox.critical(self.widget, "Error", "Not able to write outer mesh!" + "\n\n" + str(e))
        
            info += "\n"
            
            x_mesh = x_totalmesh
            y_mesh = y_totalmesh
            z_mesh = z_totalmesh
            mesh = totalmesh

        QMessageBox.information(self.widget, "Module MergeMesh", info)     
        
    def add(self):
        row = self.ui.tableWidget.currentRow()
        item = QtGui.QTableWidgetItem()
        if row == -1:
            row = 0
        self.ui.tableWidget.insertRow(row)
        self.ui.tableWidget.setItem(row, 0, item)

    def delete(self):
        row = self.ui.tableWidget.currentRow()
        self.ui.tableWidget.removeRow(row)

    def moveUp(self):
        row = self.ui.tableWidget.currentRow()
        upper_row = row - 1
        if row > 0:
            content_row = self.ui.tableWidget.item(row, 0).text()
            content_upper_row = self.ui.tableWidget.item(upper_row, 0).text()
            
            item1 = QtGui.QTableWidgetItem()
            item1.setText(content_upper_row)
            self.ui.tableWidget.setItem(row, 0, item1)            

            item2 = QtGui.QTableWidgetItem()
            item2.setText(content_row)
            self.ui.tableWidget.setItem(upper_row, 0, item2)       
            
            self.ui.tableWidget.setCurrentCell(upper_row, 0)

    def moveDown(self):
        rows = self.ui.tableWidget.rowCount()
        row = self.ui.tableWidget.currentRow()
        lower_row = row + 1
        if row < rows-1 and row != -1:
            content_row = self.ui.tableWidget.item(row, 0).text()
            content_lower_row = self.ui.tableWidget.item(lower_row, 0).text()
            
            item1 = QtGui.QTableWidgetItem()
            item1.setText(content_lower_row)
            self.ui.tableWidget.setItem(row, 0, item1)            

            item2 = QtGui.QTableWidgetItem()
            item2.setText(content_row)
            self.ui.tableWidget.setItem(lower_row, 0, item2)    

            self.ui.tableWidget.setCurrentCell(lower_row, 0)
            
    def getFileName(self):
        row = self.ui.tableWidget.currentRow()
        filetype = ("2D T3 Scalar Mesh (ASCII SingleFrame) (*.t3s)")
        filename = QFileDialog.getOpenFileName(self.widget, "Open T3S-file", self.directory, filetype)

        if filename != "":
            item = QtGui.QTableWidgetItem()
            item.setText(filename)
            self.ui.tableWidget.setItem(row, 0, item)
        
    def initialize(self):

        import os
        abs_path = os.path.abspath('.')
        dir = os.path.join(abs_path, 'examples/').replace('\\', '/')
  
        ###   ~   module MergeMesh   ~   ###

        self.ui.lineEditInputMesh.setText(dir + "example_15/bottom.t3s")
        self.ui.doubleSpinBoxOffset.setValue(0.50)
        
        self.ui.tableWidget.setRowCount(0)
        self.add()
        self.add()
        
        item1 = QtGui.QTableWidgetItem()
        item1.setText(dir + "example_15/main_channel.t3s")
        self.ui.tableWidget.setItem(0, 0, item1)

        item2 = QtGui.QTableWidgetItem()
        item2.setText(dir + "example_15/side_channel.t3s")
        self.ui.tableWidget.setItem(1, 0, item2)

        uih.setEnabledInitialize(self.ui.checkBoxOutputTotalMesh, self.ui.pushButtonOutputTotalMesh, self.ui.lineEditOutputTotalMesh)
        self.ui.lineEditOutputTotalMesh.setText(dir + "example_15/output/mesh_total.t3s")

#        uih.setEnabledInitialize(self.ui.checkBoxOutputIntersectionMesh, self.ui.pushButtonOutputIntersectionMesh, self.ui.lineEditOutputIntersectionMesh)
#        self.ui.lineEditOutputIntersectionMesh.setText(dir + "example_16/output/mesh_intersection.t3s")
        
#        uih.setEnabledInitialize(self.ui.checkBoxOutputInnerMesh, self.ui.pushButtonOutputInnerMesh, self.ui.lineEditOutputInnerMesh)
#        self.ui.lineEditOutputInnerMesh.setText(dir + "example_16/output/mesh_inner.t3s")

#        uih.setEnabledInitialize(self.ui.checkBoxOutputOuterMesh, self.ui.pushButtonOutputOuterMesh, self.ui.lineEditOutputOuterMesh)
#        self.ui.lineEditOutputOuterMesh.setText(dir + "example_16/output/mesh_outer.t3s")
        
    def getOpenFileName(self, title, fileFormat, lineEdit):
        filename = QFileDialog.getOpenFileName(self.widget, title, self.directory, fileFormat)
        if filename != "":
            lineEdit.setText(filename)

    def getSaveFileName(self, title, fileFormat, lineEdit):
        filename = QFileDialog.getSaveFileName(self.widget, title, self.directory, fileFormat)
        if filename != "":
            lineEdit.setText(filename)