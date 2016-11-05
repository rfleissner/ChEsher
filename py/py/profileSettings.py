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

"""Wrapper for module XYZ2DXF"""

__author__="Reinhard Fleissner"
__date__ ="$18.05.2016 22:38:30$"

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QDialog

# modules and classes

from uiProfileSettings import Ui_ProfileSettings

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class WrapProfileSettings(QtGui.QDialog):
    """Wrapper for module XYZ2DXF"""

    def __init__(self, settings):
        """Constructor."""
        
        self._settings = settings
        self.settings = settings.copy()
       
        # setup user interface
        super(WrapProfileSettings, self).__init__()
        
        self.ui = Ui_ProfileSettings()
        self.ui.setupUi(self)
        
        self.ui.buttonBox.clicked.connect(self.handleButtonClick)
        
    def handleButtonClick(self, button):
        sb = self.ui.buttonBox.standardButton(button)
        if sb == QtGui.QDialogButtonBox.Ok:
            QDialog.accept(self)
        elif sb == QtGui.QDialogButtonBox.Cancel:
            QDialog.close(self)
        elif sb == QtGui.QDialogButtonBox.Reset:
            self.resetSettings()

    def accept(self):
        QDialog.accept(self)
    
    def getSettings(self):
        
        self.settings["Frame"] = self.ui.checkBoxFrame.isChecked()
        self.settings["Band"] = self.ui.checkBoxBand.isChecked()
        self.settings["ProfileName"] = self.ui.lineEditInputProfileName.text()
        self.settings["ReachStation"] = self.ui.lineEditInputReachStation.text()
        self.settings["ScaleFactor"] = self.ui.lineEditInputScaleFactor.text()
        self.settings["ReferenceLevel"] = self.ui.lineEditInputReferenceLevel.text()
        self.settings["BandTitleStationing"] = self.ui.lineEditInputBandTitleStationing.text()
        self.settings["BandTitleElevation"] = self.ui.lineEditInputBandTitleElevation.text()
        self.settings["DecimalPlaces"] = self.ui.spinBoxDecimal.value()
        self.settings["doubleSpinBoxOffsetX"] = self.ui.doubleSpinBoxOffsetX.value()
        self.settings["doubleSpinBoxOffsetZ"] = self.ui.doubleSpinBoxOffsetZ.value()
        self.settings["doubleSpinBoxBandHeight"] = self.ui.doubleSpinBoxBandHeight.value()
        self.settings["doubleSpinBoxTextSizeBandTitle"] = self.ui.doubleSpinBoxTextSizeBandTitle.value()
        self.settings["doubleSpinBoxTextSizeBand"] = self.ui.doubleSpinBoxTextSizeBand.value()
        self.settings["doubleSpinBoxMarkerSize"] = self.ui.doubleSpinBoxMarkerSize.value()
        self.settings["doubleSpinBoxCleanValues"] = self.ui.doubleSpinBoxCleanValues.value()

        return self.settings
    
    def setSettings(self):
        
        self.ui.checkBoxFrame.setChecked(self.settings["Frame"])
        self.ui.checkBoxBand.setChecked(self.settings["Band"])
        self.ui.lineEditInputProfileName.setText(self.settings["ProfileName"])
        self.ui.lineEditInputReachStation.setText(self.settings["ReachStation"])
        self.ui.lineEditInputScaleFactor.setText(self.settings["ScaleFactor"])
        self.ui.lineEditInputReferenceLevel.setText(self.settings["ReferenceLevel"])
        self.ui.lineEditInputBandTitleStationing.setText(self.settings["BandTitleStationing"])
        self.ui.lineEditInputBandTitleElevation.setText(self.settings["BandTitleElevation"])
        self.ui.spinBoxDecimal.setValue(self.settings["DecimalPlaces"])
        self.ui.doubleSpinBoxOffsetX.setValue(self.settings["doubleSpinBoxOffsetX"])
        self.ui.doubleSpinBoxOffsetZ.setValue(self.settings["doubleSpinBoxOffsetZ"])
        self.ui.doubleSpinBoxBandHeight.setValue(self.settings["doubleSpinBoxBandHeight"])
        self.ui.doubleSpinBoxTextSizeBandTitle.setValue(self.settings["doubleSpinBoxTextSizeBandTitle"])
        self.ui.doubleSpinBoxTextSizeBand.setValue(self.settings["doubleSpinBoxTextSizeBand"])
        self.ui.doubleSpinBoxMarkerSize.setValue(self.settings["doubleSpinBoxMarkerSize"])
        self.ui.doubleSpinBoxCleanValues.setValue(self.settings["doubleSpinBoxCleanValues"])
        
    def resetSettings(self):
        
        self.ui.checkBoxFrame.setChecked(self._settings["Frame"])
        self.ui.checkBoxBand.setChecked(self._settings["Band"])
        self.ui.lineEditInputProfileName.setText(self._settings["ProfileName"])
        self.ui.lineEditInputReachStation.setText(self._settings["ReachStation"])
        self.ui.lineEditInputScaleFactor.setText(self._settings["ScaleFactor"])
        self.ui.lineEditInputReferenceLevel.setText(self._settings["ReferenceLevel"])
        self.ui.lineEditInputBandTitleStationing.setText(self._settings["BandTitleStationing"])
        self.ui.lineEditInputBandTitleElevation.setText(self._settings["BandTitleElevation"])
        self.ui.spinBoxDecimal.setValue(self._settings["DecimalPlaces"])
        self.ui.doubleSpinBoxOffsetX.setValue(self._settings["doubleSpinBoxOffsetX"])
        self.ui.doubleSpinBoxOffsetZ.setValue(self._settings["doubleSpinBoxOffsetZ"])
        self.ui.doubleSpinBoxBandHeight.setValue(self._settings["doubleSpinBoxBandHeight"])
        self.ui.doubleSpinBoxTextSizeBandTitle.setValue(self._settings["doubleSpinBoxTextSizeBandTitle"])
        self.ui.doubleSpinBoxTextSizeBand.setValue(self._settings["doubleSpinBoxTextSizeBand"])
        self.ui.doubleSpinBoxMarkerSize.setValue(self._settings["doubleSpinBoxMarkerSize"])
        self.ui.doubleSpinBoxCleanValues.setValue(self._settings["doubleSpinBoxCleanValues"])