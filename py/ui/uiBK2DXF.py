# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uiBK2DXF.ui'
#
# Created: Tue Nov 01 21:50:51 2016
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

class Ui_BK2DXF(object):
    def setupUi(self, BK2DXF):
        BK2DXF.setObjectName(_fromUtf8("BK2DXF"))
        BK2DXF.resize(639, 600)
        self.gridLayout = QtGui.QGridLayout(BK2DXF)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_55 = QtGui.QLabel(BK2DXF)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setUnderline(True)
        self.label_55.setFont(font)
        self.label_55.setIndent(-4)
        self.label_55.setObjectName(_fromUtf8("label_55"))
        self.gridLayout.addWidget(self.label_55, 0, 0, 1, 1)
        self.label_56 = QtGui.QLabel(BK2DXF)
        self.label_56.setIndent(18)
        self.label_56.setObjectName(_fromUtf8("label_56"))
        self.gridLayout.addWidget(self.label_56, 1, 0, 1, 1)
        self.pushButtonInputMesh = QtGui.QPushButton(BK2DXF)
        self.pushButtonInputMesh.setMinimumSize(QtCore.QSize(20, 0))
        self.pushButtonInputMesh.setMaximumSize(QtCore.QSize(40, 16777215))
        self.pushButtonInputMesh.setObjectName(_fromUtf8("pushButtonInputMesh"))
        self.gridLayout.addWidget(self.pushButtonInputMesh, 1, 1, 1, 1)
        self.lineEditInputMesh = QtGui.QLineEdit(BK2DXF)
        self.lineEditInputMesh.setObjectName(_fromUtf8("lineEditInputMesh"))
        self.gridLayout.addWidget(self.lineEditInputMesh, 1, 2, 1, 1)
        self.label_52 = QtGui.QLabel(BK2DXF)
        self.label_52.setIndent(18)
        self.label_52.setObjectName(_fromUtf8("label_52"))
        self.gridLayout.addWidget(self.label_52, 2, 0, 1, 1)
        self.pushButtonInputLineSet = QtGui.QPushButton(BK2DXF)
        self.pushButtonInputLineSet.setMinimumSize(QtCore.QSize(20, 0))
        self.pushButtonInputLineSet.setMaximumSize(QtCore.QSize(40, 16777215))
        self.pushButtonInputLineSet.setObjectName(_fromUtf8("pushButtonInputLineSet"))
        self.gridLayout.addWidget(self.pushButtonInputLineSet, 2, 1, 1, 1)
        self.lineEditInputLineSet = QtGui.QLineEdit(BK2DXF)
        self.lineEditInputLineSet.setObjectName(_fromUtf8("lineEditInputLineSet"))
        self.gridLayout.addWidget(self.lineEditInputLineSet, 2, 2, 1, 1)
        self.label_54 = QtGui.QLabel(BK2DXF)
        self.label_54.setIndent(18)
        self.label_54.setObjectName(_fromUtf8("label_54"))
        self.gridLayout.addWidget(self.label_54, 3, 0, 1, 2)
        self.radioButton3DFace = QtGui.QRadioButton(BK2DXF)
        self.radioButton3DFace.setChecked(True)
        self.radioButton3DFace.setObjectName(_fromUtf8("radioButton3DFace"))
        self.gridLayout.addWidget(self.radioButton3DFace, 3, 2, 1, 1)
        self.radioButtonPolyline = QtGui.QRadioButton(BK2DXF)
        self.radioButtonPolyline.setObjectName(_fromUtf8("radioButtonPolyline"))
        self.gridLayout.addWidget(self.radioButtonPolyline, 4, 2, 1, 1)
        self.label_53 = QtGui.QLabel(BK2DXF)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setUnderline(True)
        self.label_53.setFont(font)
        self.label_53.setObjectName(_fromUtf8("label_53"))
        self.gridLayout.addWidget(self.label_53, 6, 0, 1, 1)
        self.checkBoxOutputMesh = QtGui.QCheckBox(BK2DXF)
        self.checkBoxOutputMesh.setObjectName(_fromUtf8("checkBoxOutputMesh"))
        self.gridLayout.addWidget(self.checkBoxOutputMesh, 7, 0, 1, 1)
        self.pushButtonOutputMesh = QtGui.QPushButton(BK2DXF)
        self.pushButtonOutputMesh.setEnabled(False)
        self.pushButtonOutputMesh.setMinimumSize(QtCore.QSize(20, 0))
        self.pushButtonOutputMesh.setMaximumSize(QtCore.QSize(40, 16777215))
        self.pushButtonOutputMesh.setObjectName(_fromUtf8("pushButtonOutputMesh"))
        self.gridLayout.addWidget(self.pushButtonOutputMesh, 7, 1, 1, 1)
        self.lineEditOutputMesh = QtGui.QLineEdit(BK2DXF)
        self.lineEditOutputMesh.setEnabled(False)
        self.lineEditOutputMesh.setObjectName(_fromUtf8("lineEditOutputMesh"))
        self.gridLayout.addWidget(self.lineEditOutputMesh, 7, 2, 1, 1)
        self.checkBoxOutputLineSet = QtGui.QCheckBox(BK2DXF)
        self.checkBoxOutputLineSet.setObjectName(_fromUtf8("checkBoxOutputLineSet"))
        self.gridLayout.addWidget(self.checkBoxOutputLineSet, 8, 0, 1, 1)
        self.pushButtonOutputLineSet = QtGui.QPushButton(BK2DXF)
        self.pushButtonOutputLineSet.setEnabled(False)
        self.pushButtonOutputLineSet.setMinimumSize(QtCore.QSize(20, 0))
        self.pushButtonOutputLineSet.setMaximumSize(QtCore.QSize(40, 16777215))
        self.pushButtonOutputLineSet.setObjectName(_fromUtf8("pushButtonOutputLineSet"))
        self.gridLayout.addWidget(self.pushButtonOutputLineSet, 8, 1, 1, 1)
        self.lineEditOutputLineSet = QtGui.QLineEdit(BK2DXF)
        self.lineEditOutputLineSet.setEnabled(False)
        self.lineEditOutputLineSet.setObjectName(_fromUtf8("lineEditOutputLineSet"))
        self.gridLayout.addWidget(self.lineEditOutputLineSet, 8, 2, 1, 1)
        spacerItem = QtGui.QSpacerItem(618, 168, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 5, 0, 1, 3)
        spacerItem1 = QtGui.QSpacerItem(618, 167, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 9, 0, 1, 3)
        self.pushButtonCreate = QtGui.QPushButton(BK2DXF)
        self.pushButtonCreate.setObjectName(_fromUtf8("pushButtonCreate"))
        self.gridLayout.addWidget(self.pushButtonCreate, 10, 0, 1, 3)

        self.retranslateUi(BK2DXF)
        QtCore.QMetaObject.connectSlotsByName(BK2DXF)

    def retranslateUi(self, BK2DXF):
        BK2DXF.setWindowTitle(_translate("BK2DXF", "Form", None))
        self.label_55.setText(_translate("BK2DXF", "Inputs:", None))
        self.label_56.setText(_translate("BK2DXF", "2D T3 Mesh:", None))
        self.pushButtonInputMesh.setText(_translate("BK2DXF", "...", None))
        self.label_52.setText(_translate("BK2DXF", "Line Set:", None))
        self.pushButtonInputLineSet.setText(_translate("BK2DXF", "...", None))
        self.label_54.setText(_translate("BK2DXF", "Type of mesh for dxf-export:", None))
        self.radioButton3DFace.setText(_translate("BK2DXF", "3D Face", None))
        self.radioButtonPolyline.setText(_translate("BK2DXF", "Polyline", None))
        self.label_53.setText(_translate("BK2DXF", "Outputs:", None))
        self.checkBoxOutputMesh.setText(_translate("BK2DXF", "Mesh file:", None))
        self.pushButtonOutputMesh.setText(_translate("BK2DXF", "...", None))
        self.checkBoxOutputLineSet.setText(_translate("BK2DXF", "Line set file:", None))
        self.pushButtonOutputLineSet.setText(_translate("BK2DXF", "...", None))
        self.pushButtonCreate.setText(_translate("BK2DXF", "Let\'s go!", None))

