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
__date__ ="$30.10.2016 18:57:59$"

from matplotlib import colors

class Colour():
    """Handle different colour formats."""

    def __init__(self, colTxtRGB):
        """Constructor."""

        self.colTxtRGB = colTxtRGB

        self.colFloat_RGB = ()
        self.colFloat_BGR = ()
        self.colRGB = ()
        self.colBGR = ()
        self.colHEX_RGB = ()
        self.colHEX_BGR = ()

    def create(self):
        self.setRGB()
        self.setBGR()
        self.setFloatRGB()
        self.setFloatBGR()
        self.setHexRGB()
        self.setHexBGR()

    def setRGB(self):
        self.colRGB = (float(self.colTxtRGB[0]), float(self.colTxtRGB[1]), float(self.colTxtRGB[2]))

    def setBGR(self):
        self.colBGR = (float(self.colTxtRGB[2]), float(self.colTxtRGB[1]), float(self.colTxtRGB[0]))

    def setFloatRGB(self):
        self.colFloat_RGB = (float(self.colTxtRGB[0])/255.0, float(self.colTxtRGB[1])/255.0, float(self.colTxtRGB[2])/255.0)

    def setFloatBGR(self):
        self.colFloat_BGR = (float(self.colTxtRGB[2])/255.0, float(self.colTxtRGB[1])/255.0, float(self.colTxtRGB[0])/255.0)

    def setHexRGB(self):
        self.colHEX_RGB = colors.rgb2hex(self.colFloat_RGB)

    def setHexBGR(self):
        self.colHEX_BGR = colors.rgb2hex(self.colFloat_BGR)

    def getRGB(self):
        return self.colRGB

    def getBGR(self):
        return self.colBGR

    def getFloatRGB(self):
        return self.colFloat_RGB

    def getFloatBGR(self):
        return self.colFloat_BGR

    def getHexRGB(self):
        return self.colHEX_RGB

    def getHexBGR(self):
        return self.colHEX_BGR