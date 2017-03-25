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

"""Wrapper for module 2DM2BK"""

__author__="Reinhard Fleissner"
__date__ ="$18.05.2016 22:38:30$"

import os
import sys
import functools

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QMessageBox, QFileDialog

# modules and classes
from ui2DM2BK import Ui_TwoDM2BK
import uiHandler as uih
import fileHandler as fh

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Wrap2DM2BK():
    """Wrapper for module 2DM2BK"""

    def __init__(self):
        """Constructor."""

        # setup user interface
        self.widget = QtGui.QWidget()
        self.ui = Ui_TwoDM2BK()
        self.ui.setupUi(self.widget)
        self.directory = os.path.abspath('.')
# module 2DM2BK

        self.callbackOpen2dmInput = functools.partial(self.getOpenFileName, "Open 2D Mesh File", "SMS 2d Mesh File (*.2dm)", self.ui.lineEditInput)
        QtCore.QObject.connect(self.ui.pushButtonInput, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackOpen2dmInput)

        self.callbackOpen2dmInputData = functools.partial(self.getOpenFileName, "Open Dataset File", "ASCII Dataset Files (*.dat)", self.ui.lineEditInputData)
        QtCore.QObject.connect(self.ui.pushButtonInputData, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackOpen2dmInputData)

        self.callback2dmImpermeable = functools.partial(uih.setEnabled, self.ui.checkBoxImpermeable, self.ui.spinBoxImpermeable, self.ui.spinBoxImpermeable)
        QtCore.QObject.connect(self.ui.checkBoxImpermeable, QtCore.SIGNAL("clicked()"), self.callback2dmImpermeable)

        
        self.callback2dmBottom = functools.partial(uih.setEnabled, self.ui.checkBoxBottom, self.ui.pushButtonBottom, self.ui.lineEditBottom)
        QtCore.QObject.connect(self.ui.checkBoxBottom, QtCore.SIGNAL("clicked()"), self.callback2dmBottom)

        self.callback2dmBottomFriction = functools.partial(uih.setEnabled, self.ui.checkBoxBottomFriction, self.ui.pushButtonBottomFriction, self.ui.lineEditBottomFriction)
        QtCore.QObject.connect(self.ui.checkBoxBottomFriction, QtCore.SIGNAL("clicked()"), self.callback2dmBottomFriction)

        self.callback2dmWaterSurface = functools.partial(uih.setEnabled, self.ui.checkBoxWaterSurface, self.ui.pushButtonWaterSurface, self.ui.lineEditWaterSurface)
        QtCore.QObject.connect(self.ui.checkBoxWaterSurface, QtCore.SIGNAL("clicked()"), self.callback2dmWaterSurface)

        self.callback2dmWaterDepth = functools.partial(uih.setEnabled, self.ui.checkBoxWaterDepth, self.ui.pushButtonWaterDepth, self.ui.lineEditWaterDepth)
        QtCore.QObject.connect(self.ui.checkBoxWaterDepth, QtCore.SIGNAL("clicked()"), self.callback2dmWaterDepth)

        self.callback2dmCulvertHeight = functools.partial(uih.setEnabled, self.ui.checkBoxCulvertHeight, self.ui.pushButtonCulvertHeight, self.ui.lineEditCulvertHeight)
        QtCore.QObject.connect(self.ui.checkBoxCulvertHeight, QtCore.SIGNAL("clicked()"), self.callback2dmCulvertHeight)

        self.callback2dmNS1 = functools.partial(uih.setEnabled, self.ui.checkBoxNS1, self.ui.pushButtonNS1, self.ui.lineEditNS1)
        QtCore.QObject.connect(self.ui.checkBoxNS1, QtCore.SIGNAL("clicked()"), self.callback2dmNS1)

        self.callback2dmNS2 = functools.partial(uih.setEnabled, self.ui.checkBoxNS2, self.ui.pushButtonNS2, self.ui.lineEditNS2)
        QtCore.QObject.connect(self.ui.checkBoxNS2, QtCore.SIGNAL("clicked()"), self.callback2dmNS2)

        self.callback2dmNS3 = functools.partial(uih.setEnabled, self.ui.checkBoxNS3, self.ui.pushButtonNS3, self.ui.lineEditNS3)
        QtCore.QObject.connect(self.ui.checkBoxNS3, QtCore.SIGNAL("clicked()"), self.callback2dmNS3)

        self.callback2dmNS4 = functools.partial(uih.setEnabled, self.ui.checkBoxNS4, self.ui.pushButtonNS4, self.ui.lineEditNS4)
        QtCore.QObject.connect(self.ui.checkBoxNS4, QtCore.SIGNAL("clicked()"), self.callback2dmNS4)

        self.callback2dmNS5 = functools.partial(uih.setEnabled, self.ui.checkBoxNS5, self.ui.pushButtonNS5, self.ui.lineEditNS5)
        QtCore.QObject.connect(self.ui.checkBoxNS5, QtCore.SIGNAL("clicked()"), self.callback2dmNS5)

        self.callback2dmNS6 = functools.partial(uih.setEnabled, self.ui.checkBoxNS6, self.ui.pushButtonNS6, self.ui.lineEditNS6)
        QtCore.QObject.connect(self.ui.checkBoxNS6, QtCore.SIGNAL("clicked()"), self.callback2dmNS6)

        self.callback2dmNS7 = functools.partial(uih.setEnabled, self.ui.checkBoxNS7, self.ui.pushButtonNS7, self.ui.lineEditNS7)
        QtCore.QObject.connect(self.ui.checkBoxNS7, QtCore.SIGNAL("clicked()"), self.callback2dmNS7)

        self.callbackSave2dmBottom = functools.partial(self.getSaveFileName, "Save Bottom As", "2D T3 Mesh (*.t3s)", self.ui.lineEditBottom)
        QtCore.QObject.connect(self.ui.pushButtonBottom, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackSave2dmBottom)

        self.callbackSave2dmBottomFriction = functools.partial(self.getSaveFileName, "Save Bottom Friction As", "2D T3 Mesh (*.t3s)", self.ui.lineEditBottomFriction)
        QtCore.QObject.connect(self.ui.pushButtonBottomFriction, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackSave2dmBottomFriction)

        self.callbackSave2dmWaterSurface = functools.partial(self.getSaveFileName, "Save Water Surface As", "2D T3 Mesh (*.t3s)", self.ui.lineEditWaterSurface)
        QtCore.QObject.connect(self.ui.pushButtonWaterSurface, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackSave2dmWaterSurface)

        self.callbackSave2dmWaterDepth = functools.partial(self.getSaveFileName, "Save Water Depth As", "2D T3 Mesh (*.t3s)", self.ui.lineEditWaterDepth)
        QtCore.QObject.connect(self.ui.pushButtonWaterDepth, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackSave2dmWaterDepth)
        
        self.callbackSave2dmCulvertHeight = functools.partial(self.getSaveFileName, "Save Culvert Height As", "Point Set (*.xyz)", self.ui.lineEditCulvertHeight)
        QtCore.QObject.connect(self.ui.pushButtonCulvertHeight, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackSave2dmCulvertHeight)

        self.callbackSave2dmNS1 = functools.partial(self.getSaveFileName, "Save Node String As", "Line Sets (*.i2s)", self.ui.lineEditNS1)
        QtCore.QObject.connect(self.ui.pushButtonNS1, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackSave2dmNS1)

        self.callbackSave2dmNS2 = functools.partial(self.getSaveFileName, "Save Node String As", "Line Sets (*.i2s)", self.ui.lineEditNS2)
        QtCore.QObject.connect(self.ui.pushButtonNS2, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackSave2dmNS2)

        self.callbackSave2dmNS3 = functools.partial(self.getSaveFileName, "Save Node String As", "Line Sets (*.i2s)", self.ui.lineEditNS3)
        QtCore.QObject.connect(self.ui.pushButtonNS3, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackSave2dmNS3)

        self.callbackSave2dmNS4 = functools.partial(self.getSaveFileName, "Save Node String As", "Line Sets (*.i2s)", self.ui.lineEditNS4)
        QtCore.QObject.connect(self.ui.pushButtonNS4, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackSave2dmNS4)

        self.callbackSave2dmNS5 = functools.partial(self.getSaveFileName, "Save Node String As", "Line Sets (*.i2s)", self.ui.lineEditNS5)
        QtCore.QObject.connect(self.ui.pushButtonNS5, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackSave2dmNS5)

        self.callbackSave2dmNS6 = functools.partial(self.getSaveFileName, "Save Node String As", "Line Sets (*.i2s)", self.ui.lineEditNS6)
        QtCore.QObject.connect(self.ui.pushButtonNS6, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackSave2dmNS6)

        self.callbackSave2dmNS7 = functools.partial(self.getSaveFileName, "Save Node String As", "Line Sets (*.i2s)", self.ui.lineEditNS7)
        QtCore.QObject.connect(self.ui.pushButtonNS7, QtCore.SIGNAL(_fromUtf8("clicked()")), self.callbackSave2dmNS7)

        QtCore.QObject.connect(self.ui.pushButtonCreate, QtCore.SIGNAL("clicked()"), self.create)

    def setDir(self, directory):
        self.directory = directory
    
    def initialize(self):
        
        import os
        abs_path = os.path.abspath('.')
        dir = os.path.join(abs_path, 'examples/').replace('\\', '/')
  
        ###   ~   module 2DM2BK   ~   ###
        
        self.ui.lineEditInput.setText(dir + "example_08/input.2dm")
        self.ui.lineEditInputData.setText(dir + "example_08/water_depth.dat")
        
        uih.setEnabledInitialize(self.ui.checkBoxBottom, self.ui.pushButtonBottom, self.ui.lineEditBottom)
        uih.setEnabledInitialize(self.ui.checkBoxBottomFriction, self.ui.pushButtonBottomFriction, self.ui.lineEditBottomFriction)
        uih.setEnabledInitialize(self.ui.checkBoxWaterSurface, self.ui.pushButtonWaterSurface, self.ui.lineEditWaterSurface)
        uih.setEnabledInitialize(self.ui.checkBoxWaterDepth, self.ui.pushButtonWaterDepth, self.ui.lineEditWaterDepth)                
        uih.setEnabledInitialize(self.ui.checkBoxCulvertHeight, self.ui.pushButtonCulvertHeight, self.ui.lineEditCulvertHeight)
        uih.setEnabledInitialize(self.ui.checkBoxNS1, self.ui.pushButtonNS1, self.ui.lineEditNS1)
        uih.setEnabledInitialize(self.ui.checkBoxNS2, self.ui.pushButtonNS2, self.ui.lineEditNS2)
        uih.setEnabledInitialize(self.ui.checkBoxNS3, self.ui.pushButtonNS3, self.ui.lineEditNS3)
        uih.setEnabledInitialize(self.ui.checkBoxNS4, self.ui.pushButtonNS4, self.ui.lineEditNS4)
        uih.setEnabledInitialize(self.ui.checkBoxNS5, self.ui.pushButtonNS5, self.ui.lineEditNS5)
        uih.setEnabledInitialize(self.ui.checkBoxNS6, self.ui.pushButtonNS6, self.ui.lineEditNS6)
        uih.setEnabledInitialize(self.ui.checkBoxNS7, self.ui.pushButtonNS7, self.ui.lineEditNS7)
                                                                                             
        self.ui.lineEditBottom.setText(dir + "example_08/output/BOTTOM.t3s")
        self.ui.lineEditBottomFriction.setText(dir + "example_08/output/BOTTOM FRICTION.t3s")
        self.ui.lineEditWaterSurface.setText(dir + "example_08/output/WATER SURFACE.t3s")
        self.ui.lineEditWaterDepth.setText(dir + "example_08/output/WATER DEPTH.t3s")
        self.ui.lineEditCulvertHeight.setText(dir + "example_08/output/culvert.xyz")
        self.ui.lineEditNS1.setText(dir + "example_08/output/NS1.i2s")
        self.ui.lineEditNS2.setText(dir + "example_08/output/NS2.i2s")
        self.ui.lineEditNS3.setText(dir + "example_08/output/NS3.i2s")
        self.ui.lineEditNS4.setText(dir + "example_08/output/NS4.i2s")
        self.ui.lineEditNS5.setText(dir + "example_08/output/NS5.i2s")
        self.ui.lineEditNS6.setText(dir + "example_08/output/NS6.i2s")
        self.ui.lineEditNS7.setText(dir + "example_08/output/NS7.i2s")
        
    def create(self):

        try:
            SMS_elements, \
                SMS_nodes,\
                SMS_strings,\
                SMS_materials,\
                SMS_bc_nodes,\
                SMS_bc_strings_1,\
                SMS_bc_strings_2,\
                SMS_bc_strings_3,\
                SMS_bc_strings_4,\
                SMS_bc_strings_5,\
                SMS_bc_strings_6,\
                SMS_bc_strings_7 = fh.read2DM(self.ui.lineEditInput.text())
        except Exception, e:
            QMessageBox.critical(self.widget, "Error", "Not able to load file!\nCheck filename or content!" + "\n\n" + str(e))
            return

        # BK_materials = {BK_node_id: strickler's value}
        BK_materials = {}
        
        # MAP_node_id = {SMS_node_id: BK_node_id}
        MAP_node_id = {}
        
        # BK_nodes = {BK_node_id: [x, y, z]}
        BK_nodes = {}        
        
        # BK_elements = {element_id: [BK_node_id, BK_node_id, BK_node_id (, BK_node_id), SMS_material_id]}
        BK_elements = {}
        
        # map BK nodes to SMS nodes
        i = 0
        for key in SMS_nodes:
            i += 1
            BK_nodes[i] = SMS_nodes[key]
            MAP_node_id[key] = i

        # convert SMS mesh to BK mesh
        i = 0
        impermeableMaterialID = self.ui.spinBoxImpermeable.value()
        material_added = False

        for key in SMS_elements:
            if len(SMS_elements[key]) == 4:
                node_0 = SMS_elements[key][0]
                node_1 = SMS_elements[key][1]
                node_2 = SMS_elements[key][2]
                material = SMS_elements[key][3]
                
                if material_added is False:
                    if material not in SMS_materials:
                        SMS_materials[material] = 0.0
                        material_added = True
                    
                BK_materials[MAP_node_id[node_0]] = SMS_materials[material]
                BK_materials[MAP_node_id[node_1]] = SMS_materials[material]
                BK_materials[MAP_node_id[node_2]] = SMS_materials[material]
                
                if self.ui.checkBoxImpermeable.isChecked():
                    if material != impermeableMaterialID:
                        i += 1
                        BK_elements[i] = [MAP_node_id[node_0], MAP_node_id[node_1], MAP_node_id[node_2]]
                else:
                    i += 1
                    BK_elements[i] = [MAP_node_id[node_0], MAP_node_id[node_1], MAP_node_id[node_2]]
                        
            elif len(SMS_elements[key]) == 5:
                node_0 = SMS_elements[key][0]
                node_1 = SMS_elements[key][1]
                node_2 = SMS_elements[key][2]
                node_3 = SMS_elements[key][3]
                material = SMS_elements[key][4]
                
                if material_added is False:
                    if material not in SMS_materials:
                        SMS_materials[material] = 0.0
                        material_added = True
                        
                BK_materials[MAP_node_id[node_0]] = SMS_materials[material]
                BK_materials[MAP_node_id[node_1]] = SMS_materials[material]
                BK_materials[MAP_node_id[node_2]] = SMS_materials[material]
                BK_materials[MAP_node_id[node_3]] = SMS_materials[material]
                
                if self.ui.checkBoxImpermeable.isChecked():
                    if material != impermeableMaterialID:
                        i += 1
                        BK_elements[i] = [MAP_node_id[node_0], MAP_node_id[node_1], MAP_node_id[node_2]]
                        i += 1
                        BK_elements[i] = [MAP_node_id[node_0], MAP_node_id[node_2], MAP_node_id[node_3]]
                else:
                    i += 1
                    BK_elements[i] = [MAP_node_id[node_0], MAP_node_id[node_1], MAP_node_id[node_2]]
                    i += 1
                    BK_elements[i] = [MAP_node_id[node_0], MAP_node_id[node_2], MAP_node_id[node_3]]
                        
        def getStrings(allstrings, strings):
            i = 1
            profiles = {}
            bk_profiles = {}
            for key in strings:
                profiles[i] = allstrings[key]
                bk_profiles[i] = []
                i += 1
            for pID in profiles:
                for nID in profiles[pID]:
                    bk_profiles[pID].append(MAP_node_id[nID])

            return bk_profiles
        
        info = ""
    
        if self.ui.checkBoxBottom.isChecked():
            try:
                fh.writeT3S(BK_nodes, BK_elements, self.ui.lineEditBottom.text())
                info += " - Bottom mesh created with {0} nodes and {1} elements.\n".format(len(BK_nodes), len(BK_elements)) 
            except:
                info += " - ERROR: Not able to write bottom mesh! \n\n + str(e)"
                info += "\n"
                info += str(sys.exc_info())
                info += "\n"

        if self.ui.lineEditInputData.text() != "":
            SMS_wsf = fh.readDAT(self.ui.lineEditInputData.text())
            BK_nodes_wsf = {}
            BK_nodes_dpth = {}
            for key in SMS_nodes:
                wsf = 0.0
                if SMS_wsf[MAP_node_id[key]] <= 0.000001:
                    wsf = SMS_nodes[key][2]
                else:
                    wsf = SMS_wsf[MAP_node_id[key]]
                BK_nodes_wsf[key] = [SMS_nodes[key][0], SMS_nodes[key][1], wsf]    
                BK_nodes_dpth[key] = [SMS_nodes[key][0], SMS_nodes[key][1], wsf-SMS_nodes[key][2]] 
            try:
                fh.writeT3S(BK_nodes_wsf, BK_elements, self.ui.lineEditWaterSurface.text())
                info += " - Water surface mesh created with {0} nodes and {1} elements.\n".format(len(BK_nodes_wsf), len(BK_elements)) 
            except:
                info += " - ERROR: Not able to write water surface mesh!\n"
                info += "\n"
                info += str(sys.exc_info())
                info += "\n"
  
            try:
                fh.writeT3S(BK_nodes_dpth, BK_elements, self.ui.lineEditWaterDepth.text())
                info += " - Water depth mesh created with {0} nodes and {1} elements.\n".format(len(BK_nodes_dpth), len(BK_elements)) 
            except:
                info += " - ERROR: Not able to write water depth mesh!\n"
                info += "\n"
                info += str(sys.exc_info())
                info += "\n"
                  
        if self.ui.checkBoxBottomFriction.isChecked():
            BK_nodes_mat = {}
            for key in BK_nodes:
                if key in BK_materials:
                    BK_nodes_mat[key] = [BK_nodes[key][0], BK_nodes[key][1], BK_materials[key]]
                else:
                    BK_nodes_mat[key] = [BK_nodes[key][0], BK_nodes[key][1], 0.0]                    
            try:
                fh.writeT3S(BK_nodes_mat, BK_elements, self.ui.lineEditBottomFriction.text())
                info += " - Bottom friction mesh created with {0} nodes and {1} elements.\n".format(len(BK_nodes_mat), len(BK_elements)) 
            except:
                info += " - ERROR: Not able to write bottom friction mesh!\n"
                info += "\n"
                info += str(sys.exc_info())
                info += "\n"

        if self.ui.checkBoxCulvertHeight.isChecked():
            # convert SMS boundary condition nodes to BK points
            BK_bcNodes = {}
            for key in SMS_bc_nodes:
                height = SMS_bc_nodes[key] - SMS_nodes[key][2]
                BK_bcNodes[key] = [SMS_nodes[key][0], SMS_nodes[key][1], height]

            try:
                fh.writeXYZ(BK_bcNodes, self.ui.lineEditCulvertHeight.text())
                info += " - Culverts created with {0} nodes.\n".format(len(BK_bcNodes))
            except:
                info += " - ERROR: Not able to write culvert nodes!\n"
                info += "\n"
                info += str(sys.exc_info())
                info += "\n"
                                                                                        
        if self.ui.checkBoxNS1.isChecked():
            profiles = getStrings(SMS_strings, SMS_bc_strings_1)
            try:
                fh.writeI2S(BK_nodes, profiles, self.ui.lineEditNS1.text())
                info += " - Node string 1 created with {0} strings.\n".format(len(profiles)) 
            except:
                info += " - ERROR: Not able to write node string 1!\n"
                info += "\n"
                info += str(sys.exc_info())
                info += "\n"
                
        if self.ui.checkBoxNS2.isChecked():
            profiles = getStrings(SMS_strings, SMS_bc_strings_2)
            try:
                fh.writeI2S(BK_nodes, profiles, self.ui.lineEditNS2.text())
                info += " - Node string 2 created with {0} strings.\n".format(len(profiles)) 
            except:
                info += " - ERROR: Not able to write node string 2!\n"      
                info += "\n"
                info += str(sys.exc_info())
                info += "\n"
                
        if self.ui.checkBoxNS3.isChecked():
            profiles = getStrings(SMS_strings, SMS_bc_strings_3)
            try:
                fh.writeI2S(BK_nodes, profiles, self.ui.lineEditNS3.text())
                info += " - Node string 3 created with {0} strings.\n".format(len(profiles)) 
            except:
                info += " - ERROR: Not able to write node string 3!\n"
                info += "\n"
                info += str(sys.exc_info())
                info += "\n"
                
        if self.ui.checkBoxNS4.isChecked():
            profiles = getStrings(SMS_strings, SMS_bc_strings_4)
            try:
                fh.writeI2S(BK_nodes, profiles, self.ui.lineEditNS4.text())
                info += " - Node string 4 created with {0} strings.\n".format(len(profiles)) 
            except:
                info += " - ERROR: Not able to write node string 4!\n"
                info += "\n"
                info += str(sys.exc_info())
                info += "\n"
                
        if self.ui.checkBoxNS5.isChecked():
            profiles = getStrings(SMS_strings, SMS_bc_strings_5)
            try:
                fh.writeI2S(BK_nodes, profiles, self.ui.lineEditNS5.text())
                info += " - Node string 5 created with {0} strings.\n".format(len(profiles)) 
            except:
                info += " - ERROR: Not able to write node string 5!\n"
                info += "\n"
                info += str(sys.exc_info())
                info += "\n"
                
        if self.ui.checkBoxNS6.isChecked():
            profiles = getStrings(SMS_strings, SMS_bc_strings_6)
            try:
                fh.writeI2S(BK_nodes, profiles, self.ui.lineEditNS6.text())
                info += " - Node string 6 created with {0} strings.\n".format(len(profiles)) 
            except:
                info += " - ERROR: Not able to write node string 6!\n"
                info += "\n"
                info += str(sys.exc_info())
                info += "\n"
                
        if self.ui.checkBoxNS7.isChecked():
            profiles = getStrings(SMS_strings, SMS_bc_strings_7)
            try:
                fh.writeI2S(BK_nodes, profiles, self.ui.lineEditNS7.text())
                info += " - Node string 7 created with {0} strings.\n".format(len(profiles)) 
            except:
                info += " - ERROR: Not able to write node string 7!\n"
                info += "\n"
                info += str(sys.exc_info())
                info += "\n"
                
        QMessageBox.information(self.widget, "Module 2DM2BK", info)

    def getOpenFileName(self, title, fileFormat, lineEdit):
        filename = QFileDialog.getOpenFileName(self.widget, title, self.directory, fileFormat)
        if filename != "":
            lineEdit.setText(filename)

    def getSaveFileName(self, title, fileFormat, lineEdit):
        filename = QFileDialog.getSaveFileName(self.widget, title, self.directory, fileFormat)
        if filename != "":
            lineEdit.setText(filename)