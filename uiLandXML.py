# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uiLandXML.ui'
#
# Created: Wed Nov 02 21:28:40 2016
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

class Ui_LandXML(object):
    def setupUi(self, LandXML):
        LandXML.setObjectName(_fromUtf8("LandXML"))
        LandXML.resize(639, 600)
        self.gridLayout = QtGui.QGridLayout(LandXML)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_11 = QtGui.QLabel(LandXML)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setUnderline(True)
        self.label_11.setFont(font)
        self.label_11.setIndent(-4)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.gridLayout.addWidget(self.label_11, 0, 0, 1, 1)
        self.label_12 = QtGui.QLabel(LandXML)
        self.label_12.setIndent(18)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.gridLayout.addWidget(self.label_12, 1, 0, 1, 1)
        self.pushButtonInputMesh = QtGui.QPushButton(LandXML)
        self.pushButtonInputMesh.setMinimumSize(QtCore.QSize(20, 0))
        self.pushButtonInputMesh.setMaximumSize(QtCore.QSize(40, 16777215))
        self.pushButtonInputMesh.setObjectName(_fromUtf8("pushButtonInputMesh"))
        self.gridLayout.addWidget(self.pushButtonInputMesh, 1, 1, 1, 1)
        self.lineEditInputMesh = QtGui.QLineEdit(LandXML)
        self.lineEditInputMesh.setObjectName(_fromUtf8("lineEditInputMesh"))
        self.gridLayout.addWidget(self.lineEditInputMesh, 1, 2, 1, 1)
        self.label_15 = QtGui.QLabel(LandXML)
        self.label_15.setIndent(18)
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.gridLayout.addWidget(self.label_15, 2, 0, 1, 1)
        self.lineEditSurfaceName = QtGui.QLineEdit(LandXML)
        self.lineEditSurfaceName.setObjectName(_fromUtf8("lineEditSurfaceName"))
        self.gridLayout.addWidget(self.lineEditSurfaceName, 2, 2, 1, 1)
        spacerItem = QtGui.QSpacerItem(458, 207, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 3, 0, 1, 3)
        self.label_13 = QtGui.QLabel(LandXML)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setUnderline(True)
        self.label_13.setFont(font)
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.gridLayout.addWidget(self.label_13, 4, 0, 1, 1)
        self.label_14 = QtGui.QLabel(LandXML)
        self.label_14.setIndent(18)
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.gridLayout.addWidget(self.label_14, 5, 0, 1, 1)
        self.pushButtonOutput = QtGui.QPushButton(LandXML)
        self.pushButtonOutput.setMinimumSize(QtCore.QSize(20, 0))
        self.pushButtonOutput.setMaximumSize(QtCore.QSize(40, 16777215))
        self.pushButtonOutput.setObjectName(_fromUtf8("pushButtonOutput"))
        self.gridLayout.addWidget(self.pushButtonOutput, 5, 1, 1, 1)
        self.lineEditOutput = QtGui.QLineEdit(LandXML)
        self.lineEditOutput.setObjectName(_fromUtf8("lineEditOutput"))
        self.gridLayout.addWidget(self.lineEditOutput, 5, 2, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(458, 206, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 6, 0, 1, 3)
        self.pushButtonCreate = QtGui.QPushButton(LandXML)
        self.pushButtonCreate.setObjectName(_fromUtf8("pushButtonCreate"))
        self.gridLayout.addWidget(self.pushButtonCreate, 7, 0, 1, 3)

        self.retranslateUi(LandXML)
        QtCore.QMetaObject.connectSlotsByName(LandXML)

    def retranslateUi(self, LandXML):
        LandXML.setWindowTitle(_translate("LandXML", "Form", None))
        self.label_11.setText(_translate("LandXML", "Inputs:", None))
        self.label_12.setText(_translate("LandXML", "2D T3 Mesh:", None))
        self.pushButtonInputMesh.setText(_translate("LandXML", "...", None))
        self.label_15.setText(_translate("LandXML", "Surface name:", None))
        self.label_13.setText(_translate("LandXML", "Outputs:", None))
        self.label_14.setText(_translate("LandXML", "LandXML file:", None))
        self.pushButtonOutput.setText(_translate("LandXML", "...", None))
        self.pushButtonCreate.setText(_translate("LandXML", "Let\'s go!", None))

