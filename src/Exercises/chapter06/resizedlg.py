#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
Created on 24/03/2011

@author: rdc

Implements ResizeDlg for image resizing, used in imagechanger
'''
import sys

from PyQt4 import QtCore
from PyQt4.QtGui import (QApplication, QDialog, QSpinBox, QMessageBox, 
                         QGridLayout, QDialogButtonBox, QLabel)

class ResizeDlg(QDialog):
    """
    Dialog class for image resizing
    """ 
    def __init__(self, width, height, parent=None):
        """
        Init method, raises ValueError if given width or height are less 
        than 4
        """
        if width < 4 or height < 4:
            QMessageBox.warning(None, "Error", "Image must be at least 4x4") 
            raise ValueError
        
        super(ResizeDlg, self).__init__(parent)
        
        width_label = QLabel("Width")
        self.width_spinbox = QSpinBox()
        self.width_spinbox.setRange(4, 4 * width)
        self.width_spinbox.setValue(width)
        self.width_spinbox.setAlignment(QtCore.Qt.AlignRight)
        
        height_label = QLabel("Height")
        self.height_spinbox = QSpinBox()
        self.height_spinbox.setRange(4, 4 * height)
        self.height_spinbox.setValue(height)
        self.height_spinbox.setAlignment(QtCore.Qt.AlignRight)
        
        buttons = QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel)
        
        layout = QGridLayout()
        layout.addWidget(width_label, 0, 0)
        layout.addWidget(self.width_spinbox, 0, 1)
        layout.addWidget(height_label, 1, 0)
        layout.addWidget(self.height_spinbox, 1, 1)
        layout.addWidget(buttons, 2, 0, 1, 2)
        
        self.setLayout(layout)
        
        self.connect(buttons, QtCore.SIGNAL("accepted()"), self.accept)
        self.connect(buttons, QtCore.SIGNAL("rejected()"), self.reject)
          
    def result(self):
        """
        Returns 2-tuple (width, heiht) result of the dialog input 
        """
        return (self.width_spinbox.value(), self.height_spinbox.value())

def main():
    """
    Main function to test resizeDlg independently
    """
    app = QApplication(sys.argv)
    re_dlg = ResizeDlg(200, 200)
    re_dlg.show()
    app.exec_()
    print re_dlg.result()

if __name__ == '__main__':
    main()