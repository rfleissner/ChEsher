# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uiVectorDXF.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
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

class Ui_VectorDXF(object):
    def setupUi(self, VectorDXF):
        VectorDXF.setObjectName(_fromUtf8("VectorDXF"))
        VectorDXF.resize(639, 600)
        self.gridLayout = QtGui.QGridLayout(VectorDXF)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_38 = QtGui.QLabel(VectorDXF)
        self.label_38.setIndent(18)
        self.label_38.setObjectName(_fromUtf8("label_38"))
        self.gridLayout.addWidget(self.label_38, 12, 0, 1, 1)
        self.label_39 = QtGui.QLabel(VectorDXF)
        self.label_39.setIndent(18)
        self.label_39.setObjectName(_fromUtf8("label_39"))
        self.gridLayout.addWidget(self.label_39, 9, 0, 1, 1)
        self.doubleSpinBoxVMin = QtGui.QDoubleSpinBox(VectorDXF)
        self.doubleSpinBoxVMin.setMinimumSize(QtCore.QSize(100, 0))
        self.doubleSpinBoxVMin.setMaximumSize(QtCore.QSize(100, 16777215))
        self.doubleSpinBoxVMin.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.doubleSpinBoxVMin.setDecimals(3)
        self.doubleSpinBoxVMin.setMinimum(0.0)
        self.doubleSpinBoxVMin.setMaximum(99999999.0)
        self.doubleSpinBoxVMin.setSingleStep(1.0)
        self.doubleSpinBoxVMin.setProperty("value", 0.0)
        self.doubleSpinBoxVMin.setObjectName(_fromUtf8("doubleSpinBoxVMin"))
        self.gridLayout.addWidget(self.doubleSpinBoxVMin, 3, 2, 1, 1)
        self.label_27 = QtGui.QLabel(VectorDXF)
        self.label_27.setIndent(18)
        self.label_27.setObjectName(_fromUtf8("label_27"))
        self.gridLayout.addWidget(self.label_27, 4, 0, 1, 1)
        self.label_40 = QtGui.QLabel(VectorDXF)
        self.label_40.setIndent(18)
        self.label_40.setObjectName(_fromUtf8("label_40"))
        self.gridLayout.addWidget(self.label_40, 5, 0, 1, 1)
        self.doubleSpinBoxVMax = QtGui.QDoubleSpinBox(VectorDXF)
        self.doubleSpinBoxVMax.setMinimumSize(QtCore.QSize(100, 0))
        self.doubleSpinBoxVMax.setMaximumSize(QtCore.QSize(100, 16777215))
        self.doubleSpinBoxVMax.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.doubleSpinBoxVMax.setDecimals(3)
        self.doubleSpinBoxVMax.setMinimum(0.0)
        self.doubleSpinBoxVMax.setMaximum(99999999.0)
        self.doubleSpinBoxVMax.setSingleStep(1.0)
        self.doubleSpinBoxVMax.setProperty("value", 100.0)
        self.doubleSpinBoxVMax.setObjectName(_fromUtf8("doubleSpinBoxVMax"))
        self.gridLayout.addWidget(self.doubleSpinBoxVMax, 3, 3, 1, 1)
        self.label_37 = QtGui.QLabel(VectorDXF)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setUnderline(True)
        self.label_37.setFont(font)
        self.label_37.setObjectName(_fromUtf8("label_37"))
        self.gridLayout.addWidget(self.label_37, 11, 0, 1, 1)
        self.label_36 = QtGui.QLabel(VectorDXF)
        self.label_36.setIndent(18)
        self.label_36.setObjectName(_fromUtf8("label_36"))
        self.gridLayout.addWidget(self.label_36, 6, 0, 1, 1)
        self.label_41 = QtGui.QLabel(VectorDXF)
        self.label_41.setIndent(18)
        self.label_41.setObjectName(_fromUtf8("label_41"))
        self.gridLayout.addWidget(self.label_41, 3, 0, 1, 1)
        self.label_43 = QtGui.QLabel(VectorDXF)
        self.label_43.setIndent(18)
        self.label_43.setObjectName(_fromUtf8("label_43"))
        self.gridLayout.addWidget(self.label_43, 2, 0, 1, 1)
        self.doubleSpinBoxDY = QtGui.QDoubleSpinBox(VectorDXF)
        self.doubleSpinBoxDY.setMinimumSize(QtCore.QSize(100, 0))
        self.doubleSpinBoxDY.setMaximumSize(QtCore.QSize(100, 16777215))
        self.doubleSpinBoxDY.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.doubleSpinBoxDY.setDecimals(3)
        self.doubleSpinBoxDY.setMaximum(99999999.0)
        self.doubleSpinBoxDY.setSingleStep(1.0)
        self.doubleSpinBoxDY.setProperty("value", 10.0)
        self.doubleSpinBoxDY.setObjectName(_fromUtf8("doubleSpinBoxDY"))
        self.gridLayout.addWidget(self.doubleSpinBoxDY, 9, 2, 1, 1)
        self.spinBoxScale = QtGui.QSpinBox(VectorDXF)
        self.spinBoxScale.setMinimumSize(QtCore.QSize(100, 0))
        self.spinBoxScale.setMaximumSize(QtCore.QSize(100, 16777215))
        self.spinBoxScale.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.spinBoxScale.setMaximum(100000)
        self.spinBoxScale.setProperty("value", 1000)
        self.spinBoxScale.setObjectName(_fromUtf8("spinBoxScale"))
        self.gridLayout.addWidget(self.spinBoxScale, 5, 2, 1, 1)
        self.checkBoxUniform = QtGui.QCheckBox(VectorDXF)
        self.checkBoxUniform.setObjectName(_fromUtf8("checkBoxUniform"))
        self.gridLayout.addWidget(self.checkBoxUniform, 7, 0, 1, 1)
        self.label_35 = QtGui.QLabel(VectorDXF)
        self.label_35.setIndent(18)
        self.label_35.setObjectName(_fromUtf8("label_35"))
        self.gridLayout.addWidget(self.label_35, 8, 0, 1, 1)
        self.doubleSpinBoxLessThan = QtGui.QDoubleSpinBox(VectorDXF)
        self.doubleSpinBoxLessThan.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.doubleSpinBoxLessThan.setDecimals(2)
        self.doubleSpinBoxLessThan.setMaximum(99999999.0)
        self.doubleSpinBoxLessThan.setSingleStep(0.01)
        self.doubleSpinBoxLessThan.setProperty("value", 0.01)
        self.doubleSpinBoxLessThan.setObjectName(_fromUtf8("doubleSpinBoxLessThan"))
        self.gridLayout.addWidget(self.doubleSpinBoxLessThan, 4, 2, 1, 1)
        spacerItem = QtGui.QSpacerItem(618, 155, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 10, 0, 1, 5)
        spacerItem1 = QtGui.QSpacerItem(618, 154, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 13, 0, 1, 5)
        self.pushButtonCreate = QtGui.QPushButton(VectorDXF)
        self.pushButtonCreate.setObjectName(_fromUtf8("pushButtonCreate"))
        self.gridLayout.addWidget(self.pushButtonCreate, 14, 0, 1, 5)
        self.label_42 = QtGui.QLabel(VectorDXF)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setUnderline(True)
        self.label_42.setFont(font)
        self.label_42.setIndent(-4)
        self.label_42.setObjectName(_fromUtf8("label_42"))
        self.gridLayout.addWidget(self.label_42, 0, 0, 1, 1)
        self.doubleSpinBoxSizeFactor = QtGui.QDoubleSpinBox(VectorDXF)
        self.doubleSpinBoxSizeFactor.setMinimumSize(QtCore.QSize(100, 0))
        self.doubleSpinBoxSizeFactor.setMaximumSize(QtCore.QSize(100, 16777215))
        self.doubleSpinBoxSizeFactor.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.doubleSpinBoxSizeFactor.setDecimals(3)
        self.doubleSpinBoxSizeFactor.setMinimum(0.0)
        self.doubleSpinBoxSizeFactor.setMaximum(99999999.0)
        self.doubleSpinBoxSizeFactor.setSingleStep(0.5)
        self.doubleSpinBoxSizeFactor.setProperty("value", 10.0)
        self.doubleSpinBoxSizeFactor.setObjectName(_fromUtf8("doubleSpinBoxSizeFactor"))
        self.gridLayout.addWidget(self.doubleSpinBoxSizeFactor, 6, 2, 1, 1)
        self.doubleSpinBoxDX = QtGui.QDoubleSpinBox(VectorDXF)
        self.doubleSpinBoxDX.setMinimumSize(QtCore.QSize(100, 0))
        self.doubleSpinBoxDX.setMaximumSize(QtCore.QSize(100, 16777215))
        self.doubleSpinBoxDX.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.doubleSpinBoxDX.setDecimals(3)
        self.doubleSpinBoxDX.setMaximum(99999999.0)
        self.doubleSpinBoxDX.setSingleStep(1.0)
        self.doubleSpinBoxDX.setProperty("value", 10.0)
        self.doubleSpinBoxDX.setObjectName(_fromUtf8("doubleSpinBoxDX"))
        self.gridLayout.addWidget(self.doubleSpinBoxDX, 8, 2, 1, 1)
        self.pushButtonInput = QtGui.QPushButton(VectorDXF)
        self.pushButtonInput.setMinimumSize(QtCore.QSize(20, 0))
        self.pushButtonInput.setMaximumSize(QtCore.QSize(40, 16777215))
        self.pushButtonInput.setObjectName(_fromUtf8("pushButtonInput"))
        self.gridLayout.addWidget(self.pushButtonInput, 2, 1, 1, 1)
        self.lineEditInput = QtGui.QLineEdit(VectorDXF)
        self.lineEditInput.setObjectName(_fromUtf8("lineEditInput"))
        self.gridLayout.addWidget(self.lineEditInput, 2, 2, 1, 3)
        self.pushButtonOutput = QtGui.QPushButton(VectorDXF)
        self.pushButtonOutput.setMinimumSize(QtCore.QSize(20, 0))
        self.pushButtonOutput.setMaximumSize(QtCore.QSize(40, 16777215))
        self.pushButtonOutput.setObjectName(_fromUtf8("pushButtonOutput"))
        self.gridLayout.addWidget(self.pushButtonOutput, 12, 1, 1, 1)
        self.lineEditOutput = QtGui.QLineEdit(VectorDXF)
        self.lineEditOutput.setObjectName(_fromUtf8("lineEditOutput"))
        self.gridLayout.addWidget(self.lineEditOutput, 12, 2, 1, 3)

        self.retranslateUi(VectorDXF)
        QtCore.QMetaObject.connectSlotsByName(VectorDXF)

    def retranslateUi(self, VectorDXF):
        VectorDXF.setWindowTitle(_translate("VectorDXF", "Form", None))
        self.label_38.setText(_translate("VectorDXF", "DXF grid file:", None))
        self.label_39.setText(_translate("VectorDXF", "Y-Spacing:", None))
        self.doubleSpinBoxVMin.setToolTip(_translate("VectorDXF", "lower values are ignored", None))
        self.label_27.setText(_translate("VectorDXF", "Ignore values less than (±):", None))
        self.label_40.setText(_translate("VectorDXF", "Scale:", None))
        self.doubleSpinBoxVMax.setToolTip(_translate("VectorDXF", "higher values are ignored", None))
        self.label_37.setText(_translate("VectorDXF", "Outputs:", None))
        self.label_36.setText(_translate("VectorDXF", "Size factor:", None))
        self.label_41.setText(_translate("VectorDXF", "Minimum and maximum value of magnitude:", None))
        self.label_43.setText(_translate("VectorDXF", "2D T3 Vector Mesh:", None))
        self.doubleSpinBoxDY.setToolTip(_translate("VectorDXF", "grid interval in y-direction", None))
        self.spinBoxScale.setToolTip(_translate("VectorDXF", "text size", None))
        self.checkBoxUniform.setText(_translate("VectorDXF", "Use uniform length of vectors", None))
        self.label_35.setText(_translate("VectorDXF", "X-Spacing:", None))
        self.doubleSpinBoxLessThan.setToolTip(_translate("VectorDXF", "ignore values less than given difference from zero", None))
        self.pushButtonCreate.setText(_translate("VectorDXF", "Let\'s go!", None))
        self.label_42.setText(_translate("VectorDXF", "Inputs:", None))
        self.doubleSpinBoxSizeFactor.setToolTip(_translate("VectorDXF", "factor from amplitude to vector length", None))
        self.doubleSpinBoxDX.setToolTip(_translate("VectorDXF", "grid interval in x-direction", None))
        self.pushButtonInput.setText(_translate("VectorDXF", "...", None))
        self.pushButtonOutput.setText(_translate("VectorDXF", "...", None))

