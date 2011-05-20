#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
Created on 10/04/2011

@author: rdc
'''
import sys

from PyQt4 import QtGui, QtCore

from ui_ticket_order_hor import Ui_TicketOrderDlg

MAC = "qt_mac_set_native_menubar" in dir()

class TicketOrderDlg(QtGui.QDialog, Ui_TicketOrderDlg):
    '''
    TicketOrderDlg implements ticket_order_hor.ui as designed in QT Designer
    '''

    def __init__(self, parent=None):
        '''
        Constructor
        '''
        super(TicketOrderDlg, self).__init__(parent)
        self.setupUi(self)
        if not MAC:
            self.button_box.button(QtGui.QDialogButtonBox.Ok).\
                setFocusPolicy(QtCore.Qt.NoFocus)
            self.button_box.button(QtGui.QDialogButtonBox.Cancel).\
                setFocusPolicy(QtCore.Qt.NoFocus)
        self.update()
        self.connect(self.price_spin_box, QtCore.SIGNAL("valueChanged(int)"),
                                                        self.update)
        self.connect(self.quantity_spin_box, QtCore.SIGNAL("valueChanged(int)"),
                                                        self.update)
        self.connect(self.customer_line_edit, QtCore.SIGNAL\
                    ("textEdited(QString)"),self.update)
        self.date = QtCore.QDate().currentDate();
        self.dateTimeEdit.setDateRange(self.date.addDays(1),
                                       self.date.addYears(1))
        
    def update(self):
        '''
        Method used to update amount line edit
        '''
        amount = self.price_spin_box.value() * self.quantity_spin_box.value()
        self.amount_line_edit.setText('$ {0:.2f}'.format(amount))
        self.button_box.button(QtGui.QDialogButtonBox.Ok).setEnabled(\
            not self.customer_line_edit.text().isEmpty() and amount)
  
    def result(self):
        '''
        Return a 4-tuple (customer, date, price, quantity)
        '''
        year, month, day = self.dateTimeEdit.date().getDate()
        return (unicode(self.customer_line_edit.text()), 
                unicode("{0}/{1}/{2}".format(day, month, year)), 
                self.price_spin_box.value(), self.quantity_spin_box.value())     

def main():
    '''
    Main program for testing purposes
    '''
    app = QtGui.QApplication(sys.argv)
    to = TicketOrderDlg()
    to.show()
    app.exec_()
    print(to.result())

if __name__ == '__main__':
    main() 