# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uixyz2dxf.ui'
#
# Created: Sun Mar 26 00:09:00 2017
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_XYZ2DXF(object):
    def setupUi(self, XYZ2DXF):
        XYZ2DXF.setObjectName(_fromUtf8("XYZ2DXF"))
        XYZ2DXF.resize(627, 759)
        self.gridLayout = QtGui.QGridLayout(XYZ2DXF)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_106 = QtGui.QLabel(XYZ2DXF)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setUnderline(True)
        self.label_106.setFont(font)
        self.label_106.setIndent(-4)
        self.label_106.setObjectName(_fromUtf8("label_106"))
        self.gridLayout.addWidget(self.label_106, 0, 0, 1, 1)
        self.label_105 = QtGui.QLabel(XYZ2DXF)
        self.label_105.setIndent(18)
        self.label_105.setObjectName(_fromUtf8("label_105"))
        self.gridLayout.addWidget(self.label_105, 1, 0, 1, 1)
        self.pushButtonInputXYZ = QtGui.QPushButton(XYZ2DXF)
        self.pushButtonInputXYZ.setMinimumSize(QtCore.QSize(20, 0))
        self.pushButtonInputXYZ.setMaximumSize(QtCore.QSize(40, 16777215))
        self.pushButtonInputXYZ.setObjectName(_fromUtf8("pushButtonInputXYZ"))
        self.gridLayout.addWidget(self.pushButtonInputXYZ, 1, 1, 1, 1)
        self.lineEditInputXYZ = QtGui.QLineEdit(XYZ2DXF)
        self.lineEditInputXYZ.setObjectName(_fromUtf8("lineEditInputXYZ"))
        self.gridLayout.addWidget(self.lineEditInputXYZ, 1, 2, 1, 1)
        self.label_110 = QtGui.QLabel(XYZ2DXF)
        self.label_110.setIndent(18)
        self.label_110.setObjectName(_fromUtf8("label_110"))
        self.gridLayout.addWidget(self.label_110, 2, 0, 1, 1)
        self.spinBoxDecimal = QtGui.QSpinBox(XYZ2DXF)
        self.spinBoxDecimal.setMaximumSize(QtCore.QSize(80, 16777215))
        self.spinBoxDecimal.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.spinBoxDecimal.setMaximum(12)
        self.spinBoxDecimal.setProperty("value", 2)
        self.spinBoxDecimal.setObjectName(_fromUtf8("spinBoxDecimal"))
        self.gridLayout.addWidget(self.spinBoxDecimal, 2, 2, 1, 1)
        self.label_32 = QtGui.QLabel(XYZ2DXF)
        self.label_32.setIndent(18)
        self.label_32.setObjectName(_fromUtf8("label_32"))
        self.gridLayout.addWidget(self.label_32, 3, 0, 1, 1)
        self.spinBoxScale = QtGui.QSpinBox(XYZ2DXF)
        self.spinBoxScale.setMaximumSize(QtCore.QSize(80, 16777215))
        self.spinBoxScale.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.spinBoxScale.setMaximum(9999999)
        self.spinBoxScale.setProperty("value", 100)
        self.spinBoxScale.setObjectName(_fromUtf8("spinBoxScale"))
        self.gridLayout.addWidget(self.spinBoxScale, 3, 2, 1, 1)
        self.label_33 = QtGui.QLabel(XYZ2DXF)
        self.label_33.setIndent(18)
        self.label_33.setObjectName(_fromUtf8("label_33"))
        self.gridLayout.addWidget(self.label_33, 4, 0, 1, 1)
        self.radioButtonCircle = QtGui.QRadioButton(XYZ2DXF)
        self.radioButtonCircle.setChecked(True)
        self.radioButtonCircle.setObjectName(_fromUtf8("radioButtonCircle"))
        self.gridLayout.addWidget(self.radioButtonCircle, 4, 2, 1, 1)
        self.radioButtonCross = QtGui.QRadioButton(XYZ2DXF)
        self.radioButtonCross.setObjectName(_fromUtf8("radioButtonCross"))
        self.gridLayout.addWidget(self.radioButtonCross, 5, 2, 1, 1)
        self.radioButtonCrosshairs = QtGui.QRadioButton(XYZ2DXF)
        self.radioButtonCrosshairs.setObjectName(_fromUtf8("radioButtonCrosshairs"))
        self.gridLayout.addWidget(self.radioButtonCrosshairs, 6, 2, 1, 1)
        self.radioButtonNone = QtGui.QRadioButton(XYZ2DXF)
        self.radioButtonNone.setObjectName(_fromUtf8("radioButtonNone"))
        self.gridLayout.addWidget(self.radioButtonNone, 7, 2, 1, 1)
        self.label_107 = QtGui.QLabel(XYZ2DXF)
        self.label_107.setIndent(18)
        self.label_107.setObjectName(_fromUtf8("label_107"))
        self.gridLayout.addWidget(self.label_107, 8, 0, 1, 1)
        self.lineEditInputBlockName = QtGui.QLineEdit(XYZ2DXF)
        self.lineEditInputBlockName.setMaximumSize(QtCore.QSize(100, 16777215))
        self.lineEditInputBlockName.setObjectName(_fromUtf8("lineEditInputBlockName"))
        self.gridLayout.addWidget(self.lineEditInputBlockName, 8, 2, 1, 1)
        self.label_108 = QtGui.QLabel(XYZ2DXF)
        self.label_108.setIndent(18)
        self.label_108.setObjectName(_fromUtf8("label_108"))
        self.gridLayout.addWidget(self.label_108, 9, 0, 1, 1)
        self.lineEditInputAttributeName = QtGui.QLineEdit(XYZ2DXF)
        self.lineEditInputAttributeName.setMaximumSize(QtCore.QSize(100, 16777215))
        self.lineEditInputAttributeName.setObjectName(_fromUtf8("lineEditInputAttributeName"))
        self.gridLayout.addWidget(self.lineEditInputAttributeName, 9, 2, 1, 1)
        self.label_34 = QtGui.QLabel(XYZ2DXF)
        self.label_34.setIndent(18)
        self.label_34.setObjectName(_fromUtf8("label_34"))
        self.gridLayout.addWidget(self.label_34, 10, 0, 1, 1)
        self.pushButtonSymbolColour = QtGui.QPushButton(XYZ2DXF)
        self.pushButtonSymbolColour.setMinimumSize(QtCore.QSize(20, 0))
        self.pushButtonSymbolColour.setMaximumSize(QtCore.QSize(40, 16777215))
        self.pushButtonSymbolColour.setObjectName(_fromUtf8("pushButtonSymbolColour"))
        self.gridLayout.addWidget(self.pushButtonSymbolColour, 10, 1, 1, 1)
        self.labelSymbolColour = QtGui.QLabel(XYZ2DXF)
        self.labelSymbolColour.setMaximumSize(QtCore.QSize(100, 16777215))
        self.labelSymbolColour.setAutoFillBackground(True)
        self.labelSymbolColour.setAlignment(QtCore.Qt.AlignCenter)
        self.labelSymbolColour.setObjectName(_fromUtf8("labelSymbolColour"))
        self.gridLayout.addWidget(self.labelSymbolColour, 10, 2, 1, 1)
        self.label_35 = QtGui.QLabel(XYZ2DXF)
        self.label_35.setIndent(18)
        self.label_35.setObjectName(_fromUtf8("label_35"))
        self.gridLayout.addWidget(self.label_35, 11, 0, 1, 1)
        self.pushButtonTextColour = QtGui.QPushButton(XYZ2DXF)
        self.pushButtonTextColour.setMinimumSize(QtCore.QSize(20, 0))
        self.pushButtonTextColour.setMaximumSize(QtCore.QSize(40, 16777215))
        self.pushButtonTextColour.setObjectName(_fromUtf8("pushButtonTextColour"))
        self.gridLayout.addWidget(self.pushButtonTextColour, 11, 1, 1, 1)
        self.labelTextColour = QtGui.QLabel(XYZ2DXF)
        self.labelTextColour.setMaximumSize(QtCore.QSize(100, 16777215))
        self.labelTextColour.setAutoFillBackground(True)
        self.labelTextColour.setAlignment(QtCore.Qt.AlignCenter)
        self.labelTextColour.setObjectName(_fromUtf8("labelTextColour"))
        self.gridLayout.addWidget(self.labelTextColour, 11, 2, 1, 1)
        spacerItem = QtGui.QSpacerItem(500, 227, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 12, 0, 1, 3)
        self.label_104 = QtGui.QLabel(XYZ2DXF)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setUnderline(True)
        self.label_104.setFont(font)
        self.label_104.setObjectName(_fromUtf8("label_104"))
        self.gridLayout.addWidget(self.label_104, 13, 0, 1, 1)
        self.label_111 = QtGui.QLabel(XYZ2DXF)
        self.label_111.setIndent(18)
        self.label_111.setObjectName(_fromUtf8("label_111"))
        self.gridLayout.addWidget(self.label_111, 14, 0, 1, 1)
        self.pushButtonOutputDXF = QtGui.QPushButton(XYZ2DXF)
        self.pushButtonOutputDXF.setMinimumSize(QtCore.QSize(20, 0))
        self.pushButtonOutputDXF.setMaximumSize(QtCore.QSize(40, 16777215))
        self.pushButtonOutputDXF.setObjectName(_fromUtf8("pushButtonOutputDXF"))
        self.gridLayout.addWidget(self.pushButtonOutputDXF, 14, 1, 1, 1)
        self.lineEditOutputDXF = QtGui.QLineEdit(XYZ2DXF)
        self.lineEditOutputDXF.setObjectName(_fromUtf8("lineEditOutputDXF"))
        self.gridLayout.addWidget(self.lineEditOutputDXF, 14, 2, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(609, 255, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 15, 0, 1, 3)
        self.pushButtonCreate = QtGui.QPushButton(XYZ2DXF)
        self.pushButtonCreate.setObjectName(_fromUtf8("pushButtonCreate"))
        self.gridLayout.addWidget(self.pushButtonCreate, 16, 0, 1, 3)

        self.retranslateUi(XYZ2DXF)
        QtCore.QMetaObject.connectSlotsByName(XYZ2DXF)

    def retranslateUi(self, XYZ2DXF):
        XYZ2DXF.setWindowTitle(_translate("XYZ2DXF", "Form", None))
        self.label_106.setText(_translate("XYZ2DXF", "Inputs:", None))
        self.label_105.setText(_translate("XYZ2DXF", "Point Set file:", None))
        self.pushButtonInputXYZ.setText(_translate("XYZ2DXF", "...", None))
        self.label_110.setText(_translate("XYZ2DXF", "Decimal places:", None))
        self.label_32.setText(_translate("XYZ2DXF", "Scale factor:", None))
        self.label_33.setText(_translate("XYZ2DXF", "Symbol:", None))
        self.radioButtonCircle.setText(_translate("XYZ2DXF", "Circle", None))
        self.radioButtonCross.setText(_translate("XYZ2DXF", "Cross", None))
        self.radioButtonCrosshairs.setText(_translate("XYZ2DXF", "Crosshairs", None))
        self.radioButtonNone.setText(_translate("XYZ2DXF", "None", None))
        self.label_107.setText(_translate("XYZ2DXF", "Block name:", None))
        self.lineEditInputBlockName.setText(_translate("XYZ2DXF", "Point", None))
        self.label_108.setText(_translate("XYZ2DXF", "Attribute name:", None))
        self.lineEditInputAttributeName.setText(_translate("XYZ2DXF", "H", None))
        self.label_34.setText(_translate("XYZ2DXF", "Symbol colour:", None))
        self.pushButtonSymbolColour.setText(_translate("XYZ2DXF", "...", None))
        self.labelSymbolColour.setText(_translate("XYZ2DXF", "0, 0, 0", None))
        self.label_35.setText(_translate("XYZ2DXF", "Text colour:", None))
        self.pushButtonTextColour.setText(_translate("XYZ2DXF", "...", None))
        self.labelTextColour.setText(_translate("XYZ2DXF", "0, 0, 0", None))
        self.label_104.setText(_translate("XYZ2DXF", "Outputs:", None))
        self.label_111.setText(_translate("XYZ2DXF", "DXF file:", None))
        self.pushButtonOutputDXF.setText(_translate("XYZ2DXF", "...", None))
        self.pushButtonCreate.setText(_translate("XYZ2DXF", "Let\'s go!", None))

