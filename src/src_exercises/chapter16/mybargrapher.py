#!/usr/bin/env python
# -*- Encoding: utf-8 -*-
"""
This files solves Chpater 16 exercise from Rapid GUI Programming with Python
and Qt boook:
    Create an application that shows two widgets: a QListView and a custom Bar-
GraphView. The data should be held in a custom BarGraphModel. The user should
be able to edit the data through the QListView, using a custom BarGraphDelegate
to control both the presentation and the editing of data items in the list
view. The application is shown in Figure 16.5 from book.
"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from future_builtins import *

import random
import sys
from PyQt4.QtCore import (QVariant, Qt, QAbstractListModel, QModelIndex,
        QSize, SIGNAL, QString)
from PyQt4.QtGui import (QApplication, QHBoxLayout, QDialog, QListView, QFontMetrics,
        QWidget, QPixmap, QPainter, QColor)
class BarGraphModel(QAbstractListModel):
        """
        Custom model for chapter 16 exercise
        """
        def __init__(self, values=[], colors={}):
            """
            __init__(self, parent=None)
            """
            super(BarGraphModel, self).__init__()
            self.values = values
            self.colors = colors
            if len(values) != len(colors):
                raise AttributeError("""values and colors must have the same
                        length""")
            elif len(values) == 0:
                self.values, self.colors = fake_random_data() 

        def rowCount(self, index=QModelIndex()):
            """
            rowCount(self, index=QModelIndex())
            """
            return len(self.values)

        def data(self, index, role=Qt.DisplayRole):
            """
            data(self, index role)
            """
            if not index.isValid() or not (0 <= index.row() < len(self.values)):
                return QVariant()
            value = ascii(self.values[index.row()])
            color = self.colors[index.row() + 1]
            if role == Qt.DisplayRole:
                return QVariant(QString(value))
            elif role == Qt.TextAlignmentRole:
                return QVariant(int(Qt.AlignRight))
            elif role == Qt.UserRole:
                return QVariant(QColor(color))
            elif role == Qt.DecorationRole:
                pixmap = QPixmap(20,20)
                pixmap.fill(color)
                return QVariant(pixmap)
            else:
                QVariant()

        def setData(self, index, value, role=Qt.EditRole):
            """
            setData(self, index, value, role=Qt.EditRole)
            """
            if index.isValid() and role == Qt.EditRole:
                self.values[index.row()] = value.toInt()[0]
                self.emit(SIGNAL("dataChanged(QModelIndex, QModelIndex)"), index,
                    index)
                return True
            return False

        def flags(self, index):
            """
            flags(self, index)
                Add ItemIsEditable flag
            """
            flag = QAbstractListModel.flags(self, index)
            flag |= Qt.ItemIsEditable
            return flag


from genericdelegates import IntegerColumnDelegate

class MainForm(QDialog):
    def __init__(self, parent=None):
        """
        __init__(self, parent=None)
        """
        super(MainForm, self).__init__(parent)
        self.model = BarGraphModel()
        self.barGraphView = BarGraphView()
        self.barGraphView.setModel(self.model)
        self.listView = QListView()
        self.listView.setModel(self.model)
        self.listView.setItemDelegate(IntegerColumnDelegate(0, 1000, self))
        self.listView.setMaximumWidth(100)
        self.listView.setEditTriggers(QListView.DoubleClicked|QListView.EditKeyPressed)
        layout = QHBoxLayout()
        layout.addWidget(self.listView)
        layout.addWidget(self.barGraphView, 1)
        self.setLayout(layout)
        self.setWindowTitle("Bar Grapher")

                
class BarGraphDelegate(IntegerColumnDelegate):
    """
    Custom item delegate for chapter 16 exercise
    """
    def __init__(self, minv, maxv, parent=None):
        """
        __init__(self, min, max, parent=None)
            minv: Minimun value allowed
            maxv: Maximun value allowd
        """
        super(BarGraphDelegate, self).__init__(minv, maxv, parent)

class BarGraphView(QWidget):
    """
    Custom widget for chapter 16 exercise
    """
    def __init__(self, parent=None):
        """
        __init__(self, parent=None)
        """
        super(BarGraphView, self).__init__(parent)
        self.model = BarGraphModel()

    def setModel(self, model):
        """
        setModel(self, model)
            model: custom model keeping data for chapter 16. It must be a
                BarGraphModel
        """
        if isinstance(model, BarGraphModel):
            self.model = model
            self.connect(self.model, SIGNAL("dataChanged(QModelIndex,"
                "QModelIndex)"), self.size_changed)
            self.connect(self.model, SIGNAL("modelReset()"), self.size_changed)
            self.size_changed()
        else:
            raise TypeError("BarGraphView model must be of BarGraphModel type")

    def size_changed(self):
        """
        size_changed(self)
            Adjusts widget size each time is needed (i.e.: data changed)
        """
        self.resize(self.sizeHint())
        self.update()
        self.updateGeometry()

    def minimunSizeHint(self):
        """
        minimunSizeHint(self)
        """
        fm = QFontMetrics(self.font())
        return QSize(fm.width("1000") + 20, 20 * 4)

    def sizeHint(self):
        """
        sizeHint(self)
        """
        return self.minimunSizeHint()

    def paintEvent(self, event):
        """
        paintEvent(self, event)
        """
        if self.model is None:
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.TextAntialiasing)
        x = 0
        xsize = self.width() / self.model.rowCount()
        height = self.height()
        maxy = max([(self.model.data(self.model.index(row))).toInt()[0]
            for row in
            range(self.model.rowCount())])

        for row in range(self.model.rowCount()):
            value = (self.model.data(self.model.index(row))).toInt()[0]
            ysize = value * height / maxy
            variant = self.model.data(self.model.index(row),Qt.UserRole)
            variant.convert(QVariant.Color)
            painter.setBrush(QColor(variant))
            painter.drawRect(x, height - ysize, xsize, ysize)
            x = x + xsize


def fake_random_data():
    """
    Dummy function used for sample data generation, used by BarGraphModel
    """
    values = [random.randint(0, 1000) for _ in range(20)]
    colors = {}
    [colors.__setitem__(index + 1, random.choice((Qt.white, Qt.black,
        Qt.yellow, Qt.red, Qt.darkRed, Qt.green, Qt.darkGreen, Qt.blue,
        Qt.darkBlue, Qt.cyan, Qt.darkCyan, Qt.magenta, Qt.darkMagenta,
        Qt.darkYellow, Qt.gray, Qt.darkGray, Qt.lightGray))) 
            for index in range(20)]
    return values, colors

if __name__ == '__main__':
    application = QApplication(sys.argv)
    form = MainForm()
    form.show()
    form.resize(600, 480)
    application.exec_()
