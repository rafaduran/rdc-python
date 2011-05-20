'''
Created on 21/03/2011

@author: rdc
'''
import sys

from PyQt4 import QtCore
from PyQt4.QtGui import (QApplication, QDialog, QListWidget, QPushButton, 
                         QVBoxLayout, QGridLayout, QInputDialog, QLineEdit, 
                         QMessageBox) 

class StringListDlg(QDialog):
    '''
    Dialog used to manage a text list: Add items, edit items, remove items, up
    items, down items and sort items are allowed.
    '''
    def __init__(self, name, initial_list=None, parent=None):
        """
        Init method, adds a QListWidget initialized with a list given as second
        parameter and all buttons needed to manage the list. The window is
        titled with 'Edit name List', where name is the first parameter.
        """
        super(StringListDlg, self).__init__(parent)
        self.name = name
        
        self.stringlist = QtCore.QStringList()
        
        self.list_widget = QListWidget(self)
        self.list_widget.addItems(initial_list)
        add_button = QPushButton("&Add...")
        edit_button = QPushButton("&Edit...")
        remove_button = QPushButton("&Remove...")
        up_button = QPushButton("&Up")
        down_button = QPushButton("&Down")
        sort_button = QPushButton("&Sorted")
        close_button = QPushButton("Close")
        
        button_layout = QVBoxLayout()
        button_layout.addWidget(add_button)
        button_layout.addWidget(edit_button)
        button_layout.addWidget(remove_button)
        button_layout.addWidget(up_button)
        button_layout.addWidget(down_button)
        button_layout.addWidget(sort_button)
        button_layout.addWidget(close_button)
        
        layout = QGridLayout(self)
        layout.addWidget(self.list_widget, 0, 0)
        layout.addLayout(button_layout, 0, 1)
        self.setLayout(layout)
        
        self.connect(edit_button, QtCore.SIGNAL("clicked()"), self.edit_dlg)
        self.connect(add_button, QtCore.SIGNAL("clicked()"), self.add_dlg)
        self.connect(remove_button, QtCore.SIGNAL("clicked()"), self.remove)
        self.up_button_callback = \
            lambda direction = -1: self.down_up(direction)
        self.connect(up_button, QtCore.SIGNAL("clicked()"), 
                     self.up_button_callback)
        self.down_button_callback = \
            lambda direction = 1: self.down_up(direction)
        self.connect(down_button, QtCore.SIGNAL("clicked()"), 
                     self.down_button_callback)
        self.connect(sort_button, QtCore.SIGNAL("clicked()"), 
                     self.list_widget.sortItems)
        self.connect(close_button, QtCore.SIGNAL("clicked()"), self.close)
        
        self.setWindowTitle('Edit ' + self.name + ' list')
    
    @QtCore.pyqtSlot(int)
    def down_up(self, direction):
        """
        Selected item from list go up/down one position depending on which
        button has been clicked.
        """
        index = self.list_widget.currentRow()
        if (index + direction) >= 0 and (index + direction) <= \
            self.list_widget.count()-1:
            item = self.list_widget.takeItem(index)
            self.list_widget.insertItem(index + direction, item)
            self.list_widget.setCurrentRow(index + direction)
    
    @QtCore.pyqtSlot()    
    def remove(self):
        """
        Remove current item
        """
        index = self.list_widget.currentRow()
        if index is not None:
            if QMessageBox.Yes == QMessageBox.question(self, "Remove %s" % \
              self.name, "Are you sure?", QMessageBox.Yes | QMessageBox.No):
                item = self.list_widget.takeItem(index)
                del(item)
        
    @QtCore.pyqtSlot()
    def add_dlg(self):
        """
        Add items to stringlist
        """
        text, ok_clicked = QInputDialog.getText(self, "Add %s" % self.name, 
                                                "Add %s" % self.name)
        if ok_clicked and not text.isEmpty():
            self.list_widget.insertItem(self.list_widget.currentRow() + 1, 
                                        text)
            
    @QtCore.pyqtSlot()
    def edit_dlg(self):
        """
        Edit items from stringlist
        """
        current_index = self.list_widget.currentRow()
        text, ok_clicked = QInputDialog.getText(self, "Add %s" % self.name, 
            "Add %s" % self.name, QLineEdit.Normal, 
            self.list_widget.item(current_index).text())
        if ok_clicked and not text.isEmpty():
            self.remove()
            self.list_widget.insertItem(current_index, text)
            self.list_widget.setCurrentRow(current_index)
    def reject(self):
        """
        Calls accept
        """
        self.accept()
        
    def accept(self):
        """
        When accepted returns item list
        """
        for index in range(self.list_widget.count()):
            self.stringlist.append(self.list_widget.item(index).text())
        self.emit(QtCore.SIGNAL("AcceptedList(QStringList)"), self.stringlist)
        super(StringListDlg, self).accept()
    
    
        
def main():
    '''
    Main program
    '''
    fruit = ["Banana", "Apple", "Elderberry", "Clementine", "Fig",
             "Guava", "Mango", "Honeydew Melon", "Date", "Watermelon",
             "Tangerine", "Ugli Fruit", "Juniperberry", "Kiwi",
             "Lemon", "Nectarine", "Plum", "Raspberry", "Strawberry",
             "Orange"]
    app = QApplication(sys.argv)
    form = StringListDlg("Fruit", fruit)
    form.show()
    app.exec_()
    print "\n".join([unicode(x) for x in form.stringlist])

if __name__ == '__main__':
    main()