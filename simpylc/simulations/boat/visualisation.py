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

'''

      z
      |
      o -- y
     /
    x

'''

import random as rd
import os

import simpylc as sp

import dimensions as dm

seaColor = (0, 0, 0.006)
stripeColor = (0, 0, 0.003)
hullColor = (1, 0, 0)
mastColor = (1, 0, 1)
sailColor = (1, 1, 1)
keelColor = (0, 1, 0)
vaneColor = (1, 1, 0)

class Boat:
    def __init__ (self):
        self.keel = sp.Beam (size = (0.2, 0.01, 0.4), center = (0, 0, -0.25), color = keelColor)
        self.hull = sp.Beam (size = (0.5, 0.2, 0.15), center = (-0.25, 0, 0.25), color = hullColor)
        self.bowLeft = sp.Beam (size = (0.5, 0.1, 0.15), center = (0.49, 0.025, 0), angle = -5.5, color = hullColor)
        self.bowRight = sp.Beam (size = (0.5, 0.1, 0.15), center = (0.49, -0.025, 0), angle = 5.5, color = hullColor)
        self.bowFront = sp.Cylinder (size = (0.1, 0.1, 0.15), center = (0.73, 0, 0), color = hullColor)
        self.rudder = sp.Beam (size = (0.13, 0.01, 0.4), center = (-0.25, 0, -0.1), color = keelColor)
        self.mast = sp.Cylinder (size = (0.025, 0.025, 1.2), center = (0.4, 0, 0.6), color = mastColor)
        self.sail = sp.Beam (size = (dm.boomLength, 0.03, 0.9), center = (-0.28, 0, 0.05), joint = (0.25, 0, 0), color = sailColor)
        self.vane = sp.Beam (size = (0.2, 0.02, 0.03), center = (-0.1, 0, 0.55), joint = (0.1, 0, 0), color = vaneColor)

    def __call__ (self):
        return self.keel (position = (sp.world.physics.positionX, sp.world.physics.positionY, 0), rotation = sp.world.physics.courseAngle, parts = lambda:
            self.hull (parts = lambda:
                self.bowLeft () +
                self.bowRight () +
                self.bowFront () +
                self.rudder (rotation = sp.world.physics.rudderAngle) +
                self.mast (parts = lambda:
                    self.sail (rotation = sp.world.physics.sailAngle) +
                    self.vane (rotation = sp.world.physics.vaneAngle)
                )
            )
        )

class Sea (sp.Beam):
    side = 16
    spacing = 0.5
    halfSteps = round (0.5 * side / spacing)

    class Stripe (sp.Beam):
        def __init__ (self, **arguments):
            super () .__init__ (size = (0.004, Sea.side, 0.001), **arguments)

    def __init__ (self, **arguments):
        super () .__init__ (size = (self.side, self.side, 0.0005), color = seaColor)
        self.xStripes = [self.Stripe (center = (0, nr * self.spacing, 0.0001), angle = 90, color = (0, 0.004, 0)) for nr in range (-self.halfSteps, self.halfSteps)]
        self.yStripes = [self.Stripe (center = (nr * self.spacing, 0, 0), color = (0, 0.004, 0)) for nr in range (-self.halfSteps, self.halfSteps)]

    def __call__ (self, parts):
        return super () .__call__ (color = seaColor, parts = lambda:
            parts () +
            sum (xStripe () for xStripe in self.xStripes) +
            sum (yStripe () for yStripe in self.yStripes)
        )

class Visualisation (sp.Scene):
    def __init__ (self):
        super () .__init__ ()

        self.init = True
        self.startX = 0
        self.startY = 0

        self.camera = sp.Camera ()

        self.sea = Sea (scene = self)
        self.boat = Boat ()

    def display (self):
        if self.init:
            self.init = False
            sp.world.physics.positionX.set (self.startX)
            sp.world.physics.positionY.set (self.startY)

        if sp.world.physics.soccerView:
            self.camera (
                position = sp.tEva ((sp.world.physics.positionX, sp.world.physics.positionY - sp.world.physics.soccerDist, 2)),
                focus = sp.tEva ((sp.world.physics.positionX, sp.world.physics.positionY, 0.3))
            )
        elif sp.world.physics.heliView:
            self.camera (
                position = sp.tEva ((0, -0.0000001, sp.world.physics.heliDist)),
                focus = sp.tEva ((0, 0, 0))
            )
        elif sp.world.physics.helmsmanView:
            self.camera (
                position = sp.tEva ((sp.world.physics.positionX, sp.world.physics.positionY, 0.5)),
                focus = sp.tEva ((sp.world.physics.helmsmanFocusX, sp.world.physics.helmsmanFocusY, 0))
            )

        self.sea (parts = lambda:
            self.boat ()
        )
