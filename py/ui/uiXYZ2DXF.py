# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uiXYZ2DXF.ui'
#
# Created: Fri May 27 08:57:04 2016
#      by: PyQt4 UI code generator 4.11.2
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
        self.spinBoxDecimal.setMaximumSize(QtCore.QSize(50, 16777215))
        self.spinBoxDecimal.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.spinBoxDecimal.setMaximum(12)
        self.spinBoxDecimal.setProperty("value", 3)
        self.spinBoxDecimal.setObjectName(_fromUtf8("spinBoxDecimal"))
        self.gridLayout.addWidget(self.spinBoxDecimal, 2, 2, 1, 1)
        spacerItem = QtGui.QSpacerItem(500, 227, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 3, 0, 1, 3)
        self.label_111 = QtGui.QLabel(XYZ2DXF)
        self.label_111.setIndent(18)
        self.label_111.setObjectName(_fromUtf8("label_111"))
        self.gridLayout.addWidget(self.label_111, 5, 0, 1, 1)
        self.pushButtonOutputDXF = QtGui.QPushButton(XYZ2DXF)
        self.pushButtonOutputDXF.setMinimumSize(QtCore.QSize(20, 0))
        self.pushButtonOutputDXF.setMaximumSize(QtCore.QSize(40, 16777215))
        self.pushButtonOutputDXF.setObjectName(_fromUtf8("pushButtonOutputDXF"))
        self.gridLayout.addWidget(self.pushButtonOutputDXF, 5, 1, 1, 1)
        self.lineEditOutputDXF = QtGui.QLineEdit(XYZ2DXF)
        self.lineEditOutputDXF.setObjectName(_fromUtf8("lineEditOutputDXF"))
        self.gridLayout.addWidget(self.lineEditOutputDXF, 5, 2, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(609, 255, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 6, 0, 1, 3)
        self.pushButtonCreate = QtGui.QPushButton(XYZ2DXF)
        self.pushButtonCreate.setObjectName(_fromUtf8("pushButtonCreate"))
        self.gridLayout.addWidget(self.pushButtonCreate, 7, 0, 1, 3)
        self.label_104 = QtGui.QLabel(XYZ2DXF)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setUnderline(True)
        self.label_104.setFont(font)
        self.label_104.setObjectName(_fromUtf8("label_104"))
        self.gridLayout.addWidget(self.label_104, 4, 0, 1, 3)
        self.label_106 = QtGui.QLabel(XYZ2DXF)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setUnderline(True)
        self.label_106.setFont(font)
        self.label_106.setIndent(-4)
        self.label_106.setObjectName(_fromUtf8("label_106"))
        self.gridLayout.addWidget(self.label_106, 0, 0, 1, 3)

        self.retranslateUi(XYZ2DXF)
        QtCore.QMetaObject.connectSlotsByName(XYZ2DXF)

    def retranslateUi(self, XYZ2DXF):
        XYZ2DXF.setWindowTitle(_translate("XYZ2DXF", "Form", None))
        self.label_105.setText(_translate("XYZ2DXF", "Point Set file:", None))
        self.pushButtonInputXYZ.setText(_translate("XYZ2DXF", "...", None))
        self.label_110.setText(_translate("XYZ2DXF", "Decimal places:", None))
        self.label_111.setText(_translate("XYZ2DXF", "DXF file:", None))
        self.pushButtonOutputDXF.setText(_translate("XYZ2DXF", "...", None))
        self.pushButtonCreate.setText(_translate("XYZ2DXF", "Let\'s go!", None))
        self.label_104.setText(_translate("XYZ2DXF", "Outputs:", None))
        self.label_106.setText(_translate("XYZ2DXF", "Inputs:", None))

