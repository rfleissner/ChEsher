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

"""Wrapper for module Cont2DXF"""

__author__="Reinhard Fleissner"
__date__ ="$18.05.2016 22:38:30$"

import os
import functools
import sys

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QMessageBox, QColor, QFileDialog

# modules and classes
from uiCont2DXF import Ui_Cont2DXF
import uiHandler as uih
import fileHandler as fh
from matplotlib import colors
import matplotlib.tri as tri
import matplotlib.pyplot as plt
from random import uniform
import triangle

import numpy as np
from shapely.geometry import LinearRing, Polygon, Point

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class WrapCont2DXF():
    """Wrapper for module Cont2DXF"""

    def __init__(self):
        """Constructor."""

        # setup user interface
        self.widget = QtGui.QWidget()
        self.ui = Ui_Cont2DXF()
        self.ui.setupUi(self.widget)
        self.directory = os.path.abspath('.')
        
# module Cont2DXF

        self.callbackCont2DXFOpenMeshFile = functools.partial(self.getOpenFileName, "Open T3S-file", "2D T3 Scalar Mesh (ASCII SingleFrame) (*.t3s)", self.ui.lineEditInput)
        QtCore.QObject.connect(self.ui.pushButtonInput, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackCont2DXFOpenMeshFile)

        QtCore.QObject.connect(self.ui.pushButtonAdd, QtCore.SIGNAL(_fromUtf8("clicked()")), self.addLevel)
        QtCore.QObject.connect(self.ui.pushButtonDelete, QtCore.SIGNAL(_fromUtf8("clicked()")), self.deleteLevel)
        QtCore.QObject.connect(self.ui.pushButtonColour, QtCore.SIGNAL(_fromUtf8("clicked()")), self.setColour)
        QtCore.QObject.connect(self.ui.pushButtonLoad, QtCore.SIGNAL(_fromUtf8("clicked()")), self.loadLegend)
        QtCore.QObject.connect(self.ui.pushButtonSave, QtCore.SIGNAL(_fromUtf8("clicked()")), self.saveLegend)
        QtCore.QObject.connect(self.ui.pushButtonDefault, QtCore.SIGNAL(_fromUtf8("clicked()")), self.defaultLegend)
        
        self.callbackCont2DXFSolid = functools.partial(uih.setEnabled, self.ui.checkBoxOutputSolid, self.ui.pushButtonOutputSolid, self.ui.lineEditOutputSolid)
        QtCore.QObject.connect(self.ui.checkBoxOutputSolid, QtCore.SIGNAL("clicked()"), self.callbackCont2DXFSolid)
 
        self.callbackCont2DXFLine = functools.partial(uih.setEnabled, self.ui.checkBoxOutputLine, self.ui.pushButtonOutputLine, self.ui.lineEditOutputLine)
        QtCore.QObject.connect(self.ui.checkBoxOutputLine, QtCore.SIGNAL("clicked()"), self.callbackCont2DXFLine)
        
        legends = ["water depth", "water surface difference", "flow velocity", "bottom shear stress"]
        self.ui.comboBox.addItems(legends)
        
        QtCore.QObject.connect(self.ui.checkBoxOutputLegend, QtCore.SIGNAL("clicked()"), self.setEnabledLegend)
        
        self.callbackCont2DXFOutSolid = functools.partial(self.getSaveFileName, "Save Contours As", "Drawing Interchange File (*.dxf)", self.ui.lineEditOutputSolid)
        QtCore.QObject.connect(self.ui.pushButtonOutputSolid, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackCont2DXFOutSolid)

        self.callbackCont2DXFOutLine = functools.partial(self.getSaveFileName, "Save Contours As", "Drawing Interchange File (*.dxf)", self.ui.lineEditOutputLine)
        QtCore.QObject.connect(self.ui.pushButtonOutputLine, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackCont2DXFOutLine)

        QtCore.QObject.connect(self.ui.pushButtonCreate, QtCore.SIGNAL("clicked()"), self.create)

        header = self.ui.tableWidget.horizontalHeader()
        header.setStretchLastSection(True)

    def setDir(self, directory):
        self.directory = directory
        
    def setColour(self):
        row = self.ui.tableWidget.currentRow()
        item1 = self.ui.tableWidget.item(row, 2)
        initCol = item1.backgroundColor()
        coldia = QtGui.QColorDialog()
        col = coldia.getColor(initCol)
        if col.isValid():
            item = QtGui.QTableWidgetItem()
            item.setBackground(col)
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            item.setText(str(col.red()) + ", " + str(col.green()) + ", " + str(col.blue()))
            self.ui.tableWidget.setItem(row, 2, item)
        else:
            return
        
    def initialize(self):
        
        import os
        abs_path = os.path.abspath('.')
        dir = os.path.join(abs_path, 'examples/').replace('\\', '/')
  
        ###   ~   module Cont2DXF   ~   ##  
        
        self.ui.lineEditInput.setText(dir + "example_09/WATER DEPTH_S161_Case_A.t3s")
        self.ui.lineEditOutputLayer.setText("HQ100")
        self.ui.lineEditOutputLegendSeparator.setText(" - ")
        self.ui.lineEditOutputSolid.setText(dir + "example_09/output/contours_Case_A_water_depth.dxf")
        self.ui.lineEditOutputLine.setText(dir + "example_09/output/isolines_Case_A_water_depth.dxf")
        self.ui.checkBoxOutputLegend.setChecked(True)
        self.ui.checkBoxOutputLegendReverse.setChecked(True)
        self.setEnabledLegend()
        
        uih.setEnabledInitialize(self.ui.checkBoxOutputSolid, self.ui.pushButtonOutputSolid, self.ui.lineEditOutputSolid)
        uih.setEnabledInitialize(self.ui.checkBoxOutputLine, self.ui.pushButtonOutputLine, self.ui.lineEditOutputLine)
        
        self.defaultLegend()
        
    def addLevel(self):
        row = self.ui.tableWidget.currentRow()
        item = QtGui.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        if row == -1:
            row = 0
        self.ui.tableWidget.insertRow(row)
        self.ui.tableWidget.setItem(row, 2, item)

    def deleteLevel(self):
        row = self.ui.tableWidget.currentRow()
        self.ui.tableWidget.removeRow(row)
        
    def defaultLegend(self):
        
        def RGB2HEX(RGB):
            
            HEX = []
            for i in range(len(RGB)):
                RGB[i]
                colFloat_RGB = (float(RGB[i][0])/255.0, float(RGB[i][1])/255.0, float(RGB[i][2])/255.0)
                HEX.append(colors.rgb2hex(colFloat_RGB))
            return HEX
        
        legend = self.ui.comboBox.currentIndex()

        # water depth
        if legend == 0:

            levels = [0.01, 0.1, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 4.0, 100.0]
            col_RGB = [[190,232,255],[116,179,255],[55,141,255],[18,107,238],[0,77,168],[232,190,255],[202,123,245],[161,91,137],[130,39,100],[230,0,0]]
            col_HEX = RGB2HEX(col_RGB)
            
            self.applyLegend(levels, col_HEX)
            
            self.ui.lineEditOutputLegendTitle.setText("Water depth")
            self.ui.lineEditOutputLegendSubtitle.setText("[m]")
            
        # water surface difference
        if legend == 1:
            levels = [-100.0, -0.8, -0.6, -0.4, -0.2, -0.1, -0.05, -0.01, 0.01, 0.05, 0.1, 0.2, 0.4, 0.6, 0.8, 100.0]
            col_RGB = [[219,81,216],[255,128,255],[191,128,255],[128,128,255],[128,191,255],[128,255,255],[179,255,255],[255,255,255],[255,255,204],[255,255,128],[255,191,128],[255,128,128],[255,0,0],[202,0,0],[157,0,0]]
            col_HEX = RGB2HEX(col_RGB)
            
            self.applyLegend(levels, col_HEX)

            self.ui.lineEditOutputLegendTitle.setText("Water surface difference")
            self.ui.lineEditOutputLegendSubtitle.setText("[m]")
            
        # velocity
        if legend == 2:
            levels = [0.0, 0.1, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 4.0, 100.0]
            col_RGB = [[211,255,190],[163,255,116],[77,230,0],[55,168,0],[36,116,0],[255,190,190],[255,127,127],[230,0,0],[168,0,0], [116,0,0]]
            col_HEX = RGB2HEX(col_RGB)
            
            self.applyLegend(levels, col_HEX)

            self.ui.lineEditOutputLegendTitle.setText("Flow velocity")
            self.ui.lineEditOutputLegendSubtitle.setText("[m/s]")
            
        # bottom shear stress
        if legend == 3:
            levels = [0.0, 5.0, 12.5, 25.0, 37.5, 50.0, 75.0, 100.0, 150.0, 200.0, 1000.0]
            col_RGB = [[211,255,190],[163,255,116],[77,230,0],[55,168,0],[36,116,0],[255,190,190],[255,127,127],[230,0,0],[168,0,0], [116,0,0]]
            col_HEX = RGB2HEX(col_RGB)
            
            self.applyLegend(levels, col_HEX)

            self.ui.lineEditOutputLegendTitle.setText("Bottom shear stress")
            self.ui.lineEditOutputLegendSubtitle.setText("[N/m2]")
            
    def applyLegend(self, levels, colHEX_RGB):

        nLevels = len(levels)-1

        self.ui.tableWidget.setRowCount(nLevels)
        
        for row in range(nLevels):
            item1 = QtGui.QTableWidgetItem()
            item1.setText(str(levels[row]))
            self.ui.tableWidget.setItem(row, 0, item1)
            
            item2 = QtGui.QTableWidgetItem()
            item2.setText(str(levels[row+1]))
            self.ui.tableWidget.setItem(row, 1, item2)
            
            col = colors.hex2color(colHEX_RGB[row])
            colPy = QColor(int(col[0]*255),int(col[1]*255),int(col[2]*255))
            item3 = QtGui.QTableWidgetItem()
            item3.setBackground(colPy)
            item3.setFlags(QtCore.Qt.ItemIsEnabled)
            item3.setText(str(colPy.red()) + ", " + str(colPy.green()) + ", " + str(colPy.blue()))
            self.ui.tableWidget.setItem(row, 2, item3)
            
    def loadLegend(self):
        filename = QFileDialog.getOpenFileName(self.widget, "Load an EnSim ColourScale definition file", self.directory, "EnSim ColourScale Files (*.cs1)")
        
        if filename != "":
            try:
                levels, colHEX_BGR = fh.readCS1(filename)

                colHEX_RGB = []

                for col in range(len(colHEX_BGR)):
                    colFloat_BGR = colors.hex2color(colHEX_BGR[col])
                    colFloat_RGB = [colFloat_BGR[2], colFloat_BGR[1], colFloat_BGR[0]]
                    colHEX_RGB.append(colors.rgb2hex(colFloat_RGB)) 

                self.applyLegend(levels, colHEX_RGB)

                info = "Legend loaded with {0} levels.".format(len(levels))     
                QMessageBox.information(self.widget, "Legend", info)
            except:
                QMessageBox.critical(self.widget, "Error", "Not able to load legend!")

    def saveLegend(self):
        filename = QFileDialog.getSaveFileName(self.widget, "Save an EnSim ColourScale definition file", self.directory, "EnSim ColourScale Files (*.cs1)")
   
        if filename != "":
            try:
                levels, levels_ok, coloursHEX_RGB, coloursRGB, coloursHEX_BGR, coloursBGR, col_ok = self.getLevels()
            except:
                QMessageBox.critical(self.widget, "Error", "Check level inputs!")
                return        

            if not levels_ok:
                QMessageBox.critical(self.widget, "Error", "Check level ranges!")
                return
            if not col_ok:
                QMessageBox.critical(self.widget, "Error", "Check colours!")
                return

            try:
                fh.writeCS1(filename, levels, coloursHEX_BGR)
                info = "Legend saved with {0} levels.".format(len(levels))     
                QMessageBox.information(self.widget, "Legend", info)
            except:
                QMessageBox.critical(self.widget, "Error", "Not able to save legend!")
                return
 
    def setEnabledLegend(self):
        checked = self.ui.checkBoxOutputLegend.isChecked()
        self.ui.widgetLegend.setEnabled(checked)

    def getLevels(self):
        levels = []
        colHEX_RGB = []
        colHEX_BGR = []
        colRGB = []
        colBGR = []
        level_ok = True
        col_ok = True
        
        rows = self.ui.tableWidget.rowCount()
        
        if rows > 0:
            for row in range(rows):
                try:
                    levels.append(float(self.ui.tableWidget.item(row, 0).text()))
                    float(self.ui.tableWidget.item(row, 1).text())
                except:
                    return [], False, [], [], True
                try:
                    col = str(self.ui.tableWidget.item(row, 2).text()).split(",")

                    colFloat_RGB = (float(col[0])/255.0, float(col[1])/255.0, float(col[2])/255.0)
                    colFloat_BGR = (float(col[2])/255.0, float(col[1])/255.0, float(col[0])/255.0)
                    colRGB.append([float(col[0]), float(col[1]), float(col[2])])
                    colBGR.append([float(col[2]), float(col[1]), float(col[0])])
