# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uiDXF2BK.ui'
#
# Created: Tue Nov 01 21:19:15 2016
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

class Ui_DXF2BK(object):
    def setupUi(self, DXF2BK):
        DXF2BK.setObjectName(_fromUtf8("DXF2BK"))
        DXF2BK.resize(639, 600)
        self.gridLayout = QtGui.QGridLayout(DXF2BK)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_9 = QtGui.QLabel(DXF2BK)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setUnderline(True)
        self.label_9.setFont(font)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout.addWidget(self.label_9, 0, 0, 1, 1)
        self.label_1 = QtGui.QLabel(DXF2BK)
        self.label_1.setMinimumSize(QtCore.QSize(100, 0))
        self.label_1.setIndent(18)
        self.label_1.setObjectName(_fromUtf8("label_1"))
        self.gridLayout.addWidget(self.label_1, 1, 0, 1, 1)
        self.pushButtonInput = QtGui.QPushButton(DXF2BK)
        self.pushButtonInput.setMinimumSize(QtCore.QSize(20, 0))
        self.pushButtonInput.setMaximumSize(QtCore.QSize(40, 16777215))
        self.pushButtonInput.setObjectName(_fromUtf8("pushButtonInput"))
        self.gridLayout.addWidget(self.pushButtonInput, 1, 1, 1, 1)
        self.lineEditInput = QtGui.QLineEdit(DXF2BK)
        self.lineEditInput.setObjectName(_fromUtf8("lineEditInput"))
        self.gridLayout.addWidget(self.lineEditInput, 1, 2, 1, 1)
        spacerItem = QtGui.QSpacerItem(588, 27, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 3)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.pushButtonRefresh = QtGui.QPushButton(DXF2BK)
        self.pushButtonRefresh.setMinimumSize(QtCore.QSize(50, 0))
        self.pushButtonRefresh.setMaximumSize(QtCore.QSize(100, 16777215))
        self.pushButtonRefresh.setObjectName(_fromUtf8("pushButtonRefresh"))
        self.horizontalLayout.addWidget(self.pushButtonRefresh)
        self.pushButtonAdd = QtGui.QPushButton(DXF2BK)
        self.pushButtonAdd.setMinimumSize(QtCore.QSize(50, 0))
        self.pushButtonAdd.setMaximumSize(QtCore.QSize(100, 16777215))
        self.pushButtonAdd.setObjectName(_fromUtf8("pushButtonAdd"))
        self.horizontalLayout.addWidget(self.pushButtonAdd)
        self.pushButtonDelete = QtGui.QPushButton(DXF2BK)
        self.pushButtonDelete.setMinimumSize(QtCore.QSize(50, 0))
        self.pushButtonDelete.setMaximumSize(QtCore.QSize(100, 16777215))
        self.pushButtonDelete.setObjectName(_fromUtf8("pushButtonDelete"))
        self.horizontalLayout.addWidget(self.pushButtonDelete)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.pushButtonOpen = QtGui.QPushButton(DXF2BK)
        self.pushButtonOpen.setMinimumSize(QtCore.QSize(20, 0))
        self.pushButtonOpen.setMaximumSize(QtCore.QSize(40, 16777215))
        self.pushButtonOpen.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.pushButtonOpen.setObjectName(_fromUtf8("pushButtonOpen"))
        self.horizontalLayout.addWidget(self.pushButtonOpen)
        self.gridLayout.addLayout(self.horizontalLayout, 3, 0, 1, 3)
        self.tableWidget = QtGui.QTableWidget(DXF2BK)
        self.tableWidget.setMinimumSize(QtCore.QSize(0, 400))
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        self.gridLayout.addWidget(self.tableWidget, 4, 0, 1, 3)
        spacerItem2 = QtGui.QSpacerItem(248, 26, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 5, 0, 1, 3)
        self.pushButtonCreate = QtGui.QPushButton(DXF2BK)
        self.pushButtonCreate.setObjectName(_fromUtf8("pushButtonCreate"))
        self.gridLayout.addWidget(self.pushButtonCreate, 6, 0, 1, 3)

        self.retranslateUi(DXF2BK)
        QtCore.QMetaObject.connectSlotsByName(DXF2BK)

    def retranslateUi(self, DXF2BK):
        DXF2BK.setWindowTitle(_translate("DXF2BK", "Form", None))
        self.label_9.setText(_translate("DXF2BK", "Inputs:", None))
        self.label_1.setText(_translate("DXF2BK", "DXF file:", None))
        self.pushButtonInput.setText(_translate("DXF2BK", "...", None))
        self.pushButtonRefresh.setToolTip(_translate("DXF2BK", "load content from dxf file", None))
        self.pushButtonRefresh.setText(_translate("DXF2BK", "refresh", None))
        self.pushButtonAdd.setToolTip(_translate("DXF2BK", "add layer to table", None))
        self.pushButtonAdd.setText(_translate("DXF2BK", "add", None))
        self.pushButtonDelete.setToolTip(_translate("DXF2BK", "delete selected layer from table", None))
        self.pushButtonDelete.setText(_translate("DXF2BK", "delete", None))
        self.pushButtonOpen.setText(_translate("DXF2BK", "...", None))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("DXF2BK", "Layer", None))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("DXF2BK", "Filename", None))
        self.pushButtonCreate.setText(_translate("DXF2BK", "Let\'s go!", None))

