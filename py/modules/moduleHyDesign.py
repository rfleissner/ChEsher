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

"""Wrapper for module HyDesign"""

__author__="Reinhard Fleissner"
__date__ ="$18.05.2016 22:38:30$"

import math
from PyQt4 import QtCore, QtGui

from uiHyDesign import Ui_HyDesign

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class WrapHyDesign():
    """Wrapper for legend in result subwindow"""

    def __init__(self):
        """Constructor."""
        
        # setup user interface
        self.widget = QtGui.QWidget()
        self.ui = Ui_HyDesign()
        self.ui.setupUi(self.widget)
        # module HyDesign
        
        self.XSData = {
        "Type": 0,
        "Slope": 1.0,
        "Roughness": 24.0,
        "Discharge": "",
        "RectWidth": 10.0,
        "RectHeight": 1.0,
        "TrapWidth": 10.0,
        "TrapHeight": 1.0,
        "TrapLeftSl": 1.0,
        "TrapRightSl": 1.0,
        "TriaHeight": 1.0,
        "TriaLeftSl": 1.0,
        "TriaRightSl": 1.0,
        "CircWidth": 5.0,
        "CircRadius": 10.0,
        "ParaWidth": 10.0,
        "ParaHeight": 2.0
        } 
        
        self.ui.comboBoxTypeXSection.clear()
        self.ui.comboBoxTypeXSection.addItem("Rectangle")
        self.ui.comboBoxTypeXSection.addItem("Trapezoid")
        self.ui.comboBoxTypeXSection.addItem("Triangle")
        self.ui.comboBoxTypeXSection.addItem("Circle")
        self.ui.comboBoxTypeXSection.addItem("Parabola")

        self.ui.comboBoxTypeXSection.setCurrentIndex(self.XSData["Type"])
        self.setType()
        
        # connections combo box
        self.ui.comboBoxTypeXSection.activated.connect(self.setType)

        # connections double spin box maximum discharge
        self.ui.doubleSpinBoxStrickler.valueChanged.connect(self.calcDischarge)
        self.ui.doubleSpinBoxSlope.valueChanged.connect(self.calcDischarge)

        # connections double spin box rectangle
        self.ui.doubleSpinBoxRectWidth.valueChanged.connect(self.calcRect)
        self.ui.doubleSpinBoxRectHeight.valueChanged.connect(self.calcRect)

        # connections double spin box trapezoid
        self.ui.doubleSpinBoxTrapWidth.valueChanged.connect(self.calcTrap)
        self.ui.doubleSpinBoxTrapHeight.valueChanged.connect(self.calcTrap)
        self.ui.doubleSpinBoxTrapLeftSl.valueChanged.connect(self.calcTrap)
        self.ui.doubleSpinBoxTrapRightSl.valueChanged.connect(self.calcTrap)

        # connections double spin box triangle
        self.ui.doubleSpinBoxTriaHeight.valueChanged.connect(self.calcTria)
        self.ui.doubleSpinBoxTriaLeftSl.valueChanged.connect(self.calcTria)
        self.ui.doubleSpinBoxTriaRightSl.valueChanged.connect(self.calcTria)

        # connections double spin box circle
        self.ui.doubleSpinBoxCircWidth.valueChanged.connect(self.calcCirc)
        self.ui.doubleSpinBoxCircRadius.valueChanged.connect(self.calcCirc)

        # connections double spin box barabola
        self.ui.doubleSpinBoxParaWidth.valueChanged.connect(self.calcPara)
        self.ui.doubleSpinBoxParaHeight.valueChanged.connect(self.calcPara)

        self.calcDischarge()
    
    def updateQ(self, Q):
        
        self.ui.labelDischarge.setText("%.3f %s" % (round(Q, 3), " m\xb3/s"))
    
    def calcRect(self):
        w = self.ui.doubleSpinBoxRectWidth.value()
        h = self.ui.doubleSpinBoxRectHeight.value()

        J= self.ui.doubleSpinBoxSlope.value()/100.0
        kst = self.ui.doubleSpinBoxStrickler.value()

        A = w*h
        U = w+2*h
        if U>0:
            R = A/U
        else:
            R = 0
        Q = kst * math.pow(R, 2.0/3.0) * math.pow(J, 1.0/2.0)*A
        
        self.updateQ(Q)
        self.drawXSection()
    
    def calcTrap(self):

        w = self.ui.doubleSpinBoxTrapWidth.value()
        h = self.ui.doubleSpinBoxTrapHeight.value()
        sl = self.ui.doubleSpinBoxTrapLeftSl.value()
        sr = self.ui.doubleSpinBoxTrapRightSl.value()

        e = h/sl
        f = h/sr
        A = 0
        U = 0
        
        if w - e - f <= 0:
            a = w / (1/sl + 1/sr)
            m = a/sl
            n = a/sr
            A = w/2*a
            U = math.sqrt(pow(a, 2)+pow(m, 2)) + math.sqrt(pow(a, 2)+pow(n, 2))
        else:
            c = w-e-f
            A = (w+c)/2*h
            U = math.sqrt(pow(h, 2)+pow(e, 2)) + math.sqrt(pow(h, 2)+pow(f, 2)) + c

        J= self.ui.doubleSpinBoxSlope.value()/100.0
        kst = self.ui.doubleSpinBoxStrickler.value()

        if U>0:
            R = A/U
        else:
            R = 0
        Q = kst * math.pow(R, 2.0/3.0) * math.pow(J, 1.0/2.0)*A

        self.updateQ(Q)
        self.drawXSection()

    def calcTria(self):

        h = self.ui.doubleSpinBoxTriaHeight.value()
        sl = self.ui.doubleSpinBoxTriaLeftSl.value()
        sr = self.ui.doubleSpinBoxTriaRightSl.value()
        
        w = h/sl + h/sr

        J= self.ui.doubleSpinBoxSlope.value()/100.0
        kst = self.ui.doubleSpinBoxStrickler.value()

        e = h/sl
        f = h/sr

        A = (e+f)/2*h
        U = math.sqrt(pow(h, 2)+pow(e, 2)) + math.sqrt(pow(h, 2)+pow(f, 2))
        if U>0:
            R = A/U
        else:
            R = 0
        Q = kst * math.pow(R, 2.0/3.0) * math.pow(J, 1.0/2.0)*A

        self.updateQ(Q)
        self.drawXSection()

    def calcCirc(self):

        w = self.ui.doubleSpinBoxCircWidth.value()
        r = self.ui.doubleSpinBoxCircRadius.value()

        if w >= 2*r:
            r = w/2
            self.ui.doubleSpinBoxCircRadius.setValue(r)

        a = 0
        if r > 0:
            a = 2*math.asin(w/2/r)

        J= self.ui.doubleSpinBoxSlope.value()/100.0
        kst = self.ui.doubleSpinBoxStrickler.value()

        A = math.pow(r, 2)/2*(a-math.sin(a))
        U = r*a
        if U>0:
            R = A/U
        else:
            R = 0
        Q = kst * math.pow(R, 2.0/3.0) * math.pow(J, 1.0/2.0)*A

        self.updateQ(Q)
        self.drawXSection()

    def calcPara(self):

        w = self.ui.doubleSpinBoxParaWidth.value()
        h = self.ui.doubleSpinBoxParaHeight.value()

        J= self.ui.doubleSpinBoxSlope.value()/100.0
        kst = self.ui.doubleSpinBoxStrickler.value()

        A = 0
        U = 0
        if h > 0:
            A = 2.0/3.0*w/math.sqrt(h)*math.pow(h, 3.0/2.0)
            U = 2*((8*math.pow(h, 2)*math.sqrt(math.pow(w,2)/math.pow(h,2)+16)+math.pow(w,2)*math.log(8*math.pow(h,2)*(math.sqrt(math.pow(w,2)/math.pow(h,2)+16)+4)+math.pow(w,2)))/(32*h)-math.pow(w,2)*math.log(math.pow(w,2))/(32*h))
        else:
            A = 0
            U = 0

        if U>0:
            R = A/U
        else:
            R = 0
        Q = kst * math.pow(R, 2.0/3.0) * math.pow(J, 1.0/2.0)*A
        
        self.updateQ(Q)
        self.drawXSection()

    def calcDischarge(self):
        type = self.ui.comboBoxTypeXSection.currentIndex()
        self.ui.stackedWidgetType.setCurrentIndex(type)
        if type == 0:
            self.calcRect()
        elif type == 1:
            self.calcTrap()
        elif type == 2:
            self.calcTria()
        elif type == 3:
            self.calcCirc()
        elif type == 4:
            self.calcPara()
        
    def updateUi(self):
        
        self.updateUiRect()
        self.updateUiTrap()
        self.updateUiTria()
        self.updateUiCirc()
        self.updateUiPara()
        self.ui.labelDischarge.setText(self.XSData["Discharge"])

    def setType(self):
        self.calcDischarge()
        self.updateUi()
        
    def checkRectangle(self):
        w = self.ui.doubleSpinBoxRectWidth.value()
        h = self.ui.doubleSpinBoxRectHeight.value()

        if w == 0.0:
            QMessageBox.warning(self, "Eingabefehler", \
                "Ungueltige Breite!")
            return
        elif h == 0.0:
            QMessageBox.warning(self, "Eingabefehler", \
                "Ungueltige Hoehe!")
            return
        else:
            self.XSData["Type"] = 0
            self.XSData["RectWidth"] = w
            self.XSData["RectHeight"] = h

    def checkTrapezoid(self):
        w = self.ui.doubleSpinBoxTrapWidth.value()
        h = self.ui.doubleSpinBoxTrapHeight.value()
        sl = self.ui.doubleSpinBoxTrapLeftSl.value()
        sr = self.ui.doubleSpinBoxTrapRightSl.value()

        if w == 0.0:
            QMessageBox.warning(self, "Eingabefehler", \
                "Ungueltige Breite!")
            return
        elif h == 0.0:
            QMessageBox.warning(self, "Eingabefehler", \
                "Ungueltige Hoehe!")
            return
        else:
            self.XSData["Type"] = 1
            self.XSData["TrapWidth"] = w
            self.XSData["TrapHeight"] = h
            self.XSData["TrapLeftSl"] = sl
            self.XSData["TrapRightSl"] = sr

    def checkTriangle(self):
        h = self.ui.doubleSpinBoxTriaHeight.value()
        sl = self.ui.doubleSpinBoxTriaLeftSl.value()
        sr = self.ui.doubleSpinBoxTriaRightSl.value()

        if h == 0.0:
            QMessageBox.warning(self, "Eingabefehler", \
                "Ungueltige Hoehe!")
            return
        else:
            self.XSData["Type"] = 2
            self.XSData["TriaHeight"] = h
            self.XSData["TriaLeftSl"] = sl
            self.XSData["TriaRightSl"] = sr

    def checkCircle(self):
        w = self.ui.doubleSpinBoxCircWidth.value()
        r = self.ui.doubleSpinBoxCircRadius.value()
        N = self.ui.doubleSpinBoxCircVert.value()

        if w == 0.0:
            QMessageBox.warning(self, "Eingabefehler", \
                "Ungueltige Breite!")
            return
        elif r == 0.0:
            QMessageBox.warning(self, "Eingabefehler", \
                "Ungueltiger Radius!")
            return
        else:
            self.XSData["Type"] = 3
            self.XSData["CircWidth"] = w
            self.XSData["CircRadius"] = r
            self.XSData["CircVert"] = N

    def checkParabola(self):
        w = self.ui.doubleSpinBoxParaWidth.value()
        h = self.ui.doubleSpinBoxParaHeight.value()
        N = self.ui.doubleSpinBoxParaVert.value()

        if w == 0.0:
            QMessageBox.warning(self, "Eingabefehler", \
                "Ungueltige Breite!")
            return
        elif h == 0.0:
            QMessageBox.warning(self, "Eingabefehler", \
                "Ungueltige Hoehe!")
            return
        else:
            self.XSData["Type"] = 4
            self.XSData["ParaWidth"] = w
            self.XSData["ParaHeight"] = h
            self.XSData["ParaVert"] = N

    def getXSData(self):
        return self.XSData, self.xList, self.zList

    def updateUiRect(self):
        self.ui.doubleSpinBoxRectWidth.setValue(self.XSData["RectWidth"])
        self.ui.doubleSpinBoxRectHeight.setValue(self.XSData["RectHeight"])

    def updateUiTrap(self):
        self.ui.doubleSpinBoxTrapWidth.setValue(self.XSData["TrapWidth"])
        self.ui.doubleSpinBoxTrapHeight.setValue(self.XSData["TrapHeight"])
        self.ui.doubleSpinBoxTrapLeftSl.setValue(self.XSData["TrapLeftSl"])
        self.ui.doubleSpinBoxTrapRightSl.setValue(self.XSData["TrapRightSl"])

    def updateUiTria(self):
        self.ui.doubleSpinBoxTriaHeight.setValue(self.XSData["TriaHeight"])
        self.ui.doubleSpinBoxTriaLeftSl.setValue(self.XSData["TriaLeftSl"])
        self.ui.doubleSpinBoxTriaRightSl.setValue(self.XSData["TriaRightSl"])

    def updateUiCirc(self):
        self.ui.doubleSpinBoxCircWidth.setValue(self.XSData["CircWidth"])
        self.ui.doubleSpinBoxCircRadius.setValue(self.XSData["CircRadius"])

    def updateUiPara(self):
        self.ui.doubleSpinBoxParaWidth.setValue(self.XSData["ParaWidth"])
        self.ui.doubleSpinBoxParaHeight.setValue(self.XSData["ParaHeight"])

    def drawXSection(self):
        pass