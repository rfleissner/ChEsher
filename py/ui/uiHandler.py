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

"""Module with functins for reading and writing files."""

__author__="Reinhard Fleissner"
__date__ ="$29.08.2014 18:21:40$"

# libraries
from PyQt4.QtGui import QFileDialog

def getOpenFileName(title, fileFormat, lineEdit, directory, wid):
    filename = QFileDialog.getOpenFileName(wid, title, directory, fileFormat)
    print "uih", directory
    if filename != "":
        lineEdit.setText(filename)

def getSaveFileName(title, fileFormat, lineEdit, directory, wid):
    filename = QFileDialog.getSaveFileName(wid, title, directory, fileFormat)
    if filename != "":
        lineEdit.setText(filename)

def setEnabled(checkBox, pushButton, lineEdit):
        checked = checkBox.isChecked()
        pushButton.setEnabled(checked)
        lineEdit.setEnabled(checked)
      
def setEnabledInitialize(checkBox, pushButton, lineEdit):
    checkBox.setChecked(True)
    pushButton.setEnabled(True)
    lineEdit.setEnabled(True)
    