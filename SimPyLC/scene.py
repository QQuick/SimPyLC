# ====== Legal notices
#
# Copyright (C) 2013 -2018 GEATEC engineering
#
# This program is free software.
# You can use, redistribute and/or modify it, but only under the terms stated in the QQuickLicense.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY, without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the QQuickLicense for details.
#
# The QQuickLicense can be accessed at: http://www.qquick.org/license.html
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
from inspect import *
import builtins

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# from numpy import *
from .base import *

useTexture = False
if useTexture:
    from PIL import Image

        
class Camera:
    def __init__ (self,
        position = (5, 0, 0),   # Camera position
        focus = (0, 0, 0.7),    # Point looked at
        up = (0, 0, 1),         # Up in the image
        tracking = True
    ):
        self.position = position
        self.focus = focus
        self.up = up
        self.tracking = tracking
       
    def __call__ (self, position = None, focus = None, up = None):
        
        if position:
            self.position = position
        if focus:
            self.focus = focus
        if up:
            self.up = up
        
    def _transform (self, forced):
        if self.tracking or forced:
            glMatrixMode (GL_PROJECTION)
            glLoadIdentity()
            gluPerspective (45, self.scene.width / float (self.scene.height), 1, 100)      
            gluLookAt (*self.position, *self.focus, *self.up)
            glMatrixMode (GL_MODELVIEW)
        
class Scene:
    _dmCheck, _dmUpdate, _dmRender, _dmAsync = range (4)

    def __init__ (self, name = None, width = 600, height = 400):
        self.name = name if name else self.__class__.__name__.lower ()
        self.width = width
        self.height = height
        self.camera = Camera (tracking = False)
        self._displayMode = Scene._dmCheck
        self._async = False
        
    def _registerWithCamera (self):
        self.camera.scene = self
        
    def _registerWithThings (self):                
        for thing in Thing.instances:
            thing.scene = self
         
        if self._displayMode == Scene._dmCheck:
            self.display ()
            if self._async:
                self._displayMode = Scene._dmAsync
            else:
                self._displayMode = Scene._dmUpdate
        else:
            abortInvalidDisplayMode (currentframe ())
        
    def _createWindow (self):
        glutInitWindowSize (self.width, self.height)
        self.window = glutCreateWindow (getTitle (self.name) .encode ('ascii'))
        
        glClearColor (0, 0, 0, 0)
        
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
        
        # Operations related to projection matrix: gluPerspective, gluLookat
        # They will work on the camera

        # Operations related to model view matrix: glTranslate, glRotate, glScale.
        # They will work on the objects
                    
        if self._displayMode in {Scene._dmRender, Scene._dmAsync}:        
            self.camera._transform (False)   # Expensive so only if tracking, not forced
                    
            glLoadIdentity ()
            glClear (GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) 
            
            glPushMatrix ()
            self.display () # Since we'll render in GL_MODELVIEW mode, operations in self.display () will move the objects
            glPopMatrix ()

            glFlush ()
            glutSwapBuffers ()
            
            if self._displayMode == Scene._dmRender:
                self._displayMode = Scene._dmUpdate
            
    def _reshape (self, width, height):
        self.width = width
        self.height = height
        glViewport (0, 0, self.width, self.height)
        self.camera ()
        self.camera._transform (True)        
        
    def update (self):
        if self._displayMode == Scene._dmUpdate:
            self.display ()
            self._displayMode = Scene._dmRender
    
