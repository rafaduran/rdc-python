'''
Created on 11/03/2011

@author: rdc
'''
import sys

from PyQt4 import QtCore
from PyQt4.QtGui import (QApplication, QDialog, QDoubleSpinBox, QComboBox,
                         QGridLayout, QLabel) 

class Interest(QDialog):
    """
    Interest dialog, for a given amount, rate and years shows compound
    interest.
    """
    def __init__(self, parent=None):
        """init method for interest dialog"""
        super(Interest, self).__init__(parent)
        
        self.principal = QDoubleSpinBox()
        self.principal.setRange(0.0, 1000000.0)
        self.principal.setValue(1000.0)
        self.principal.setPrefix('$')
        
        self.rate = QDoubleSpinBox()
        self.rate.setRange(0.0, 100.0)
        self.rate.setValue(5.0)
        self.rate.setSuffix('%')
        
        self.years = QComboBox()
        self.years.addItems(['1 year',] +\
                            [str(i) + ' years' for i in range(2,11)])
        
        self.amount = QLabel('Nothing')        
        
        layout = QGridLayout()
        layout.addWidget(QLabel('Principal'), 0, 0)
        layout.addWidget(self.principal, 0, 1)
        layout.addWidget(QLabel('Rate'), 1, 0)
        layout.addWidget(self.rate, 1, 1)
        layout.addWidget(QLabel('Years'), 2, 0)
        layout.addWidget(self.years, 2, 1)
        layout.addWidget(QLabel('Amount'), 3, 0)
        layout.addWidget(self.amount, 3, 1)
        
        self.setLayout(layout)
        
        self.connect(self.principal, QtCore.SIGNAL("valueChanged(double)"), 
                     self.update_ui)
        self.connect(self.rate, QtCore.SIGNAL("valueChanged(double)"), 
                     self.update_ui)
        self.connect(self.years, QtCore.SIGNAL("currentIndexChanged(int)"), 
                     self.update_ui)
        
        self.update_ui()
        
        self.setWindowTitle('Interest calculator')
    
    def update_ui(self):
        """
        Method used to update interest dialog
        """
        principal = self.principal.value()
        rate = self.rate.value()
        years = self.years.currentIndex()+1
        self.amount.setText('$'+ 
                            str(principal * ((1 + (rate / 100.0)) ** years)))
        
def main():
    """main method"""
    app = QApplication(sys.argv)
    interest = Interest()
    interest.show()
    app.exec_()
    
if __name__ == '__main__':
    main()