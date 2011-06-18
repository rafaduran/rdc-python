# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/rdc/workspace/rdc-pyqt/src/src_exercises/chapter15/reference.ui'
#
# Created: Fri Jun 17 23:52:05 2011
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_RefDataDlg(object):
    def setupUi(self, RefDataDlg):
        RefDataDlg.setObjectName("RefDataDlg")
        RefDataDlg.resize(516, 308)
        self.gridLayout = QtGui.QGridLayout(RefDataDlg)
        self.gridLayout.setObjectName("gridLayout")
        self.table_view = QtGui.QTableView(RefDataDlg)
        self.table_view.setObjectName("table_view")
        self.gridLayout.addWidget(self.table_view, 0, 0, 1, 4)
        self.add_button = QtGui.QPushButton(RefDataDlg)
        self.add_button.setObjectName("add_button")
        self.gridLayout.addWidget(self.add_button, 1, 0, 1, 1)
        self.delete_button = QtGui.QPushButton(RefDataDlg)
        self.delete_button.setObjectName("delete_button")
        self.gridLayout.addWidget(self.delete_button, 1, 1, 1, 1)
        self.sort_button = QtGui.QPushButton(RefDataDlg)
        self.sort_button.setObjectName("sort_button")
        self.gridLayout.addWidget(self.sort_button, 1, 2, 1, 1)
        self.close_button = QtGui.QPushButton(RefDataDlg)
        self.close_button.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.close_button.setObjectName("close_button")
        self.gridLayout.addWidget(self.close_button, 1, 3, 1, 1)

        self.retranslateUi(RefDataDlg)
        QtCore.QMetaObject.connectSlotsByName(RefDataDlg)

    def retranslateUi(self, RefDataDlg):
        RefDataDlg.setWindowTitle(QtGui.QApplication.translate("RefDataDlg", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.add_button.setText(QtGui.QApplication.translate("RefDataDlg", "&Add", None, QtGui.QApplication.UnicodeUTF8))
        self.delete_button.setText(QtGui.QApplication.translate("RefDataDlg", "&Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.sort_button.setText(QtGui.QApplication.translate("RefDataDlg", "&Sort", None, QtGui.QApplication.UnicodeUTF8))
        self.close_button.setText(QtGui.QApplication.translate("RefDataDlg", "Close", None, QtGui.QApplication.UnicodeUTF8))