#                    colHex = colors.rgb2hex(colFloat_RGB)
                    colHEX_RGB.append(colors.rgb2hex(colFloat_RGB))
                    colHEX_BGR.append(colors.rgb2hex(colFloat_BGR))
                except:
                    return [], True, [], [], False
         
            # check if level ranges are in ascending order
            for row in range(rows-1):
                
                level_ai = round(float(self.ui.tableWidget.item(row, 0).text()), 6)
                level_aj = round(float(self.ui.tableWidget.item(row, 1).text()), 6)
                level_bi = round(float(self.ui.tableWidget.item(row+1, 0).text()), 6)
                
                if level_aj != level_bi:
                    level_ok = False
                if level_aj <= level_ai:
                    level_ok = False
                    
            level_1i = float(self.ui.tableWidget.item(0, 0).text())
            level_1j = float(self.ui.tableWidget.item(0, 1).text())
            
            if level_1j <= level_1i:
                level_ok = False

            level_Ni = float(self.ui.tableWidget.item(rows-1, 0).text())
            level_Nj = float(self.ui.tableWidget.item(rows-1, 1).text())
            
            if level_Nj <= level_Ni:
                level_ok = False
            
            levels.append(float(self.ui.tableWidget.item(rows-1, 1).text()))
            
        return levels, level_ok, colHEX_RGB, colRGB, colHEX_BGR, colBGR, col_ok
    
    def create(self):
        
        def hole(polycoord):
            """Polygon is a hole, if the vertices are defined clockwise."""
            
            ring = LinearRing(polycoord)
            if ring.is_ccw is False:
                return True
            else:
                return False
                
        def getHole(polycoord):
            """Create random point inside polygon."""
            
            polygon = Polygon(polycoord)
            bounds = polygon.bounds
            
            while True:
                randX = uniform(bounds[0], bounds[2])
                randY = uniform(bounds[1], bounds[3])
                randPoint = Point(randX,randY)

                if randPoint.within(polygon):
                    break
            return [randX, randY]
        
        info = ""

        # get levels and colours
        try:
            levels, levels_ok, coloursHEX_RGB, coloursRGB, coloursHEX_BGR, coloursBGR, col_ok = self.getLevels()
        except Exception, e:
            QMessageBox.critical(self.widget, "Error", "Check level inputs!" + "\n\n" + str(e))
            return
        
        if not levels_ok:
            QMessageBox.critical(self.widget, "Error", "Check level ranges!")
            return
        if not col_ok:
            QMessageBox.critical(self.widget, "Error", "Check colours!")
            return
        
        # read input meshes
        try:
            x, y, z, triangles = fh.readT3STriangulation(self.ui.lineEditInput.text())
            triang = tri.Triangulation(x, y, triangles)
        except Exception, e:
            QMessageBox.critical(self.widget, "Error", "Not able to load mesh file!\nCheck filename or content!" + "\n\n" + str(e))
            return

        contours = []
        
        # loop over contour levels
        for level in range(len(levels)-1):

            # create contour plot with matplotlib.pyplot.tricontourf
            cs = plt.tricontourf(triang, z, levels=[levels[level], levels[level+1]], colors=coloursHEX_RGB[level])

            # instantiate the dictionary for the triangulation
            geometry = {}
            geometry["vertices"] = []
            geometry["segments"] = []
            geometry["holes"] = []

            # nodecounter for level
            nodeID = 0
            
            # loop over matplotlib collection
            for cc in cs.collections:
                for pp in cc.get_paths():
                    
                    # paths to polygons
                    polys = pp.to_polygons()

                    eps = 0.000001
                    polys_ = []
                    
                    # loop over polygons
                    for pID in range(len(polys)):
                        poly = polys[pID]
                        nodeIDs = []
                        
                        if len(poly) > 1:
                            
                            # add random point if polygon defines a hole
                            if hole(poly):
                                geometry["holes"].append(getHole(poly))
                            
                            # nodecounter for polygon
                            counter = 0
                            
                            # add vertices and segments
                            # triangle crashes, if vertices are too close to each other,
                            # which would result in zero area triangles
                            for vID in range(len(poly)):
                                vert = np.array(poly[vID])
                                vert = vert.reshape((1,2))
                                
                                # first vertice in polygon
                                if len(geometry["vertices"]) == 0:
                                    geometry["vertices"] = np.array(vert)
                                    nodeIDs.append(nodeID)
                                    counter += 1
                                    nodeID += 1
                                else:
                                    # subtract actual vertice from array of vertices
                                    vertices_ = geometry["vertices"] - vert
                                    
                                    # calculate the length of the vectors
                                    norm = np.linalg.norm(vertices_, axis = 1)
                                    
                                    # get smallest vector norm
                                    min_norm = norm.min()

                                    # if smallest vector norm is greater than a defined value, apply vertice
                                    if min_norm > eps:
                                        counter += 1
                                        geometry["vertices"] = np.concatenate((geometry["vertices"], vert))
                                        nodeIDs.append(nodeID)
                                        nodeID += 1
                                    # else get index of smallest vector norm and apply node-ID
                                    else:
                                        min_index = np.argmin(norm)
                                        # print "comparison: ", min_index, geometry["vertices"][min_index], vID, poly[vID]
                                        nodeIDs.append(min_index)

                            # close polygon by adding id from first vertice
                            nodeIDs.append(nodeID-counter)

                        polys_.append(nodeIDs)

                    # create segments
                    for pID in range(len(polys_)):
                        for nID in range(len(polys_[pID])-1):
                            geometry["segments"].append([polys_[pID][nID], polys_[pID][nID+1]])

            # delete holes from dictionary, if no holes exist
            if len(geometry["holes"]) == 0:
                del geometry["holes"]
            if len(geometry["vertices"]) >= 3:
                t = triangle.triangulate(geometry, 'p')
                contours.append(t)
            else:
                contours.append(None)
                
