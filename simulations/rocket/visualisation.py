# ====== Legal notices
#
# Copyright (C) 2013 - 2018 GEATEC engineering
#
# This program is free software.
# You can use, redistribute and/or modify it, but only under the terms stated in the QQuickLicence.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY, without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the QQuickLicence for details.
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
# Removing this header ends your licence.
#

from random import *

from SimPyLC import *

from common import *

seed ()

class Visualisation (Scene):
    def __init__ (self):
        Scene.__init__ (self)
        
        self.camera = Camera ()
        
        self.earth = Ellipsoid (size = 3 * (earthDiam,), center = (0, 0, 0), color = (0, 0, 0.9))
        self.moon = Ellipsoid (size = 3 * (moonDiam,), center = (0, 0, earthMoonDist), color = (0.6, 0.6, 0.6))

        self.body = Cylinder (size = (0.3, 0.3, 1), center = (0, 0, 0.85 + 0.4), pivot = (0, 0, 1), color = (1, 1, 0.2))
        self.nose = Cone (size = (0.3, 0.3, 0.5), center = (0, 0, 0.75), color = (1, 1, 0.2))
        self.bracket = Cylinder (size = (0.1, 0.1, 0.1), center = (0, 0, -0.55), color = (1, 1, 0.2))
        self.gimbal = Ellipsoid (size = 3 * (0.12,), center = (0, 0, -0.05), pivot = (1, 0, 0), color = (1, 1, 0.2))
        self.thruster = Cone (size = (0.2, 0.2, 0.3), pivot = (0, -1, 0), center = (0, 0, -0.09), joint = (0, 0, 0.09), color = (1, 1, 0.2))   # See thruster_rotation.jpg for pivot
                                                                                                                                               # Center at -(0.3/2 - 0.12/2)
        self.flame = Cone (size = (0.1, 0.1, 1), center = (0, 0, -0.65), joint = (0, 0, 0.5), axis = (0, 1, 0), angle = 180, color = (1, 0.7, 0))
        self.tankRed = Ellipsoid (size = 3 * (0.1,), center = (0.16, 0, 0), color = (1, 0, 0))
        self.tankGreen = Ellipsoid (size = 3 * (0.1,), center = (-0.16, 0, 0), color = (0, 1, 0))
        self.tankYellow = Ellipsoid (size = 3 * (0.1,), center = (0, 0.16, 0), color = (1, 1, 0))
        self.tankBlue = Ellipsoid (size = 3 * (0.1,), center = (0, -0.16, 0), color = (0, 0, 1))
 
    def display (self):
        self.camera (
            position = tEva ((world.rocket.positionX + 5, world.rocket.positionY, world.rocket.positionZ + 3)),
            focus = tEva ((world.rocket.positionX, world.rocket.positionY, world.rocket.positionZ + 0.4))
        )
    
        self.earth ()
        self.moon ()
    
        self.body (
            position = tEva ((world.rocket.positionX, world.rocket.positionY, world.rocket.positionZ)),
            attitude = world.rocket._shipRotMat,
            parts = lambda:
                self.nose () +
                self.bracket (
                    parts = lambda:
                        self.tankGreen () +
                        self.tankRed () +
                        self.tankBlue () +            
                        self.tankYellow () +
                        self.gimbal (
                            rotation = world.rocket.blueYellowAngle,
                            parts = lambda:
                                self.thruster (
                                    rotation = world.rocket.greenRedAngle,
                                    parts = lambda:
                                        self.flame (
                                            scale = tsMul ((1, 1, 1),
                                            world.rocket.thrust / world.rocket.thrusterMaxForce * (0.9 + 0.1 * random ())),
                                            color = (1, 0.3 + 0.7 * random (), 0))
        )       )       )       )
        