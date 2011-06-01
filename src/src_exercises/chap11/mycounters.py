#!usr/bin/env python
#-*- Encoding: utf-8 -*-
"""
Counters exercise from 'Rapid GUI Programming with Python and Qt' chapter 11
"""
import sys

from PyQt4.QtGui import (QWidget, QApplication, QPainter, QBrush, QSizePolicy,
    QPen)
from PyQt4 import QtCore
from PyQt4.QtCore import QSize

class Squares(object):
    """
    This class keep all information about the squares at Counteres
    """
    def __init__(self, xsize, ysize, nx=3, ny=3):
        """
        __ini__(self, xsize, ysize, nx=3, ny=3)

        xsize:
            total x size

        ysize:
            total y size

        nx:
            x partitions (column number)

        ny:
            y partitions (row number)
        """
        self._square_states = [[0,] * xsize for _y in range(ysize)]
        self._current = (0, 0)
        self._xsize = xsize / nx
        self._ysize = ysize / ny
        self._nx = nx
        self._ny = ny

    @property
    def current(self):
        """
        current(self) return tuple: _current
        _current getter
        """
        return self._current

    @current.setter
    def current(self, pos):
        """
        current(self, pos)

        pos:
            (x,y) should be coordenates tuple, used to set the current square
        """
        if isinstance(pos, tuple) and len(pos) == 2 and \
        isinstance(pos[0],int) and isinstance(pos[1], int):
            xcurrent, ycurrent = None, None
            for xindex in range(self._nx):
                for yindex in range(self._ny):
                    if pos[0] > xindex * self._xsize and pos[0] <\
                    (xindex+1) * self._xsize:
                        xcurrent = xindex
                    if yindex * self._ysize <= pos[1] and (yindex+1) *\
                    self._ysize > pos[1]:
                        ycurrent = yindex
            if xcurrent is not None and ycurrent is not None:
                self._current = (xcurrent, ycurrent)
            else:
                raise ValueError
        else:
                raise TypeError
    def __iter__(self):
        """
        __iter__(Self) return tuple's list: ((x,y), state)
            (x, y) square vortix coordinates
            state: square state
        """
        for xindex in range(self._nx):
            for yindex in range(self._n):
                yield ((xindex * self._xsize, yindex * self._ysize),
                    self._square_states[xindex][yindex])

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
        self.setSizePolicy(QSizePolicy.Expanding, #pylint:disable=C0103
                QSizePolicy.Expanding) #pylint:disable=C0103
        self.current = [0, 0]
        self.squares = [[0, 0, 0] for _ in range(3)]
        self.setMinimumSize(self.minimumSizeHint())

    def sizeHint(self): #pylint:disable=C0103,R0201
        """
        sizeHint(self)
        """
        return QSize(600, 600)

    def minimumSizeHint(self):
        """
        minimunSizeHint(self)
        """
        return QSize(100, 100)

    def paintEvent(self, event=None):   #pylint:disable=C0103
        """
        paintEvent(self):   We set here how Counters widget will be painted
                            each time is needed
        """
        ysize = self.height() / 3
        xsize = self.width() / 3

        painter = QPainter(self)
        painter.setPen(QtCore.Qt.SolidLine)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(event.rect(), QBrush(QtCore.Qt.white))

        for xindex in range(3):
            for yindex in range(3):
                painter.setBrush(QtCore.Qt.white)
                painter.drawRect(xindex * xsize, yindex * ysize, xsize, ysize)
            if self.squares[xindex][yindex] == 1:
                print xindex, yindex, "1"
                painter.setBrush(QtCore.Qt.red)
                painter.drawEllipse(xindex * xsize, yindex * ysize, xsize,
                        ysize)
            elif  self.squares[xindex][yindex] == 2:
                print xindex, yindex, "2"
                painter.setBrush(QtCore.Qt.yellow)
                painter.drawEllipse(xindex * xsize, yindex * ysize, xsize,
                        ysize)

        painter.setBrush(QtCore.Qt.NoBrush)
        painter.setPen(QPen(QBrush(QtCore.Qt.SolidPattern), 4.0,
            QtCore.Qt.SolidLine))
        painter.drawRect(self.current[0] * xsize ,
                self.current[1] * ysize,
                xsize, ysize)
    def test():
        for index, state in enumerate(self.square_states):
            if(state == 1):
                painter.setBrush(QtCore.Qt.red)
                painter.drawEllipse(self.points[square_to_point[index]][0],
                        self.points[square_to_point[index]][1], 200,200)
            if(state == 2):
                painter.setBrush(QtCore.Qt.yellow)
                painter.drawEllipse(self.points[square_to_point[index]][0],
                        self.points[square_to_point[index]][1], 200,200)

        painter.setBrush(QtCore.Qt.NoBrush)
        painter.setPen(QPen(QBrush(QtCore.Qt.SolidPattern), 4.0,
            QtCore.Qt.SolidLine))
        painter.drawRect(self.points[square_to_point[self.current]][0],
            self.points[square_to_point[self.current]][1], 200,200)


    def mousePressEvent(self, event=None): #pylint:disable=C0103
        """
        mousePressEvent(self, event=None)

        self:
            object reference

        event:
            event triggerid
        """
        if event.button() == QtCore.Qt.LeftButton:
            xpos = event.pos().x()
            ypos = event.pos().y()
            square = self.coord_to_square(xpos, ypos)
            self.square_states[square] = (self.square_states[square] + 1) % 3
            self.current = square
            self.update()
            event.accept()
        else:
            event.ignore()

    def keyPressEvent(self, event): #pylint:disable=C0103
        """
        keyPressEvent(self, event)

        self:
            object reference

        event:
            event triggered
        """
        if event.key() == QtCore.Qt.Key_Right and self.current[0] != 2:
            self.current[0] = self.current[0] + 1
        elif event.key() == QtCore.Qt.Key_Left and self.current[0] != 0:
            self.current[0] = self.current[0] - 1
        elif event.key() == QtCore.Qt.Key_Up and self.current[1] != 0:
            self.current[1] = self.current[1] - 1
        elif event.key() == QtCore.Qt.Key_Down and self.current[1] != 2:
            self.current[1] = self.current[1] + 1
        elif event.key() == QtCore.Qt.Key_Space:
            self.squares[self.current[0]][self.current[1]] = \
                (self.squares[self.current[0]][self.current[1]] + 1) % 3
            print self.squares[self.current[0]][self.current[1]]

        self.update()

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

def test_counters():
    application = QApplication(sys.argv)    #pylint:disable=C0103
    counter = Counters()                    #pylint:disable=C0103
    counter.show()
    application.exec_()

def test_square():
    square = Squares(30, 30)
    print square.current
    square.current = (5,5)
    print square.current
    square.current = (1,19)
    print square.current
    square.current = (25, 29)
    print square.current
    for sq in square:
        print sq

if __name__ == '__main__':
    test_square()

