# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/Exercises/chapter07/AddDialog.ui'
#
# Created: Sun Apr 10 10:56:53 2011
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_AddDialog(object):
    def setupUi(self, AddDialog):
        AddDialog.setObjectName("AddDialog")
        AddDialog.resize(448, 285)
        self.widget = QtGui.QWidget(AddDialog)
        self.widget.setGeometry(QtCore.QRect(-20, 0, 450, 275))
        self.widget.setObjectName("widget")
        self.gridLayout = QtGui.QGridLayout(self.widget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit = QtGui.QLineEdit(self.widget)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.label = QtGui.QLabel(self.widget)
        self.label.setEnabled(True)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.add_button = QtGui.QPushButton(self.widget)
        self.add_button.setToolTip("")
        self.add_button.setWhatsThis("")
        self.add_button.setObjectName("add_button")
        self.verticalLayout.addWidget(self.add_button)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 2)
        self.listView = QtGui.QListView(self.widget)
        self.listView.setToolTip("")
        self.listView.setWhatsThis("")
        self.listView.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.listView.setAlternatingRowColors(True)
        self.listView.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.listView.setObjectName("listView")
        self.gridLayout.addWidget(self.listView, 0, 2, 2, 1)
        spacerItem = QtGui.QSpacerItem(188, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 2)
        spacerItem1 = QtGui.QSpacerItem(17, 48, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 2, 2, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(108, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 3, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(self.widget)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 3, 1, 1, 2)
        self.label.setBuddy(self.lineEdit)

        self.retranslateUi(AddDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), AddDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), AddDialog.reject)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), self.buttonBox.close)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), AddDialog.accept)
        QtCore.QMetaObject.connectSlotsByName(AddDialog)

    def retranslateUi(self, AddDialog):
        AddDialog.setWindowTitle(QtGui.QApplication.translate("AddDialog", "Add something", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("AddDialog", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.add_button.setText(QtGui.QApplication.translate("AddDialog", "Add", None, QtGui.QApplication.UnicodeUTF8))

