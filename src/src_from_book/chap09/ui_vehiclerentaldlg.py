# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/rdc/workspace/rdc-pyqt/src/src_from_book/chap09/vehiclerentaldlg.ui'
#
# Created: Sun May 22 20:04:49 2011
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_VehicleRentalDlg(object):
    def setupUi(self, VehicleRentalDlg):
        VehicleRentalDlg.setObjectName("VehicleRentalDlg")
        VehicleRentalDlg.resize(206, 246)
        self.gridlayout = QtGui.QGridLayout(VehicleRentalDlg)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")
        self.buttonBox = QtGui.QDialogButtonBox(VehicleRentalDlg)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.NoButton|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridlayout.addWidget(self.buttonBox, 4, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(188, 16, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem, 3, 0, 1, 1)
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")
        self.label_6 = QtGui.QLabel(VehicleRentalDlg)
        self.label_6.setObjectName("label_6")
        self.hboxlayout.addWidget(self.label_6)
        self.mileageLabel = QtGui.QLabel(VehicleRentalDlg)
        self.mileageLabel.setFrameShape(QtGui.QFrame.StyledPanel)
        self.mileageLabel.setFrameShadow(QtGui.QFrame.Sunken)
        self.mileageLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.mileageLabel.setObjectName("mileageLabel")
        self.hboxlayout.addWidget(self.mileageLabel)
        self.gridlayout.addLayout(self.hboxlayout, 2, 0, 1, 1)
        self.stackedWidget = QtGui.QStackedWidget(VehicleRentalDlg)
        self.stackedWidget.setObjectName("stackedWidget")
        self.page_2 = QtGui.QWidget()
        self.page_2.setObjectName("page_2")
        self.gridlayout1 = QtGui.QGridLayout(self.page_2)
        self.gridlayout1.setMargin(9)
        self.gridlayout1.setSpacing(6)
        self.gridlayout1.setObjectName("gridlayout1")
        self.colorComboBox = QtGui.QComboBox(self.page_2)
        self.colorComboBox.setObjectName("colorComboBox")
        self.colorComboBox.addItem("")
        self.colorComboBox.addItem("")
        self.colorComboBox.addItem("")
        self.colorComboBox.addItem("")
        self.colorComboBox.addItem("")
        self.colorComboBox.addItem("")
        self.colorComboBox.addItem("")
        self.gridlayout1.addWidget(self.colorComboBox, 0, 1, 1, 1)
        self.label_4 = QtGui.QLabel(self.page_2)
        self.label_4.setObjectName("label_4")
        self.gridlayout1.addWidget(self.label_4, 0, 0, 1, 1)
        self.label_5 = QtGui.QLabel(self.page_2)
        self.label_5.setObjectName("label_5")
        self.gridlayout1.addWidget(self.label_5, 1, 0, 1, 1)
        self.seatsSpinBox = QtGui.QSpinBox(self.page_2)
        self.seatsSpinBox.setAlignment(QtCore.Qt.AlignRight)
        self.seatsSpinBox.setMaximum(12)
        self.seatsSpinBox.setMinimum(2)
        self.seatsSpinBox.setProperty("value", 4)
        self.seatsSpinBox.setObjectName("seatsSpinBox")
        self.gridlayout1.addWidget(self.seatsSpinBox, 1, 1, 1, 1)
        self.stackedWidget.addWidget(self.page_2)
        self.page = QtGui.QWidget()
        self.page.setObjectName("page")
        self.gridlayout2 = QtGui.QGridLayout(self.page)
        self.gridlayout2.setMargin(9)
        self.gridlayout2.setSpacing(6)
        self.gridlayout2.setObjectName("gridlayout2")
        self.weightSpinBox = QtGui.QSpinBox(self.page)
        self.weightSpinBox.setAlignment(QtCore.Qt.AlignRight)
        self.weightSpinBox.setMaximum(8)
        self.weightSpinBox.setMinimum(1)
        self.weightSpinBox.setObjectName("weightSpinBox")
        self.gridlayout2.addWidget(self.weightSpinBox, 0, 1, 1, 1)
        self.label_3 = QtGui.QLabel(self.page)
        self.label_3.setObjectName("label_3")
        self.gridlayout2.addWidget(self.label_3, 1, 0, 1, 1)
        self.label_2 = QtGui.QLabel(self.page)
        self.label_2.setObjectName("label_2")
        self.gridlayout2.addWidget(self.label_2, 0, 0, 1, 1)
        self.volumeSpinBox = QtGui.QSpinBox(self.page)
        self.volumeSpinBox.setAlignment(QtCore.Qt.AlignRight)
        self.volumeSpinBox.setMaximum(22)
        self.volumeSpinBox.setMinimum(4)
        self.volumeSpinBox.setProperty("value", 10)
        self.volumeSpinBox.setObjectName("volumeSpinBox")
        self.gridlayout2.addWidget(self.volumeSpinBox, 1, 1, 1, 1)
        self.stackedWidget.addWidget(self.page)
        self.gridlayout.addWidget(self.stackedWidget, 1, 0, 1, 1)
        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setMargin(0)
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setObjectName("hboxlayout1")
        self.label = QtGui.QLabel(VehicleRentalDlg)
        self.label.setObjectName("label")
        self.hboxlayout1.addWidget(self.label)
        self.vehicleComboBox = QtGui.QComboBox(VehicleRentalDlg)
        self.vehicleComboBox.setObjectName("vehicleComboBox")
        self.vehicleComboBox.addItem("")
        self.vehicleComboBox.addItem("")
        self.hboxlayout1.addWidget(self.vehicleComboBox)
        self.gridlayout.addLayout(self.hboxlayout1, 0, 0, 1, 1)
        self.label_4.setBuddy(self.colorComboBox)
        self.label_5.setBuddy(self.seatsSpinBox)
        self.label_3.setBuddy(self.volumeSpinBox)
        self.label_2.setBuddy(self.seatsSpinBox)
        self.label.setBuddy(self.vehicleComboBox)

        self.retranslateUi(VehicleRentalDlg)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.vehicleComboBox, QtCore.SIGNAL("currentIndexChanged(int)"), self.stackedWidget.setCurrentIndex)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), VehicleRentalDlg.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), VehicleRentalDlg.reject)
        QtCore.QMetaObject.connectSlotsByName(VehicleRentalDlg)

    def retranslateUi(self, VehicleRentalDlg):
        VehicleRentalDlg.setWindowTitle(QtGui.QApplication.translate("VehicleRentalDlg", "Vehicle Rental", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("VehicleRentalDlg", "Max. Mileage:", None, QtGui.QApplication.UnicodeUTF8))
        self.mileageLabel.setText(QtGui.QApplication.translate("VehicleRentalDlg", "1000 miles", None, QtGui.QApplication.UnicodeUTF8))
        self.colorComboBox.setItemText(0, QtGui.QApplication.translate("VehicleRentalDlg", "Black", None, QtGui.QApplication.UnicodeUTF8))
        self.colorComboBox.setItemText(1, QtGui.QApplication.translate("VehicleRentalDlg", "Blue", None, QtGui.QApplication.UnicodeUTF8))
        self.colorComboBox.setItemText(2, QtGui.QApplication.translate("VehicleRentalDlg", "Green", None, QtGui.QApplication.UnicodeUTF8))
        self.colorComboBox.setItemText(3, QtGui.QApplication.translate("VehicleRentalDlg", "Red", None, QtGui.QApplication.UnicodeUTF8))
        self.colorComboBox.setItemText(4, QtGui.QApplication.translate("VehicleRentalDlg", "Silver", None, QtGui.QApplication.UnicodeUTF8))
        self.colorComboBox.setItemText(5, QtGui.QApplication.translate("VehicleRentalDlg", "White", None, QtGui.QApplication.UnicodeUTF8))
        self.colorComboBox.setItemText(6, QtGui.QApplication.translate("VehicleRentalDlg", "Yellow", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("VehicleRentalDlg", "&Color:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("VehicleRentalDlg", "&Seats:", None, QtGui.QApplication.UnicodeUTF8))
        self.weightSpinBox.setSuffix(QtGui.QApplication.translate("VehicleRentalDlg", " tons", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("VehicleRentalDlg", "V&olume:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("VehicleRentalDlg", "&Weight:", None, QtGui.QApplication.UnicodeUTF8))
        self.volumeSpinBox.setSuffix(QtGui.QApplication.translate("VehicleRentalDlg", " cu m", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("VehicleRentalDlg", "&Vehicle Type:", None, QtGui.QApplication.UnicodeUTF8))
        self.vehicleComboBox.setItemText(0, QtGui.QApplication.translate("VehicleRentalDlg", "Car", None, QtGui.QApplication.UnicodeUTF8))
        self.vehicleComboBox.setItemText(1, QtGui.QApplication.translate("VehicleRentalDlg", "Van", None, QtGui.QApplication.UnicodeUTF8))

