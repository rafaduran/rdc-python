#!/usr/bin/env python
# Copyright (c) 2008 Qtrac Ltd. All rights reserved.
# This program or module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 2 of the License, or
# version 3 of the License, or (at your option) any later version. It is
# provided for educational purposes and is distributed in the hope that
# it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
# the GNU General Public License for more details.

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from future_builtins import *

import sys
from PyQt4.QtCore import (QFile, QString, QTimer, Qt, SIGNAL, QLocale,
        QTranslator)
from PyQt4.QtGui import (QApplication, QDialog, QHBoxLayout, QLabel,
        QMessageBox, QPushButton, QSplitter, QTableView, QVBoxLayout,
        QWidget, QFileDialog)
import ships
import  qrc_ship_resources
MAC = True
try:
    from PyQt4.QtGui import qt_mac_set_native_menubar
except ImportError:
    MAC = False


class MainForm(QDialog):

    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)

        self.model = ships.ShipTableModel(QString("ships.dat"))
        tableLabel1 = QLabel(self.tr("Table &1"))
        self.tableView1 = QTableView()
        tableLabel1.setBuddy(self.tableView1)
        self.tableView1.setModel(self.model)
        self.tableView1.setItemDelegate(ships.ShipDelegate(self))
        tableLabel2 = QLabel(self.tr("Table &2"))
        self.tableView2 = QTableView()
        tableLabel2.setBuddy(self.tableView2)
        self.tableView2.setModel(self.model)
        self.tableView2.setItemDelegate(ships.ShipDelegate(self))

        addShipButton = QPushButton(self.tr("&Add Ship"))
        removeShipButton = QPushButton(self.tr("&Remove Ship"))
        export_button = QPushButton(self.tr("E&xport..."))
        quitButton = QPushButton(self.tr("&Quit"))
        if not MAC:
            addShipButton.setFocusPolicy(Qt.NoFocus)
            removeShipButton.setFocusPolicy(Qt.NoFocus)
            export_button.setFocusPolicy(Qt.NoFocus)
            quitButton.setFocusPolicy(Qt.NoFocus)

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(addShipButton)
        buttonLayout.addWidget(removeShipButton)
        buttonLayout.addWidget(export_button)
        buttonLayout.addStretch()
        buttonLayout.addWidget(quitButton)
        splitter = QSplitter(Qt.Horizontal)
        vbox = QVBoxLayout()
        vbox.addWidget(tableLabel1)
        vbox.addWidget(self.tableView1)
        widget = QWidget()
        widget.setLayout(vbox)
        splitter.addWidget(widget)
        vbox = QVBoxLayout()
        vbox.addWidget(tableLabel2)
        vbox.addWidget(self.tableView2)
        widget = QWidget()
        widget.setLayout(vbox)
        splitter.addWidget(widget)
        layout = QVBoxLayout()
        layout.addWidget(splitter)
        layout.addLayout(buttonLayout)
        self.setLayout(layout)

        for tableView in (self.tableView1, self.tableView2):
            header = tableView.horizontalHeader()
            self.connect(header, SIGNAL("sectionClicked(int)"),
                         self.sortTable)
        self.connect(addShipButton, SIGNAL("clicked()"), self.addShip)
        self.connect(removeShipButton, SIGNAL("clicked()"),
                     self.removeShip)
        self.connect(export_button, SIGNAL("clicked()"),
                     self.export)
        self.connect(quitButton, SIGNAL("clicked()"), self.accept)

        self.setWindowTitle(self.tr("Ships (delegate)"))
        QTimer.singleShot(0, self.initialLoad)


    def initialLoad(self):
        if not QFile.exists(self.model.filename):
            for ship in ships.generateFakeShips():
                self.model.ships.append(ship)
                self.model.owners.add(unicode(ship.owner))
                self.model.countries.add(unicode(ship.country))
            self.model.reset()
            self.model.dirty = False
        else:
            try:
                self.model.load()
            except IOError, e:
                QMessageBox.warning(self, self.tr("Ships - Error"),
                        self.tr(QString("Failed to load: %1").arg(e)))
        self.model.sortByName()
        self.resizeColumns()


    def resizeColumns(self):
        self.tableView1.resizeColumnsToContents()
        self.tableView2.resizeColumnsToContents()


    def reject(self):
        self.accept()


    def accept(self):
        if (self.model.dirty and
            QMessageBox.question(self, self.tr("Ships - Save?"),
                    self.tr("Save unsaved changes?"),
                    QMessageBox.Yes|QMessageBox.No) ==
                    QMessageBox.Yes):
            try:
                self.model.save()
            except IOError, e:
                QMessageBox.warning(self, self.tr("Ships - Error"),
                        self.tr(QString("Failed to save: %1").arg(e)))
        QDialog.accept(self)

    
    def sortTable(self, section):
        if section in (ships.OWNER, ships.COUNTRY):
            self.model.sortByCountryOwner()
        elif section == ships.TEU:
            self.model.sort_by_teu()
        else:
            self.model.sortByName()
        self.resizeColumns()


    def addShip(self):
        row = self.model.rowCount()
        self.model.insertRows(row)
        index = self.model.index(row, 0)
        tableView = self.tableView1
        if self.tableView2.hasFocus():
            tableView = self.tableView2
        tableView.setFocus()
        tableView.setCurrentIndex(index)
        tableView.edit(index)


    def removeShip(self):
        tableView = self.tableView1
        if self.tableView2.hasFocus():
            tableView = self.tableView2
        index = tableView.currentIndex()
        if not index.isValid():
            return
        row = index.row()
        name = self.model.data(
                    self.model.index(row, ships.NAME)).toString()
        owner = self.model.data(
                    self.model.index(row, ships.OWNER)).toString()
        country = self.model.data(
                    self.model.index(row, ships.COUNTRY)).toString()
        if (QMessageBox.question(self, self.tr("Ships - Remove"), 
                (QString(self.tr("Remove %1 of %2/%3?")).arg(name).arg(owner)
                        .arg(country)),
                QMessageBox.Yes|QMessageBox.No) ==
                QMessageBox.No):
            return
        self.model.removeRows(row)
        self.resizeColumns()
    
    def export(self):
        """
        export(self): popups a QFileDialog asking for a file to export data as
            plain txt
        """
        filename = "."
        filename = QFileDialog.getSaveFileName(self,
               self.tr("Ships choose export file"), filename,
                self.tr("Export files(*.txt)"),options=QFileDialog.DontUseNativeDialog)
        if not filename.isEmpty():
            succes, error = self.model.export(filename)

            if succes:
                QMessageBox.information(self, 
                    self.tr("Ships-delegate -- Export Succes"),
                        self.tr("Exported!!!!"))
                return True
            else:
                QMessageBox.warning(self, 
                    self.tr("Ships-delegate -- Export Error"),
                    self.tr(QString("Failed to save %1: %2").arg(filename).\
                    arg(error)))
        return False

app = QApplication(sys.argv)
locale = QLocale.system().name()
qtTranslator = QTranslator()
if qtTranslator.load("qt_" + locale, ":/"):
    app.installTranslator(qtTranslator)
appTranslator = QTranslator()
if appTranslator.load("ships_" + locale, ":/"):
    app.installTranslator(appTranslator)

form = MainForm()
form.show()
app.exec_()
