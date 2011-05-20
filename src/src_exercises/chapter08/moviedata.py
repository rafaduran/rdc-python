#!/usr/bin/env python
# Copyright (c) 2007-8 Qtrac Ltd. All rights reserved.
# This program or module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 2 of the License, or
# version 3 of the License, or (at your option) any later version. It is
# provided for educational purposes and is distributed in the hope that
# it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
# the GNU General Public License for more details.

import bisect
import codecs
import copy_reg
import cPickle
import gzip
from PyQt4.QtCore import * #pylint:disable=W0614
from PyQt4.QtXml import * #pylint:disable=W0614


CODEC = "UTF-8"
NEWPARA = unichr(0x2029)
NEWLINE = unichr(0x2028)
DATEFORMAT = "ddd MMM d, yyyy"


def intFromQStr(qstr):
    i, ok = qstr.toInt()
    if not ok:
        raise ValueError, unicode(qstr)
    return i


def _pickleQDate(date):
    return QDate, (date.year(), date.month(), date.day())
    
def _pickleQString(qstr):
    return QString, (unicode(qstr),)
    
copy_reg.pickle(QDate, _pickleQDate)
copy_reg.pickle(QString, _pickleQString)


def encodedNewlines(text):
    return text.replace("\n\n", NEWPARA).replace("\n", NEWLINE)


def decodedNewlines(text):
    return text.replace(NEWPARA, "\n\n").replace(NEWLINE, "\n")



class Movie(object):
    """A Movie object holds the details of a movie.
    
    The data held are the title, year, minutes length, date acquired,
    and notes. If the year is unknown it is set to 1890. If the minutes
    is unknown it is set to 0. The title and notes are held as QStrings,
    and the notes may contain embedded newlines. Both are plain text,
    and can contain any Unicode characters. The title cannot contain
    newlines or tabs, but the notes can contain both. The date acquired
    is held as a QDate.
    """

    UNKNOWNYEAR = 1890
    UNKNOWNMINUTES = 0

    def __init__(self, title=None, year=UNKNOWNYEAR,
                 minutes=UNKNOWNMINUTES, acquired=None, notes=None,
                 location=None):
        self.title = title
        self.year = year
        self.minutes = minutes
        self.acquired = acquired \
                if acquired is not None else QDate.currentDate()
        self.notes = notes
        self.location = location


