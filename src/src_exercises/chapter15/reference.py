#!/usr/bin/env python
# -*- Encoding: utf-8 -*-
"""
This files solves Chpater 15 exercise from Rapid GUI Programming with Python
and Qt:
    Create a dialog-style application for adding, editing, and deleting records
in a reference table. This application creates the reference.db database the 
first time it is run, with a single, empty table "reference".
"""
from __future__ import print_function
from __future__ import unicode_literals
from future_builtins import *

import os
import sys
from functools import partial

from PyQt4.QtCore import (Qt, SIGNAL, QFile, QVariant, QString)
from PyQt4.QtGui import (QDialog, QApplication, QMenu, QTableView, QMessageBox)
from PyQt4.QtSql import (QSqlDatabase, QSqlQuery, QSqlTableModel)

from ui_reference import Ui_RefDataDlg

MAC = True
try:
    from PyQt4.QtGui import qt_mac_set_native_menubar
except ImportError:
    MAC = False

class ReferenceDataDlg(QDialog, Ui_RefDataDlg):
    """
    ReferenceDataDlg Class
        Dialog for adding, editing and deleting records in refernce table
    """
    def __init__(self, parent=None):
        """
        __init__(self, parent=None)
        """
        super(ReferenceDataDlg, self).__init__(parent)
        self.setupUi(self)
        self.model = QSqlTableModel(self)
        self.model.setTable("reference")
        self.model.select()
        self.table_view.setModel(self.model)
        self.table_view.setSelectionMode(QTableView.SingleSelection)
        self.table_view.setSelectionBehavior(QTableView.SelectRows)
        for index, header in enumerate(
                ("Id", "Category", "Short Desc.", "Long Desc.")):
            self.model.setHeaderData(index, Qt.Horizontal,
                    QVariant(header))
        self.table_view.setColumnHidden(0, True)
        self.table_view.resizeColumnsToContents()

        sort_menu = QMenu(self)
        for index, order in enumerate(("By Id", "By Category", "By"
           "  Description")):
            order_type = partial(self.model.sort, index, Qt.AscendingOrder)
            sort_menu.addAction(order, order_type)
        self.sort_button.setMenu(sort_menu)

        if not MAC:
            self.add_button.setFocusPolicy(Qt.NoFocus)
            self.delete_button.setFocusPolicy(Qt.NoFocus)
            self.sort_button.setFocusPolicy(Qt.NoFocus)

        self.connect(self.add_button, SIGNAL("clicked()"), self.add)
        self.connect(self.delete_button, SIGNAL("clicked()"), self.delete)
        self.connect(self.close_button, SIGNAL("clicked()"), self.accept)
        
        self.setWindowTitle("Reference Data")

    def add(self):
        """
        add(self)
            Adds a new row
        """
        row = self.model.rowCount()
        self.model.insertRow(row)
        index = self.model.index(row, 1)
        self.table_view.setCurrentIndex(index)
        self.table_view.edit(index)

    def delete(self):
        """
        delete(self)
            Deletes an existent row
        """
        rows = set([index.row() for index in self.table_view.selectedIndexes()])
        if rows is not None and len(rows) == 1:
            row = rows.pop()
            if QMessageBox.warning(self, "Reference Data", "Delete row {0}"
                " from table?".format(row + 1),
                    QMessageBox.Yes | QMessageBox.No) == QMessageBox.No:
                return
            deleted = self.model.deleteRowFromTable(row)
            if deleted:
                self.model.select()
                return
        QMessageBox.warning(None, "Reference Data","Error deleting: One (and"
                " only one) row must be selected")

def create_fake_data():
    """
    createFakeData()
        Dummy function for database initialization
    """
    print("Dropping table...")
    query = QSqlQuery()
    query.exec_("DROP TABLE reference")
    QApplication.processEvents()

    print("Creating tables...")
    query.exec_("""CREATE TABLE reference (
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
        category VARCHAR(30) NOT NULL,
        shortdesc VARCHAR(30) NOT NULL,
        longdesc VARCHAR(80))""")
    QApplication.processEvents()

def get_data():
    """
    get_data()
    """
    filename = os.path.join(os.path.dirname(__file__), "reference.db")
    create = not QFile.exists(filename)
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName(filename)
    if not db.open():
        QMessageBox.warning(None, "Reference Data",
            QString("Database Error: %1")
            .arg(db.lastError().text()))
        sys.exit(1)

    if create:
        create_fake_data()
    return db

if __name__ == '__main__':
    application = QApplication(sys.argv)
    db = get_data()
    application.processEvents()
    ref_data = ReferenceDataDlg()
    ref_data.show()
    application.exec_()
    del db
