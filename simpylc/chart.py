'''
====== Legal notices

Copyright (C) 2013 - 2021 GEATEC engineering

This program is free software.
You can use, redistribute and/or modify it, but only under the terms stated in the QQuickLicense.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY, without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the QQuickLicense for details.

The QQuickLicense can be accessed at: http://www.qquick.org/license.html

__________________________________________________________________________


 THIS PROGRAM IS FUNDAMENTALLY UNSUITABLE FOR CONTROLLING REAL SYSTEMS !!

__________________________________________________________________________

It is meant for training purposes only.

Removing this header ends your license.
'''

from time import *
from collections import deque
from itertools import islice
from copy import copy
import builtins

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from .base import *

class Entry:
    def __init__ (self, chart, index, height):
        self.chart = chart
        self.index = index
        self.height = height
        self.top = self.chart.entries [-1] .bottom if self.chart.entries else 0
        self.bottom = self.top + self.height
        
    def adapt (self):
        pass
        
    def _render (self):
        pass
        
class Group (Entry):
    def __init__ (self, chart, index, text, height):
        Entry.__init__ (self, chart, index, height)
        self.text = text
            
class Channel (Entry):
    def __init__ (self, chart, index, circuit, min, max, height):
        Entry.__init__ (self, chart, index, height)
        self.circuit = circuit

        self.min = float (evaluate (min))
        self.max = float (evaluate (max))
        self.mean = (self.min + self.max) / 2
        
        self.ceiling = self.top + 2
        self.floor = self.bottom - 2
        self.middle = (self.floor + self.ceiling) / 2
        
        self.scale = (self.floor - self.ceiling) / (self.max - self.min)
        self.values = deque ()
        
    def adapt (self):
        if self.values:
            self.values.rotate (-1)
            self.values [-1] = self.circuit ()

    def _render (self):
        values = copy (self.values)

        glColor (*backgroundFromRgb (self.circuit.color))
        glBegin (GL_QUADS)
        glVertex (0, self.floor)
        glVertex (self.chart.width, self.floor)
        glVertex (self.chart.width, self.ceiling)
        glVertex (0, self.ceiling)
        glEnd ()
        
        glColor (*self.circuit.color)
        glBegin (GL_LINE_STRIP)
        for iValue, value in enumerate (values):
            if value != None:
                value = max (min (value, self.max), self.min)
                glVertex (1 * iValue, self.middle - self.scale * (value - self.mean))
        glEnd ()
        
        glRasterPos (2, self.middle + 5)
        glutBitmapString (GLUT_BITMAP_HELVETICA_12, self.circuit._name.encode ('ascii'))    

class Chart:
    def __init__ (self, name = None, width = 600, height = 400):
        self.name = name if name else self.__class__.__name__.lower ()
        self.width = width
        self.height = height
        self.entries = []
        
    def _createWindow (self):
        glutInitWindowSize (self.width, self.height)
        self.window = glutCreateWindow (getTitle (self.name) .encode ('ascii'))
        
        glEnable (GL_LINE_SMOOTH)
        glEnable(GL_BLEND);
        glEnable (GL_MULTISAMPLE)
        
        glShadeModel (GL_SMOOTH)
        glHint (GL_LINE_SMOOTH_HINT, GL_DONT_CARE)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glLineWidth (1.5)
        
        glDisable (GL_LIGHTING)

        glutDisplayFunc (self._display)
        glutReshapeFunc (self._reshape)
        
    def update (self):
        for entry in self.entries:
            entry.adapt ()
        
    def _render (self):
        glColor (1, 1, 1)
            
        for entry in self.entries:
            entry._render ()
        
    def _display (self):
        glMatrixMode (GL_MODELVIEW)
        glLoadIdentity ()
        glClearColor (* (panelBackgroundColor + (0,)))  
    
        glClear (GL_COLOR_BUFFER_BIT)   
        
        glPushMatrix ()
        glLineWidth (1)
        self._render ()
        glPopMatrix ()
        
        glFlush ()
        
        glutSwapBuffers ()
        
    def _reshape (self, width, height):
        self.width = width
        self.height = height
        
        glViewport (0, 0, width, height)
        glMatrixMode (GL_PROJECTION);       
        glLoadIdentity ()
        glOrtho (0, self.width, self.height, 0, 0, 1)
        
        for entry in self.entries:
            if isinstance (entry, Channel):
                if self.width > len (entry.values):
                    entry.values =  deque ([None for i in range (self.width - len (entry.values))] + list (entry.values))
                else:
                    start = len (entry.values) - self.width
                    stop = None
                    entry.values = deque (islice (entry.values, start, stop))
        
    def group (self, text = '', height = 10):
        self.entries.append (Group (self, len (self.entries), text, height))
        
    def channel (self, circuit, color = None, minimum = 0, maximum = 1, height = 15):
        circuit.color = color
        self.entries.append (Channel (self, len (self.entries), circuit, minimum, maximum, height))
        
