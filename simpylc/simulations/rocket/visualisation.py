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

import random as rd

import simpylc as sp

import common as cm

rd.seed ()

'''

      z
      |
      o -- y
     /
    x

'''


class Visualisation (sp.Scene):
    def __init__ (self):
        sp.Scene.__init__ (self)
        
        self.camera = sp.Camera ()
        
        self.earth = sp.Ellipsoid (size = 3 * (cm.earthDiam,), center = (0, 0, 0), color = (0, 0, 0.9))
        self.moon = sp.Ellipsoid (size = 3 * (cm.moonDiam,), center = (0, 0, cm.earthMoonDist), color = (0.6, 0.6, 0.6))

        self.body = sp.Cylinder (size = (0.3, 0.3, 1), center = (0, 0, 0.85 + 0.4), pivot = (0, 0, 1), color = (1, 1, 0.2))
        self.nose = sp.Cone (size = (0.3, 0.3, 0.5), center = (0, 0, 0.75), color = (1, 1, 0.2))
        self.bracket = sp.Cylinder (size = (0.1, 0.1, 0.1), center = (0, 0, -0.55), color = (1, 1, 0.2))
        self.gimbal = sp.Ellipsoid (size = 3 * (0.12,), center = (0, 0, -0.05), pivot = (1, 0, 0), color = (1, 1, 0.2))
        self.thruster = sp.Cone (size = (0.2, 0.2, 0.3), pivot = (0, -1, 0), center = (0, 0, -0.09), joint = (0, 0, 0.09), color = (1, 1, 0.2))   # See thruster_rotation.jpg for pivot
                                                                                                                                               # Center at -(0.3/2 - 0.12/2)
        self.flame = sp.Cone (size = (0.1, 0.1, 1), center = (0, 0, -0.65), joint = (0, 0, 0.5), axis = (0, 1, 0), angle = 180, color = (1, 0.7, 0))
        self.tankRed = sp.Ellipsoid (size = 3 * (0.1,), center = (0.16, 0, 0), color = (1, 0, 0))
        self.tankGreen = sp.Ellipsoid (size = 3 * (0.1,), center = (-0.16, 0, 0), color = (0, 1, 0))
        self.tankYellow = sp.Ellipsoid (size = 3 * (0.1,), center = (0, 0.16, 0), color = (1, 1, 0))
        self.tankBlue = sp.Ellipsoid (size = 3 * (0.1,), center = (0, -0.16, 0), color = (0, 0, 1))
 
    def display (self):
        self.camera (
            position = sp.tEva ((sp.world.rocket.positionX + 4, sp.world.rocket.positionY, sp.world.rocket.positionZ)),
            focus = sp.tEva ((sp.world.rocket.positionX, sp.world.rocket.positionY, sp.world.rocket.positionZ + 1.5))
        )
    
        self.earth ()
        self.moon ()
    
        self.body (
            position = sp.tEva ((sp.world.rocket.positionX, sp.world.rocket.positionY, sp.world.rocket.positionZ)),
            attitude = sp.world.rocket._shipRotMat,
            parts = lambda:
                self.nose () +
                self.bracket (
                    parts = lambda:
                        self.tankGreen () +
                        self.tankRed () +
                        self.tankBlue () +            
                        self.tankYellow () +
                        self.gimbal (
                            rotation = sp.world.rocket.blueYellowAngle,
                            parts = lambda:
                                self.thruster (
                                    rotation = sp.world.rocket.greenRedAngle,
                                    parts = lambda:
                                        self.flame (
                                            scale = sp.tsMul ((1, 1, 1),
                                            sp.world.rocket.thrust / sp.world.rocket.thrusterMaxForce * (0.9 + 0.1 * rd.random ())),
                                            color = (1, 0.3 + 0.7 * rd.random (), 0))
        )       )       )       )
        
