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

from SimPyLC import *

import parameters as pm

class BodyPart (Beam):
    def __init__ (self, **arguments):
        super () .__init__ (color = (1, 0, 0), **arguments)

class Wheel:
    def __init__ (self, **arguments):
        self.suspension = Cylinder (size = (0.01, 0.01, 0.001), axis = (0, 1, 0), angle = 90, pivot = (0, 0, 1), **arguments)
        self.rim = Beam (size = (0.02, 0.08, 0.06), axis = (0, 1, 0), angle = 90, pivot = (1, 0, 0), color = (0, 0, 0))
        self.tire = Cylinder (size = (pm.wheelDiameter, pm.wheelDiameter, 0.04), axis = (0, 1, 0), angle = 90, color = (1, 1, 0))
        
    def __call__ (self, wheelAngle, courseAngle = 0):
        return self.suspension (rotation = courseAngle, parts = lambda:
            self.rim (rotation = wheelAngle, parts = lambda:
                self.tire ()
        )   )
        
class Window (Beam):
    def __init__ (self, **arguments):
        super () .__init__ (axis = (1, 0, 0), color = (0, 0, 1), **arguments)
        
class Floor (Beam):
    side = 10
    spacing = 0.2
    halfSteps = round (0.5 * side / spacing)

    class Stripe (Beam):
        def __init__ (self, **arguments):
            super () .__init__ (size = (0.01, Floor.side, 0.001), **arguments)
            
    def __init__ (self, **arguments):
        super () .__init__ (size = (self.side, self.side, 0.0005), color = (0, 0.003, 0))
        self.xStripes = [self.Stripe (center = (0, nr * self.spacing, 0), angle = 90, color = (1, 1, 1)) for nr in range (-self.halfSteps, self.halfSteps)]
        self.yStripes = [self.Stripe (center = (nr * self.spacing, 0, 0), color = (0, 0, 0)) for nr in range (-self.halfSteps, self.halfSteps)]
        
    def __call__ (self, parts):
        return super () .__call__ (parts = lambda:
            parts () +
            sum (xStripe () for xStripe in self.xStripes) +
            sum (yStripe () for yStripe in self.yStripes)
        )

class Visualisation (Scene):
    def __init__ (self):
        super () .__init__ ()
        
        self.camera = Camera ()
        
        self.floor = Floor ()

        self.fuselage = BodyPart (size = (0.16, 0.70, 0.08), center = (0, 0, 0.07), pivot = (0, 0, 1))
        self.cabin = BodyPart (size = (0.16, 0.20, 0.06), center = (0, 0.06, 0.07))
        
        self.wheelFrontLeft = Wheel (center = (0.08, -0.20, -0.02))
        self.wheelFrontRight = Wheel (center = (-0.08, -0.20, -0.02))
        
        self.wheelRearLeft = Wheel (center = (0.08, 0.20, -0.02))
        self.wheelRearRight = Wheel (center = (-0.08, 0.20, -0.02))
        
        self.windowFront = Window (size = (0.14, 0.05, 0.14), center = (0, -0.14, -0.025), angle = -60)    
        self.windowRear = Window (size = (0.14, 0.05, 0.18), center = (0, 0.18, -0.025),angle = 72) 
                
    def display (self):
        self.camera (
            position = tAdd (self.fuselage.center, (3, 0, 2)),
            focus = tAdd (self.fuselage.center, (0, 0.001, 0))
        )    
    
        self.floor (parts = lambda:            
            self.fuselage (rotation = 40, parts = lambda:
                self.cabin (parts = lambda:
                    self.windowFront () +
                    self.windowRear ()
                ) +
                
                self.wheelFrontLeft (wheelAngle = world.physics.wheelAngle, courseAngle = world.physics.courseAngle) +
                self.wheelFrontRight (wheelAngle = world.physics.wheelAngle, courseAngle = world.physics.courseAngle) +
                
                self.wheelRearLeft (wheelAngle = world.physics.wheelAngle) +
                self.wheelRearRight (wheelAngle = world.physics.wheelAngle)
            )
        )
        