# plot triangulation using matplotlib
#            plt.figure(1)
#            ax1 = plt.subplot(111, aspect='equal')
#            triangle.plot.plot(ax1, **t)
#            plt.show()

        xLeg = max(x)
        yLeg = min(y)
        origin = (xLeg, yLeg)
        
        title = self.ui.lineEditOutputLegendTitle.text()
        subtitle = self.ui.lineEditOutputLegendSubtitle.text()

        if self.ui.checkBoxOutputSolid.isChecked():
            try:
                fh.writeContSolidDXF(
                    self.ui.lineEditOutputSolid.text(), 
                    contours,
                    levels,
                    coloursRGB, 
                    self.ui.lineEditOutputLayer.text(),
                    self.ui.checkBoxOutputLegend.isChecked(),
                    title,
                    subtitle,
                    origin,
                    self.ui.lineEditOutputLegendSeparator.text(),
                    self.ui.checkBoxOutputLegendReverse.isChecked()
                )
                info += "Contours:\n"
                info += " - Contours created with {0} levels.\n".format(len(levels)) 
                if self.ui.checkBoxOutputLegend.isChecked():
                    info += " - Legend created.\n"
                info += " - DXF written to {0}.\n\n".format(self.ui.lineEditOutputSolid.text())
            except:
                info += " - ERROR: Not able to write contour to dxf!\n"
                info += "\n"
                info += str(sys.exc_info())
                info += "\n"
            
        if self.ui.checkBoxOutputLine.isChecked():
            try:
                fh.writeContIsoLineDXF(
                self.ui.lineEditOutputLine.text(), 
                contours, 
                levels,
                coloursRGB, 
                self.ui.lineEditOutputLayer.text(),
                self.ui.checkBoxOutputLegend.isChecked(),
                title,
                subtitle,
                origin,
                self.ui.lineEditOutputLegendSeparator.text(),
                self.ui.checkBoxOutputLegendReverse.isChecked()
                )
                info += "Isolines:\n"
                info += " - Isolines created with {0} levels.\n".format(len(levels))
                if self.ui.checkBoxOutputLegend.isChecked():
                    info += " - Legend created.\n"
                info += " - DXF written to {0}.\n".format(self.ui.lineEditOutputLine.text())
            except:
                info += " - ERROR: Not able to write isolines to dxf!\n"            
                info += "\n"
                info += str(sys.exc_info())
                info += "\n"
                
        QMessageBox.information(self.widget, "Module Cont2DXF", info)
    
    def getOpenFileName(self, title, fileFormat, lineEdit):
        filename = QFileDialog.getOpenFileName(self.widget, title, self.directory, fileFormat)
        if filename != "":
            lineEdit.setText(filename)

    def getSaveFileName(self, title, fileFormat, lineEdit):
        filename = QFileDialog.getSaveFileName(self.widget, title, self.directory, fileFormat)
        if filename != "":
            lineEdit.setText(filename)