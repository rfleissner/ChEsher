# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uiProfilesDXF.ui'
#
# Created: Sun Oct 30 21:06:48 2016
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

class Ui_ProfilesDXF(object):
    def setupUi(self, ProfilesDXF):
        ProfilesDXF.setObjectName(_fromUtf8("ProfilesDXF"))
        ProfilesDXF.resize(639, 600)
        self.gridLayout = QtGui.QGridLayout(ProfilesDXF)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_105 = QtGui.QLabel(ProfilesDXF)
        self.label_105.setIndent(18)
        self.label_105.setObjectName(_fromUtf8("label_105"))
        self.gridLayout.addWidget(self.label_105, 1, 0, 1, 1)
        self.gridLayout_11 = QtGui.QGridLayout()
        self.gridLayout_11.setObjectName(_fromUtf8("gridLayout_11"))
        self.label_59 = QtGui.QLabel(ProfilesDXF)
        self.label_59.setMinimumSize(QtCore.QSize(70, 0))
        self.label_59.setIndent(18)
        self.label_59.setObjectName(_fromUtf8("label_59"))
        self.gridLayout_11.addWidget(self.label_59, 0, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_11.addItem(spacerItem, 0, 1, 1, 1)
        self.comboBoxDefault = QtGui.QComboBox(ProfilesDXF)
        self.comboBoxDefault.setMinimumSize(QtCore.QSize(120, 0))
        self.comboBoxDefault.setObjectName(_fromUtf8("comboBoxDefault"))
        self.gridLayout_11.addWidget(self.comboBoxDefault, 0, 2, 1, 1)
        self.pushButtonDefault = QtGui.QPushButton(ProfilesDXF)
        self.pushButtonDefault.setMinimumSize(QtCore.QSize(50, 0))
        self.pushButtonDefault.setMaximumSize(QtCore.QSize(100, 16777215))
        self.pushButtonDefault.setObjectName(_fromUtf8("pushButtonDefault"))
        self.gridLayout_11.addWidget(self.pushButtonDefault, 0, 3, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_11, 11, 0, 1, 5)
        self.lineEditInputReach = QtGui.QLineEdit(ProfilesDXF)
        self.lineEditInputReach.setObjectName(_fromUtf8("lineEditInputReach"))
        self.gridLayout.addWidget(self.lineEditInputReach, 2, 2, 1, 3)
        self.pushButtonInputProfiles = QtGui.QPushButton(ProfilesDXF)
        self.pushButtonInputProfiles.setMinimumSize(QtCore.QSize(20, 0))
        self.pushButtonInputProfiles.setMaximumSize(QtCore.QSize(40, 16777215))
        self.pushButtonInputProfiles.setObjectName(_fromUtf8("pushButtonInputProfiles"))
        self.gridLayout.addWidget(self.pushButtonInputProfiles, 1, 1, 1, 1)
        self.pushButtonCreate = QtGui.QPushButton(ProfilesDXF)
        self.pushButtonCreate.setObjectName(_fromUtf8("pushButtonCreate"))
        self.gridLayout.addWidget(self.pushButtonCreate, 17, 0, 1, 5)
        spacerItem1 = QtGui.QSpacerItem(609, 255, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 16, 0, 1, 5)
        self.lineEditOutputPlan = QtGui.QLineEdit(ProfilesDXF)
        self.lineEditOutputPlan.setEnabled(False)
        self.lineEditOutputPlan.setObjectName(_fromUtf8("lineEditOutputPlan"))
        self.gridLayout.addWidget(self.lineEditOutputPlan, 15, 2, 1, 3)
        self.pushButtonOutputPlan = QtGui.QPushButton(ProfilesDXF)
        self.pushButtonOutputPlan.setEnabled(False)
        self.pushButtonOutputPlan.setMinimumSize(QtCore.QSize(20, 0))
        self.pushButtonOutputPlan.setMaximumSize(QtCore.QSize(40, 16777215))
        self.pushButtonOutputPlan.setObjectName(_fromUtf8("pushButtonOutputPlan"))
        self.gridLayout.addWidget(self.pushButtonOutputPlan, 15, 1, 1, 1)
        self.checkBoxOutputPlan = QtGui.QCheckBox(ProfilesDXF)
        self.checkBoxOutputPlan.setObjectName(_fromUtf8("checkBoxOutputPlan"))
        self.gridLayout.addWidget(self.checkBoxOutputPlan, 15, 0, 1, 1)
        self.lineEditOutputProfiles = QtGui.QLineEdit(ProfilesDXF)
        self.lineEditOutputProfiles.setEnabled(False)
        self.lineEditOutputProfiles.setObjectName(_fromUtf8("lineEditOutputProfiles"))
        self.gridLayout.addWidget(self.lineEditOutputProfiles, 14, 2, 1, 3)
        self.pushButtonOutputProfiles = QtGui.QPushButton(ProfilesDXF)
        self.pushButtonOutputProfiles.setEnabled(False)
        self.pushButtonOutputProfiles.setMinimumSize(QtCore.QSize(20, 0))
        self.pushButtonOutputProfiles.setMaximumSize(QtCore.QSize(40, 16777215))
        self.pushButtonOutputProfiles.setObjectName(_fromUtf8("pushButtonOutputProfiles"))
        self.gridLayout.addWidget(self.pushButtonOutputProfiles, 14, 1, 1, 1)
        self.checkBoxOutputProfiles = QtGui.QCheckBox(ProfilesDXF)
        self.checkBoxOutputProfiles.setObjectName(_fromUtf8("checkBoxOutputProfiles"))
        self.gridLayout.addWidget(self.checkBoxOutputProfiles, 14, 0, 1, 1)
        self.label_104 = QtGui.QLabel(ProfilesDXF)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setUnderline(True)
        self.label_104.setFont(font)
        self.label_104.setObjectName(_fromUtf8("label_104"))
        self.gridLayout.addWidget(self.label_104, 13, 0, 1, 1)
        self.label_122 = QtGui.QLabel(ProfilesDXF)
        self.label_122.setIndent(18)
        self.label_122.setObjectName(_fromUtf8("label_122"))
        self.gridLayout.addWidget(self.label_122, 6, 0, 1, 1)
        self.spinBoxScale = QtGui.QSpinBox(ProfilesDXF)
        self.spinBoxScale.setMaximumSize(QtCore.QSize(80, 16777215))
        self.spinBoxScale.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.spinBoxScale.setMaximum(9999999)
        self.spinBoxScale.setProperty("value", 100)
        self.spinBoxScale.setObjectName(_fromUtf8("spinBoxScale"))
        self.gridLayout.addWidget(self.spinBoxScale, 5, 2, 1, 1)
        self.tableWidget = QtGui.QTableWidget(ProfilesDXF)
        self.tableWidget.setMinimumSize(QtCore.QSize(0, 150))
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        self.gridLayout.addWidget(self.tableWidget, 9, 0, 1, 5)
        self.label_117 = QtGui.QLabel(ProfilesDXF)
        self.label_117.setIndent(18)
        self.label_117.setObjectName(_fromUtf8("label_117"))
        self.gridLayout.addWidget(self.label_117, 5, 0, 1, 1)
        self.lineEditInputReachName = QtGui.QLineEdit(ProfilesDXF)
        self.lineEditInputReachName.setObjectName(_fromUtf8("lineEditInputReachName"))
        self.gridLayout.addWidget(self.lineEditInputReachName, 4, 2, 1, 3)
        self.gridLayout_10 = QtGui.QGridLayout()
        self.gridLayout_10.setObjectName(_fromUtf8("gridLayout_10"))
        self.pushButtonAdd = QtGui.QPushButton(ProfilesDXF)
        self.pushButtonAdd.setMinimumSize(QtCore.QSize(50, 0))
        self.pushButtonAdd.setMaximumSize(QtCore.QSize(100, 16777215))
        self.pushButtonAdd.setObjectName(_fromUtf8("pushButtonAdd"))
        self.gridLayout_10.addWidget(self.pushButtonAdd, 0, 1, 1, 1)
        self.pushButtonDelete = QtGui.QPushButton(ProfilesDXF)
        self.pushButtonDelete.setMinimumSize(QtCore.QSize(50, 0))
        self.pushButtonDelete.setMaximumSize(QtCore.QSize(100, 16777215))
        self.pushButtonDelete.setObjectName(_fromUtf8("pushButtonDelete"))
        self.gridLayout_10.addWidget(self.pushButtonDelete, 0, 2, 1, 1)
        self.pushButtonColour = QtGui.QPushButton(ProfilesDXF)
        self.pushButtonColour.setMinimumSize(QtCore.QSize(50, 0))
        self.pushButtonColour.setMaximumSize(QtCore.QSize(100, 16777215))
        self.pushButtonColour.setObjectName(_fromUtf8("pushButtonColour"))
        self.gridLayout_10.addWidget(self.pushButtonColour, 0, 3, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_10.addItem(spacerItem2, 0, 4, 1, 1)
        self.label_60 = QtGui.QLabel(ProfilesDXF)
        self.label_60.setMinimumSize(QtCore.QSize(70, 0))
        self.label_60.setIndent(18)
        self.label_60.setObjectName(_fromUtf8("label_60"))
        self.gridLayout_10.addWidget(self.label_60, 0, 0, 1, 1)
        self.pushButtonInputWaterSurface = QtGui.QPushButton(ProfilesDXF)
        self.pushButtonInputWaterSurface.setMinimumSize(QtCore.QSize(20, 0))
        self.pushButtonInputWaterSurface.setMaximumSize(QtCore.QSize(40, 16777215))
        self.pushButtonInputWaterSurface.setObjectName(_fromUtf8("pushButtonInputWaterSurface"))
        self.gridLayout_10.addWidget(self.pushButtonInputWaterSurface, 0, 5, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_10, 8, 0, 1, 5)
        spacerItem3 = QtGui.QSpacerItem(50, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 7, 0, 1, 5)
        self.pushButtonProfileSettings = QtGui.QPushButton(ProfilesDXF)
        self.pushButtonProfileSettings.setObjectName(_fromUtf8("pushButtonProfileSettings"))
        self.gridLayout.addWidget(self.pushButtonProfileSettings, 6, 4, 1, 1)
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem4, 6, 3, 1, 1)
        self.doubleSpinBoxSuperelevation = QtGui.QDoubleSpinBox(ProfilesDXF)
        self.doubleSpinBoxSuperelevation.setMaximumSize(QtCore.QSize(80, 16777215))
        self.doubleSpinBoxSuperelevation.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.doubleSpinBoxSuperelevation.setMinimum(0.01)
        self.doubleSpinBoxSuperelevation.setMaximum(99999.99)
        self.doubleSpinBoxSuperelevation.setProperty("value", 1.0)
        self.doubleSpinBoxSuperelevation.setObjectName(_fromUtf8("doubleSpinBoxSuperelevation"))
        self.gridLayout.addWidget(self.doubleSpinBoxSuperelevation, 6, 2, 1, 1)
        self.label_108 = QtGui.QLabel(ProfilesDXF)
        self.label_108.setIndent(18)
        self.label_108.setObjectName(_fromUtf8("label_108"))
        self.gridLayout.addWidget(self.label_108, 4, 0, 1, 1)
        self.lineEditInputBottom = QtGui.QLineEdit(ProfilesDXF)
        self.lineEditInputBottom.setObjectName(_fromUtf8("lineEditInputBottom"))
        self.gridLayout.addWidget(self.lineEditInputBottom, 3, 2, 1, 3)
        self.pushButtonInputBottom = QtGui.QPushButton(ProfilesDXF)
        self.pushButtonInputBottom.setMinimumSize(QtCore.QSize(20, 0))
        self.pushButtonInputBottom.setMaximumSize(QtCore.QSize(40, 16777215))
        self.pushButtonInputBottom.setObjectName(_fromUtf8("pushButtonInputBottom"))
        self.gridLayout.addWidget(self.pushButtonInputBottom, 3, 1, 1, 1)
        self.label_107 = QtGui.QLabel(ProfilesDXF)
        self.label_107.setIndent(18)
        self.label_107.setObjectName(_fromUtf8("label_107"))
        self.gridLayout.addWidget(self.label_107, 3, 0, 1, 1)
        self.pushButtonInputReach = QtGui.QPushButton(ProfilesDXF)
        self.pushButtonInputReach.setMinimumSize(QtCore.QSize(20, 0))
        self.pushButtonInputReach.setMaximumSize(QtCore.QSize(40, 16777215))
        self.pushButtonInputReach.setObjectName(_fromUtf8("pushButtonInputReach"))
        self.gridLayout.addWidget(self.pushButtonInputReach, 2, 1, 1, 1)
        self.lineEditInputProfiles = QtGui.QLineEdit(ProfilesDXF)
        self.lineEditInputProfiles.setObjectName(_fromUtf8("lineEditInputProfiles"))
        self.gridLayout.addWidget(self.lineEditInputProfiles, 1, 2, 1, 3)
        self.label_106 = QtGui.QLabel(ProfilesDXF)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setUnderline(True)
        self.label_106.setFont(font)
        self.label_106.setIndent(-4)
        self.label_106.setObjectName(_fromUtf8("label_106"))
        self.gridLayout.addWidget(self.label_106, 0, 0, 1, 1)
        self.label_103 = QtGui.QLabel(ProfilesDXF)
        self.label_103.setIndent(18)
        self.label_103.setObjectName(_fromUtf8("label_103"))
        self.gridLayout.addWidget(self.label_103, 2, 0, 1, 1)
        spacerItem5 = QtGui.QSpacerItem(500, 227, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem5, 12, 0, 1, 5)

        self.retranslateUi(ProfilesDXF)
        QtCore.QMetaObject.connectSlotsByName(ProfilesDXF)

    def retranslateUi(self, ProfilesDXF):
        ProfilesDXF.setWindowTitle(_translate("ProfilesDXF", "Form", None))
        self.label_105.setText(_translate("ProfilesDXF", "Channel profiles file:", None))
        self.label_59.setText(_translate("ProfilesDXF", "Default settings:", None))
        self.pushButtonDefault.setToolTip(_translate("ProfilesDXF", "set default legend", None))
        self.pushButtonDefault.setText(_translate("ProfilesDXF", "set default", None))
        self.pushButtonInputProfiles.setText(_translate("ProfilesDXF", "...", None))
        self.pushButtonCreate.setText(_translate("ProfilesDXF", "Let\'s go!", None))
        self.pushButtonOutputPlan.setText(_translate("ProfilesDXF", "...", None))
        self.checkBoxOutputPlan.setText(_translate("ProfilesDXF", "DXF file plan view:", None))
        self.pushButtonOutputProfiles.setText(_translate("ProfilesDXF", "...", None))
        self.checkBoxOutputProfiles.setText(_translate("ProfilesDXF", "DXF file profiles:", None))
        self.label_104.setText(_translate("ProfilesDXF", "Outputs:", None))
        self.label_122.setText(_translate("ProfilesDXF", "Superelevation factor:", None))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("ProfilesDXF", "Water Surface Mesh", None))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("ProfilesDXF", "Name", None))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("ProfilesDXF", "Colour", None))
        self.label_117.setText(_translate("ProfilesDXF", "Scale factor:", None))
        self.pushButtonAdd.setToolTip(_translate("ProfilesDXF", "add layer to table", None))
        self.pushButtonAdd.setText(_translate("ProfilesDXF", "add", None))
        self.pushButtonDelete.setToolTip(_translate("ProfilesDXF", "delete selected layer from table", None))
        self.pushButtonDelete.setText(_translate("ProfilesDXF", "delete", None))
        self.pushButtonColour.setToolTip(_translate("ProfilesDXF", "set colour for selected level", None))
        self.pushButtonColour.setText(_translate("ProfilesDXF", "colour", None))
        self.label_60.setText(_translate("ProfilesDXF", "Water Surface mesh files:", None))
        self.pushButtonInputWaterSurface.setText(_translate("ProfilesDXF", "...", None))
        self.pushButtonProfileSettings.setText(_translate("ProfilesDXF", "output settings", None))
        self.label_108.setText(_translate("ProfilesDXF", "Reach name:", None))
        self.pushButtonInputBottom.setText(_translate("ProfilesDXF", "...", None))
        self.label_107.setText(_translate("ProfilesDXF", "Bottom mesh file:", None))
        self.pushButtonInputReach.setText(_translate("ProfilesDXF", "...", None))
        self.label_106.setText(_translate("ProfilesDXF", "Inputs:", None))
        self.label_103.setText(_translate("ProfilesDXF", "Channel reach file:", None))
