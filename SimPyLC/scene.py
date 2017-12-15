# ====== Legal notices
#
# Copyright (C) 2013 GEATEC engineering
#
# This program is free software.
# You can use, redistribute and/or modify it, but only under the terms stated in the QQuickLicense.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY, without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the QQuickLicense for details.
#
# The QQuickLicense can be accessed at: http://www.geatec.com/qqLicense.html
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
# Removing this header ends your license.
#

from time import *
from math import *
import builtins

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# from numpy import *
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
        # [object coords] > (model view matrix) > [eye coords] (projection matrix) > [clip coords]
        
        # Operations related to model view matrix: glTranslate, glRotate, glScale.
        # They will work on the objects
        
        # Operations related to projection matrix: gluPerspective, gluLookat
        # They will work on the camera

        
        glMatrixMode (GL_MODELVIEW)
        glLoadIdentity ()
        glClearColor (0, 0, 0, 0)   
    
        glClear (GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) 
        
        glPushMatrix ()
        self.display () # Since we're in GL_MODELVIEW mode, operations in self.display () will move the objects
        glPopMatrix ()
        
        glFlush ()
        
        glutSwapBuffers ()
        
    def _reshape (self, width, height):
        glViewport (0, 0, width, height)
        glMatrixMode (GL_PROJECTION)
        glLoadIdentity()
        gluPerspective (45, width / float (height), 2, 10)      
        gluLookAt (
            0, 0, 5,    # Camera position
            0, 0, 0.7,  # Point looked at
            0, 1, 0     # Up in the image
        )
        
def tEva (v):
    return (evaluate (v [0]), evaluate (v [1]), evaluate (v [2]))
                
def tNeg (v):
    return (-v [0], -v [1], -v [2])
    
def tAdd (v0, v1):
    return (v0 [0] + v1 [0], v0 [1] + v1 [1], v0 [2] + v1 [2])
    
def tSub (v0, v1):
    return (v0 [0] - v1 [0], v0 [1] - v1 [1], v0 [2] - v1 [2])
        
def tMul (v0, v1):
    return (x [0] * v [0], x [1] * v [1], x [2] * v [2])

def tsMul (v, x):
    return (v [0] * x, v [1] * x, v [2] * x)
    
def tDiv (v, x):
    return (v [0] / x [0], v [1] / x [1], v [2] / x [2])

def tsDiv (v, x):
    return (v [0] / x, v [1] / x, v [2] / x)
   
def tNor (v):
    return sqrt (v [0] * v [0] + v [1] * v[1] + v [2] * v [2])
    
def tUni (v):
    return divide (v, norm (v))
    
class Nothing:
    def __init__ (
        self,
        size = (0, 0, 0),   # Initial size of the initial bounding box
        
        center = (0, 0, 0), # Initial position of the center with respect to (0, 0, 0) or to the center of the containing element
        axis = (0, 0, 1),   # Initial attitude of the axis of inital rotation around the center
        angle = 0,          # Initial rotation angle
        
        joint = (0, 0, 0),  # Initial position of the axis of dynamical rotation with respect to the center
        pivot = (0, 0, 1),  # Initial attitude of the axis of dynamical rotation around the joint

        rest = (0, 0, 0),   # Inital position of the point that stays at rest when scaling dynamically
        
        color = (1, 1, 1)   # Initial color
    ):
        self.center = center
        self.size = size
        self.axis = axis
        self.angle = angle
        self.joint = joint
        self.pivot = pivot
        self.color = color
        
    def _draw (self):
        pass
        
    def __call__ (
        self,
        pivot = None,
        color = None,
        position = (0, 0, 0),   # Dynamic displacement of the center
        shift = (0, 0, 0),      # Dynamic shift of the joint in natural position, so before dynamic rotation
        scale = (1, 1, 1),      # Dynamic multiplication in natural position, so before dynamic rotation, with respect to the joint, done before the shift
        angle = 0,              # Dynamic rotation angle around pivot through joint
        
        parts = lambda: None
    ):
        # We are in GL_MODELVIEW mode, so the transformations conceptually are performed upon the objects
        #
        # If you think in the global coordinate system then:
        #   - Transformations appear in the code in opposite order, so the first transformation that affects the object is the nearest to drawing the object in the code
        #   - Transformations move the object in the normal direction
        #
        # If you think in the local coordinate system then:
        #   - Transformations appear in the code in normal order, so the last transformation that affecs the object is the nearest to drawing the object in the code
        #   - Transformations move the  coordinate frame in the opposite direction
    
        if pivot != None:                                                               # If there's a dynamical center
            self.pivot = pivot                                                          #   replace the original static center by it
            
        if color != None:                                                               # If there's a dynamical color
            self.color = color                                                          #   replace the original static color by it
            
        glPushMatrix ()                                                                 # Remember transformation state before drawing this _thing
        glTranslate (*tAdd (tAdd (self.center, position), self.joint))                                   # 8.    First translate object to get shifted joint into right place (see scene_transformations.jpg)
        glRotate (evaluate (angle), *self.pivot)                                        # 7.    Rotate object object over dynamic angle around the shifted joint (if arm shifts out, joint shifts in) 
        glTranslate (*tEva (shift))                                                     # 6.    Translate object to put shifted joint in the origin
        glScale (*tEva (scale))                                                         # 5.    Scale with respect to joint that's in the origin
        glTranslate (*tNeg (self.joint))                                                # 4.    Translate object to put joint in the origin
        glPushMatrix ()
        glRotate (self.angle, *self.axis)                                               # 3.    Rotate object over initial angle to put it in natural position
        glScale (*self.size)                                                            # 2.    Scale to natural size
        glColor (*self.color)

        self._draw ()                                                                   # 1.    Place object with center in origin
        glPopMatrix ()
        parts ()                                                                        # Draw parts in local coord frame
        glPopMatrix ()                                                                  # Restore transformation state from before drawing this _thing
        return 0                                                                        # Make concatenable by e.g. + operator
        
class Beam (Nothing):
    def __init__ (self, **arguments):
        Nothing.__init__ (self, **arguments)
        
    def _draw (self):
        glutSolidCube (1)
            
class Cylinder (Nothing):
    def __init__ (self, **arguments):
        Nothing.__init__ (self, **arguments)
        
    def _draw (self):
        glTranslate (0, 0, -0.5)
        glutSolidCylinder (0.5, 1, 100, 1)
        
class Ellipsoid (Nothing):
    def __init__ (self, **arguments):
        Nothing.__init__ (self, **arguments)

    def _draw (self):
        glutSolidSphere (0.5, 100, 100)
        
        
class Cone (Nothing):
    def __init__ (self,  **arguments):
        Nothing.__init__ (self, **arguments)
        
    def _draw (self):
        glTranslate (0, 0, -0.5)
        glutSolidCone (0.5, 1, 100, 100)
