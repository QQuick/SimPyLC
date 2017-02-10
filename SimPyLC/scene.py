# ====== Legal notices
#
# Copyright (C) 2013 GEATEC engineering
#
# This program is free software.
# You can use, redistribute and/or modify it, but only under the terms stated in the QQuickLicence.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY, without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the QQuickLicence for details.
#
# The QQuickLicense can be accessed at: http://www.geatec.com/qqLicence.html
#
# __________________________________________________________________________
#
#
#  THIS PROGRAM IS FUNDAMENTALLY UNSUITABLE FOR CONTROLLING REAL SYSTEMS !!
#
# __________________________________________________________________________
#
# It is meant for training purposes only.
#
# Removing this header ends your licence.
#

from time import *
from math import *
import builtins

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from numpy import *

from .base import *

useTexture = False
if useTexture:
    from PIL import Image

class Scene:
    def __init__ (self, name = None, width = 600, height = 400):
        self.name = name if name else self.__class__.__name__.lower ()
        self.width = width
        self.height = height
        
    def _createWindow (self):
        glutInitWindowSize (self.width, self.height)
        self.window = glutCreateWindow (getTitle (self.name) .encode ('ascii'))
        
        glEnable (GL_LINE_SMOOTH)
        glEnable(GL_BLEND);
        glEnable (GL_MULTISAMPLE)
        glEnable (GL_DEPTH_TEST)
        
        glShadeModel (GL_SMOOTH)
        glHint (GL_LINE_SMOOTH_HINT, GL_DONT_CARE)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glLineWidth (1.5)
        
        glEnable (GL_LIGHTING)
        glColorMaterial (GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
        glEnable (GL_COLOR_MATERIAL)

        glLight (GL_LIGHT0, GL_POSITION, (5, 5, 0, 0))
        glLight (GL_LIGHT0, GL_DIFFUSE, (0.2, 0.2, 0.2))
        glEnable (GL_LIGHT0)
        
        glLight (GL_LIGHT1, GL_POSITION, (5, -5, 0, 0))
        glLight (GL_LIGHT1, GL_DIFFUSE, (0, 0, 0.6))
        glEnable (GL_LIGHT1)
        
        glLight (GL_LIGHT3, GL_POSITION, (0, 0, 5, 0))
        glLight (GL_LIGHT3, GL_DIFFUSE, (0.1, 0.1, 0.5))
        glEnable (GL_LIGHT3)
        
        glLight (GL_LIGHT4, GL_POSITION, (0, 0, -1, 0))
        glLight (GL_LIGHT4, GL_DIFFUSE, (0.05, 0, 0))
        glEnable (GL_LIGHT4)
        
        glutDisplayFunc (self._display)
        glutReshapeFunc (self._reshape)
        
    def _display (self):
        glMatrixMode (GL_MODELVIEW)
        glLoadIdentity ()
        glClearColor (0, 0, 0, 0)   
    
        glClear (GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) 
        
        glPushMatrix ()
        self.display ()
        glPopMatrix ()
        
        glFlush ()
        
        glutSwapBuffers ()
        
    def _reshape (self, width, height):
        glViewport (0, 0, width, height)
        glMatrixMode (GL_PROJECTION)
        glLoadIdentity()
        gluPerspective (45, width / float (height), 2, 10)      
        gluLookAt (5, 0, 0, 0, 0, 0.7, 0, 0, 1) 
                
def tNeg (v):
    return (-v [0], -v [1], -v [2])
    
def tAdd (v0, v1):
    return (v0 [0] + v1 [0], v0 [1] + v1 [1], v0 [2] + v1 [2])
    
def tSub (v0, v1):
    return (v0 [0] - v1 [0], v0 [1] - v1 [1], v0 [2] - v1 [2])
        
def tMul (s, v):
    return (s * v [0], s * v [1], s * v [2])
    
def tDiv (v, s):
    s = float (s)
    return (v [0] / s, v [1] / s, v [2] / s)
    
def tNor (v):
    return sqrt (v [0] * v [0] + v [1] * v[1] + v [2] * v [2])
    
def tUni (v):
    return divide (v, norm (v))
    
class _Thing:

    def __init__ (self, size = (0, 0, 0), axis = (0, 0, 1), angle = 0, center = (0, 0, 0), joint = (0, 0, 0), pivot = (0, 0, 1), color = (1, 1, 1)):
        self.size = size
        self.axis = axis
        self.angle = angle
        self.center = center
        self.joint = joint
        self.pivot = pivot
        self.color = color
        
    def __call__ (self, angle = 0, shift = (0, 0, 0), color = None, parts = lambda: None):
        if color != None:
            self.color = color
        glPushMatrix ()
        glTranslate (*tAdd (self.center, self.joint))   # Put joint at correct position
        glRotate (evaluate (angle), *self.pivot)        # Rotate over varying angle parameter, so NOT fixed self.angle attribute, around self.pivot to move
        glTranslate (*shift)                            # Put joint at correct position
        glTranslate (*tNeg (self.joint))                # Put joint in origin
        glPushMatrix ()
        glRotate (self.angle, *self.axis)               # Rotate over fixed self.angle attribute, set by the constructor, around self.axis to achieve intial attitude
        glColor (*self.color)
        self._draw ()
        glPopMatrix ()
        parts ()
        glPopMatrix ()
        return 0                                        # Make concatenable by e.g. + operator
        
class Beam (_Thing):
    def __init__ (self, **arguments):
        _Thing.__init__ (self, **arguments)
        
    def _draw (self):
        glScale (*self.size)
        glutSolidCube (1)
            
class Cylinder (_Thing):
    def __init__ (self, **arguments):
        _Thing.__init__ (self, **arguments)
        
    def _draw (self):
        glScale (*self.size)
        glTranslate (0, 0, -0.5)
        glutSolidCylinder (0.5, 1, 100, 1)