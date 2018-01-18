# ====== Legal notices
#
# Copyright (C) 2013 - 2018 GEATEC engineering
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

from threading import Thread
from time import *
import builtins

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from .base import *

class Graphics (Thread):
    def __init__ (self, world):
        if world._scenes or world._charts:
            Thread.__init__ (self)
            self.world = world
            self.daemon = True
            self.start ()
                
    def idle (self):
        for scene in self.world._scenes:
            glutSetWindow (scene.window)
            glutPostRedisplay ()
    
        for chart in self.world._charts:
            glutSetWindow (chart.window)
            glutPostRedisplay ()

        sleep (self.world.refresh ())
                
    def run (self): 
        glutInit ()
        glutInitDisplayMode (GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH | GLUT_MULTISAMPLE)

        for scene in self.world._scenes:
            scene._graphics= self
            scene._createWindow ()      
        
        for chart in self.world._charts:
            chart._graphics = self
            chart._createWindow ()
            
        glutIdleFunc (self.idle)
        glutMainLoop ()
        