class MovieContainer(object):
    """A MovieContainer holds a set of Movie objects.

    The movies are held in a canonicalized order based on their title
    and year, so if either of these fields is changed the movies must be
    re-sorted. For this reason (and to maintain the dirty flag), all
    updates to movies should be made through this class's updateMovie()
    method.
    """

    MAGIC_NUMBER = 0x3051E
    FILE_VERSION = 101 
    
    def __init__(self): 
        self.__fname = QString() 
        self.__movies = [] 
        self.__movieFromId = {} 
        self.__dirty = False 

    def key(self, title, year): 
        text = unicode(title).lower() 
        if text.startswith("a "): 
            text = text[2:] 
        elif text.startswith("an "): 
            text = text[3:] 
        elif text.startswith("the "): 
            text = text[4:] 
            parts = text.split(" ", 1) 
            if parts[0].isdigit(): 
                text = "%08d " % int(parts[0])
            if len(parts) > 1:
                text += parts[1]
        return u"%s\t%d" % (text.replace(" ", ""), year)


    def isDirty(self):
        return self.__dirty


    def setDirty(self, dirty=True):
        self.__dirty = dirty


    def clear(self, clearFilename=True):
        self.__movies = []
        self.__movieFromId = {}
        if clearFilename:
            self.__fname = QString()
        self.__dirty = False


    def movieFromId(self, id):
        """Returns the movie with the given Python ID."""
        return self.__movieFromId[id]


    def movieAtIndex(self, index):
        """Returns the index-th movie."""
        return self.__movies[index][1]


    def add(self, movie):
        """Adds the given movie to the list if it isn't already
        present. Returns True if added; otherwise returns False."""
        if id(movie) in self.__movieFromId:
            return False
        key = self.key(movie.title, movie.year)
        bisect.insort_left(self.__movies, [key, movie])
        self.__movieFromId[id(movie)] = movie
        self.__dirty = True
        return True


    def delete(self, movie):
        """Deletes the given movie from the list and returns True;
        returns False if the movie isn't in the list."""
        if id(movie) not in self.__movieFromId:
            return False
        key = self.key(movie.title, movie.year)
        i = bisect.bisect_left(self.__movies, [key, movie])
        del self.__movies[i]
        del self.__movieFromId[id(movie)]
        self.__dirty = True
        return True


    def updateMovie(self, movie, title, year, minutes=None,
                    notes=None, location=None):
        if location is not None:
            movie.location = location
        if minutes is not None:
            movie.minutes = minutes
        if notes is not None:
            movie.notes = notes
        if title != movie.title or year != movie.year:
            key = self.key(movie.title, movie.year)
            i = bisect.bisect_left(self.__movies, [key, movie])
            self.__movies[i][0] = self.key(title, year)
            movie.title = title
            movie.year = year
            self.__movies.sort()
        self.__dirty = True


    def __iter__(self):
        for pair in iter(self.__movies):
            yield pair[1]


    def __len__(self):
        return len(self.__movies)


    def setFilename(self, fname):
        self.__fname = fname


    def filename(self):
        return self.__fname


    @staticmethod
    def formats():
        return "*.mqb"# *.mpb *.mqt *.mpt"


    def save(self, fname=QString()):
        if not fname.isEmpty():
            self.__fname = fname
        if self.__fname.endsWith(".mqb"):
            return self.saveQDataStream()
        return False, "Failed to save: invalid file extension"


    def load(self, fname=QString()):
        if not fname.isEmpty():
            self.__fname = fname
        if self.__fname.endsWith(".mqb"):
            return self.loadQDataStream()
        return False, "Failed to load: invalid file extension"


    def saveQDataStream(self):
        error = None
        fh = None
        try:
            fh = QFile(self.__fname)
            if not fh.open(QIODevice.WriteOnly):
                raise IOError, unicode(fh.errorString())
            stream = QDataStream(fh)
            stream.writeInt32(MovieContainer.MAGIC_NUMBER)
            stream.writeInt32(MovieContainer.FILE_VERSION)
            stream.setVersion(QDataStream.Qt_4_6)
            for key, movie in self.__movies:
                stream << movie.title
                stream.writeInt16(movie.year)
                stream.writeInt16(movie.minutes)
                stream << movie.acquired << movie.notes
                if movie.location is not None:
                    stream << movie.location
                else:
                    stream << QString()
        except (IOError, OSError), e:
            error = "Failed to save: %s" % e
        finally:
            if fh is not None:
                fh.close()
            if error is not None:
                return False, error
            self.__dirty = False
            return True, "Saved %d movie records to %s" % (
                    len(self.__movies),
                    QFileInfo(self.__fname).fileName())


    def loadQDataStream(self):
        error = None
        fh = None
        try:
            fh = QFile(self.__fname)
            if not fh.open(QIODevice.ReadOnly):
                raise IOError, unicode(fh.errorString())
            stream = QDataStream(fh)
            magic = stream.readInt32()
            if magic != MovieContainer.MAGIC_NUMBER:
                raise IOError, "unrecognized file type"
            version = stream.readInt32()
            if version < MovieContainer.FILE_VERSION:
                stream.setVersion(QDataStream.Qt_4_2)
            elif version == MovieContainer.FILE_VERSION:
                stream.setVersion(QDataStream.Qt_4_6)
            else:
                raise IOError, "new and unreadable file format"
            self.clear(False)
            while not stream.atEnd():
                title = QString()
                acquired = QDate()
                notes = QString()
                location = QString()
                stream >> title
                year = stream.readInt16()
                minutes = stream.readInt16()
                stream >> acquired >> notes >> location
                self.add(Movie(title, year, minutes, acquired, notes, location))
        except (IOError, OSError), e:
            error = "Failed to load: %s" % e
        finally:
            if fh is not None:
                fh.close()
            if error is not None:
                return False, error
            self.__dirty = False
            return True, "Loaded %d movie records from %s" % (
                    len(self.__movies),
                    QFileInfo(self.__fname).fileName())


    def savePickle(self):
        error = None
        fh = None
        try:
            fh = gzip.open(unicode(self.__fname), "wb")
            cPickle.dump(self.__movies, fh, 2)
        except (IOError, OSError), e:
            error = "Failed to save: %s" % e
        finally:
            if fh is not None:
                fh.close()
            if error is not None:
                return False, error
            self.__dirty = False
            return True, "Saved %d movie records to %s" % (
                    len(self.__movies),
                    QFileInfo(self.__fname).fileName())


    def loadPickle(self):
        error = None
        fh = None
        try:
            fh = gzip.open(unicode(self.__fname), "rb")
            self.clear(False)
            self.__movies = cPickle.load(fh)
            for key, movie in self.__movies:
                self.__movieFromId[id(movie)] = movie
        except (IOError, OSError), e:
            error = "Failed to load: %s" % e
        finally:
            if fh is not None:
                fh.close()
            if error is not None:
                return False, error
            self.__dirty = False
            return True, "Loaded %d movie records from %s" % (
                    len(self.__movies),
                    QFileInfo(self.__fname).fileName())

    def exportXml(self, fname):
        error = None
        fh = None
        try:
            fh = QFile(fname)
            if not fh.open(QIODevice.WriteOnly):
                raise IOError, unicode(fh.errorString())
            stream = QTextStream(fh)
            stream.setCodec(CODEC)
            stream << ("<?xml version='1.0' encoding='%s'?>\n"
                       "<!DOCTYPE MOVIES>\n"
                       "<MOVIES VERSION='1.0'>\n" % CODEC)
            for key, movie in self.__movies:
                stream << ("<MOVIE YEAR='%d' MINUTES='%d' "
                           "ACQUIRED='%s'>\n" % (
                        movie.year, movie.minutes,
                        movie.acquired.toString(Qt.ISODate))) \
                       << "<TITLE>" << Qt.escape(movie.title) \
                       << "</TITLE>\n<NOTES>"
                if not movie.notes.isEmpty():
                    stream << "\n" << Qt.escape(
                            encodedNewlines(movie.notes))
                stream << "\n</NOTES>\n" << "<LOCATION>" << movie.location << \
                "</LOCATION>\n" << "</MOVIE>\n"
            stream << "</MOVIES>\n"
        except (IOError, OSError), e:
            error = "Failed to export: %s" % e
        finally:
            if fh is not None:
                fh.close()
            if error is not None:
                return False, error
            self.__dirty = False
            return True, "Exported %d movie records to %s" % (
                    len(self.__movies),
                    QFileInfo(fname).fileName())


    def importDOM(self, fname):
        dom = QDomDocument()
        error = None
        fh = None
        try:
            fh = QFile(fname)
            if not fh.open(QIODevice.ReadOnly):
                raise IOError, unicode(fh.errorString())
            if not dom.setContent(fh):
                raise ValueError, "could not parse XML"
        except (IOError, OSError, ValueError), e:
            error = "Failed to import: %s" % e
        finally:
            if fh is not None:
                fh.close()
            if error is not None:
                return False, error
        try:
            self.populateFromDOM(dom)
        except ValueError, e:
            return False, "Failed to import: %s" % e
        self.__fname = QString()
        self.__dirty = True
        return True, "Imported %d movie records from %s" % (
                    len(self.__movies), QFileInfo(fname).fileName())


    def populateFromDOM(self, dom):
        root = dom.documentElement()
        if root.tagName() != "MOVIES":
            raise ValueError, "not a Movies XML file"
        self.clear(False)
        node = root.firstChild()
        while not node.isNull():
            if node.toElement().tagName() == "MOVIE":
                self.readMovieNode(node.toElement())
            node = node.nextSibling()


    def readMovieNode(self, element):
        def getText(node):
            child = node.firstChild()
            text = QString()
            while not child.isNull():
                if child.nodeType() == QDomNode.TextNode:
                    text += child.toText().data()
                child = child.nextSibling()
            return text.trimmed()

        year = intFromQStr(element.attribute("YEAR"))
        minutes = intFromQStr(element.attribute("MINUTES"))
        ymd = element.attribute("ACQUIRED").split("-")
        if ymd.count() != 3:
            raise ValueError, "invalid acquired date %s" % \
                    unicode(element.attribute("ACQUIRED"))
        acquired = QDate(intFromQStr(ymd[0]), intFromQStr(ymd[1]),
                         intFromQStr(ymd[2]))
        title = notes = location = None
        node = element.firstChild()
        while title is None or location is None:
            if node.isNull():
                raise ValueError, "missing title or notes"
            if node.toElement().tagName() == "TITLE":
                title = getText(node)
            elif node.toElement().tagName() == "NOTES":
                notes = getText(node)
            elif node.toElement().tagName() == "LOCATION":
                location = getText(node)
            node = node.nextSibling()
        if title.isEmpty():
            raise ValueError, "missing title"
        self.add(Movie(title, year, minutes, acquired,
                 decodedNewlines(notes), location))

    def importSAX(self, fname):
        error = None
        fh = None
        try:
            handler = SaxMovieHandler(self)
            parser = QXmlSimpleReader()
            parser.setContentHandler(handler)
            parser.setErrorHandler(handler)
            fh = QFile(fname)
            input = QXmlInputSource(fh)
            self.clear(False)
            if not parser.parse(input):
                raise ValueError, handler.error
        except (IOError, OSError, ValueError), e:
            error = "Failed to import: %s" % e
        finally:
            if fh is not None:
                fh.close()
            if error is not None:
                return False, error
            self.__fname = QString()
            self.__dirty = True
            return True, "Imported %d movie records from %s" % (
                    len(self.__movies), QFileInfo(fname).fileName())


