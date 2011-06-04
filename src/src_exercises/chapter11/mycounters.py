#!usr/bin/env python
#-*- Encoding: utf-8 -*-
"""
Counters exercise from 'Rapid GUI Programming with Python and Qt' chapter 11
"""
import sys

from PyQt4.QtGui import (QWidget, QApplication, QPainter, QSizePolicy, QPen)
from PyQt4 import QtCore
from PyQt4.QtCore import QSize

class Squares(object):  #pylint:disable=R0902
    """
    This class keep all information about the squares at Counteres
    """
    def __init__(self, xsize, ysize, numx=3, numy=3):
        """
        __ini__(self, xsize, ysize, nx=3, ny=3)
        xsize:
            total x size
        ysize:
            total y size
        numx:
            x partitions (column number)
        numy:
            y partitions (row number)
        """
        self._square_state = [[0,] * xsize for _y in range(ysize)]
        self._current = (0, 0)
        self._xsize = xsize / numx
        self._ysize = ysize / numy
        self._nx = numx
        self._ny = numy

    @property
    def xsize(self):
        """
        xsize(self)
            _xsize getter
        """
        return self._xsize

    @xsize.setter   #pylint:disable=E1101
    def xsize(self, value): #pylint:disable=E0102
        """
        xsize(self, value)
        value:
            new xsize to be set
        """
        self._xsize = value / self._nx

    @property
    def ysize(self):
        """
        ysize(self)
            _ysize getter
        """
        return self._ysize

    @ysize.setter #pylint:disable=E1101
    def ysize(self, value): #pylint:disable=E0102
        """
        xsize(self, value)
        value:
            new ysize to be set
        """
        self._ysize = value / self._ny

    @property
    def current(self):  #pylint:disable=E0202
        """
        current(self) return tuple: _current
        _current getter
        """
        return self._current

    @current.setter #pylint:disable=E1101
    def current(self, pos): #pylint:disable=E0102,E0202
        """
        current(self, pos)
        pos:
            should be (x,y) coordenates tuple, used to set the current square
        """
        self._current = self.index_of(pos)

    @property
    def square_state(self): #pylint:disable=E0202
        """
        square_state(self) return int: represents square state of current
        square
        """
        return self._square_state[self._current[0]][self._current[1]]

    @square_state.setter    #pylint:disable=E1101
    def square_state(self, value):  #pylint:disable=E0102,E0202
        """
        square_state(self, value)
            We change state to value for current square.
        """
        if value > 2 or value < 0:
            raise ValueError("States values can be only 0, 1 or 2")
        self._square_state[self.current[0]][self._current[1]] = value

    def next_state(self):
        """
        next_state(self)
            Current square changes state to the next
        """
        self._square_state[self._current[0]][self._current[1]] = \
        (self._square_state[self._current[0]][self._current[1]] + 1) % 3
        
    def index_of(self, pos):
        """
        index_of(self, pos)
        pos:
            should be (x,y) coordenates tuple, used for looking for matching
            square
        """
        if isinstance(pos, tuple) and len(pos) == 2 and \
        isinstance(pos[0],int) and isinstance(pos[1], int):
            xcurrent, ycurrent = None, None
            for xindex in range(self._nx):
                for yindex in range(self._ny):
                    if pos[0] >= xindex * self._xsize and pos[0] < \
                   (xindex+1) * self._xsize:
                        xcurrent = xindex
                    if yindex * self._ysize <= pos[1] and (yindex+1) * \
                    self._ysize > pos[1]:
                        ycurrent = yindex
            if xcurrent is not None and ycurrent is not None:
                return (xcurrent, ycurrent)
            else:
                raise ValueError(pos[0], pos[1])
        else:
            raise TypeError

    def __iter__(self):
        """
        __iter__(Self) return a 3 tuple each time: (x, y, state)
            where: x, y are square vortix coordinates and state is square state
        """
        old_current = self._current
        self._current = 0
        for xindex in range(self._nx):
            for yindex in range(self._ny):
                yield (xindex * self._xsize, yindex * self._ysize,
                        self._square_state[xindex][yindex])
                self._current = self._current + 1
        else:
            self._current = old_current

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
        self.squares = Squares(600, 600)
        self.setMinimumSize(self.minimumSizeHint())

    def sizeHint(self): #pylint:disable=C0103,R0201
        """
        sizeHint(self)
        """
        return QSize(600, 600)

    def minimumSizeHint(self):  #pylint:disable=R0201,C0103
        """
        minimunSizeHint(self)
        """
        return QSize(100, 100)

    def paintEvent(self, event=None):   #pylint:disable=C0103,W0613
        """
        paintEvent(self):   We set here how Counters widget will be painted
                            each time is needed
        """
        painter = QPainter(self)
        painter.setPen(QtCore.Qt.SolidLine)
        painter.setRenderHint(QPainter.Antialiasing)
        
        for square in self.squares:
            painter.drawRect(square[0], square[1], self.squares.xsize, 
                    self.squares.ysize)
            if square[2] == 1:                
                painter.setBrush(QtCore.Qt.red)
                painter.drawEllipse(square[0], square[1], self.squares.xsize, 
                        self.squares.ysize)
            elif square[2] == 2:
                painter.setBrush(QtCore.Qt.yellow)
                painter.drawEllipse(square[0], square[1], self.squares.xsize, 
                        self.squares.ysize)
            painter.setBrush(QtCore.Qt.NoBrush)
        else:
            painter.setPen(QPen(QtCore.Qt.blue, 3))
            xindex, yindex = self.squares.current
            painter.drawRect(xindex * self.squares.xsize, yindex * 
                self.squares.ysize, self.squares.xsize, self.squares.ysize)

    def resizeEvent(self, event=None):  #pylint:disable=C0103
        """
        resizeEvent(self, event)
        event:
            Event triggering the resize
        """
        self.squares.xsize = self.width()
        self.squares.ysize = self.height()
        event.accept()

    def mousePressEvent(self, event=None): #pylint:disable=C0103
        """
        mousePressEvent(self, event=None)
        self:
            object reference
        event:
            event triggered
        """
        if event.button() == QtCore.Qt.LeftButton:
            xpos = event.pos().x()
            ypos = event.pos().y()
            old_current = self.squares.current
            self.squares.current = (xpos, ypos)
            if old_current == self.squares.current:
                self.squares.next_state()
            self.update()

    def keyPressEvent(self, event): #pylint:disable=C0103
        """
        keyPressEvent(self, event)
        self:
            object reference
        event:
            event triggered
        """
        xindex, yindex = self.squares.current
        change = False
        if event.key() == QtCore.Qt.Key_Right and xindex != 2:
            self.squares.current = ((xindex + 1) * self.squares.xsize, yindex *
                    self.squares.ysize)
            change = True
        elif event.key() == QtCore.Qt.Key_Left and xindex != 0:
            self.squares.current = ((xindex - 1) * self.squares.xsize, yindex *
                    self.squares.ysize)
            change = True
        elif event.key() == QtCore.Qt.Key_Up and yindex != 0:
            self.squares.current = (xindex * self.squares.xsize, (yindex - 1) *
                    self.squares.ysize)
            change = True
        elif event.key() == QtCore.Qt.Key_Down and yindex != 2:
            self.squares.current = (xindex * self.squares.xsize, (yindex + 1) *
                    self.squares.ysize)
            change = True
        elif event.key() == QtCore.Qt.Key_Space:
            self.squares.next_state()
            change = True
        if change:
            self.update()

def test_counters():
    """
    Dummy test function for Counters class
    """
    application = QApplication(sys.argv)    #pylint:disable=C0103
    counter = Counters()                    #pylint:disable=C0103
    counter.show()
    application.exec_()

def test_square():
    """
    Dummy test function for Squares class
    """
    square = Squares(30, 30)
    print square.current
    square.current = (5, 5)
    print square.current
    square.current = (1, 19)
    print square.current
    square.current = (25, 29)
    print square.current
    for squar in square:
        print squar
    print square.current
    
    print square.square_state
    square.square_state = 1
    print square.square_state
    square.next_state()
    print square.square_state
    square.next_state()
    print square.square_state
    square.xsize, square.ysize = 300, 300
    print square.xsize, square.ysize
    square.xsize, square.ysize = 400, 300
    print square.xsize, square.ysize
if __name__ == '__main__':
    test_square()
    test_counters()

