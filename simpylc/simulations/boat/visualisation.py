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
import sys as ss

ss.path.append ('./control_client')

import simpylc as sp

import constants as cs
import almanac as an

seaColor = (0.001, 0.001, 0.006)
stripeColor = (0.5, 0.5, 1)
hullColor = (1, 0, 0)
mastColor = (1, 0, 1)
sailColor = (1, 1, 1)
keelColor = (0, 1, 0)
vaneColor = (1, 1, 0)

class Boat:
    def __init__ (self):
        self.keel = sp.Beam (size = (0.6, 0.03, 1.2), center = (0, 0, -0.75), color = keelColor)
        self.hull = sp.Beam (size = (1.5, 0.6, 0.45), center = (-0.75, 0, 0.75), color = hullColor)
        self.bowLeft = sp.Beam (size = (1.5, 0.3, 0.45), center = (1.47, 0.075, 0), angle = -5.5, color = hullColor)
        self.bowRight = sp.Beam (size = (1.5, 0.3, 0.45), center = (1.47, -0.075, 0), angle = 5.5, color = hullColor)
        self.bowFront = sp.Cylinder (size = (0.3, 0.3, 0.45), center = (2.19, 0, 0), color = hullColor)
        self.rudder = sp.Beam (size = (0.39, 0.03, 1.2), center = (-0.75, 0, -0.3), color = keelColor)
        self.mast = sp.Cylinder (size = (0.075, 0.075, 3.6), center = (1.2, 0, 1.8), color = mastColor)
        self.sail = sp.Beam (size = (cs.boomLength, 0.09, 2.7), center = (-0.84, 0, 0.15), joint = (0.75, 0, 0), color = sailColor)
        self.vane = sp.Beam (size = (0.6, 0.06, 0.09), center = (-0.3, 0, 1.65), joint = (0.3, 0, 0), color = vaneColor)

    def __call__ (self):
        return self.keel (position = (0, 0, 0), rotation = sp.world.vessel.carthesianAngle, parts = lambda:
            self.hull (parts = lambda:
                self.bowLeft () +
                self.bowRight () +
                self.bowFront () +
                self.rudder (rotation = sp.world.vessel.rudderAngle) +
                self.mast (parts = lambda:
                    self.sail (rotation = sp.world.vessel.sailAngle) +
                    self.vane (rotation = sp.world.vessel.vaneAngle)
                )
            )
        )

class Sea (sp.Beam):
    side = 1600
    spacing = 4
    halfSteps = round (0.5 * side / spacing)

    class Stripe (sp.Beam):
        def __init__ (self, **arguments):
            super () .__init__ (size = (0.05, Sea.side, 0.001), **arguments)

    def __init__ (self, lattitude, longitude):
        super () .__init__ (size = (self.side, self.side, 0.0005), color = seaColor)

        self.lattitude = lattitude
        self.longitude = longitude

        self.xStripes = [self.Stripe (center = (0, nr * self.spacing, 0.0001), angle = 90, color =  stripeColor) for nr in range (-self.halfSteps, self.halfSteps)]
        self.yStripes = [self.Stripe (center = (nr * self.spacing, 0, 0), color = stripeColor) for nr in range (-self.halfSteps, self.halfSteps)]

    def __call__ (self, lattitudeBoat, longitudeBoat):
        distanceX, distanceY = an.getLeg (
            (lattitudeBoat, longitudeBoat),
            (self.lattitude, self.longitude)
        )

        return super () .__call__ (color = seaColor, position = (distanceX, distanceY, 0), parts = lambda:
            sum (xStripe () for xStripe in self.xStripes) +
            sum (yStripe () for yStripe in self.yStripes)
        )

class Buoy:
    def __init__ (self, lattitude, longitude):
        self.lattitude = lattitude
        self.longitude = longitude

        self.cone = sp.Cone (
            size = (0.3, 0.3, 0.3),
            center = (0, 0, 0.3),
            color = (1, 1, 0),
            group = 1
        )

    def __call__ (self, lattitudeBoat, longitudeBoat):
        distanceX, distanceY = an.getLeg (
            (lattitudeBoat, longitudeBoat),
            (self.lattitude, self.longitude)
        )

        return self.cone (
            position = (distanceX, distanceY, 0),
            scale = (10, 10, 1) if sp.eva (sp.world.vessel.heliView) and sp.eva (sp.world.vessel.heliFocusDist > 100) else (1, 1, 1)
        )

class Visualisation (sp.Scene):
    def __init__ (self):
        super () .__init__ ()
        self.buoys = []

        self.camera = sp.Camera ()
        self.boat = Boat ()

        waypoints = an.getWaypoints ()

        self.sea = Sea (waypoints [0][0], waypoints [1][1])

        for waypoint in waypoints:
            self.buoys.append (Buoy (waypoint [0], waypoint [1]))

    def display (self):
        if sp.world.vessel.soccerView:
            self.camera (
                position = sp.tEva ((0, -sp.world.vessel.soccerFocusDist, 2)),
                focus = sp.tEva ((0, 0, 0.3))
            )
        elif sp.world.vessel.heliView:
            self.camera (
                position = sp.tEva ((0, -0.0000001, sp.world.vessel.heliFocusDist)),
                focus = sp.tEva ((0, 0, 0))
            )
        elif sp.world.vessel.helmsmanView:
            self.camera (
                position = sp.tEva ((0, 0, 0.5)),
                focus = sp.tEva ((sp.world.vessel.helmsmanFocusDistX, sp.world.vessel.helmsmanFocusDistY, 0))
            )

        self.boat ()
        self.sea (*sp.tEva ((sp.world.vessel.lattitude, sp.world.vessel.longitude)))

        for buoy in self.buoys:
            buoy (*sp.tEva ((sp.world.vessel.lattitude, sp.world.vessel.longitude)))