class SaxMovieHandler(QXmlDefaultHandler):

    def __init__(self, movies):
        super(SaxMovieHandler, self).__init__()
        self.movies = movies
        self.text = QString()
        self.error = None


    def clear(self):
        self.year = None
        self.minutes = None
        self.acquired = None
        self.title = None
        self.notes = None
        self.location = None


    def startElement(self, namespaceURI, localName, qName, attributes):
        if qName == "MOVIE":
            self.clear()
            self.year = intFromQStr(attributes.value("YEAR"))
            self.minutes = intFromQStr(attributes.value("MINUTES"))
            ymd = attributes.value("ACQUIRED").split("-")
            if ymd.count() != 3:
                raise ValueError, "invalid acquired date %s" % \
                        unicode(attributes.value("ACQUIRED"))
            self.acquired = QDate(intFromQStr(ymd[0]),
                                  intFromQStr(ymd[1]),
                                  intFromQStr(ymd[2]))
        elif qName in ("TITLE", "NOTES", "LOCATION"): 
            self.text = QString() 
        return True 


    def characters(self, text):
        self.text += text
        return True


    def endElement(self, namespaceURI, localName, qName):
        if qName == "MOVIE":
            if self.year is None or self.minutes is None or \
               self.acquired is None or self.title is None or \
               self.notes is None or self.title.isEmpty():
                raise ValueError, "incomplete movie record"
            if self.location is not None:
                self.movies.add(Movie(self.title, self.year,
                    self.minutes, self.acquired,
                    decodedNewlines(self.notes), self.location))
            else:
                self.movies.add(Movie(self.title, self.year,
                    self.minutes, self.acquired, decodedNewlines(self.notes)))
            self.clear()
        elif qName == "TITLE":
            self.title = self.text.trimmed()
        elif qName == "NOTES":
            self.notes = self.text.trimmed()
        elif qName == "LOCATION":
            self.location = self.text.trimmed()
        return True


    def fatalError(self, exception):
        self.error = "parse error at line %d column %d: %s" % (
                exception.lineNumber(), exception.columnNumber(),
                exception.message())
        return False


