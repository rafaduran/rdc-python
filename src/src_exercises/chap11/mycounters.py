#!usr/bin/env python
#-*- Encoding: utf-8 -*-
"""
Counters exercise from 'Rapid GUI Programming with Python and Qt' chapter 11
"""
#TODO: Square class + SquareContainerClass, supporting all squares information
import sys

from PyQt4.QtGui import (QWidget, QApplication, QPainter, QBrush, QSizePolicy,
    QRegion, QPaintEvent)
from PyQt4 import QtCore
from PyQt4.QtCore import QSize

class Counters(QWidget):
    """
    Counters class is a cutom widget showing a 3 * 3 grid. Each square can have
    three different states:
        - Blank
        - Red ellipse
        - Yellow ellipse
    Each time user clicks inside a square or presses spacebar current square
    (marked with a thick blue pen) will change to the next state following
    swhon order, passing from Yellow state to Blank in an inifinite loop. Arrow
    keys can be used to move throught the squeare.
    """

    def __init__(self, parent = None):
        """
        __init__(self, parent=None)
        
        self:
            object reference
        parent:
            parent widget/window, default=None
        """
        super(Counters, self).__init__(parent)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, #pylint:disable=C0103
                QSizePolicy.Preferred) #pylint:disable=C0103
        sizePolicy.setHeightForWidth(True)
        self.setSizePolicy(sizePolicy) #pylint:disable=C0103
        self.points = None
        self.square_states = [0 for _ in range(9)]

    def heightForWidth(self, width): #pylint:disable=C0103,R0201
        """
        heightForWidth(self, width)
        """
        return width * 1

    def sizeHint(self): #pylint:disable=C0103,R0201
        """
        sizeHint(self)
        """
        return QSize(600, 600)

    def update_states(self):
        """
        update_state(self): Each time occurs an event changing square state
                            this function should be called
        """
        pass

                

    def resizeEvent(self, event=None): #pylint:disable=C0103,R0201
        """
        resizeEvent
        """
        event.ignore()

    def paintEvent(self, event=None):   #pylint:disable=C0103
        """
        paintEvent(self):   We set here how Counters widget will be painted
                            each time is needed
        """
        print self.height(), self.width()
        logical_size = self.height() / 3

        def logicalfromphysical(length, side):
            """
            logicalfromphysical(length, side):  Tiny function to transform
                                                physical to logical coordenates
            """
            return (length / side) * logical_size
        print logicalfromphysical(600, 400)

        self.painter = QPainter(self)
        self.painter.setPen(QtCore.Qt.SolidLine)
        self.painter.setRenderHint(QPainter.Antialiasing)
        self.painter.fillRect(event.rect(), QBrush(QtCore.Qt.white))


        self.points = [(x, y) for x in range(0 , 3 * logical_size +\
            logical_size, logical_size)for y in range(0, 3 *\
            logical_size + logical_size , logical_size)]

        for index in range(4):
            self.painter.drawLine(self.points[index][0], self.points[index][1],
                    self.points[index +12][0], self.points[index + 12][1])
            self.painter.drawLine(self.points[index * 4][0], self.points[index *
                4][1], self.points[4* index + 3][0], self.points[4 *\
                index + 3][1])

        square_to_point = {0: 0, 1: 4, 2: 8, 3: 1, 4: 5, 5: 9, 6: 2, 7: 6, 8:
                10 }

        for index,state in enumerate(self.square_states):
            if(state == 1):
                self.painter.setBrush(QtCore.Qt.red)
                self.painter.drawEllipse(self.points[square_to_point[index]][0],
                        self.points[square_to_point[index]][1], 200,200)
            if(state == 2):
                self.painter.setBrush(QtCore.Qt.yellow)
                self.painter.drawEllipse(self.points[square_to_point[index]][0],
                        self.points[square_to_point[index]][1], 200,200)


    def mousePressEvent(self, event=None): #pylint:disable=C0103
        """
        mousePressEvent(self, event=None)

        self:
            object reference

        event:
            event triggering the mousePressEvent
        """
        if event.button() == QtCore.Qt.LeftButton:
            xpos = event.pos().x()
            ypos = event.pos().y()
            square = self.coord_to_square(xpos, ypos)
            print square
            self.square_states[square] = (self.square_states[square] + 1) % 3
            print self.square_states[square]
            #self.paintEvent(QPaintEvent(QRegion(0, 0, self.height(),
            #    self.width())))
            self.update()
            event.accept()
        else:
            event.ignore()

    def coord_to_square(self, xpos, ypos):
        """
        coord_to_square(self, xpos, ypos)

        self:
            object reference

        xpos:
            x position

        ypos:
            y position
        """
        for index in range(3):
            if xpos > self.points[index * 4][0] and xpos < \
            self.points[index * 4 + 4][0]:
                col = index
            if ypos > self.points[index][1] and ypos < \
            self.points[index + 1][1]:
                row = index

        switch = {(0, 0): 0, (0, 1): 1, (0, 2): 2,
                  (1, 0): 3, (1, 1): 4, (1, 2): 5,
                  (2, 0): 6, (2, 1): 7, (2, 2): 8}

        return switch[row, col]

if __name__ == '__main__':
    application = QApplication(sys.argv)    #pylint:disable=C0103
    counter = Counters()                    #pylint:disable=C0103
    counter.show()
    application.exec_()