class Thing:
    instances = []

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
        
        Thing.instances.append (self)
        self.checked = False
        
    def _draw (self):
        pass
        
    def __call__ (
        self,
        pivot = None,
        color = None,
        position = (0, 0, 0),   # Dynamic displacement of the center
        shift = (0, 0, 0),      # Dynamic shift of the joint in natural position, so before dynamic rotation
        scale = (1, 1, 1),      # Dynamic multiplication in natural position, so before dynamic rotation, with respect to the joint, done before the shift
        rotation = 0,           # Dynamic rotation angle around pivot through joint
        attitude = None,        # Dynamic 3 x 3 rotation matrix, may be used instead of pivot and rotation
        angle = None,           # Deprecated in favor of 'rotation'             
        
        parts = lambda: None
    ):
        if self.scene._displayMode == Scene._dmCheck:
            if self.checked:                    # If an instance Thing occurs twice in the display function
                self.scene._async = True        # then it has no identity and must be stateless, hence async rather than cached
                
                if self.scene.camera.tracking:
                    warnAsyncTrack (currentframe () .f_back) 
            else:
                self.checked = True
        
            if angle != None:
                warnDeprecated (currentframe () .f_back, "parameter 'angle' of 'Thing.__call__'", "parameter 'rotation'")
                
            parts ()
            
        else:
            if self.scene._displayMode in {Scene._dmUpdate, Scene._dmAsync}:
                if pivot != None:                   # If there's a dynamical center
                    self.pivot = pivot              #   replace the original static center by it
                    
                if color != None:                   # If there's a dynamical color
                    self.color = color              #   replace the original static color by it
                    
                self.position = position
                self.shift = shift
                self.scale = scale
                
                if angle == None:
                    self.rotation = rotation
                else:
                    self.rotation = angle
                    
                self.attitude = attitude
                   
                if self.scene._displayMode == Scene._dmUpdate:
                    parts ()
            
            if self.scene._displayMode in {Scene._dmRender, Scene._dmAsync}:
                # We are in GL_MODELVIEW mode, so the transformations conceptually are performed upon the objects
                #
                # If you think in the global coordinate system then:
                #   - Transformations appear in the code in opposite order, so the first transformation that affects the object is the nearest to drawing the object in the code
                #   - Transformations move the object in the normal direction
                #
                # If you think in the local coordinate system then:
                #   - Transformations appear in the code in normal order, so the last transformation that affecs the object is the nearest to drawing the object in the code
                #   - Transformations move the  coordinate frame in the opposite direction
            
                glPushMatrix ()                                                                 # Remember transformation state before drawing this _thing
                glTranslate (*tAdd (tAdd (self.center, self.position), self.joint))             # 8.    First translate object to get shifted joint into right place
                                                                                                #       (See scene_transformations.jpg)
                if self.attitude is None:                                                       # Use 'is' to be NumPy compatible
                    glRotate (evaluate (self.rotation), *self.pivot)                            # 7b.   Rotate object object over dynamic angle around the shifted joint vector
                else:
                    glMultMatrixd ((                                                            # 7a.   Rotate object according to dynamic attitude around shifted joint point
                        self.attitude [0][0],   self.attitude [1][0],   self.attitude [2][0],   0,
                        self.attitude [0][1],   self.attitude [1][1],   self.attitude [2][1],   0,
                        self.attitude [0][2],   self.attitude [1][2],   self.attitude [2][2],   0,
                        0,                      0,                      0,                      1
                    ))
                                                                                                #       (If arm shifts out, joint shifts in)
                glTranslate (*tEva (self.shift))                                                # 6.    Translate object to put shifted joint in the origin
                glScale (*tEva (self.scale))                                                    # 5.    Scale with respect to joint that's in the origin
                glTranslate (*tNeg (self.joint))                                                # 4.    Translate object to put joint in the origin
                
                glPushMatrix ()
                glRotate (self.angle, *self.axis)                                               # 3.    Rotate object over initial angle to put it in natural position
                glScale (*self.size)                                                            # 2.    Scale to natural size
                glColor (*self.color)
                self._draw ()                                                                   # 1.    Place object with center in origin
                glPopMatrix ()
                
                parts ()                                                                        # Draw parts in local coord frame
                glPopMatrix ()                                                                  # Restore transformation state from before drawing this
        
        return 0    # Make concatenable, e.g. by the + operator
        
class Beam (Thing):
    def __init__ (self, **arguments):
        Thing.__init__ (self, **arguments)
        
    def _draw (self):
        glutSolidCube (1)
            
class Cylinder (Thing):
    def __init__ (self, **arguments):
        Thing.__init__ (self, **arguments)
        
    def _draw (self):
        glTranslate (0, 0, -0.5)
        glutSolidCylinder (0.5, 1, 100, 1)
        
class Ellipsoid (Thing):
    def __init__ (self, **arguments):
        Thing.__init__ (self, **arguments)

    def _draw (self):
        glutSolidSphere (0.5, 100, 100)
        
class Cone (Thing):
    def __init__ (self,  **arguments):
        Thing.__init__ (self, **arguments)
        
    def _draw (self):
        glTranslate (0, 0, -0.5)
        glutSolidCone (0.5, 1, 100, 100)
