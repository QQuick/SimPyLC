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

from random import *

from SimPyLC import *

seed ()

class Visualisation (Scene):
    def __init__ (self):
        Scene.__init__ (self)
        self.body = Cylinder (size = (0.3, 0.3, 1), center = (0, 0, 1), pivot = (0, 0, 1), color = (1, 1, 0.2))
        self.nose = Cone (size = (0.3, 0.3, 0.5), center = (0, 0, 0.75), color = (1, 1, 0.2))
        self.bracket = Cylinder (size = (0.1, 0.1, 0.1), center = (0, 0, -0.55), color = (1, 1, 0.2))
        self.gimbal = Beam (size = (0.12, 0.12, 0.12), center = (0, 0, -0.05), pivot = (1, 0, 0), color = (1, 1, 0.2))
        self.thruster = Cone (size = (0.2, 0.2, 0.2), center = (0, 0, -0.1), pivot = (0, -1, 0), color = (1, 1, 0.2))   # See thruster_rotation.jpg for pivot
        self.flame = Cone (size = (0.1, 0.1, 1), center = (0, 0, -0.6), joint = (0, 0, 0.5), axis = (0, 1, 0), angle = 180, color = (1, 0.7, 0))
        self.tankRed = Ellipsoid (size = (0.1, 0.1, 0.1), center = (0.1, 0, 0), color = (1, 0, 0))
        self.tankGreen = Ellipsoid (size = (0.1, 0.1, 0.1), center = (-0.1, 0, 0), color = (0, 1, 0))
        self.tankYellow = Ellipsoid (size = (0.1, 0.1, 0.1), center = (0, 0.1, 0), color = (1, 1, 0))
        self.tankBlue = Ellipsoid (size = (0.1, 0.1, 0.1), center = (0, -0.1, 0), color = (0, 0, 1))
        
    def display (self):
        self.body (parts = lambda:
            self.nose () +
            self.bracket (parts = lambda:
                self.tankGreen () +
                self.tankRed () +
                self.tankBlue () +            
                self.tankYellow () +
                self.gimbal (angle = world.rocket.blueYellowAngle, parts = lambda:
                    self.thruster (angle = world.rocket.greenRedAngle, parts = lambda:
                        self.flame (scale = tsMul ((1, 1, 1), world.rocket.thrusterForce / world.rocket.thrusterMaxForce * (0.9 + 0.1 * random ())), color = (1, 0.3 + 0.7 * random (), 0))
                    )
                )
            )
        )
        