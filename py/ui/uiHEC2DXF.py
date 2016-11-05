# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uiHEC2DXF.ui'
#
# Created: Tue May 31 17:25:40 2016
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

class Ui_HEC2DXF(object):
    def setupUi(self, HEC2DXF):
        HEC2DXF.setObjectName(_fromUtf8("HEC2DXF"))
        HEC2DXF.resize(627, 759)
        self.gridLayout = QtGui.QGridLayout(HEC2DXF)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_105 = QtGui.QLabel(HEC2DXF)
        self.label_105.setIndent(18)
        self.label_105.setObjectName(_fromUtf8("label_105"))
        self.gridLayout.addWidget(self.label_105, 1, 0, 1, 1)
        self.pushButtonInputSDF = QtGui.QPushButton(HEC2DXF)
        self.pushButtonInputSDF.setMinimumSize(QtCore.QSize(20, 0))
        self.pushButtonInputSDF.setMaximumSize(QtCore.QSize(40, 16777215))
        self.pushButtonInputSDF.setObjectName(_fromUtf8("pushButtonInputSDF"))
        self.gridLayout.addWidget(self.pushButtonInputSDF, 1, 1, 1, 1)
        self.lineEditInputSDF = QtGui.QLineEdit(HEC2DXF)
        self.lineEditInputSDF.setObjectName(_fromUtf8("lineEditInputSDF"))
        self.gridLayout.addWidget(self.lineEditInputSDF, 1, 2, 1, 1)
        spacerItem = QtGui.QSpacerItem(500, 227, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 3)
        self.label_111 = QtGui.QLabel(HEC2DXF)
        self.label_111.setIndent(18)
        self.label_111.setObjectName(_fromUtf8("label_111"))
        self.gridLayout.addWidget(self.label_111, 4, 0, 1, 1)
        self.pushButtonOutputDXF = QtGui.QPushButton(HEC2DXF)
        self.pushButtonOutputDXF.setMinimumSize(QtCore.QSize(20, 0))
        self.pushButtonOutputDXF.setMaximumSize(QtCore.QSize(40, 16777215))
        self.pushButtonOutputDXF.setObjectName(_fromUtf8("pushButtonOutputDXF"))
        self.gridLayout.addWidget(self.pushButtonOutputDXF, 4, 1, 1, 1)
        self.lineEditOutputDXF = QtGui.QLineEdit(HEC2DXF)
        self.lineEditOutputDXF.setObjectName(_fromUtf8("lineEditOutputDXF"))
        self.gridLayout.addWidget(self.lineEditOutputDXF, 4, 2, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(609, 255, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 5, 0, 1, 3)
        self.pushButtonCreate = QtGui.QPushButton(HEC2DXF)
        self.pushButtonCreate.setObjectName(_fromUtf8("pushButtonCreate"))
        self.gridLayout.addWidget(self.pushButtonCreate, 6, 0, 1, 3)
        self.label_104 = QtGui.QLabel(HEC2DXF)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setUnderline(True)
        self.label_104.setFont(font)
        self.label_104.setObjectName(_fromUtf8("label_104"))
        self.gridLayout.addWidget(self.label_104, 3, 0, 1, 3)
        self.label_106 = QtGui.QLabel(HEC2DXF)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setUnderline(True)
        self.label_106.setFont(font)
        self.label_106.setIndent(-4)
        self.label_106.setObjectName(_fromUtf8("label_106"))
        self.gridLayout.addWidget(self.label_106, 0, 0, 1, 3)

        self.retranslateUi(HEC2DXF)
        QtCore.QMetaObject.connectSlotsByName(HEC2DXF)

    def retranslateUi(self, HEC2DXF):
        HEC2DXF.setWindowTitle(_translate("HEC2DXF", "Form", None))
        self.label_105.setText(_translate("HEC2DXF", "Spatial Data Format:", None))
        self.pushButtonInputSDF.setText(_translate("HEC2DXF", "...", None))
        self.label_111.setText(_translate("HEC2DXF", "DXF file:", None))
        self.pushButtonOutputDXF.setText(_translate("HEC2DXF", "...", None))
        self.pushButtonCreate.setText(_translate("HEC2DXF", "Let\'s go!", None))
        self.label_104.setText(_translate("HEC2DXF", "Outputs:", None))
        self.label_106.setText(_translate("HEC2DXF", "Inputs:", None))

