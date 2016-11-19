# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui\uiHEC2DXF.ui'
#
# Created: Sat Nov 19 18:28:10 2016
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

class Ui_HEC2DXF(object):
    def setupUi(self, HEC2DXF):
        HEC2DXF.setObjectName(_fromUtf8("HEC2DXF"))
        HEC2DXF.resize(627, 759)
        self.gridLayout = QtGui.QGridLayout(HEC2DXF)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_106 = QtGui.QLabel(HEC2DXF)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setUnderline(True)
        self.label_106.setFont(font)
        self.label_106.setIndent(-4)
        self.label_106.setObjectName(_fromUtf8("label_106"))
        self.gridLayout.addWidget(self.label_106, 0, 0, 1, 1)
        self.label_105 = QtGui.QLabel(HEC2DXF)
        self.label_105.setIndent(18)
        self.label_105.setObjectName(_fromUtf8("label_105"))
        self.gridLayout.addWidget(self.label_105, 1, 0, 1, 1)
        self.pushButtonInputSDF = QtGui.QPushButton(HEC2DXF)
        self.pushButtonInputSDF.setMinimumSize(QtCore.QSize(20, 0))
        self.pushButtonInputSDF.setMaximumSize(QtCore.QSize(40, 16777215))
        self.pushButtonInputSDF.setObjectName(_fromUtf8("pushButtonInputSDF"))
        self.gridLayout.addWidget(self.pushButtonInputSDF, 1, 1, 1, 1)
        self.label_117 = QtGui.QLabel(HEC2DXF)
        self.label_117.setIndent(18)
        self.label_117.setObjectName(_fromUtf8("label_117"))
        self.gridLayout.addWidget(self.label_117, 2, 0, 1, 2)
        self.spinBoxScale = QtGui.QSpinBox(HEC2DXF)
        self.spinBoxScale.setMaximumSize(QtCore.QSize(80, 16777215))
        self.spinBoxScale.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.spinBoxScale.setMaximum(9999999)
        self.spinBoxScale.setProperty("value", 100)
        self.spinBoxScale.setObjectName(_fromUtf8("spinBoxScale"))
        self.gridLayout.addWidget(self.spinBoxScale, 2, 2, 1, 1)
        self.label_122 = QtGui.QLabel(HEC2DXF)
        self.label_122.setIndent(18)
        self.label_122.setObjectName(_fromUtf8("label_122"))
        self.gridLayout.addWidget(self.label_122, 3, 0, 1, 2)
        self.doubleSpinBoxSuperelevation = QtGui.QDoubleSpinBox(HEC2DXF)
        self.doubleSpinBoxSuperelevation.setMaximumSize(QtCore.QSize(80, 16777215))
        self.doubleSpinBoxSuperelevation.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.doubleSpinBoxSuperelevation.setMinimum(0.01)
        self.doubleSpinBoxSuperelevation.setMaximum(99999.99)
        self.doubleSpinBoxSuperelevation.setProperty("value", 1.0)
        self.doubleSpinBoxSuperelevation.setObjectName(_fromUtf8("doubleSpinBoxSuperelevation"))
        self.gridLayout.addWidget(self.doubleSpinBoxSuperelevation, 3, 2, 1, 1)
        self.label_59 = QtGui.QLabel(HEC2DXF)
        self.label_59.setMinimumSize(QtCore.QSize(70, 0))
        self.label_59.setIndent(18)
        self.label_59.setObjectName(_fromUtf8("label_59"))
        self.gridLayout.addWidget(self.label_59, 4, 0, 1, 2)
        self.pushButtonProfileSettings = QtGui.QPushButton(HEC2DXF)
        self.pushButtonProfileSettings.setMinimumSize(QtCore.QSize(120, 0))
        self.pushButtonProfileSettings.setObjectName(_fromUtf8("pushButtonProfileSettings"))
        self.gridLayout.addWidget(self.pushButtonProfileSettings, 4, 2, 1, 1)
        self.comboBoxDefault = QtGui.QComboBox(HEC2DXF)
        self.comboBoxDefault.setMinimumSize(QtCore.QSize(120, 0))
        self.comboBoxDefault.setObjectName(_fromUtf8("comboBoxDefault"))
        self.gridLayout.addWidget(self.comboBoxDefault, 4, 3, 1, 1)
        self.pushButtonDefault = QtGui.QPushButton(HEC2DXF)
        self.pushButtonDefault.setMinimumSize(QtCore.QSize(50, 0))
        self.pushButtonDefault.setMaximumSize(QtCore.QSize(100, 16777215))
        self.pushButtonDefault.setObjectName(_fromUtf8("pushButtonDefault"))
        self.gridLayout.addWidget(self.pushButtonDefault, 4, 4, 1, 1)
        spacerItem = QtGui.QSpacerItem(568, 259, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 5, 0, 1, 5)
        self.label_104 = QtGui.QLabel(HEC2DXF)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setUnderline(True)
        self.label_104.setFont(font)
        self.label_104.setObjectName(_fromUtf8("label_104"))
        self.gridLayout.addWidget(self.label_104, 6, 0, 1, 1)
        self.label_111 = QtGui.QLabel(HEC2DXF)
        self.label_111.setIndent(18)
        self.label_111.setObjectName(_fromUtf8("label_111"))
        self.gridLayout.addWidget(self.label_111, 7, 0, 1, 1)
        self.pushButtonOutputDXF = QtGui.QPushButton(HEC2DXF)
        self.pushButtonOutputDXF.setMinimumSize(QtCore.QSize(20, 0))
        self.pushButtonOutputDXF.setMaximumSize(QtCore.QSize(40, 16777215))
        self.pushButtonOutputDXF.setObjectName(_fromUtf8("pushButtonOutputDXF"))
        self.gridLayout.addWidget(self.pushButtonOutputDXF, 7, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(609, 255, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 8, 0, 1, 5)
        self.lineEditInputSDF = QtGui.QLineEdit(HEC2DXF)
        self.lineEditInputSDF.setObjectName(_fromUtf8("lineEditInputSDF"))
        self.gridLayout.addWidget(self.lineEditInputSDF, 1, 2, 1, 3)
        self.lineEditOutputDXF = QtGui.QLineEdit(HEC2DXF)
        self.lineEditOutputDXF.setObjectName(_fromUtf8("lineEditOutputDXF"))
        self.gridLayout.addWidget(self.lineEditOutputDXF, 7, 2, 1, 3)
        self.pushButtonCreate = QtGui.QPushButton(HEC2DXF)
        self.pushButtonCreate.setObjectName(_fromUtf8("pushButtonCreate"))
        self.gridLayout.addWidget(self.pushButtonCreate, 9, 0, 1, 5)

        self.retranslateUi(HEC2DXF)
        QtCore.QMetaObject.connectSlotsByName(HEC2DXF)

    def retranslateUi(self, HEC2DXF):
        HEC2DXF.setWindowTitle(_translate("HEC2DXF", "Form", None))
        self.label_106.setText(_translate("HEC2DXF", "Inputs:", None))
        self.label_105.setText(_translate("HEC2DXF", "Spatial Data Format:", None))
        self.pushButtonInputSDF.setText(_translate("HEC2DXF", "...", None))
        self.label_117.setText(_translate("HEC2DXF", "Scale factor:", None))
        self.label_122.setText(_translate("HEC2DXF", "Superelevation factor:", None))
        self.label_59.setText(_translate("HEC2DXF", "Output settings:", None))
        self.pushButtonProfileSettings.setText(_translate("HEC2DXF", "output settings", None))
        self.pushButtonDefault.setToolTip(_translate("HEC2DXF", "set default legend", None))
        self.pushButtonDefault.setText(_translate("HEC2DXF", "set default", None))
        self.label_104.setText(_translate("HEC2DXF", "Outputs:", None))
        self.label_111.setText(_translate("HEC2DXF", "DXF file:", None))
        self.pushButtonOutputDXF.setText(_translate("HEC2DXF", "...", None))
        self.pushButtonCreate.setText(_translate("HEC2DXF", "Let\'s go!", None))

